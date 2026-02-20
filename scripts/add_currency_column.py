
import asyncio
import sys
import os
from sqlalchemy import text

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.session import async_session_maker

async def add_currency_column():
    print("Adding currency column to payments table...")
    async with async_session_maker() as session:
        try:
            # Check if column exists first to be safe (though error implied it doesn't)
            # Simplest is to just try adding it. If it fails, we catch it.
            # But the error logs confirmed it's missing.
            
            await session.execute(text("ALTER TABLE payments ADD COLUMN currency VARCHAR(3) DEFAULT 'NGN' NOT NULL"))
            await session.commit()
            print("Successfully added 'currency' column to 'payments' table.")
            
        except Exception as e:
            print(f"Error adding column (might already exist): {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(add_currency_column())
