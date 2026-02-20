"""
AGM Store Builder - App-Level Configuration

Re-exports core settings for convenience.
This module provides easy access to settings from the app package level.
"""

from app.core.config import Settings, get_settings, settings

__all__ = ["Settings", "get_settings", "settings"]
