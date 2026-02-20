import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.session import async_session_maker
from app.services.payment_service import PaymentService

async def debug_payment(reference: str):
    async with async_session_maker() as session:
        service = PaymentService(session)
        print(f"Fetching payment with reference: {reference}")
        try:
            payment = await service.get_payment_details(reference)
            print("Payment details retrieved successfully:")
            print(payment)
        except Exception as e:
            print(f"Error retrieving payment: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    reference = "PAY-00102133-bd9ce286"
    if len(sys.argv) > 1:
        reference = sys.argv[1]
    asyncio.run(debug_payment(reference))
