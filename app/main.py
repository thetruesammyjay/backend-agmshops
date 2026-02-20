"""
AGM Store Builder - FastAPI Application Entry Point

Main application setup with lifespan events, middleware, and route configuration.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from loguru import logger

from app.core.config import settings
from app.core.constants import API_V1_PREFIX
from app.core.exceptions import AGMException
from app.database.connection import init_database, close_database
from app.api.v1.router import api_v1_router
from app.middleware.error_handler import setup_exception_handlers
from app.middleware.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan context manager.
    
    Handles startup and shutdown events:
    - Startup: Initialize database connection pool
    - Shutdown: Close database connections gracefully
    """
    # Startup
    logger.info("🚀 Starting AGM Store Builder API...")
    logger.info(f"Environment: {settings.APP_ENV}")
    logger.info(f"Debug mode: {settings.APP_DEBUG}")
    
    # Initialize database
    await init_database()
    logger.info("✅ Database connection pool initialized")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down AGM Store Builder API...")
    await close_database()
    logger.info("✅ Database connections closed")


def create_application() -> FastAPI:
    """
    Application factory function.
    
    Creates and configures the FastAPI application with all middleware,
    exception handlers, and routes.
    
    Returns:
        Configured FastAPI application instance
    """
    # Configure logging
    setup_logging()
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.APP_NAME,
        description="Production-ready e-commerce backend API for AGM Store Builder",
        version=settings.APP_VERSION,
        docs_url="/docs" if settings.APP_DEBUG else None,
        redoc_url="/redoc" if settings.APP_DEBUG else None,
        openapi_url="/openapi.json" if settings.APP_DEBUG else None,
        lifespan=lifespan,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Setup exception handlers
    setup_exception_handlers(app)
    
    # Include API routers
    app.include_router(api_v1_router, prefix=API_V1_PREFIX)
    
    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        """API root endpoint - health check."""
        return {
            "success": True,
            "message": f"Welcome to {settings.APP_NAME} API",
            "version": settings.APP_VERSION,
            "docs": "/docs" if settings.APP_DEBUG else "Disabled in production",
        }
    
    # Health check endpoint (outside of API versioning)
    @app.get("/health", tags=["Health"])
    async def health_check():
        """
        Health check endpoint for monitoring and load balancers.
        """
        return {
            "status": "healthy",
            "environment": settings.APP_ENV,
            "version": settings.APP_VERSION,
        }
    
    return app


# Create the application instance
app = create_application()


# For running with uvicorn directly
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.APP_DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
