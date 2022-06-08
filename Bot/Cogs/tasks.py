import asyncio
import datetime
import logging

from beryl_events_utils import BerylEventsUtils
from discord.ext import commands, tasks

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
        projectedValues = await berylUtils.findProjection()
        for res in projectedValues:
            dictRes = dict(res)
            today = datetime.date.today()
            eventDate = datetime.date(dictRes["year"], dictRes["month"], dictRes["day"])
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
        self.checkEvents.start()

    # Not sure if this will work or not...
    @tasks.loop()
    async def checkEvents(self):
        celeCheckerUtils = tasksCheckerUtils()
        await asyncio.sleep(5)
        logging.info("Checking events...")
        await celeCheckerUtils.celeCheck()


def setup(bot):
    bot.add_cog(tasksUtils(bot))
