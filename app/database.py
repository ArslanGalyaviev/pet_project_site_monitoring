from sqlmodel import SQLModel

DATABASE_URL = "sqlite+aiosqlite:///./monitoring.db"


async def init_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
