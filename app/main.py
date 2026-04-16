"""
Main FastAPI Application for 5G Network Slicing System.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import logging

from app.core.config import config
from app.api import routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=config.API_TITLE,
    version=config.API_VERSION,
    description="AI-Driven Adaptive Network Slice Configuration System for 5G",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with system information."""
    return {
        "service": config.API_TITLE,
        "version": config.API_VERSION,
        "status": "operational",
        "timestamp": datetime.now().timestamp(),
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "slices": "/slices",
            "prediction": "/predict/{slice_id}",
            "ingest": "/ingest",
            "stream": "/stream (WebSocket)",
        },
    }


# Include routes
app.include_router(routes.router, prefix="/api", tags=["Network Slicing"])


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle global exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "timestamp": datetime.now().timestamp(),
        },
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Execute on application startup."""
    logger.info(f"Starting {config.API_TITLE} v{config.API_VERSION}")
    logger.info(f"Debug mode: {config.DEBUG}")
    logger.info(f"Configured slices: {list(config.SLICES.keys())}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Execute on application shutdown."""
    logger.info(f"Shutting down {config.API_TITLE}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
