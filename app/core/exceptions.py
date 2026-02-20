"""
AGM Store Builder - Custom Exceptions

Custom exception classes for the application with proper error handling.
"""

from typing import Any, Dict, Optional


class AGMException(Exception):
    """Base exception for AGM Store Builder."""
    
    def __init__(
        self,
        message: str = "An error occurred",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(AGMException):
    """Raised when authentication fails."""
    
    def __init__(
        self,
        message: str = "Authentication failed",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=401, details=details)


class AuthorizationError(AGMException):
    """Raised when user lacks required permissions."""
    
    def __init__(
        self,
        message: str = "You don't have permission to perform this action",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=403, details=details)


class NotFoundError(AGMException):
    """Raised when a resource is not found."""
    
    def __init__(
        self,
        message: str = "Resource not found",
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
    ):
        details = {}
        if resource_type:
            details["resource_type"] = resource_type
        if resource_id:
            details["resource_id"] = resource_id
        super().__init__(message=message, status_code=404, details=details)


class ValidationError(AGMException):
    """Raised when input validation fails."""
    
    def __init__(
        self,
        message: str = "Validation error",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=422, details=details)


class ConflictError(AGMException):
    """Raised when there's a resource conflict (e.g., duplicate entry)."""
    
    def __init__(
        self,
        message: str = "Resource already exists",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=409, details=details)


class BadRequestError(AGMException):
    """Raised for invalid request data."""
    
    def __init__(
        self,
        message: str = "Bad request",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=400, details=details)


class RateLimitError(AGMException):
    """Raised when rate limit is exceeded."""
    
    def __init__(
        self,
        message: str = "Too many requests. Please try again later.",
        retry_after: int = 60,
    ):
        super().__init__(
            message=message,
            status_code=429,
            details={"retry_after": retry_after},
        )


class PaymentError(AGMException):
    """Raised when payment processing fails."""
    
    def __init__(
        self,
        message: str = "Payment processing failed",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=400, details=details)


class ExternalServiceError(AGMException):
    """Raised when an external service (Monnify, SendGrid, etc.) fails."""
    
    def __init__(
        self,
        message: str = "External service error",
        service_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        error_details = details or {}
        if service_name:
            error_details["service"] = service_name
        super().__init__(message=message, status_code=502, details=error_details)


class OTPError(AGMException):
    """Raised when OTP verification fails."""
    
    def __init__(
        self,
        message: str = "Invalid or expired OTP",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=400, details=details)


class TokenError(AGMException):
    """Raised when token operations fail."""
    
    def __init__(
        self,
        message: str = "Token error",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=401, details=details)


class FileUploadError(AGMException):
    """Raised when file upload fails."""
    
    def __init__(
        self,
        message: str = "File upload failed",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=400, details=details)


class DatabaseError(AGMException):
    """Raised when database operations fail."""
    
    def __init__(
        self,
        message: str = "Database operation failed",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=500, details=details)


class ServiceUnavailableError(AGMException):
    """Raised when a service is temporarily unavailable."""
    
    def __init__(
        self,
        message: str = "Service temporarily unavailable",
        details: Optional[Dict[str, Any]] = None,
        retry_after: int = 60,
    ):
        error_details = details or {}
        error_details["retry_after"] = retry_after
        super().__init__(message=message, status_code=503, details=error_details)
