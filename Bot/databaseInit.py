import asyncio
import os

import uvloop
from disquest_utils import DisQuestUsers
from dotenv import load_dotenv

load_dotenv()

PASSWORD = os.getenv("Postgres_Password")
IP = os.getenv("Postgres_IP")
USER = os.getenv("Postgres_User")
DATABASE = os.getenv("Postgres_Database")
PORT = os.getenv("Postgres_Port")


utils = DisQuestUsers()


async def main():
    await utils.initTables()


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(main())
