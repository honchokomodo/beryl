import asyncio
import os
import uuid
from datetime import date, datetime

import discord
import uvloop
from beryl_events_utils import BerylEventsUtils
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv

load_dotenv()

MONGO_PASSWORD = os.getenv("MongoDB_Password")
MONGO_IP = os.getenv("MongoDB_IP")
MONGO_USER = os.getenv("MongoDB_User")

eventUtils = BerylEventsUtils()
today = datetime.now()
dateToday = date.today()


class BerylEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    berylEvents = SlashCommandGroup(
        "events", "Commands for Beryl Events", guild_ids=[978909341665079366]
    )

    @berylEvents.command(name="add")
    async def eventsList(
        self,
        ctx,
        *,
        month: Option(int, "The month that the event is on"),
        day: Option(int, "The number of the day"),
        name: Option(str, "The name of the event"),
        description: Option(str, "The description of the event"),
    ):
        """Adds an event"""
        guild_id = ctx.guild.id
        user_id = ctx.author.id
        mainUUID = uuid.uuid4().hex[:16]
        dateEntry = today.strftime("%B %d, %Y %H:%M:%S")
        todayYear = dateToday.year
        passedCheck = False
        await eventUtils.ins(
            uuid=mainUUID,
            date=dateEntry,
            guild_id=guild_id,
            author_id=user_id,
            month_entry=month,
            day_entry=day,
            year_entry=todayYear,
            name=name,
            description=description,
            passed=passedCheck,
        )
        await ctx.respond("Event added")

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @berylEvents.command(name="view")
    async def viewAll(self, ctx):
        """Views all events for your user"""
        user_id = ctx.author.id
        items = await eventUtils.listAll(user_id=user_id)
        mainPages = pages.Paginator(
            pages=[
                discord.Embed(
                    title=dict(mainItem)["name"],
                    description=dict(mainItem)["description"],
                )
                .add_field(name="Month", value=dict(mainItem)["month"], inline=True)
                .add_field(name="Day", value=dict(mainItem)["day"], inline=True)
                .add_field(name="Passed", value=dict(mainItem)["passed"], inline=True)
                .add_field(name="Date Added", value=dict(mainItem)["date"], inline=True)
                .add_field(name="UUID", value=dict(mainItem)["uuid"], inline=True)
                for mainItem in items
            ]
        )
        await mainPages.respond(ctx.interaction, ephemeral=False)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @berylEvents.command(name="countdown")
    async def dayCountDown(self, ctx, name: Option(str, "The name of the event")):
        """Checks how much days there is left before the event takes place"""
        uid = ctx.author.id
        itemsOne = await eventUtils.findEntry(user_id=uid, name=name)
        for items3 in itemsOne:
            eventDate = date(
                dict(items3)["year"], dict(items3)["month"], dict(items3)["day"]
            )
            diff = eventDate - dateToday
            monthObj = datetime.strptime(str(eventDate.month), "%m")
            monthName = monthObj.strftime("%B")
        pagesMain = pages.Paginator(
            pages=[
                discord.Embed(
                    title=dict(mainItem)["name"],
                    description=dict(mainItem)["description"],
                )
                .add_field(name="Days Remaining", value=diff.days, inline=True)
                .add_field(name="Event Date", value=eventDate, inline=True)
                .add_field(
                    name="Event Date (Full)",
                    value=f"{monthName} {eventDate.day}, {eventDate.year}",
                    inline=True,
                )
                for mainItem in itemsOne
            ]
        )
        await pagesMain.respond(ctx.interaction, ephemeral=False)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @berylEvents.command(name="Update")
    async def updateEvent(
        self,
        ctx,
        *,
        original_name: Option(str, "The original name of the event"),
        new_name: Option(str, "The name of the event"),
        description: Option(str, "The description of the event"),
        month: Option(int, "The month that the event is on"),
        day: Option(int, "The number of the day"),
        year: Option(int, "The year that the event is on"),
    ):
        """Updates an event"""
        user_id = ctx.author.id
        await eventUtils.findEntryUpdate(
            user_id=user_id,
            original_name=original_name,
            new_name=new_name,
            description=description,
            month=month,
            day=day,
            year=year,
        )
        await ctx.respond("The entry has been updated")

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(BerylEvents(bot))
