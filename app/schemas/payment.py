"""
AGM Store Builder - Payment Schemas

Pydantic schemas for payment-related requests and responses.
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class BankAccountRequest(BaseModel):
    """Add bank account request."""
    account_name: str = Field(min_length=2, max_length=255)
    account_number: str = Field(min_length=10, max_length=10)
    bank_code: str
    bank_name: str


class ResolveBankAccountRequest(BaseModel):
    """Resolve bank account request."""
    account_number: str = Field(min_length=10, max_length=10)
    bank_code: str


class ResolveBankAccountData(BaseModel):
    """Resolved bank account data."""
    account_name: str
    account_number: str
    bank_code: str
    bank_name: str


class ResolveBankAccountResponse(BaseModel):
    """Resolve bank account response."""
    success: bool = True
    data: ResolveBankAccountData


class BankAccountData(BaseModel):
    """Bank account data."""
    id: str
    user_id: str
    account_name: str
    account_number: str
    bank_code: str
    bank_name: str
    is_verified: bool = False
    is_primary: bool = False
    created_at: str


class BankData(BaseModel):
    """Nigerian bank data."""
    name: str
    code: str


class PaymentAccountDetails(BaseModel):
    """Virtual account details for payment."""
    accountNumber: str
    accountName: str
    bankName: str
    amount: float


class PaymentVerifyData(BaseModel):
    """Payment verification data."""
    verified: bool
    status: str
    payment: Dict[str, Any]
    order: Dict[str, Any]


class PaymentDetailData(BaseModel):
    """Payment detail data."""
    id: str
    order_id: str
    payment_reference: str
    monnify_reference: Optional[str] = None
    transaction_reference: Optional[str] = None
    checkout_url: Optional[str] = None
    amount: float
    status: str
    payment_method: Optional[str] = None
    accountDetails: Optional[PaymentAccountDetails] = None
    paid_at: Optional[str] = None
    expires_at: Optional[str] = None
    created_at: str


class PaymentReinitializeData(BaseModel):
    """Payment reinitialize data."""
    payment_reference: str
    transaction_reference: Optional[str] = None
    checkout_url: Optional[str] = None
    accountDetails: PaymentAccountDetails
    expires_at: str


class PaymentVerifyResponse(BaseModel):
    """Payment verify response."""
    success: bool = True
    data: PaymentVerifyData


class PaymentDetailResponse(BaseModel):
    """Payment detail response."""
    success: bool = True
    data: PaymentDetailData


class PaymentReinitializeResponse(BaseModel):
    """Payment reinitialize response."""
    success: bool = True
    data: PaymentReinitializeData
    message: Optional[str] = None


class BankAccountResponse(BaseModel):
    """Bank account response."""
    success: bool = True
    data: BankAccountData
    message: Optional[str] = None


class BankAccountListResponse(BaseModel):
    """Bank account list response."""
    success: bool = True
    data: List[BankAccountData]


class BankListResponse(BaseModel):
    """Nigerian banks list response."""
    success: bool = True
    data: List[BankData]
