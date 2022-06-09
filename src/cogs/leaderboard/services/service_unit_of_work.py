from .score_leaderboard_service import ScoreLeaderboardService
from ..storage import StorageUnitOfWork
from src.kiyomi import BaseServiceUnitOfWork, Kiyomi


class ServiceUnitOfWork(BaseServiceUnitOfWork[StorageUnitOfWork]):
    def __init__(self, bot: Kiyomi, storage_uow: StorageUnitOfWork):
        super().__init__(storage_uow)

        self.score_leaderboards = ScoreLeaderboardService(bot, storage_uow)
