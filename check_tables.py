
import asyncio
from sqlalchemy import text
from app.database.connection import get_engine
from app.core.config import settings

async def check_tables():
    print(f"Connecting to {settings.DB_NAME}...")
    engine = get_engine()
    
    async with engine.connect() as conn:
        result = await conn.execute(text("SHOW TABLES"))
        tables = result.fetchall()
        print(f"Found {len(tables)} tables:")
        for table in tables:
            print(f" - {table[0]}")

if __name__ == "__main__":
    asyncio.run(check_tables())
