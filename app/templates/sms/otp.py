"""
AGM Store Builder - SMS Template: OTP

Generates plain-text SMS messages for one-time password delivery.
"""


def otp_message(
    otp_code: str,
    expiry_minutes: int = 10,
    purpose: str = "verification",
) -> str:
    """
    Build the SMS body for an OTP notification.

    Args:
        otp_code: The one-time password / verification code.
        expiry_minutes: Minutes until the code expires.
        purpose: Context label (e.g. "verification", "password reset").

    Returns:
        Formatted SMS string.
    """
    return (
        f"Your AGMshops {purpose} code is: {otp_code}. "
        f"It expires in {expiry_minutes} min. "
        f"Do NOT share this code with anyone."
    )
