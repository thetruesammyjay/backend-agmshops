"""
AGM Store Builder - Payment Endpoints

Payment management endpoints including verification, bank accounts, and Nigerian banks.
"""

from typing import List
from fastapi import APIRouter, status

from app.api.deps import DatabaseSession, CurrentUserId
from app.services.payment_service import PaymentService
from app.schemas.payment import (
    PaymentVerifyResponse,
    PaymentDetailResponse,
    PaymentReinitializeResponse,
    BankAccountRequest,
    BankAccountResponse,
    BankAccountListResponse,
    BankListResponse,
    ResolveBankAccountRequest,
    ResolveBankAccountResponse,
)
from app.schemas.common import MessageResponse

router = APIRouter()


# =====================
# Bank Account Endpoints (must be before /{reference} to avoid conflicts)
# =====================

@router.get("/banks", response_model=BankListResponse)
async def get_nigerian_banks():
    """
    Get list of Nigerian banks (public).
    
    Returns bank names and codes for bank selection.
    """
    from app.utils.constants import NIGERIAN_BANKS
    
    return {
        "success": True,
        "data": NIGERIAN_BANKS,
    }


@router.post("/bank-accounts/resolve", response_model=ResolveBankAccountResponse)
async def resolve_bank_account(
    request: ResolveBankAccountRequest,
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Resolve/verify a bank account number.
    
    Looks up the account name from bank code and account number.
    Uses Paystack or returns mock data in development.
    """
    payment_service = PaymentService(db)
    result = await payment_service.resolve_bank_account(
        account_number=request.account_number,
        bank_code=request.bank_code,
    )
    
    return {
        "success": True,
        "data": result,
    }


@router.get("/bank-accounts", response_model=BankAccountListResponse)
async def list_bank_accounts(
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Get user's bank accounts.
    
    Returns all bank accounts linked to the user.
    """
    payment_service = PaymentService(db)
    accounts = await payment_service.get_user_bank_accounts(user_id)
    
    return {
        "success": True,
        "data": accounts,
    }


@router.post(
    "/bank-accounts",
    response_model=BankAccountResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_bank_account(
    request: BankAccountRequest,
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Add a bank account for payouts.
    
    Adds a new bank account to the user's profile.
    """
    payment_service = PaymentService(db)
    account = await payment_service.add_bank_account(
        user_id=user_id,
        account_name=request.account_name,
        account_number=request.account_number,
        bank_code=request.bank_code,
        bank_name=request.bank_name,
    )
    
    return {
        "success": True,
        "data": account,
        "message": "Bank account added successfully",
    }


@router.put("/bank-accounts/{account_id}/primary", response_model=BankAccountResponse)
async def set_primary_bank_account(
    account_id: str,
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Set a bank account as primary.
    
    Sets the specified account as the default payout account.
    """
    payment_service = PaymentService(db)
    account = await payment_service.set_primary_bank_account(account_id, user_id)
    
    return {
        "success": True,
        "data": account,
        "message": "Primary bank account updated successfully",
    }


@router.delete("/bank-accounts/{account_id}", response_model=MessageResponse)
async def delete_bank_account(
    account_id: str,
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Delete a bank account.
    
    Removes a bank account from the user's profile.
    """
    payment_service = PaymentService(db)
    await payment_service.delete_bank_account(account_id, user_id)
    
    return {
        "success": True,
        "message": "Bank account deleted successfully",
    }


# =====================
# Payment Endpoints (generic routes last)
# =====================

@router.get("/verify/{reference}", response_model=PaymentVerifyResponse)
async def verify_payment(
    reference: str,
    db: DatabaseSession,
):
    """
    Verify payment status by reference (public).
    
    Checks payment status with Monnify.
    """
    payment_service = PaymentService(db)
    result = await payment_service.verify_payment(reference)
    
    return {
        "success": True,
        "data": result,
    }


@router.post("/{reference}/reinitialize", response_model=PaymentReinitializeResponse)
async def reinitialize_payment(
    reference: str,
    db: DatabaseSession,
):
    """
    Reinitialize an expired payment (public).
    
    Generates a new virtual account for payment.
    """
    payment_service = PaymentService(db)
    result = await payment_service.reinitialize_payment(reference)
    
    return {
        "success": True,
        "data": result,
        "message": "Payment reinitialized successfully",
    }


@router.get("/{reference}", response_model=PaymentDetailResponse)
async def get_payment(
    reference: str,
    db: DatabaseSession,
):
    """
    Get payment details by reference (public).
    
    Returns payment details including bank account info.
    """
    payment_service = PaymentService(db)
    payment = await payment_service.get_payment_details(reference)
    
    return {
        "success": True,
        "data": payment,
    }
