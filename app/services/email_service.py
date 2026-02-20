"""
AGM Store Builder - Email Service

Email sending via SendGrid.
"""

from typing import Optional, Dict, Any
from loguru import logger

from app.core.config import settings


class EmailService:
    """Email service using SendGrid."""
    
    def __init__(self):
        self.api_key = settings.SENDGRID_API_KEY
        self.from_email = settings.SENDGRID_FROM_EMAIL
        self.from_name = settings.SENDGRID_FROM_NAME
    
    async def _send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
    ) -> bool:
        """Send email via SendGrid."""
        if settings.is_development or not self.api_key:
            logger.info(f"Development mode: Email to {to_email} - {subject}")
            return True
        
        try:
            import sendgrid
            from sendgrid.helpers.mail import Mail, Email, To, Content
            
            sg = sendgrid.SendGridAPIClient(api_key=self.api_key)
            
            message = Mail(
                from_email=Email(self.from_email, self.from_name),
                to_emails=To(to_email),
                subject=subject,
                html_content=Content("text/html", html_content),
            )
            
            if text_content:
                message.add_content(Content("text/plain", text_content))
            
            response = sg.send(message)
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"Email sent to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    async def send_otp(self, to_email: str, otp: str) -> bool:
        """Send OTP verification email."""
        subject = f"Your verification code: {otp}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center; }}
                .header h1 {{ color: white; margin: 0; }}
                .content {{ padding: 30px; background: #f9f9f9; }}
                .otp {{ font-size: 32px; font-weight: bold; color: #667eea; text-align: center; padding: 20px; background: white; border-radius: 8px; margin: 20px 0; letter-spacing: 5px; }}
                .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{settings.APP_NAME}</h1>
                </div>
                <div class="content">
                    <h2>Email Verification</h2>
                    <p>Use the following code to verify your email address:</p>
                    <div class="otp">{otp}</div>
                    <p>This code will expire in 10 minutes.</p>
                    <p>If you didn't request this code, please ignore this email.</p>
                </div>
                <div class="footer">
                    <p>&copy; {settings.APP_NAME}. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self._send_email(to_email, subject, html_content)
    
    async def send_password_reset_otp(self, to_email: str, otp: str) -> bool:
        """Send password reset OTP email."""
        subject = f"Password Reset Code: {otp}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center; }}
                .header h1 {{ color: white; margin: 0; }}
                .content {{ padding: 30px; background: #f9f9f9; }}
                .otp {{ font-size: 32px; font-weight: bold; color: #667eea; text-align: center; padding: 20px; background: white; border-radius: 8px; margin: 20px 0; letter-spacing: 5px; }}
                .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{settings.APP_NAME}</h1>
                </div>
                <div class="content">
                    <h2>Password Reset</h2>
                    <p>Use the following code to reset your password:</p>
                    <div class="otp">{otp}</div>
                    <p>This code will expire in 10 minutes.</p>
                    <p>If you didn't request a password reset, please ignore this email and your password will remain unchanged.</p>
                </div>
                <div class="footer">
                    <p>&copy; {settings.APP_NAME}. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self._send_email(to_email, subject, html_content)
    
    async def send_order_confirmation(
        self,
        to_email: str,
        order_number: str,
        customer_name: str,
        items: list,
        total: float,
        store_name: str,
    ) -> bool:
        """Send order confirmation email."""
        subject = f"Order Confirmation - {order_number}"
        
        items_html = "".join([
            f"""
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">{item['product_name']}</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">{item['quantity']}</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: right;">₦{item['subtotal']:,.2f}</td>
            </tr>
            """
            for item in items
        ])
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center; }}
                .header h1 {{ color: white; margin: 0; }}
                .content {{ padding: 30px; background: #f9f9f9; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th {{ background: #667eea; color: white; padding: 12px; text-align: left; }}
                .total {{ font-size: 20px; font-weight: bold; text-align: right; padding: 20px 0; }}
                .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{store_name}</h1>
                </div>
                <div class="content">
                    <h2>Order Confirmed!</h2>
                    <p>Hi {customer_name},</p>
                    <p>Thank you for your order. Here's your order summary:</p>
                    <p><strong>Order Number:</strong> {order_number}</p>
                    
                    <table>
                        <tr>
                            <th>Item</th>
                            <th style="text-align: center;">Qty</th>
                            <th style="text-align: right;">Price</th>
                        </tr>
                        {items_html}
                    </table>
                    
                    <div class="total">
                        Total: ₦{total:,.2f}
                    </div>
                    
                    <p>We'll notify you when your order ships.</p>
                </div>
                <div class="footer">
                    <p>Powered by {settings.APP_NAME}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self._send_email(to_email, subject, html_content)
    
    async def send_payment_confirmation(
        self,
        to_email: str,
        order_number: str,
        amount: float,
    ) -> bool:
        """Send payment confirmation email."""
        subject = f"Payment Received - {order_number}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; text-align: center; }}
                .header h1 {{ color: white; margin: 0; }}
                .content {{ padding: 30px; background: #f9f9f9; text-align: center; }}
                .amount {{ font-size: 36px; font-weight: bold; color: #10b981; padding: 20px; }}
                .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Payment Received</h1>
                </div>
                <div class="content">
                    <h2>✓ Payment Successful</h2>
                    <p>We've received your payment for order <strong>{order_number}</strong></p>
                    <div class="amount">₦{amount:,.2f}</div>
                    <p>Your order is now being processed.</p>
                </div>
                <div class="footer">
                    <p>Powered by {settings.APP_NAME}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self._send_email(to_email, subject, html_content)
