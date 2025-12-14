from aiogram.types import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from infrastructure.domain.models import UserModel

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_telegram_id(self, telegram_id: int) -> UserModel | None:
        query = select(UserModel).where(UserModel.telegram_id == telegram_id)
        return await self.session.scalar(query)

    async def is_user_exists(self, telegram_id: int) -> bool:
        return bool(await self.get_user_by_telegram_id(telegram_id))

    async def create_user(self, user: UserModel) -> UserModel:
        self.session.add(user)
        try:
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def get_or_create_user(self, user: User, chat_id: int | None = None) -> UserModel:
        user_model = UserModel(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            language_code=user.language_code,
            chat_id=chat_id,
        )
        existing_user = await self.get_user_by_telegram_id(user_model.telegram_id)
        if existing_user:
            return existing_user
        return await self.create_user(user_model)        