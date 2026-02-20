"""
AGM Store Builder - Logging Configuration

Structured logging setup using Loguru.
"""

import sys
from loguru import logger

from app.core.config import settings


def setup_logging() -> None:
    """
    Configure application logging using Loguru.
    
    Sets up:
    - Console output with color formatting
    - Log level based on settings
    - Structured log format
    """
    # Remove default handler
    logger.remove()
    
    # Define log format
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    # Simple format for production
    simple_format = (
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level: <8} | "
        "{name}:{function}:{line} | "
        "{message}"
    )
    
    # Add console handler
    logger.add(
        sys.stdout,
        format=log_format if settings.APP_DEBUG else simple_format,
        level=settings.LOG_LEVEL.upper(),
        colorize=settings.APP_DEBUG,
        backtrace=settings.APP_DEBUG,
        diagnose=settings.APP_DEBUG,
    )
    
    # In production, you might want to add file handlers
    if settings.is_production:
        # Add file handler for errors
        logger.add(
            "logs/error.log",
            format=simple_format,
            level="ERROR",
            rotation="10 MB",
            retention="30 days",
            compression="gz",
            backtrace=True,
            diagnose=False,
        )
        
        # Add file handler for all logs
        logger.add(
            "logs/app.log",
            format=simple_format,
            level=settings.LOG_LEVEL.upper(),
            rotation="50 MB",
            retention="7 days",
            compression="gz",
        )
    
    logger.info(f"Logging configured at {settings.LOG_LEVEL} level")
