from aiogram_dialog import DialogManager

from infrastructure.repo_holder import RepoHolder


async def get_user_data(
    dialog_manager: DialogManager,
    repo_holder: RepoHolder,
    **kwargs,
) -> dict:
    user = await repo_holder.user_repo.get_user_by_telegram_id(dialog_manager.event.from_user.id)
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "language_code": user.language_code,
    }

async def get_bot_info(
    dialog_manager: DialogManager,
    repo_holder: RepoHolder,
    **kwargs,
) -> dict:
    bot = await dialog_manager.event.bot.get_me()
    return {
        "bot_username": bot.username,
    }