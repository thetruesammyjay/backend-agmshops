"""
AGM Store Builder - Global Error Handler

Centralized exception handling for consistent API error responses.
"""

from typing import Optional
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError as PydanticValidationError
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger

from app.core.exceptions import AGMException


def create_error_response(
    status_code: int,
    message: str,
    details: Optional[dict] = None,
) -> JSONResponse:
    """
    Create a standardized error response.
    
    Args:
        status_code: HTTP status code
        message: Error message
        details: Optional additional error details
        
    Returns:
        JSONResponse with standardized error format
    """
    content = {
        "success": False,
        "message": message,
        "statusCode": status_code,
    }
    
    if details:
        content["details"] = details
    
    # Include CORS headers in error responses
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, PATCH, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "*",
    }
    
    return JSONResponse(
        status_code=status_code,
        content=content,
        headers=headers,
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """
    Configure exception handlers for the FastAPI application.
    
    Args:
        app: FastAPI application instance
    """
    
    @app.exception_handler(AGMException)
    async def agm_exception_handler(request: Request, exc: AGMException):
        """Handle custom AGM exceptions."""
        logger.warning(
            f"AGMException: {exc.message} | "
            f"Status: {exc.status_code} | "
            f"Path: {request.url.path}"
        )
        return create_error_response(
            status_code=exc.status_code,
            message=exc.message,
            details=exc.details if exc.details else None,
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        """Handle Pydantic validation errors from request parsing."""
        errors = {}
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error["loc"][1:])  # Skip 'body'
            if field:
                errors[field] = error["msg"]
            else:
                errors["body"] = error["msg"]
        
        logger.warning(
            f"Validation Error | Path: {request.url.path} | Errors: {errors}"
        )
        
        return create_error_response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message="Validation error",
            details=errors,
        )
    
    @app.exception_handler(PydanticValidationError)
    async def pydantic_exception_handler(
        request: Request,
        exc: PydanticValidationError,
    ):
        """Handle Pydantic validation errors from data processing."""
        errors = {}
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            errors[field] = error["msg"]
        
        return create_error_response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message="Validation error",
            details=errors,
        )
    
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(
        request: Request,
        exc: SQLAlchemyError,
    ):
        """Handle database errors."""
        logger.error(
            f"Database Error | Path: {request.url.path} | Error: {str(exc)}"
        )
        
        return create_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="A database error occurred",
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle all unhandled exceptions."""
        logger.exception(
            f"Unhandled Exception | Path: {request.url.path} | Error: {str(exc)}"
        )
        
        return create_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="An unexpected error occurred",
        )
