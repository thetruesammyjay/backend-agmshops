"""
AGM Store Builder - Validators

Custom validation utilities for the application.
"""

import re
from typing import Optional, List


class ValidationError(Exception):
    """Custom validation error."""
    
    def __init__(self, message: str, field: Optional[str] = None):
        self.message = message
        self.field = field
        super().__init__(message)


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If email is invalid
    """
    if not email:
        raise ValidationError("Email is required", "email")
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError("Invalid email format", "email")
    
    return True


def validate_password(password: str, min_length: int = 8) -> bool:
    """
    Validate password strength.
    
    Args:
        password: Password to validate
        min_length: Minimum password length
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If password is weak
    """
    if not password:
        raise ValidationError("Password is required", "password")
    
    if len(password) < min_length:
        raise ValidationError(
            f"Password must be at least {min_length} characters",
            "password"
        )
    
    if not re.search(r'[a-z]', password):
        raise ValidationError(
            "Password must contain at least one lowercase letter",
            "password"
        )
    
    if not re.search(r'[A-Z]', password):
        raise ValidationError(
            "Password must contain at least one uppercase letter",
            "password"
        )
    
    if not re.search(r'\d', password):
        raise ValidationError(
            "Password must contain at least one number",
            "password"
        )
    
    return True


def validate_phone(phone: str) -> bool:
    """
    Validate Nigerian phone number.
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If phone is invalid
    """
    if not phone:
        raise ValidationError("Phone number is required", "phone")
    
    # Remove all non-digits
    digits = re.sub(r'\D', '', phone)
    
    # Valid formats
    valid = False
    if len(digits) == 11 and digits.startswith('0'):
        valid = True
    elif len(digits) == 13 and digits.startswith('234'):
        valid = True
    elif len(digits) == 10:  # Without leading 0 or country code
        valid = True
    
    if not valid:
        raise ValidationError("Invalid phone number format", "phone")
    
    return True


def validate_username(username: str) -> bool:
    """
    Validate store username.
    
    Args:
        username: Username to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If username is invalid
    """
    if not username:
        raise ValidationError("Username is required", "username")
    
    if len(username) < 3:
        raise ValidationError(
            "Username must be at least 3 characters",
            "username"
        )
    
    if len(username) > 30:
        raise ValidationError(
            "Username must be at most 30 characters",
            "username"
        )
    
    # Only allow lowercase letters, numbers, and underscores
    if not re.match(r'^[a-z0-9_]+$', username.lower()):
        raise ValidationError(
            "Username can only contain letters, numbers, and underscores",
            "username"
        )
    
    # Cannot start/end with underscore
    if username.startswith('_') or username.endswith('_'):
        raise ValidationError(
            "Username cannot start or end with underscore",
            "username"
        )
    
    # Reserved usernames
    reserved = [
        'admin', 'administrator', 'api', 'app', 'auth', 'checkout',
        'dashboard', 'help', 'home', 'login', 'logout', 'profile',
        'register', 'settings', 'shop', 'store', 'support', 'www',
    ]
    
    if username.lower() in reserved:
        raise ValidationError(
            "This username is not available",
            "username"
        )
    
    return True


def validate_account_number(account_number: str) -> bool:
    """
    Validate Nigerian bank account number.
    
    Args:
        account_number: Account number to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If account number is invalid
    """
    if not account_number:
        raise ValidationError("Account number is required", "account_number")
    
    # Remove any spaces
    account_number = account_number.replace(' ', '')
    
    # Must be exactly 10 digits
    if not re.match(r'^\d{10}$', account_number):
        raise ValidationError(
            "Account number must be exactly 10 digits",
            "account_number"
        )
    
    return True


def validate_price(price: float) -> bool:
    """
    Validate product price.
    
    Args:
        price: Price to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If price is invalid
    """
    if price is None:
        raise ValidationError("Price is required", "price")
    
    if price < 0:
        raise ValidationError("Price cannot be negative", "price")
    
    if price > 100000000:  # 100 million NGN max
        raise ValidationError("Price exceeds maximum allowed", "price")
    
    return True


def validate_quantity(quantity: int) -> bool:
    """
    Validate product quantity.
    
    Args:
        quantity: Quantity to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If quantity is invalid
    """
    if quantity is None:
        raise ValidationError("Quantity is required", "quantity")
    
    if quantity < 0:
        raise ValidationError("Quantity cannot be negative", "quantity")
    
    if quantity > 1000000:  # 1 million max
        raise ValidationError("Quantity exceeds maximum allowed", "quantity")
    
    return True


def validate_image_url(url: str) -> bool:
    """
    Validate image URL format.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If URL is invalid
    """
    if not url:
        return True  # Optional
    
    # Basic URL pattern
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    if not re.match(pattern, url, re.IGNORECASE):
        raise ValidationError("Invalid URL format", "url")
    
    # Check for valid image extensions or Cloudinary URL
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    is_cloudinary = 'cloudinary.com' in url.lower()
    has_valid_ext = any(url.lower().endswith(ext) for ext in valid_extensions)
    
    if not is_cloudinary and not has_valid_ext:
        raise ValidationError(
            "URL must point to a valid image file",
            "url"
        )
    
    return True
