import asyncio
import logging
import os
import random

import discord
import uvloop
from discord.commands import slash_command
from discord.ext import commands
from disquest_utils import DisQuestUsers, lvl
from dotenv import load_dotenv
from sqlalchemy import (BigInteger, Column, Integer, MetaData, Table, func,
                        select)
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

PASSWORD = os.getenv("Postgres_Password")
IP = os.getenv("Postgres_IP")
USER = os.getenv("Postgres_User")
DATABASE = os.getenv("Postgres_Database")
PORT = os.getenv("Postgres_Port")

user = DisQuestUsers()

logging.basicConfig(
    level=logging.WARNING,
    format="[%(levelname)s] | %(asctime)s >> %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)


class View(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    @discord.ui.button(
        label="Yes",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:check:314349398811475968>"),
    )
    async def button_callback(self, button, interaction):
        await user.onInit(interaction.user.id, interaction.guild_id)
        await interaction.response.send_message(
            "Confirmed. Now you can compete for higher scores! "
        )

    @discord.ui.button(
        label="No",
        row=0,
        style=discord.ButtonStyle.primary,
        emoji=discord.PartialEmoji.from_str("<:xmark:314349398824058880>"),
    )
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_message("Welp, you choose not to ig...")


class DisQuest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="mylvl",
        description="Displays your activity level!",
        guild_ids=[978909341665079366],
    )
    async def mylvl(self, ctx):
        try:
            xp = await user.getxp(ctx.user.id, ctx.guild.id)
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 217, 254))
            embedVar.add_field(name="User", value=f"{ctx.author.mention}", inline=True)
            embedVar.add_field(name="LVL", value=f"{lvl.cur(xp)}", inline=True)
            embedVar.add_field(name="XP", value=f"{xp}/{lvl.next(xp)*100}", inline=True)
            await ctx.respond(embed=embedVar)
        except TypeError:
            embedError = discord.Embed()
            embedError.description = "It seems like you haven't created a DisQuest account yet. Please run the command `/disquest-init` to first create your account."
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class DisQuestV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="rank",
        description="Displays the most active members of your server!",
        guild_ids=[978909341665079366],
    )
    async def rank(self, ctx):
        gid = ctx.guild.id
        meta = MetaData()
        engine = create_async_engine(
            f"postgresql+asyncpg://{USER}:{PASSWORD}@{IP}:{PORT}/{DATABASE}"
        )
        users = Table(
            "users",
            meta,
            Column("id", BigInteger),
            Column("gid", BigInteger),
            Column("xp", Integer),
        )
        async with engine.connect() as conn:
            s = (
                select(Column("id", BigInteger), Column("xp", Integer))
                .where(users.c.gid == gid)
                .order_by(users.c.xp.desc())
            )
            results = await conn.execute(s)
            members = list(results.fetchall())
            for i, mem in enumerate(members):
                members[
                    i
                ] = f"{i}. {(await self.bot.fetch_user(mem[0])).name} | XP. {mem[1]}\n"
            embedVar = discord.Embed(color=discord.Color.from_rgb(254, 255, 217))
            embedVar.description = f"**Server Rankings**\n{''.join(members)}"
            await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class DisQuestV3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="globalrank",
        description="Displays the most active members of all servers that this bot is connected to!",
        guild_ids=[978909341665079366],
    )
    async def grank(self, ctx):
        meta = MetaData()
        engine = create_async_engine(
            f"postgresql+asyncpg://{USER}:{PASSWORD}@{IP}:{PORT}/{DATABASE}"
        )
        users = Table(
            "users",
            meta,
            Column("id", BigInteger),
            Column("gid", BigInteger),
            Column("xp", Integer),
        )
        async with engine.connect() as conn:
            s = (
                select(Column("id", Integer), func.sum(users.c.xp).label("txp"))
                .group_by(users.c.id)
                .group_by(users.c.xp)
                .order_by(users.c.xp.desc())
                .limit(10)
            )
            results = await conn.execute(s)
            results_fetched = results.fetchall()
            members = list(results_fetched)
            for i, mem in enumerate(members):
                members[
                    i
                ] = f"{i}. {(await self.bot.fetch_user(mem[0])).name} | XP. {mem[1]}\n"
            embedVar = discord.Embed(color=discord.Color.from_rgb(217, 255, 251))
            embedVar.description = f"**Global Rankings**\n{''.join(members)}"
            await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class DisQuestV4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return
        reward = random.randint(0, 20)
        try:
            await user.addxp(reward, ctx.author.id, ctx.guild.id)
        except TypeError:
            logging.error(
                f"[{ctx.author.name}#{ctx.author.discriminator} - {ctx.guild}] User has not initialized DisQuest account"
            )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class DisQuestV5(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="disquest-init",
        description="Initializes the database for DisQuest!",
        guild_ids=[978909341665079366],
    )
    async def disquestInit(self, ctx):
        embed = discord.Embed()
        embed.description = "Do you wish to initialize your DisQuest account? This is completely optional. Click on the buttons to confirm"
        await ctx.respond(embed=embed, view=View())


def setup(bot):
    bot.add_cog(DisQuest(bot))
    bot.add_cog(DisQuestV2(bot))
    bot.add_cog(DisQuestV3(bot))
    bot.add_cog(DisQuestV4(bot))
    bot.add_cog(DisQuestV5(bot))
