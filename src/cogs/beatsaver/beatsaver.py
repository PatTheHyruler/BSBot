from typing import List, TYPE_CHECKING

from discord import app_commands, Interaction
from discord.app_commands import Transform
from discord.ext import commands

from src.kiyomi import Kiyomi
from src.log import Logger
from .services import BeatmapAutocompleteService, BeatmapService
from .beatsaver_cog import BeatSaverCog
from .errors import BeatmapNotFound
from .messages.views.song_view import SongView
from src.cogs.settings.storage.model.emoji_setting import EmojiSetting
from .storage.model.beatmap import Beatmap
from .transformers.beatmap_key_transformer import BeatmapKeyTransformer

if TYPE_CHECKING:
    from src.cogs.scoresaber.storage.model.leaderboard import Leaderboard


class BeatSaver(BeatSaverCog, name="Beat Saver"):
    def __init__(
            self,
            bot: Kiyomi,
            beatmap_service: BeatmapService,
            beatmap_autocomplete_service: BeatmapAutocompleteService
    ):
        super().__init__(bot, beatmap_service, beatmap_autocomplete_service)

        # Register events
        self.events()

    def events(self):

        @self.bot.events.on("on_new_leaderboards")
        async def attach_song_to_score(leaderboards: List["Leaderboard"]):
            song_hashes = [leaderboard.song_hash for leaderboard in leaderboards]

            try:
                await self.beatmap_service.get_beatmaps_by_hashes(list(set(song_hashes)))
            except BeatmapNotFound as error:
                Logger.log("on_new_leaderboards", error)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.beatmap_service.start_scoresaber_api_client()

        settings = [
            EmojiSetting.create(self.bot, "Easy emoji", "easy_difficulty_emoji"),
            EmojiSetting.create(self.bot, "Normal emoji", "normal_difficulty_emoji"),
            EmojiSetting.create(self.bot, "Hard emoji", "hard_difficulty_emoji"),
            EmojiSetting.create(self.bot, "Expert emoji", "expert_difficulty_emoji"),
            EmojiSetting.create(self.bot, "Expert+ emoji", "expert_plus_difficulty_emoji"),
            EmojiSetting.create(self.bot, "Standard emoji", "standard_game_mode_emoji"),
            EmojiSetting.create(self.bot, "One Saber emoji", "one_saber_game_mode_emoji"),
            EmojiSetting.create(self.bot, "No Arrows emoji", "no_arrows_game_mode_emoji"),
            EmojiSetting.create(self.bot, "90 Degree emoji", "90_degree_game_mode_emoji"),
            EmojiSetting.create(self.bot, "360 Degree emoji", "360_degree_game_mode_emoji"),
            EmojiSetting.create(self.bot, "Lightshow emoji", "lightshow_game_mode_emoji"),
            EmojiSetting.create(self.bot, "Lawless emoji", "lawless_game_mode_emoji")
        ]

        self.bot.events.emit("setting_register", settings)

    @app_commands.command()
    @app_commands.rename(beatmap="key")
    @app_commands.describe(beatmap="Beatmap key (25f)")
    async def map(
            self,
            ctx: Interaction,
            beatmap: Transform[Beatmap, BeatmapKeyTransformer]
    ):
        """Displays song info."""

        song_view = SongView(self.bot, ctx.guild, beatmap)

        await song_view.respond(ctx)
