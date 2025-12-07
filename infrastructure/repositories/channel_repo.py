from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import delete, select

from infrastructure.domain.models import ChannelModel


class ChannelRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_channel_by_id(self, id: int) -> ChannelModel | None:
        stmt = (
            select(ChannelModel)
            .where(ChannelModel.id == id)
            .options(joinedload(ChannelModel.user))
        )
        return await self.session.scalar(stmt)

    async def get_channels_by_user_id(self, user_id: int) -> list[ChannelModel]:
        stmt = (
            select(ChannelModel)
            .where(ChannelModel.user_id == user_id)
            .options(joinedload(ChannelModel.user))
        )
        return await self.session.scalars(stmt)

    async def create_channel(self, channel: ChannelModel) -> ChannelModel:
        self.session.add(channel)
        try:
            await self.session.commit()
            await self.session.refresh(channel)
            return channel
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def remove_channel_by_id(self, id: int) -> None:
        stmt = (
            delete(ChannelModel)
            .where(ChannelModel.id == id)
        )
        await self.session.execute(stmt)
        await self.session.commit()
