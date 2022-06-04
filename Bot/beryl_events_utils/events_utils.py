import os

import motor.motor_asyncio
from beanie import Document, init_beanie
from dotenv import load_dotenv

load_dotenv()

MONGO_PASSWORD = os.getenv("MongoDB_Password")
MONGO_IP = os.getenv("MongoDB_IP")
MONGO_USER = os.getenv("MongoDB_User")
MONGODB_PORT = os.getenv("MongoDB_Port")


class Events(Document):
    guild_id: int
    author_id: int
    month: int
    day: int
    name: str
    description: str
    passed: bool


class BerylEventsUtils:
    def __init__(self):
        self.self = self

    async def ins(
        self,
        guild_id: int,
        author_id: int,
        month: int,
        day: int,
        name: str,
        description: str,
        passed: bool,
    ):
        """Inserts a new events entry into the database

        Args:
            guild_id (int): Discord Guild ID
            author_id (int): Discord User ID
            month (int): Month of the event
            day (int): Day of the event
            name (str): Name of the event
            description (str): Description of the event
            passed (bool): Whether the event has already passed or not
        """
        client = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_IP}:{MONGODB_PORT}"
        )
        await init_beanie(database=client.beryl_events, document_models=[Events])
        entry = Events(
            guild_id=guild_id,
            author_id=author_id,
            month=month,
            day=day,
            name=name,
            description=description,
            passed=passed,
        )
        await entry.create()

    async def listAll(self, user_id: int):
        """Returns all events in the database"""
        clientList = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_IP}:{MONGODB_PORT}"
        )
        await init_beanie(database=clientList.beryl_events, document_models=[Events])
        return await Events.find(Events.author_id == user_id).to_list()
