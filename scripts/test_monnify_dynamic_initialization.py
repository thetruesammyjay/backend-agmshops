
import asyncio
import sys
import os
import httpx
import base64
from datetime import datetime, timezone, timedelta
from uuid import uuid4

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings

async def test_dynamic_initialization():
    print("Testing Monnify Dynamic Account Initialization (2-Step)...")
    
    base_url = settings.MONNIFY_BASE_URL
    api_key = settings.MONNIFY_API_KEY
    secret_key = settings.MONNIFY_SECRET_KEY
    contract_code = settings.MONNIFY_CONTRACT_CODE
    
    # 1. Authenticate
    credentials = f"{api_key}:{secret_key}"
    encoded = base64.b64encode(credentials.encode()).decode()
    
    async with httpx.AsyncClient() as client:
        print("Authenticating...")
        auth_resp = await client.post(
            f"{base_url}/api/v1/auth/login",
            headers={"Authorization": f"Basic {encoded}"}
        )
        
        if auth_resp.status_code != 200:
            print(f"Auth Failed: {auth_resp.text}")
            return
            
        access_token = auth_resp.json()["responseBody"]["accessToken"]
        print("Auth Success.")
        
        # 2. Initialize Transaction
        print("Initializing Transaction...")
        ref = f"PAY-TEST-DYN-{str(uuid4())[:8]}"
        amount = 5000.00
        
        init_payload = {
            "amount": amount,
            "customerName": "Test Customer",
            "customerEmail": "test@example.com",
            "paymentReference": ref,
            "paymentDescription": "Test Payment",
            "currencyCode": "NGN",
            "contractCode": contract_code,
            "redirectUrl": "http://localhost:3000/callback",
            "paymentMethods": ["ACCOUNT_TRANSFER"]
        }
        
        init_resp = await client.post(
            f"{base_url}/api/v1/merchant/transactions/init-transaction",
            headers={"Authorization": f"Bearer {access_token}"},
            json=init_payload
        )
        
        if init_resp.status_code != 200:
            print(f"Init Failed: {init_resp.text}")
            return
            
        init_body = init_resp.json()["responseBody"]
        transaction_ref = init_body["transactionReference"]
        print(f"Transaction Initialized. Ref: {transaction_ref}")
        
        # 3. Init Bank Transfer Payment
        print("initializing Bank Transfer Payment...")
        transfer_payload = {
            "transactionReference": transaction_ref,
            "bankCode": "035" # Optional: Wema Bank? Or leave empty to let Monnify choose?
                              # Documentation says optional. Let's try without first, then with if needed.
        }
        
        # Trying without bankCode first
        transfer_resp = await client.post(
            f"{base_url}/api/v1/merchant/bank-transfer/init-payment",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"transactionReference": transaction_ref}
        )
        
        print(f"Transfer Init Response Status: {transfer_resp.status_code}")
        print(f"Transfer Init Response Body: {transfer_resp.json()}")

if __name__ == "__main__":
    asyncio.run(test_dynamic_initialization())
