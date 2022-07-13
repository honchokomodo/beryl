import asyncio
import datetime
import logging

from beryl_events_utils import BerylEventsUtils
from discord.ext import commands

berylUtils = BerylEventsUtils()

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] | %(asctime)s >> %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)


class tasksCheckerUtils:
    def __init__(self):
        self.self = self

    async def celeCheck(self):
        while True:
            await asyncio.sleep(3600)
            projectedValues = await berylUtils.findProjection()
            for res in projectedValues:
                dictRes = dict(res)
                today = datetime.date.today()
                eventDate = datetime.date(
                    dictRes["year"], dictRes["month"], dictRes["day"]
                )
                if eventDate is not today:
                    logging.info(f"Date: {today} | There are no events today :(")
                elif eventDate > today:
                    logging.info("Setting event as passed")
                    await berylUtils.setEventPassed()
                else:
                    logging.info(f"Date: {today} | There are events today! :3")


class tasksUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        celeCheckerUtils = tasksCheckerUtils()
        task = asyncio.create_task(celeCheckerUtils.celeCheck(), name="CeleCheck")
        background_tasks = set()
        background_tasks.add(await task)
        task.add_done_callback(background_tasks.discard)
        logging.info("Started Event Checker - Events will be checked every hour")


def setup(bot):
    bot.add_cog(tasksUtils(bot))
