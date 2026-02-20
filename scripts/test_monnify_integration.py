
import asyncio
import sys
import os
from loguru import logger

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.monnify_service import MonnifyService

async def test_monnify():
    print("Testing Monnify Integration with current .env keys...")
    
    service = MonnifyService()
    print(f"Base URL: {service.base_url}")
    print(f"API Key present: {bool(service.api_key)}")
    
    # 1. Test Auth
    print("\n1. Testing Authentication...")
    try:
        token = await service._get_access_token()
        print(f"Auth Success! Token received (truncated): {token[:20]}...")
    except Exception as e:
        print(f"Auth Failed: {e}")
        return

    # 2. Test Account Validation (using a generic test account)
    # Monnify Sandbox often uses specific test accounts. 
    # Attempting to validate a random real-looking number to see API response.
    print("\n2. Testing Account Validation...")
    try:
        # Using a dummy GTBank account number often used in testing or just a random one
        # 042 is GTBank code in Nigeria usually, but let's see what the API expects.
        # Using User provided details: 6971805050, Fidelity Bank (070)
        res = await service.validate_bank_account("6971805050", "070")
        print(f"Validation Result: {res}")
    except Exception as e:
        print(f"Validation Failed (Expected if account invalid in Sandbox): {e}")

    # 3. Test Payment Creation
    print("\n3. Testing Payment Creation...")
    try:
        # We need to hack the service to print the response since it's internal
        # Or just rely on the fact that if it fails to get account number, we want to know why.
        # Let's verify what the service returns first.
        payment = await service.create_payment(
            order_id="TEST-ORD-DEBUG",
            user_id="USER-123",
            amount=5000.00,
            customer_name="Test Customer",
            customer_email="test@example.com"
        )
        print("Payment Creation Result (Dict):")
        print(payment)
    except Exception as e:
        print(f"Payment Creation Failed: {e}")
        return

    # 4. Test Payment Verification
    print("\n4. Testing Payment Verification...")
    payment_ref = payment.get('payment_reference')
    if payment_ref:
        try:
            print(f"Verifying ref: {payment_ref}")
            # Ensure we are using the same service instance
            verification = await service.verify_payment(payment_ref)
            print("Verification Result:")
            print(verification)
        except Exception as e:
             print(f"Verification Failed: {e}")
    else:
        print("Skipping verification as payment creation returned no reference.")

if __name__ == "__main__":
    asyncio.run(test_monnify())
