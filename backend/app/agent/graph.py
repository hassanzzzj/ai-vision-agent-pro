"""
LangGraph Workflow Definition
Sabhi nodes ko connect karke complete workflow banata hai
"""
from typing import Literal
from langgraph.graph import StateGraph, END
from .state import AgentState, NodeStatus
from .nodes import (
    planner_node,
    generator_node,
    critic_node,
    human_approval_node
)


def should_continue_generation(state: AgentState) -> Literal["generator", "end"]:
    """
    Conditional edge: Decide karna hai ke generation continue karein ya end
    
    Returns:
        - "generator": Agar quality low hai aur iterations baaki hain
        - "end": Agar quality acceptable hai ya max iterations complete
    """
    # Check for errors
    if state.get("node_status") == NodeStatus.FAILED:
        return "end"
    
    # Check if regeneration needed
    should_regenerate = state.get("should_regenerate", False)
    iteration_count = state.get("iteration_count", 0)
    max_iterations = state.get("max_iterations", 3)
    
    if should_regenerate and iteration_count < max_iterations:
        print(f"🔄 Continuing: Iteration {iteration_count}/{max_iterations}")
        return "generator"
    else:
        print(f"✅ Ending: Final result ready")
        return "end"


def should_get_approval(state: AgentState) -> Literal["human_approval", "generator"]:
    """
    Conditional edge: Human approval check
    
    Returns:
        - "human_approval": Agar human-in-the-loop enabled hai
        - "generator": Directly generation start karo
    """
    # Check if human approval is required
    # Production mein ye setting se control hoga
    human_in_loop_enabled = False  # Toggle this for human approval
    
    if human_in_loop_enabled and not state.get("user_approved"):
        return "human_approval"
    else:
        return "generator"


def create_agent_graph() -> StateGraph:
    """
    Complete LangGraph workflow create karta hai
    
    Workflow:
    1. START → Planner
    2. Planner → Human Approval (optional) → Generator
    3. Generator → Critic
    4. Critic → Decision (Continue or End)
       - If continue: Go back to Generator
       - If end: END
    
    Returns:
        Compiled StateGraph ready for execution
    """
    # Initialize graph
    workflow = StateGraph(AgentState)
    
    # Add all nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("human_approval", human_approval_node)
    workflow.add_node("generator", generator_node)
    workflow.add_node("critic", critic_node)
    
    # Define edges
    
    # START → Planner
    workflow.set_entry_point("planner")
    
    # Planner → Human Approval or Generator (conditional)
    workflow.add_conditional_edges(
        "planner",
        should_get_approval,
        {
            "human_approval": "human_approval",
            "generator": "generator"
        }
    )
    
    # Human Approval → Generator
    workflow.add_edge("human_approval", "generator")
    
    # Generator → Critic
    workflow.add_edge("generator", "critic")
    
    # Critic → Generator (loop) or END (conditional)
    workflow.add_conditional_edges(
        "critic",
        should_continue_generation,
        {
            "generator": "generator",
            "end": END
        }
    )
    
    # Compile the graph
    app = workflow.compile()
    
    print("✅ LangGraph workflow compiled successfully")
    print("📊 Nodes: planner → human_approval → generator → critic")
    
    return app


# Create global graph instance
agent_graph = create_agent_graph()


async def run_agent(
    prompt: str,
    task_id: str,
    reference_image: str = None,
    max_iterations: int = 3
) -> AgentState:
    """
    Main function to execute the complete workflow
    
    Args:
        prompt: User's image generation prompt
        task_id: Unique task identifier
        reference_image: Optional reference image (base64)
        max_iterations: Maximum regeneration attempts
    
    Returns:
        Final AgentState with generated image and metadata
    """
    from datetime import datetime
    
    print(f"\n{'='*60}")
    print(f"🚀 Starting Agent Workflow")
    print(f"📝 Task ID: {task_id}")
    print(f"💬 Prompt: {prompt}")
    print(f"{'='*60}\n")
    
    # Initialize state
    initial_state: AgentState = {
        "original_prompt": prompt,
        "reference_image": reference_image,
        "optimized_prompt": None,
        "prompt_analysis": None,
        "generated_image": None,
        "generation_params": None,
        "quality_score": None,
        "feedback": None,
        "issues_found": None,
        "iteration_count": 0,
        "max_iterations": max_iterations,
        "should_regenerate": False,
        "current_node": "start",
        "node_status": NodeStatus.PENDING,
        "error_message": None,
        "task_id": task_id,
        "timestamp": datetime.now().isoformat(),
        "user_approved": None
    }
    
    try:
        # Run the graph
        final_state = await agent_graph.ainvoke(initial_state)
        
        print(f"\n{'='*60}")
        print(f"✅ Workflow Completed Successfully")
        print(f"⭐ Quality Score: {final_state.get('quality_score', 'N/A')}")
        print(f"🔄 Iterations: {final_state.get('iteration_count', 0)}")
        print(f"{'='*60}\n")
        
        return final_state
        
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"❌ Workflow Failed: {str(e)}")
        print(f"{'='*60}\n")
        
        # Return error state
        initial_state["node_status"] = NodeStatus.FAILED
        initial_state["error_message"] = str(e)
        return initial_state
