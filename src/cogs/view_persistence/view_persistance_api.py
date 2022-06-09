from discord.ext import commands

from .services import ServiceUnitOfWork
from .errors import MissingPersistentViewClass
from .storage.model.persistence import Persistence
from src.kiyomi import BaseCog
from src.log import Logger


class ViewPersistenceAPI(BaseCog[ServiceUnitOfWork]):
    def register_events(self):
        @self.bot.events.on("on_new_view_sent")
        async def mark_scores_sent(persistence: Persistence):
            await self.service_uow.message_views.add_persistent_view(persistence)
            await self.service_uow.save_changes()

    @commands.Cog.listener()
    async def on_ready(self):
        persistences = await self.service_uow.message_views.get_persistent_views()

        for persistence in persistences:
            try:
                view = await persistence.get_view(self.bot)
                self.bot.add_view(view=view, message_id=persistence.message_id)
            except MissingPersistentViewClass as error:
                await error.handle()

        Logger.log("View Persistence", f"Loaded {len(persistences)} persistent views")
