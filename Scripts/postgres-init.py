import asyncio
import os
from pathlib import Path

import uvloop
from beryl_events_utils import BerylEventsUtils
from disquest_utils import DisQuestUsers
from dotenv import load_dotenv

path = Path(__file__).parents[1]
envPath = os.path.join(path, "Bot", ".env")

load_dotenv(envPath)

POSTGRES_PASSWORD = os.getenv("Postgres_Password")
POSTGRES_SERVER_IP = os.getenv("Postgres_IP")
POSTGRES_EVENTS_DATABASE = os.getenv("Postgres_Events_Database")
POSTGRES_DISQUEST_DATABASE = os.getenv("Postgres_Database")
POSTGRES_USERNAME = os.getenv("Postgres_User")
POSTGRES_PORT = os.getenv("Postgres_Port")
EVENTS_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_EVENTS_DATABASE}"
DISQUEST_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_DISQUEST_DATABASE}"

utils = DisQuestUsers()
eventUtils = BerylEventsUtils()


async def main():
    await utils.initTables(uri=DISQUEST_CONNECTION_URI)
    await eventUtils.initTables(uri=EVENTS_CONNECTION_URI)


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(main())
