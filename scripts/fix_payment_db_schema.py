
import asyncio
import sys
import os
from sqlalchemy import text

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.session import async_session_maker

async def fix_payment_schema():
    print("Fixing payments table schema...")
    async with async_session_maker() as session:
        try:
            print("Renaming 'reference' to 'payment_reference'...")
            # MySQL syntax: ALTER TABLE table_name CHANGE old_col_name new_col_name column_definition
            # We need to specify the definition again.
            # reference is varchar(100) NOT NULL
            await session.execute(text("ALTER TABLE payments CHANGE COLUMN reference payment_reference VARCHAR(100) NOT NULL"))
            print("Successfully renamed 'reference' to 'payment_reference'.")
        except Exception as e:
            print(f"Error renaming column (might already be renamed): {e}")

        try:
            print("Adding 'payment_metadata' column...")
            await session.execute(text("ALTER TABLE payments ADD COLUMN payment_metadata JSON NULL"))
            print("Successfully added 'payment_metadata' column.")
        except Exception as e:
            print(f"Error adding payment_metadata (might already exist): {e}")
            
        await session.commit()
        print("Schema fix completed.")

if __name__ == "__main__":
    asyncio.run(fix_payment_schema())
