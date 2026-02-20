
"""
AGM Store Builder - SMS Service

Service for sending SMS messages using Termii API.
"""

from typing import Dict, Any, Optional
import httpx
from loguru import logger

from app.core.config import settings
from app.core.exceptions import ServiceUnavailableError


class SmsService:
    """Service for handling SMS operations via Termii."""
    
    def __init__(self):
        self.base_url = settings.TERMII_BASE_URL
        self.api_key = settings.TERMII_API_KEY
        self.sender_id = settings.TERMII_SENDER_ID
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    
    async def send_sms(self, to: str, message: str) -> Dict[str, Any]:
        """
        Send an SMS message.
        
        Args:
            to: Recipient phone number/msisdn (e.g., 2348123456789)
            message: Text message content
            
        Returns:
            Dictionary containing API response
        """
        # Format phone number if needed (ensure international format 234)
        if to.startswith("0"):
            to = "234" + to[1:]
        elif to.startswith("+"):
            to = to[1:]
            
        payload = {
            "to": to,
            "from": self.sender_id,
            "sms": message,
            "type": "plain",
            "channel": "generic",
            "api_key": self.api_key,
        }
        
        # Development mode bypass
        if settings.is_development and not self.api_key:
            logger.info(f"DEV MODE: Simulating SMS to {to}: {message}")
            return {
                "message_id": "mock-msg-id-12345",
                "message": "Successfully Sent",
                "balance": 0,
                "user": "development_user"
            }
            
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.base_url}/sms/send",
                    json=payload,
                    headers=self.headers
                )
                
                response_data = response.json()
                
                if response.status_code not in [200, 201]:
                    logger.error(f"Termii SMS failed: {response_data}")
                    # Don't raise error immediately, let the caller handle it or retry
                    # But if critical, we might want to know
                    return {"error": "Failed to send SMS", "details": response_data}
                
                logger.info(f"SMS sent successfully to {to}")
                return response_data
                
        except httpx.RequestError as e:
            logger.error(f"Error connecting to Termii: {e}")
            raise ServiceUnavailableError(message="SMS service temporarily unavailable")
        except Exception as e:
            logger.error(f"Unexpected error sending SMS: {e}")
            raise ServiceUnavailableError(message="Failed to process SMS request")
