import asyncio
import os

from beryl_events_utils import BerylEventsUtils
from dotenv import load_dotenv

eventUtils = BerylEventsUtils()

load_dotenv()

MONGO_PASSWORD = os.getenv("MongoDB_Password")
MONGO_IP = os.getenv("MongoDB_IP")
MONGO_USER = os.getenv("MongoDB_User")
MONGODB_PORT = os.getenv("MongoDB_Port")


async def main():
    # print(await eventUtils.ins(343, 5453, 4, 4, "test", "test3", False))
    mainRes = await eventUtils.findProjection()
    for res in mainRes:
        print(dict(res))


asyncio.run(main())
