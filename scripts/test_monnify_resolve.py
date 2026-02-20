
import sys
import os
import asyncio
from fastapi.testclient import TestClient

# Add project root to path
sys.path.append(os.getcwd())

from app.main import app
from app.dependencies import get_current_user_id

# Override the current user dependency to bypass authentication
def override_get_current_user_id():
    return "test-user-id"

app.dependency_overrides[get_current_user_id] = override_get_current_user_id

client = TestClient(app)

def test_resolve_bank_account():
    print("Testing Bank Account Resolution...")
    
    payload = {
        "account_number": "6971805050",
        "bank_code": "070"
    }
    
    print(f"Sending Request: {payload}")
    
    try:
        response = client.post(
            "/api/v1/payments/bank-accounts/resolve",
            json=payload
        )
        
        print(f"Status Code: {response.status_code}")
        print("Response Body:")
        print(response.json())
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_resolve_bank_account()
