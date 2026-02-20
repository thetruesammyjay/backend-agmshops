"""
AGM Store Builder - Webhook Endpoints

Webhook handlers for external service callbacks (Monnify).
"""

from fastapi import APIRouter, Request, HTTPException, status, Header
from typing import Optional
import hashlib
import hmac
from loguru import logger

from app.api.deps import DatabaseSession
from app.core.config import settings
from app.services.payment_service import PaymentService
from app.schemas.common import MessageResponse

router = APIRouter()


def verify_monnify_signature(
    payload: bytes,
    signature: str,
    secret: str,
) -> bool:
    """
    Verify Monnify webhook signature.
    
    Monnify signs webhooks with HMAC SHA-512.
    """
    computed_hash = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha512,
    ).hexdigest()
    
    return hmac.compare_digest(computed_hash, signature)


@router.post("/monnify", response_model=MessageResponse)
async def monnify_webhook(
    request: Request,
    db: DatabaseSession,
    monnify_signature: Optional[str] = Header(None, alias="Monnify-Signature"),
):
    """
    Handle Monnify payment webhooks.
    
    Processes payment notifications from Monnify.
    """
    # Get raw body for signature verification
    body = await request.body()
    
    # Verify signature in production
    if settings.is_production and settings.MONNIFY_WEBHOOK_SECRET:
        if not monnify_signature:
            logger.warning("Missing Monnify signature")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing webhook signature",
            )
        
        if not verify_monnify_signature(
            body,
            monnify_signature,
            settings.MONNIFY_WEBHOOK_SECRET,
        ):
            logger.warning("Invalid Monnify signature")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid webhook signature",
            )
    
    # Parse webhook data
    try:
        data = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse webhook data: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON payload",
        )
    
    event_type = data.get("eventType")
    event_data = data.get("eventData", {})
    
    logger.info(f"Received Monnify webhook: {event_type}")
    
    # Process based on event type
    payment_service = PaymentService(db)
    
    if event_type == "SUCCESSFUL_TRANSACTION":
        payment_reference = event_data.get("paymentReference")
        monnify_reference = event_data.get("transactionReference")
        amount_paid = float(event_data.get("amountPaid", 0))
        
        await payment_service.process_successful_payment(
            payment_reference=payment_reference,
            monnify_reference=monnify_reference,
            amount_paid=amount_paid,
            event_data=event_data,
        )
        
        logger.info(f"Processed successful payment: {payment_reference}")
    
    elif event_type == "FAILED_TRANSACTION":
        payment_reference = event_data.get("paymentReference")
        
        await payment_service.process_failed_payment(
            payment_reference=payment_reference,
            event_data=event_data,
        )
        
        logger.info(f"Processed failed payment: {payment_reference}")
    
    elif event_type == "EXPIRED_TRANSACTION":
        payment_reference = event_data.get("paymentReference")
        
        await payment_service.process_expired_payment(
            payment_reference=payment_reference,
            event_data=event_data,
        )
        
        logger.info(f"Processed expired payment: {payment_reference}")
    
    else:
        logger.info(f"Ignored webhook event type: {event_type}")
    
    # Handle disbursement events
    if event_type == "SUCCESSFUL_DISBURSEMENT":
        disbursement_reference = event_data.get("reference")
        logger.info(f"Processed successful disbursement: {disbursement_reference}")
        # TODO: Update disbursement status in database
    
    elif event_type == "FAILED_DISBURSEMENT":
        disbursement_reference = event_data.get("reference")
        failure_reason = event_data.get("responseMessage", "Unknown error")
        logger.info(f"Processed failed disbursement: {disbursement_reference} - {failure_reason}")
        # TODO: Update disbursement status in database
    
    elif event_type == "REVERSED_DISBURSEMENT":
        disbursement_reference = event_data.get("reference")
        logger.info(f"Processed reversed disbursement: {disbursement_reference}")
        # TODO: Update disbursement status in database
    
    # Handle refund events
    elif event_type == "SUCCESSFUL_REFUND":
        refund_reference = event_data.get("refundReference")
        logger.info(f"Processed successful refund: {refund_reference}")
        # TODO: Update refund status in database
    
    elif event_type == "FAILED_REFUND":
        refund_reference = event_data.get("refundReference")
        failure_reason = event_data.get("responseMessage", "Unknown error")
        logger.info(f"Processed failed refund: {refund_reference} - {failure_reason}")
        # TODO: Update refund status in database
    
    return {
        "success": True,
        "message": "Webhook processed successfully",
    }
