from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.repositories.user_repo import UserRepository

class RepoHolder:
    def __init__(self, session: AsyncSession):
        self.session = session

        # Repositories
        self.user_repo = UserRepository(session)