from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from infrastructure.domain.models import UserModel

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_telegram_id(self, telegram_id: int) -> UserModel | None:
        query = select(UserModel).where(UserModel.telegram_id == telegram_id)
        return self.session.scalar(query)

    def is_user_exists(self, telegram_id: int) -> bool:
        return bool(self.get_user_by_telegram_id(telegram_id))

    # def create_user(self, user: UserModel) -> UserModel:
        