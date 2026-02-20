
import sys
import os
import asyncio

# Add project root to path
sys.path.append(os.getcwd())

from app.core.config import settings
from app.services.sms_service import SmsService

async def test_send_sms():
    print("Testing SMS Service (Termii)...")
    
    # Initialize service
    sms_service = SmsService()
    
    # Test Data
    phone_number = "09133468248"
    message = "Hello from AGMshops! This is a test SMS."
    
    print(f"Sending SMS to: {phone_number}")
    print(f"Message: {message}")
    print("-" * 30)
    
    # Check if API Key is set
    if not settings.TERMII_API_KEY:
        print("WARNING: TERMII_API_KEY is not set in .env")
        print("The service will run in Development/Mock mode.")
    else:
        print("TERMII_API_KEY is found. Sending real SMS...")
        
    try:
        result = await sms_service.send_sms(
            to=phone_number,
            message=message
        )
        
        print("\nResult:")
        print(result)
        
        if "message_id" in result:
             print("\n✅ SMS Sent Successfully!")
        elif "error" in result:
             print("\n❌ SMS Failed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(test_send_sms())
