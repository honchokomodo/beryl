import asyncio
import os

import uvloop
from beryl_events_utils import BerylEventsUtils
from disquest_utils import DisQuestUsers
from dotenv import load_dotenv

load_dotenv()


POSTGRES_PASSWORD = os.getenv("Postgres_Password")
POSTGRES_SERVER_IP = os.getenv("Postgres_IP")
POSTGRES_DATABASE = os.getenv("Postgres_Events_Database")
POSTGRES_USERNAME = os.getenv("Postgres_User")
POSTGRES_PORT = os.getenv("Postgres_Port")
CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

utils = DisQuestUsers()
eventUtils = BerylEventsUtils()


async def main():
    await utils.initTables()
    await eventUtils.initTables(uri=CONNECTION_URI)


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(main())
