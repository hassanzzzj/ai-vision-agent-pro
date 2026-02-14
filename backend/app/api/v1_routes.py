"""
FastAPI Routes (v1)
Frontend se connect karne ke liye REST API endpoints
"""
import uuid
import asyncio
from typing import Dict, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field

from ..agent.graph import run_agent
from ..agent.state import TaskStatus, NodeStatus
from ..services.monitor import monitor


# Request/Response Models

class GenerateRequest(BaseModel):
    """Request body for /generate endpoint"""
    prompt: str = Field(..., min_length=3, max_length=1000)
    reference_image: Optional[str] = None  # Base64 encoded
    max_iterations: int = Field(default=3, ge=1, le=5)
    enable_monitoring: bool = Field(default=True)


class GenerateResponse(BaseModel):
    """Response for /generate endpoint"""
    task_id: str
    status: str
    message: str


class StatusResponse(BaseModel):
    """Response for /status endpoint"""
    task_id: str
    status: str
    progress: int
    current_step: str
    generated_image: Optional[str] = None
    feedback: Optional[str] = None
    error: Optional[str] = None
    quality_score: Optional[float] = None


class FeedbackRequest(BaseModel):
    """Request body for /feedback endpoint"""
    task_id: str
    rating: float = Field(..., ge=0.0, le=1.0)
    comment: Optional[str] = None


# Global storage for tasks (Production mein Redis ya Database use karein)
tasks_store: Dict[str, dict] = {}


# Router
router = APIRouter(prefix="/api/v1", tags=["Agent"])


@router.post("/generate", response_model=GenerateResponse)
async def generate_image(
    request: GenerateRequest,
    background_tasks: BackgroundTasks
):
    """
    Start image generation workflow
    
    Returns task_id immediately and runs generation in background
    """
    try:
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Validate prompt
        if not request.prompt or len(request.prompt.strip()) < 3:
            raise HTTPException(
                status_code=400,
                detail="Prompt must be at least 3 characters long"
            )
        
        # Initialize task in store
        tasks_store[task_id] = {
            "task_id": task_id,
            "status": "pending",
            "progress": 0,
            "current_step": "initializing",
            "generated_image": None,
            "feedback": None,
            "error": None,
            "quality_score": None,
            "created_at": datetime.now().isoformat()
        }
        
        # Create monitoring trace
        if request.enable_monitoring and monitor.enabled:
            trace = monitor.create_trace(
                name="image_generation_workflow",
                metadata={
                    "task_id": task_id,
                    "prompt": request.prompt,
                    "max_iterations": request.max_iterations
                }
            )
        
        # Run agent in background
        background_tasks.add_task(
            execute_agent_workflow,
            task_id=task_id,
            prompt=request.prompt,
            reference_image=request.reference_image,
            max_iterations=request.max_iterations
        )
        
        return GenerateResponse(
            task_id=task_id,
            status="accepted",
            message="Image generation started. Use /status endpoint to check progress."
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start generation: {str(e)}")


@router.get("/status/{task_id}", response_model=StatusResponse)
async def get_task_status(task_id: str):
    """
    Get current status of a generation task
    
    Returns real-time progress and result
    """
    if task_id not in tasks_store:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_data = tasks_store[task_id]
    
    return StatusResponse(
        task_id=task_data["task_id"],
        status=task_data["status"],
        progress=task_data["progress"],
        current_step=task_data["current_step"],
        generated_image=task_data.get("generated_image"),
        feedback=task_data.get("feedback"),
        error=task_data.get("error"),
        quality_score=task_data.get("quality_score")
    )


@router.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    """
    Submit user feedback for a completed task
    
    Logs feedback to monitoring system
    """
    if request.task_id not in tasks_store:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Log to Langfuse
    if monitor.enabled:
        monitor.log_feedback(
            trace_id=request.task_id,
            score=request.rating,
            comment=request.comment
        )
    
    return {
        "message": "Feedback received",
        "task_id": request.task_id
    }


@router.delete("/task/{task_id}")
async def delete_task(task_id: str):
    """Delete a task from storage"""
    if task_id not in tasks_store:
        raise HTTPException(status_code=404, detail="Task not found")
    
    del tasks_store[task_id]
    
    return {"message": "Task deleted successfully"}


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_tasks": len(tasks_store)
    }


# Background Task Execution

async def execute_agent_workflow(
    task_id: str,
    prompt: str,
    reference_image: Optional[str],
    max_iterations: int
):
    """
    Execute the complete agent workflow in background
    
    Updates task status as workflow progresses
    """
    try:
        # Update status: running
        tasks_store[task_id].update({
            "status": "running",
            "progress": 10,
            "current_step": "planning"
        })
        
        # Run the agent
        final_state = await run_agent(
            prompt=prompt,
            task_id=task_id,
            reference_image=reference_image,
            max_iterations=max_iterations
        )
        
        # Check for errors
        if final_state.get("node_status") == NodeStatus.FAILED:
            tasks_store[task_id].update({
                "status": "failed",
                "progress": 0,
                "current_step": "error",
                "error": final_state.get("error_message", "Unknown error")
            })
            return
        
        # Update with success
        tasks_store[task_id].update({
            "status": "completed",
            "progress": 100,
            "current_step": "done",
            "generated_image": final_state.get("generated_image"),
            "feedback": final_state.get("feedback"),
            "quality_score": final_state.get("quality_score"),
            "iteration_count": final_state.get("iteration_count", 0)
        })
        
        # Flush monitoring events
        if monitor.enabled:
            monitor.flush()
        
    except Exception as e:
        # Update with error
        tasks_store[task_id].update({
            "status": "failed",
            "progress": 0,
            "current_step": "error",
            "error": str(e)
        })
        
        # Log error
        if monitor.enabled:
            monitor.log_error(
                trace_id=task_id,
                error_message=str(e)
            )
