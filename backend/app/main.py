"""
FastAPI Application Entry Point
Complete backend server with CORS, error handling, and routing
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from app.api.v1_routes import router as v1_router
from app.services.monitor import monitor


# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events
    Startup aur shutdown ke time special actions
    """
    # Startup
    print("\n" + "="*60)
    print("🚀 AI Vision Agent Pro - Backend Starting")
    print("="*60)
    print(f"📍 Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"🔍 Monitoring: {'Enabled' if monitor.enabled else 'Disabled'}")
    print(f"🌐 CORS: Enabled for frontend")
    print("="*60 + "\n")
    
    yield
    
    # Shutdown
    print("\n" + "="*60)
    print("👋 AI Vision Agent Pro - Backend Shutting Down")
    
    # Flush monitoring events
    if monitor.enabled:
        print("📊 Flushing monitoring events...")
        monitor.flush()
    
    print("="*60 + "\n")


# Initialize FastAPI app
app = FastAPI(
    title="AI Vision Agent Pro",
    description="Agentic Image Generation with LangGraph + SiliconFlow",
    version="1.0.0",
    lifespan=lifespan
)


# CORS Configuration
# Frontend se requests allow karne ke liye
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default
        "http://localhost:3000",  # Alternative
        "http://frontend:5173",   # Docker network
        os.getenv("FRONTEND_URL", "http://localhost:5173")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global error handler
    Sari unexpected errors ko handle karta hai
    """
    print(f"❌ Unhandled Exception: {exc}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "path": str(request.url)
        }
    )


# Include API routes
app.include_router(v1_router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API info"""
    return {
        "name": "AI Vision Agent Pro API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "generate": "/api/v1/generate",
            "status": "/api/v1/status/{task_id}",
            "feedback": "/api/v1/feedback",
            "health": "/api/v1/health",
            "docs": "/docs"
        }
    }


# Run with: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
