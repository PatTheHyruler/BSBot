from discord import app_commands, Interaction

from .services import ServiceUnitOfWork
from .storage.model.presence import Presence
from src.kiyomi import permissions, BaseCog
from src.kiyomi.permissions import admin_guild_list


class FancyPresence(BaseCog[ServiceUnitOfWork]):
    def register_events(self):
        pass

    status = app_commands.Group(
        name="status",
        description="Commands related to Kiyomi's status",
        guild_ids=admin_guild_list(),
    )

    @status.command(name="update")
    @permissions.is_bot_owner()
    async def status_update(self, ctx: Interaction):
        """Force update status"""

        await self.service_uow.presences.update_status()

        await ctx.response.send_message("Status force updated!", ephemeral=True)

    @status.command(name="set")
    @app_commands.describe(text="Text to display as status")
    @permissions.is_bot_owner()
    async def status_set(self, ctx: Interaction, text: str):
        """Force status text"""

        await self.service_uow.presences.set_presence(Presence(0, text))

        await ctx.response.send_message("Status updated!", ephemeral=True)

    @status.command(name="reset")
    @permissions.is_bot_owner()
    async def status_reset(self, ctx: Interaction):
        """Reset forced status"""

        await self.service_uow.presences.reset_presence()

        await ctx.response.send_message("Status updated!", ephemeral=True)
