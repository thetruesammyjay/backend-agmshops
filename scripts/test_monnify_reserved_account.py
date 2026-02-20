
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

async def test_reserved_account():
    print("Testing Monnify Reserved Account API...")
    
    base_url = settings.MONNIFY_BASE_URL
    api_key = settings.MONNIFY_API_KEY
    secret_key = settings.MONNIFY_SECRET_KEY
    contract_code = settings.MONNIFY_CONTRACT_CODE
    
    print(f"Base URL: {base_url}")
    print(f"Contract Code: {contract_code}")

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
        
        # 2. Create Reserved Account
        print("Creating Reserved Account...")
        ref = f"REF-{str(uuid4())[:12]}"
        
        payload = {
            "accountReference": ref,
            "accountName": "AGM Test Customer",
            "currencyCode": "NGN",
            "contractCode": contract_code,
            "customerEmail": "test@example.com",
            "customerName": "Test Customer",
            "reservedAccountType": "INVOICE", # or GENERAL
            "incomeSplitConfig": []
        }
        
        resp = await client.post(
            f"{base_url}/api/v1/bank-transfer/reserved-accounts",
            headers={"Authorization": f"Bearer {access_token}"},
            json=payload
        )
        
        print(f"Response Status: {resp.status_code}")
        print(f"Response Body: {resp.json()}")

if __name__ == "__main__":
    asyncio.run(test_reserved_account())
