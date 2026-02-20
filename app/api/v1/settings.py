"""
AGM Store Builder - Settings Endpoints

User settings endpoints for notification preferences, etc.
"""

import uuid
from pydantic import BaseModel
from fastapi import APIRouter
from sqlalchemy import select

from app.api.deps import DatabaseSession, CurrentUserId
from app.models.user_settings import UserSettings

router = APIRouter()


class NotificationPreferences(BaseModel):
    """Notification preferences matching frontend shape."""
    emailOrders: bool = True
    smsOrders: bool = False
    marketingEmails: bool = False


async def _get_or_create_settings(db: DatabaseSession, user_id: str) -> UserSettings:
    """Get user settings, creating defaults if none exist."""
    result = await db.execute(
        select(UserSettings).where(UserSettings.user_id == user_id)
    )
    settings = result.scalar_one_or_none()

    if not settings:
        settings = UserSettings(
            id=str(uuid.uuid4()),
            user_id=user_id,
        )
        db.add(settings)
        await db.commit()
        await db.refresh(settings)

    return settings


@router.get("/notifications")
async def get_notification_settings(
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Get notification preferences.

    Returns the user's notification settings mapped to frontend field names.
    """
    settings = await _get_or_create_settings(db, user_id)

    return {
        "success": True,
        "data": {
            "emailOrders": settings.email_notifications and settings.order_notifications,
            "smsOrders": settings.sms_notifications and settings.order_notifications,
            "marketingEmails": settings.marketing_notifications,
        },
    }


@router.put("/notifications")
async def update_notification_settings(
    prefs: NotificationPreferences,
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Update notification preferences.

    Maps frontend field names back to the UserSettings model columns.
    """
    settings = await _get_or_create_settings(db, user_id)

    # Map frontend fields -> model columns
    settings.email_notifications = prefs.emailOrders
    settings.order_notifications = prefs.emailOrders or prefs.smsOrders
    settings.sms_notifications = prefs.smsOrders
    settings.marketing_notifications = prefs.marketingEmails

    await db.commit()
    await db.refresh(settings)

    return {
        "success": True,
        "data": {
            "emailOrders": prefs.emailOrders,
            "smsOrders": prefs.smsOrders,
            "marketingEmails": prefs.marketingEmails,
        },
        "message": "Notification preferences updated",
    }
