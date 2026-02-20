"""
AGM Store Builder - Utility Helpers

Common utility functions for the application.
"""

import re
import random
import string
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from uuid import uuid4


def generate_uuid() -> str:
    """Generate a new UUID string."""
    return str(uuid4())


def generate_order_number() -> str:
    """Generate a unique order number."""
    now = datetime.now(timezone.utc)
    date_part = now.strftime("%Y%m%d")
    random_part = random.randint(10000, 99999)
    return f"ORD-{date_part}-{random_part}"


def generate_reference(prefix: str = "REF") -> str:
    """Generate a unique reference string."""
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return f"{prefix}-{random_part}"


def generate_otp(length: int = 6) -> str:
    """Generate a random numeric OTP code."""
    return ''.join(random.choices(string.digits, k=length))


def format_currency(amount: float, symbol: str = "₦") -> str:
    """Format amount as currency string."""
    return f"{symbol}{amount:,.2f}"


def format_phone(phone: str, country_code: str = "234") -> str:
    """
    Format phone number to international format.
    
    Args:
        phone: Phone number (can include country code or not)
        country_code: Default country code
        
    Returns:
        Formatted phone number
    """
    # Remove all non-digits
    digits = re.sub(r'\D', '', phone)
    
    # Handle Nigerian numbers
    if digits.startswith('0') and len(digits) == 11:
        digits = country_code + digits[1:]
    elif digits.startswith('234') and len(digits) == 13:
        pass  # Already formatted
    elif digits.startswith('+234'):
        digits = digits[1:]  # Remove +
    
    return digits


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """Validate Nigerian phone number."""
    digits = re.sub(r'\D', '', phone)
    
    # Valid formats: 0XXXXXXXXXX, 234XXXXXXXXXX, +234XXXXXXXXXX
    if len(digits) == 11 and digits.startswith('0'):
        return True
    if len(digits) == 13 and digits.startswith('234'):
        return True
    
    return False


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def truncate(text: str, length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length."""
    if len(text) <= length:
        return text
    return text[:length - len(suffix)].rsplit(' ', 1)[0] + suffix


def mask_email(email: str) -> str:
    """Mask email for privacy."""
    if '@' not in email:
        return email
    
    local, domain = email.split('@')
    if len(local) <= 2:
        masked = local[0] + '*' + '@' + domain
    else:
        masked = local[0] + '*' * (len(local) - 2) + local[-1] + '@' + domain
    
    return masked


def mask_phone(phone: str) -> str:
    """Mask phone number for privacy."""
    digits = re.sub(r'\D', '', phone)
    if len(digits) < 4:
        return phone
    
    return digits[:3] + '*' * (len(digits) - 6) + digits[-3:]


def mask_account_number(account_number: str) -> str:
    """Mask bank account number for privacy."""
    if len(account_number) < 6:
        return account_number
    
    return account_number[:3] + '*' * (len(account_number) - 6) + account_number[-3:]


def calculate_percentage(part: float, whole: float) -> float:
    """Calculate percentage value."""
    if whole == 0:
        return 0
    return (part / whole) * 100


def get_nigerian_state_lgas(state: str) -> List[str]:
    """Get list of LGAs for a Nigerian state."""
    # This would typically come from a database or external source
    # Simplified example
    lgas_by_state = {
        "Lagos": [
            "Agege", "Ajeromi-Ifelodun", "Alimosho", "Amuwo-Odofin", "Apapa",
            "Badagry", "Epe", "Eti-Osa", "Ibeju-Lekki", "Ifako-Ijaiye",
            "Ikeja", "Ikorodu", "Kosofe", "Lagos Island", "Lagos Mainland",
            "Mushin", "Ojo", "Oshodi-Isolo", "Shomolu", "Surulere",
        ],
        "Abuja": [
            "Abaji", "Bwari", "Gwagwalada", "Kuje", "Kwali", "Municipal Area Council",
        ],
        # Add more states as needed
    }
    
    return lgas_by_state.get(state, [])


def parse_json_safely(json_string: str, default: Any = None) -> Any:
    """Safely parse JSON string."""
    import json
    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        return default


def dict_to_query_string(params: Dict[str, Any]) -> str:
    """Convert dictionary to URL query string."""
    from urllib.parse import urlencode
    return urlencode({k: v for k, v in params.items() if v is not None})
