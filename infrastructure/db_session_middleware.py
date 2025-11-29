from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.orm import sessionmaker

from infrastructure.repo_holder import RepoHolder

class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session: sessionmaker):
        self.session_pool = session

    async def __call__(
        self, 
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
        event: TelegramObject, 
        data: dict[str, Any]
    ) -> Any:
        async with self.session_pool() as session:
            data['repo_holder'] = RepoHolder(session)

            result = await handler(event, data)
            await session.commit()
            
            return result