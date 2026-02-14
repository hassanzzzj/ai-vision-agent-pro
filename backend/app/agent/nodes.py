"""
LangGraph Nodes
Har node ek specific kaam karta hai (Planning, Generation, Criticism, etc.)
"""
import json
from typing import Dict, Any
from datetime import datetime
from .state import AgentState, NodeStatus
from ..services.silicon_flow import silicon_flow_service
from ..services.monitor import monitor


async def planner_node(state: AgentState) -> Dict[str, Any]:
    """
    Step 1: Prompt ko analyze aur optimize karta hai
    
    Ye node user ki prompt ko better banata hai image generation ke liye
    """
    try:
        print(f"🧠 Planner: Analyzing prompt...")
        
        original_prompt = state["original_prompt"]
        
        # Simple prompt optimization
        # Production mein yahan LLM use kar sakte hain (OpenAI, Anthropic, etc.)
        optimized_prompt = enhance_prompt(original_prompt)
        
        # Prompt analysis
        analysis = {
            "original_length": len(original_prompt),
            "optimized_length": len(optimized_prompt),
            "keywords_added": extract_keywords(optimized_prompt),
            "style_hints": "photorealistic, highly detailed, 4k"
        }
        
        # Monitor logging
        if monitor.enabled:
            with monitor.span(
                state["task_id"], 
                "planner",
                {"original_prompt": original_prompt}
            ) as span:
                if span:
                    span.end(output={
                        "optimized_prompt": optimized_prompt,
                        "analysis": analysis
                    })
        
        print(f"✅ Planner: Optimized prompt ready")
        
        return {
            "optimized_prompt": optimized_prompt,
            "prompt_analysis": analysis,
            "current_node": "planner",
            "node_status": NodeStatus.COMPLETED
        }
        
    except Exception as e:
        print(f"❌ Planner Error: {e}")
        return {
            "current_node": "planner",
            "node_status": NodeStatus.FAILED,
            "error_message": f"Planner failed: {str(e)}"
        }


async def generator_node(state: AgentState) -> Dict[str, Any]:
    """
    Step 2: Actual image generation
    
    SiliconFlow API use karke image banata hai
    """
    try:
        print(f"🎨 Generator: Creating image...")
        
        prompt = state.get("optimized_prompt") or state["original_prompt"]
        
        # Validate prompt
        if not silicon_flow_service.validate_prompt(prompt):
            raise ValueError("Invalid or inappropriate prompt")
        
        # Generation parameters
        params = {
            "width": 1024,
            "height": 1024,
            "num_inference_steps": 30,
            "guidance_scale": 7.5
        }
        
        # Generate image
        result = await silicon_flow_service.generate_image(
            prompt=prompt,
            **params
        )
        
        # Monitor logging
        if monitor.enabled:
            monitor.log_generation(
                trace_id=state["task_id"],
                name="image_generation",
                prompt=prompt,
                output="Image generated successfully",
                metadata=params
            )
        
        print(f"✅ Generator: Image created successfully")
        
        return {
            "generated_image": result["image"],
            "generation_params": params,
            "current_node": "generator",
            "node_status": NodeStatus.COMPLETED
        }
        
    except Exception as e:
        print(f"❌ Generator Error: {e}")
        
        if monitor.enabled:
            monitor.log_error(
                trace_id=state["task_id"],
                error_message=f"Generation failed: {str(e)}"
            )
        
        return {
            "current_node": "generator",
            "node_status": NodeStatus.FAILED,
            "error_message": f"Generation failed: {str(e)}"
        }


async def critic_node(state: AgentState) -> Dict[str, Any]:
    """
    Step 3: Generated image ki quality check
    
    Image ko analyze karke feedback deta hai
    """
    try:
        print(f"🔍 Critic: Analyzing image quality...")
        
        # Simple quality checks
        # Production mein yahan vision model use kar sakte hain
        quality_score, feedback, issues = analyze_image_quality(state)
        
        # Log feedback
        if monitor.enabled:
            monitor.log_feedback(
                trace_id=state["task_id"],
                score=quality_score,
                comment=feedback
            )
        
        should_regenerate = quality_score < 0.7 and state["iteration_count"] < state["max_iterations"]
        
        if should_regenerate:
            print(f"⚠️ Critic: Quality score {quality_score:.2f} - Regeneration needed")
        else:
            print(f"✅ Critic: Quality score {quality_score:.2f} - Acceptable")
        
        return {
            "quality_score": quality_score,
            "feedback": feedback,
            "issues_found": issues,
            "should_regenerate": should_regenerate,
            "iteration_count": state["iteration_count"] + 1,
            "current_node": "critic",
            "node_status": NodeStatus.COMPLETED
        }
        
    except Exception as e:
        print(f"❌ Critic Error: {e}")
        return {
            "current_node": "critic",
            "node_status": NodeStatus.FAILED,
            "error_message": f"Critic failed: {str(e)}"
        }


async def human_approval_node(state: AgentState) -> Dict[str, Any]:
    """
    Step 4: Human-in-the-loop approval
    
    User se permission leta hai before generation
    """
    print(f"👤 Human Approval: Waiting for user confirmation...")
    
    # Yahan frontend se approval wait karna hoga
    # For now, auto-approve kar rahe hain
    # Production mein ye WebSocket ya polling se handle hoga
    
    return {
        "user_approved": True,  # Frontend se aayega
        "current_node": "human_approval",
        "node_status": NodeStatus.COMPLETED
    }


# Helper Functions

def enhance_prompt(prompt: str) -> str:
    """Prompt ko enhance karta hai better results ke liye"""
    # Basic enhancement
    enhanced = prompt.strip()
    
    # Add quality modifiers if not present
    quality_keywords = ["detailed", "high quality", "4k", "professional"]
    has_quality = any(keyword in enhanced.lower() for keyword in quality_keywords)
    
    if not has_quality:
        enhanced += ", highly detailed, professional quality, 4k"
    
    # Add style hints
    if "photo" not in enhanced.lower() and "realistic" not in enhanced.lower():
        enhanced += ", photorealistic"
    
    return enhanced


def extract_keywords(prompt: str) -> list:
    """Prompt se important keywords extract karta hai"""
    # Simple keyword extraction
    words = prompt.lower().split()
    
    # Filter common words
    stop_words = {"a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for"}
    keywords = [word for word in words if word not in stop_words and len(word) > 3]
    
    return keywords[:10]  # Top 10 keywords


def analyze_image_quality(state: AgentState) -> tuple:
    """
    Image quality analysis
    
    Returns: (score, feedback, issues)
    
    Note: Ye simple heuristic hai. Production mein CLIP ya vision model use karein.
    """
    # Check if image exists
    if not state.get("generated_image"):
        return (0.0, "No image generated", ["missing_image"])
    
    # Check prompt alignment
    optimized_prompt = state.get("optimized_prompt", "")
    original_prompt = state.get("original_prompt", "")
    
    issues = []
    score = 0.8  # Base score
    
    # Simple checks
    if len(optimized_prompt) < 10:
        issues.append("prompt_too_short")
        score -= 0.2
    
    # Iteration penalty
    iteration_count = state.get("iteration_count", 0)
    if iteration_count > 2:
        score -= 0.1
    
    # Generate feedback
    if score >= 0.8:
        feedback = "Excellent quality! Image meets all requirements."
    elif score >= 0.7:
        feedback = "Good quality with minor improvements possible."
    else:
        feedback = f"Quality needs improvement. Issues: {', '.join(issues)}"
    
    return (max(0.0, min(1.0, score)), feedback, issues)
