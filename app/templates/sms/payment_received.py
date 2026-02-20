"""
AGM Store Builder - SMS Template: Payment Received

Generates plain-text SMS messages for payment confirmation notifications.
"""


def payment_received_message(
    customer_name: str,
    amount: float,
    order_number: str,
    payment_reference: str,
) -> str:
    """
    Build the SMS body for a payment-received notification.

    Args:
        customer_name: Customer's first name or display name.
        amount: Payment amount (Naira).
        order_number: The associated order number.
        payment_reference: Unique payment reference code.

    Returns:
        Formatted SMS string.
    """
    return (
        f"Hi {customer_name}, your payment of NGN{amount:,.2f} "
        f"for order #{order_number} has been confirmed! "
        f"Ref: {payment_reference}. "
        f"Your order is now being processed. "
        f"Thank you for shopping with us! - AGMshops"
    )
