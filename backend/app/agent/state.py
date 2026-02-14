"""
LangGraph State Schema
Ye file define karti hai ke graph ke andar kaunsa data flow hoga
"""
from typing import TypedDict, Optional, List, Dict, Any
from enum import Enum


class NodeStatus(str, Enum):
    """Node execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentState(TypedDict):
    """
    Complete state jo LangGraph ke sabhi nodes ke beech share hogi
    """
    # User Input
    original_prompt: str
    reference_image: Optional[str]  # Base64 encoded image (agar ho)
    
    # Planner Output
    optimized_prompt: Optional[str]
    prompt_analysis: Optional[Dict[str, Any]]
    
    # Generator Output
    generated_image: Optional[str]  # Base64 encoded generated image
    generation_params: Optional[Dict[str, Any]]
    
    # Critic Output
    quality_score: Optional[float]  # 0.0 to 1.0
    feedback: Optional[str]
    issues_found: Optional[List[str]]
    
    # Workflow Control
    iteration_count: int
    max_iterations: int
    should_regenerate: bool
    
    # Status Tracking
    current_node: str
    node_status: NodeStatus
    error_message: Optional[str]
    
    # Metadata
    task_id: str
    timestamp: str
    user_approved: Optional[bool]  # Human-in-the-loop


class TaskStatus(TypedDict):
    """API response ke liye task status"""
    task_id: str
    status: str
    progress: int  # 0-100
    current_step: str
    generated_image: Optional[str]
    error: Optional[str]
    feedback: Optional[str]
