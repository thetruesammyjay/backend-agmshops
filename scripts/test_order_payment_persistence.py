
import asyncio
import sys
import os
from loguru import logger

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.session import async_session_maker
from app.services.order_service import OrderService
from app.repositories.payment_repository import PaymentRepository

async def test_order_persistence():
    print("Testing order creation and payment persistence...")
    async with async_session_maker() as session:
        order_service = OrderService(session)
        payment_repo = PaymentRepository(session)
        
        # Test data (using IDs from previous logs)
        store_username = "felicitiy"
        product_id = "a2e9119b-ea9c-4278-826d-6118bee0bcff"
        
        items = [{
            "product_id": product_id,
            "quantity": 1,
            "variant_selection": None
        }]
        
        try:
            print(f"Creating order for store: {store_username}")
            result = await order_service.create_order(
                store_username=store_username,
                customer_name="Test User",
                customer_phone="08012345678",
                delivery_address="Test Address",
                delivery_state="Lagos",
                items=items,
                customer_email="test@example.com"
            )
            
            payment_data = result["payment"]
            payment_ref = payment_data["payment_reference"]
            print(f"Order created. Payment Reference: {payment_ref}")
            
            # Verify payment exists in DB
            print(f"Verifying payment in database...")
            payment = await payment_repo.get_by_reference(payment_ref)
            
            if payment:
                print(f"SUCCESS: Payment found in DB! ID: {payment.id}, Amount: {payment.amount}")
            else:
                print("FAILURE: Payment NOT found in DB.")
                
        except Exception as e:
            print(f"Error during test: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_order_persistence())
