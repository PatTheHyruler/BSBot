from .emoji_echo import EmojiEcho
from .emoji_echo_api import EmojiEchoAPI
from .services import ServiceUnitOfWork
from .storage import StorageUnitOfWork
from src.kiyomi import Kiyomi


async def setup(bot: Kiyomi):
    storage_uow = StorageUnitOfWork(await bot.database.get_session())
    service_uow = ServiceUnitOfWork(bot, storage_uow)

    await bot.add_cog(EmojiEcho(bot, service_uow))
    await bot.add_cog(EmojiEchoAPI(bot, service_uow))
