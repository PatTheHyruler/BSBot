from .achievements_api import AchievementsAPI
from .actions import Actions
from .storage.uow import UnitOfWork
from .achievements import Achievements


def setup(bot):
    uow = UnitOfWork(bot)
    achievements_actions = Actions(uow)

    bot.add_cog(Achievements(uow, achievements_actions))
    bot.add_cog(AchievementsAPI(uow, achievements_actions))
