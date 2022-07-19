import asyncio
import logging
import os
from datetime import datetime

import uvloop
from beryl_events_utils import BerylEventsUtils
from dateutil import parser
from discord.ext import commands
from dotenv import load_dotenv
from rin_exceptions import NoItemsError

load_dotenv()

POSTGRES_PASSWORD = os.getenv("Postgres_Password")
POSTGRES_SERVER_IP = os.getenv("Postgres_IP")
POSTGRES_DATABASE = os.getenv("Postgres_Events_Database")
POSTGRES_USERNAME = os.getenv("Postgres_User")
POSTGRES_PORT = os.getenv("Postgres_Port")
CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] | %(asctime)s >> %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)

eventUtils = BerylEventsUtils()
today = datetime.now()


class EventTaskProcess:
    def __init__(self):
        self.self = self

    async def checkEventPassed(self):
        """Checks if the event has passed, and then set the value as passed. This will happen for every 1 hour"""
        while True:
            await asyncio.sleep(3600)
            mainRes = await eventUtils.obtainEventsBool(False, uri=CONNECTION_URI)
            try:
                if len(mainRes) == 0:
                    raise NoItemsError
                else:
                    for mainItems in mainRes:
                        eventDate = dict(mainItems)["event_date"]
                        eventParsedDate = parser.isoparse(eventDate)
                        if eventParsedDate < today:
                            await eventUtils.setEventPassed(
                                uuid=dict(mainItems)["event_item_uuid"],
                                event_passed=True,
                            )
                        elif eventParsedDate == today:
                            await eventUtils.setEventPassed(
                                uuid=dict(mainItems)["event_item_uuid"],
                                event_passed=True,
                            )
                        elif eventParsedDate > today:
                            continue
            except NoItemsError:
                logging.warn(
                    "No events found within the database. Continuing to check for more"
                )
                continue

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class EventTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(ctx):
        mainProcesses = EventTaskProcess()
        mainProc = asyncio.create_task(
            mainProcesses.checkEventPassed(), name="CheckEventPassed"
        )
        backgroundTasks = set()
        backgroundTasks.add(mainProc)
        mainProc.add_done_callback(backgroundTasks.discard)
        logging.info("Successfully started Beryl's Event Checker")


def setup(bot):
    bot.add_cog(EventTasks(bot))
