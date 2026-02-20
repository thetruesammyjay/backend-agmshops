"""
AGM Store Builder - Template Loader

Jinja2 template loading and rendering utilities.
"""

from typing import Dict, Any
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Template directory
TEMPLATE_DIR = Path(__file__).parent


def get_template_environment() -> Environment:
    """Get Jinja2 template environment."""
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(['html', 'xml']),
    )
    
    # Add custom filters
    env.filters['number_format'] = lambda x: f"{x:,.2f}" if x else "0.00"
    
    return env


def render_template(template_path: str, context: Dict[str, Any]) -> str:
    """
    Render a template with the given context.
    
    Args:
        template_path: Path to template relative to templates folder
        context: Template context variables
        
    Returns:
        Rendered HTML string
    """
    env = get_template_environment()
    template = env.get_template(template_path)
    return str(template.render(**context))


def render_email_template(template_name: str, context: Dict[str, Any]) -> str:
    """
    Render an email template.
    
    Args:
        template_name: Name of the email template (without path)
        context: Template context variables
        
    Returns:
        Rendered HTML string
    """
    # Add common context
    from datetime import datetime
    context.setdefault('year', datetime.now().year)
    
    return render_template(f"email/{template_name}", context)


# Export commonly used templates
EMAIL_TEMPLATES = {
    "welcome": "welcome.html",
    "verify_email": "verify_email.html",
    "password_reset": "password_reset.html",
    "order_confirmation": "order_confirmation.html",
    "payment_received": "payment_received.html",
    "new_order": "new_order.html",
    "payout_completed": "payout_completed.html",
}
