import logging
from sqlalchemy.ext.asyncio import AsyncEngine

from infrastructure.domain.base import BaseEntity

async def create_db_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(BaseEntity.metadata.create_all)

    logging.info("DB tables created")