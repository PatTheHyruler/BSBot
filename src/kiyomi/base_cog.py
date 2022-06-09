from abc import abstractmethod
from typing import Generic, TypeVar

from discord.app_commands import CommandInvokeError
from discord.ext import commands
from discord.ext.commands import Context, CogMeta
from termcolor import colored

from .service import BaseServiceUnitOfWork
from .error import KiyomiException, CogException
from .kiyomi import Kiyomi
from src.log import Logger

TServiceUOW = TypeVar("TServiceUOW", bound=BaseServiceUnitOfWork)


class BaseCog(commands.Cog, Generic[TServiceUOW], metaclass=CogMeta):
    def __init__(self, bot: Kiyomi, service_uow: TServiceUOW):
        self.bot = bot
        self.service_uow = service_uow

        self.register_events()

    @abstractmethod
    def register_events(self):
        pass

    async def cog_before_invoke(self, ctx: Context[Kiyomi]):
        command_args = [f"{item['name']}: {item['value']}" for item in ctx.interaction.data["options"]]

        Logger.log(
            self.qualified_name,
            f"{colored(ctx.interaction.user.name, 'blue')} executed command "
            f"{colored('/' + ctx.command.qualified_name, 'blue')} "
            f"{colored(''.join(command_args), 'cyan')} in "
            f"{colored(f'#{ctx.interaction.channel.name}', 'blue')} at "
            f"{colored(ctx.interaction.guild.name, 'blue')}",
        )

        await ctx.trigger_typing()

    async def cog_command_error(self, ctx: Context[Kiyomi], error: Exception):
        if isinstance(error, CommandInvokeError):
            error = error.original

        if isinstance(error, KiyomiException):
            if error.is_handled:
                return

        if isinstance(error, CogException):
            return await error.handle(ctx=ctx, bot=self.bot)
