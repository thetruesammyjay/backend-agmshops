
import sys
import os
import asyncio
from datetime import datetime

# Add project root to path
sys.path.append(os.getcwd())

from app.core.config import settings
from app.services.monnify_service import MonnifyService

async def test_init_payment():
    print("Testing Monnify Payment Initialization...")
    
    # Initialize service
    monnify = MonnifyService()
    
    # Test Data
    order_id = f"TEST-{int(datetime.now().timestamp())}"
    user_id = "test-user-id"
    amount = 5000.00
    customer_name = "Test Customer"
    customer_email = "test@example.com"
    
    print(f"Creating payment for Order: {order_id}")
    print(f"Amount: {amount}")
    
    try:
        result = await monnify.create_payment(
            order_id=order_id,
            user_id=user_id,
            amount=amount,
            customer_name=customer_name,
            customer_email=customer_email
        )
        
        print("\nPayment Created Successfully!")
        print("-" * 30)
        print(f"Payment Reference: {result.get('payment_reference')}")
        print(f"Transaction Reference: {result.get('transaction_reference')}")
        print(f"Checkout URL: {result.get('checkout_url')}")
        print(f"Account Number: {result.get('accountDetails', {}).get('accountNumber')}")
        print("-" * 30)
        print("\nFull Response:")
        print(result)
        
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(test_init_payment())
