"""
Langfuse Monitoring Service
LangGraph ke har step ko track karne ke liye
"""
import os
from typing import Optional, Dict, Any
from langfuse import Langfuse
from contextlib import contextmanager


class MonitoringService:
    """Langfuse integration for observability"""
    
    def __init__(self):
        self.enabled = os.getenv("LANGFUSE_ENABLED", "false").lower() == "true"
        
        if self.enabled:
            self.client = Langfuse(
                public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
                secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
                host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
            )
        else:
            self.client = None
            print("⚠️ Langfuse monitoring is disabled")
    
    def create_trace(
        self, 
        name: str, 
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Create a new trace for tracking"""
        if not self.enabled or not self.client:
            return None
        
        try:
            return self.client.trace(
                name=name,
                user_id=user_id,
                metadata=metadata or {}
            )
        except Exception as e:
            print(f"⚠️ Failed to create trace: {e}")
            return None
    
    @contextmanager
    def span(
        self, 
        trace_id: str,
        name: str, 
        input_data: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Context manager for tracking individual operations
        
        Usage:
            with monitor.span(trace_id, "planner", {"prompt": prompt}) as span:
                result = do_planning()
                if span:
                    span.end(output={"optimized_prompt": result})
        """
        if not self.enabled or not self.client:
            yield None
            return
        
        try:
            span_obj = self.client.span(
                trace_id=trace_id,
                name=name,
                input=input_data or {},
                metadata=metadata or {}
            )
            yield span_obj
            
        except Exception as e:
            print(f"⚠️ Span tracking error: {e}")
            yield None
    
    def log_generation(
        self,
        trace_id: str,
        name: str,
        prompt: str,
        output: str,
        model: str = "stable-diffusion-xl",
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log image generation event"""
        if not self.enabled or not self.client:
            return
        
        try:
            self.client.generation(
                trace_id=trace_id,
                name=name,
                model=model,
                input={"prompt": prompt},
                output={"result": output},
                metadata=metadata or {}
            )
        except Exception as e:
            print(f"⚠️ Failed to log generation: {e}")
    
    def log_error(
        self,
        trace_id: str,
        error_message: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log error event"""
        if not self.enabled or not self.client:
            return
        
        try:
            self.client.score(
                trace_id=trace_id,
                name="error",
                value=0,
                comment=error_message,
                metadata=metadata or {}
            )
        except Exception as e:
            print(f"⚠️ Failed to log error: {e}")
    
    def log_feedback(
        self,
        trace_id: str,
        score: float,
        comment: Optional[str] = None
    ):
        """Log user feedback or quality score"""
        if not self.enabled or not self.client:
            return
        
        try:
            self.client.score(
                trace_id=trace_id,
                name="quality_score",
                value=score,
                comment=comment
            )
        except Exception as e:
            print(f"⚠️ Failed to log feedback: {e}")
    
    def flush(self):
        """Flush pending events to Langfuse"""
        if self.enabled and self.client:
            try:
                self.client.flush()
            except Exception as e:
                print(f"⚠️ Failed to flush events: {e}")


# Global instance
monitor = MonitoringService()
