"""
AGM Store Builder - Monnify Service

Integration with Monnify payment gateway.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timezone, timedelta
from uuid import uuid4
import httpx
import base64
from loguru import logger

from app.core.config import settings


class MonnifyService:
    """Monnify payment gateway integration."""
    
    def __init__(self):
        self.base_url = settings.MONNIFY_BASE_URL
        self.api_key = settings.MONNIFY_API_KEY
        self.secret_key = settings.MONNIFY_SECRET_KEY
        self.contract_code = settings.MONNIFY_CONTRACT_CODE
        self.redirect_url = settings.get_monnify_redirect_url
        self._access_token: Optional[str] = None
        self._token_expires: Optional[datetime] = None
    
    async def _get_access_token(self) -> str:
        """Get or refresh Monnify access token."""
        if self._access_token and self._token_expires:
            if datetime.now(timezone.utc) < self._token_expires:
                return self._access_token
        
        # Generate auth credentials
        credentials = f"{self.api_key}:{self.secret_key}"
        encoded = base64.b64encode(credentials.encode()).decode()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/auth/login",
                headers={
                    "Authorization": f"Basic {encoded}",
                    "Content-Type": "application/json",
                },
            )
            
            if response.status_code != 200:
                logger.error(f"Monnify auth failed: {response.text}")
                raise Exception("Failed to authenticate with Monnify")
            
            data = response.json()
            self._access_token = data["responseBody"]["accessToken"]
            # Token expires in 5 minutes, refresh at 4 minutes
            self._token_expires = datetime.now(timezone.utc) + timedelta(minutes=4)
            
            return self._access_token
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make authenticated request to Monnify API."""
        token = await self._get_access_token()
        
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=f"{self.base_url}{endpoint}",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                json=data,
            )
            
            result: Dict[str, Any] = response.json()
            return result
    
    async def create_payment(
        self,
        order_id: str,
        user_id: str,
        amount: float,
        customer_name: str,
        customer_email: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a reserved account for payment.
        
        In development mode, returns mock data.
        """
        payment_reference = f"PAY-{order_id[:8]}-{str(uuid4())[:8]}"
        expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
        
        # Development mode - return mock data only if no API key
        if not self.api_key:
            logger.info(f"Mock payment created for {payment_reference} (No API Key)")
            
            return {
                "payment_reference": payment_reference,
                "accountDetails": {
                    "accountNumber": "1234567890",
                    "accountName": f"AGM-{customer_name}",
                    "bankName": "Wema Bank",
                    "amount": amount,
                },
                "expires_at": expires_at.isoformat(),
            }
        
        # Production - create dynamic account for this transaction
        try:
            # Step 1: Initialize Transaction
            init_response = await self._make_request(
                "POST",
                "/api/v1/merchant/transactions/init-transaction",
                {
                    "amount": amount,
                    "customerName": customer_name,
                    "customerEmail": customer_email or "customer@example.com",
                    "paymentReference": payment_reference,
                    "paymentDescription": f"Payment for order {order_id}",
                    "currencyCode": "NGN",
                    "contractCode": self.contract_code,
                    "redirectUrl": self.redirect_url,
                    "paymentMethods": ["ACCOUNT_TRANSFER"],
                },
            )
            
            if not init_response.get("requestSuccessful"):
                logger.error(f"Monnify init transaction failed: {init_response}")
                raise Exception("Failed to initialize transaction")
            
            transaction_ref = init_response["responseBody"]["transactionReference"]
            
            # Step 2: Initialize Bank Transfer to get Account Details
            transfer_response = await self._make_request(
                "POST",
                "/api/v1/merchant/bank-transfer/init-payment",
                {
                    "transactionReference": transaction_ref,
                    "bankCode": "232"  # Sterling Bank is often used for dynamic accounts, or let Monnify decide
                },
            )
            
            if not transfer_response.get("requestSuccessful"):
                 # Fallback: Sometimes init-transaction response already has account info if Account Transfer is enabled
                 # Check init_response first
                checkout_url = init_response["responseBody"].get("checkoutUrl")
                logger.warning(f"Monnify bank transfer init failed: {transfer_response}. Using checkout URL: {checkout_url}")
                
                return {
                    "payment_reference": payment_reference,
                    "transaction_reference": transaction_ref,
                    "checkout_url": checkout_url,
                    "accountDetails": {
                        "accountNumber": "",
                        "accountName": "",
                        "bankName": "",
                        "amount": amount,
                    },
                    "expires_at": expires_at.isoformat(),
                }

            logger.info(f"Monnify Bank Transfer Response: {transfer_response}")
            body = transfer_response["responseBody"]
            
            return {
                "payment_reference": payment_reference,
                "transaction_reference": transaction_ref,
                "checkout_url": None, 
                "accountDetails": {
                    "accountNumber": body.get("accountNumber", ""),
                    "accountName": body.get("accountName", ""),
                    "bankName": body.get("bankName", ""),
                    "amount": body.get("totalPayable", amount),
                },
                "expires_at": body.get("expiresOn", expires_at.isoformat()),
            }
            
        except Exception as e:
            logger.error(f"Error creating Monnify payment: {e}")
            raise
    
    async def verify_payment(self, payment_reference: str) -> Dict[str, Any]:
        """
        Verify payment status with Monnify.
        
        In development mode, returns mock data.
        """
        if not self.api_key:
            logger.info(f"Mock payment verification for {payment_reference} (No API Key)")
            return {
                "status": "pending",
                "monnify_reference": None,
                "payment_method": None,
            }
        
        try:
            response = await self._make_request(
                "GET",
                f"/api/v2/merchant/transactions/query?paymentReference={payment_reference}",
            )
            
            if not response.get("requestSuccessful"):
                return {"status": "pending", "monnify_reference": None}
            
            body = response["responseBody"]
            status_map = {
                "PAID": "paid",
                "PENDING": "pending",
                "OVERPAID": "paid",
                "PARTIALLY_PAID": "pending",
                "FAILED": "failed",
                "EXPIRED": "expired",
            }
            
            return {
                "status": status_map.get(body.get("paymentStatus"), "pending"),
                "monnify_reference": body.get("transactionReference"),
                "payment_method": body.get("paymentMethod"),
            }
            
        except Exception as e:
            logger.error(f"Error verifying payment: {e}")
            return {"status": "pending", "monnify_reference": None}
    
    async def validate_bank_account(
        self,
        account_number: str,
        bank_code: str,
    ) -> Dict[str, Any]:
        """
        Validate a bank account number using Monnify API.
        
        In development mode, returns mock data.
        """
        if not self.api_key:
            # Generate mock account name based on account number
            mock_names = [
                "JOHN DOE",
                "JANE SMITH",
                "ADEBAYO EMMANUEL",
                "CHIOMA OKONKWO",
                "IBRAHIM MUSA",
            ]
            name_index = int(account_number[-1]) % len(mock_names)
            mock_account_name = mock_names[name_index]
            
            logger.info(f"Mock bank validation for {account_number} (No API Key)")
            
            return {
                "account_name": mock_account_name,
                "account_number": account_number,
                "bank_code": bank_code,
            }
        
        try:
            response = await self._make_request(
                "GET",
                f"/api/v1/disbursements/account/validate?accountNumber={account_number}&bankCode={bank_code}",
            )
            
            if not response.get("requestSuccessful"):
                logger.error(f"Monnify bank validation failed: {response}")
                raise Exception("Failed to validate bank account")
            
            body = response["responseBody"]
            
            return {
                "account_name": body.get("accountName"),
                "account_number": body.get("accountNumber"),
                "bank_code": bank_code,
            }
            
        except Exception as e:
            logger.error(f"Error validating bank account: {e}")
            raise
    
    async def initiate_payout(
        self,
        amount: float,
        account_number: str,
        bank_code: str,
        account_name: str,
        reference: str,
    ) -> Dict[str, Any]:
        """
        Initiate a payout/transfer to a bank account.
        
        In development mode, returns mock data.
        """
        if not self.api_key:
            logger.info(f"Mock payout initiated for {reference} (No API Key)")
            return {
                "reference": reference,
                "status": "pending",
            }
        
        try:
            response = await self._make_request(
                "POST",
                "/api/v2/disbursements/single",
                {
                    "amount": amount,
                    "reference": reference,
                    "narration": "AGM Store Payout",
                    "destinationBankCode": bank_code,
                    "destinationAccountNumber": account_number,
                    "currency": "NGN",
                    "sourceAccountNumber": "",  # Will use default
                },
            )
            
            if not response.get("requestSuccessful"):
                logger.error(f"Monnify payout failed: {response}")
                raise Exception("Failed to initiate payout")
            
            return {
                "reference": reference,
                "status": "pending",
            }
            
        except Exception as e:
            logger.error(f"Error initiating payout: {e}")
            raise
