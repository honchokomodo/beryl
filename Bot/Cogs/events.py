import os

import discord
from beryl_events_utils import BerylEventsUtils
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv

load_dotenv()

MONGO_PASSWORD = os.getenv("MongoDB_Password")
MONGO_IP = os.getenv("MongoDB_IP")
MONGO_USER = os.getenv("MongoDB_User")

eventUtils = BerylEventsUtils()


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
        description: Option(str, "The description of the event")
    ):
        """Adds an event"""
        guild_id = ctx.guild.id
        user_id = ctx.author.id
        passedCheck = False
        await eventUtils.ins(
            guild_id, user_id, month, day, name, description, passedCheck
        )
        await ctx.respond("Event added")

    @berylEvents.command(name="view")
    async def viewAll(self, ctx):
        """Views all events for your user"""
        user_id = ctx.author.id
        items = await eventUtils.listAll(user_id=user_id)
        print(items)
        mainPages = pages.Paginator(
            pages=[
                discord.Embed(
                    title=dict(mainItem)["name"],
                    description=dict(mainItem["description"]),
                )
                .add_field(name="Month", value=dict(mainItem)["month"], inline=True)
                .add_field(name="Day", value=dict(mainItem)["day"], inline=True)
                .add_field(name="Passed", value=dict(mainItem)["passed"], inline=True)
                for mainItem in items
            ]
        )
        await mainPages.respond(ctx.interaction, ephemeral=False)


def setup(bot):
    bot.add_cog(BerylEvents(bot))
