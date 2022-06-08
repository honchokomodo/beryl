import asyncio
import os

import motor.motor_asyncio
import uvloop
from beanie import Document, init_beanie
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

MONGO_PASSWORD = os.getenv("MongoDB_Password")
MONGO_IP = os.getenv("MongoDB_IP")
MONGO_USER = os.getenv("MongoDB_User")
MONGODB_PORT = os.getenv("MongoDB_Port")


class Events(Document):
    uuid: str
    date: str
    guild_id: int
    author_id: int
    month: int
    day: int
    year: int
    name: str
    description: str
    passed: bool


class EventsProjectDates(BaseModel):
    month: int
    day: int
    year: int
    passed: bool


class BerylEventsUtils:
    def __init__(self):
        self.self = self

    async def ins(
        self,
        uuid: int,
        date: int,
        guild_id: int,
        author_id: int,
        month_entry: int,
        day_entry: int,
        year_entry: int,
        name: str,
        description: str,
        passed: bool,
    ):
        """Inserts a new events entry into the database

        Args:
            uuid (int): The unique ID of the event
            date (int): The date of when it is added
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
            uuid=uuid,
            date=date,
            guild_id=guild_id,
            author_id=author_id,
            month=month_entry,
            day=day_entry,
            year=year_entry,
            name=name,
            description=description,
            passed=passed,
        )
        await entry.create()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def listAll(self, user_id: int):
        """Returns all events in the database"""
        clientList = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_IP}:{MONGODB_PORT}"
        )
        await init_beanie(database=clientList.beryl_events, document_models=[Events])
        return await Events.find(Events.author_id == user_id).to_list()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def findEntry(self, user_id: int, name: str):
        """Finds 1 entry from a user's event based on the given name

        Args:
            user_id (int): User's Discord ID
            name (int): The name of the event
        """
        clientFindOne = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_IP}:{MONGODB_PORT}"
        )
        await init_beanie(database=clientFindOne.beryl_events, document_models=[Events])
        return await Events.find(
            Events.author_id == user_id, Events.name == name
        ).to_list()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def findEntryUpdate(
        self,
        user_id: int,
        original_name: str,
        new_name: str,
        description: str,
        month: int,
        day: int,
        year: int,
    ):
        """Finds 1 entry from a user's event based on the given name and updates the data

        Args:
            user_id (int): User's Discord ID
            name (int): The name of the event
        """
        clientFindOne = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_IP}:{MONGODB_PORT}"
        )
        await init_beanie(database=clientFindOne.beryl_events, document_models=[Events])
        mainUpdate = await Events.find_one(
            Events.author_id == user_id, Events.name == original_name
        )
        mainUpdate.name = new_name
        mainUpdate.description = description
        mainUpdate.month = month
        mainUpdate.day = day
        mainUpdate.year = year
        await mainUpdate.save()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def findProjection(self):
        """Finds projected values"""
        clientProjection = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_IP}:{MONGODB_PORT}"
        )
        await init_beanie(
            database=clientProjection.beryl_events, document_models=[Events]
        )
        return await Events.find_all().project(EventsProjectDates).to_list()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def setEventPassed(self):
        """Sets the event as passed"""
        clientPassed = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_IP}:{MONGODB_PORT}"
        )
        await init_beanie(database=clientPassed.beryl_events, document_models=[Events])
        mainPassed = Events.find(Events.passed == False)
        mainPassed.passed = True
        await mainPassed.save()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def removeEvent(self, uid: int, name: str):
        """Removes an event from the database

        Args:
            uid (int): Discord User's ID
            name (str): Name of the event
        """
        clientRmEvent = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_IP}:{MONGODB_PORT}"
        )
        await init_beanie(database=clientRmEvent.beryl_events, document_models=[Events])
        await Events.find(Events.author_id == uid, Events.name == name).delete()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
