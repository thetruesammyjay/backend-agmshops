
import asyncio
import sys
import os
from sqlalchemy import text

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.session import async_session_maker

async def check_schema():
    print("Checking payments table schema...")
    async with async_session_maker() as session:
        try:
            # Describe table
            result = await session.execute(text("DESCRIBE payments"))
            rows = result.fetchall()
            print(f"{'Field':<25} {'Type':<20} {'Null':<10} {'Key':<10} {'Default':<20}")
            print("-" * 85)
            for row in rows:
                # row is a tuple-like object. indices: 0=Field, 1=Type, 2=Null, 3=Key, 4=Default, 5=Extra
                print(f"{row[0]:<25} {row[1]:<20} {row[2]:<10} {row[3]:<10} {str(row[4]):<20}")
                
        except Exception as e:
            print(f"Error checking schema: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_schema())
