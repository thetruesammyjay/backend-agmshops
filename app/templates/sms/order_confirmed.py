"""
AGM Store Builder - SMS Template: Order Confirmed

Generates plain-text SMS messages for order confirmation notifications.
"""


def order_confirmed_message(
    customer_name: str,
    order_number: str,
    total_amount: float,
    item_count: int = 1,
) -> str:
    """
    Build the SMS body for an order-confirmed notification.

    Args:
        customer_name: Customer's first name or display name.
        order_number: The unique order number.
        total_amount: Total order amount (Naira).
        item_count: Number of items in the order.

    Returns:
        Formatted SMS string.
    """
    items_label = "item" if item_count == 1 else "items"
    return (
        f"Hi {customer_name}, your order #{order_number} "
        f"({item_count} {items_label}, NGN{total_amount:,.2f}) "
        f"has been confirmed! "
        f"We'll notify you when it ships. "
        f"Thank you for shopping with us! - AGMshops"
    )
