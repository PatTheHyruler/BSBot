import glob
import os

import discord
from sqlalchemy import create_engine

from BSBot import BSBot
from src.api import ScoreSaber, BeatSaver
from src.commands.beatsaber import Security
from src.commands.beatsaber.actions import Actions
from src.commands.beatsaber.beatsaber import BeatSaber
from src.commands.beatsaber.tasks import Tasks
from src.storage.database import Database
from src.storage.uow import UnitOfWork
from src.utils import Utils
from .factories import *
import discord.ext.test as dpytest


@pytest.fixture
def pre_bot(event_loop):
    intents = discord.Intents.default()
    intents.members = True
    return BSBot("!", loop=event_loop, intents=intents)


@pytest.fixture(scope="session")
def scoresaber():
    return ScoreSaber()


@pytest.fixture(scope="session")
def beatsaver():
    return BeatSaver()


@pytest.fixture
def uow(pre_bot, scoresaber, beatsaver):
    engine = create_engine('sqlite:///:memory:')
    database = Database(engine)

    return UnitOfWork(pre_bot, database, scoresaber, beatsaver)


@pytest.fixture
def tasks(uow):
    return Tasks(uow)


@pytest.fixture
def actions(uow, tasks):
    return Actions(uow, tasks)


@pytest.fixture(autouse=True)
def disable_security():
    Security._running_tests = True


@pytest.fixture
def beatsaber_cog(uow, tasks, actions):
    return BeatSaber(uow, tasks, actions)


@pytest.fixture
def bot(pre_bot, beatsaber_cog):
    pre_bot.add_cog(beatsaber_cog)

    dpytest.configure(pre_bot, num_guilds=2, num_channels=1, num_members=1)
    return pre_bot


@pytest.fixture(autouse=True)
async def bot_is_ready(bot):
    Utils.running_tests = True


def pytest_sessionfinish():
    # dat files are created when using attachements
    print("\n-------------------------\nClean dpytest_*.dat files")
    file_list = glob.glob('./dpytest_*.dat')
    for file_path in file_list:
        try:
            os.remove(file_path)
        except Exception:
            print("Error while deleting file : ", file_path)
