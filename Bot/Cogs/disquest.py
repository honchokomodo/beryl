import asyncio
import os
import random
import uuid

import discord
import uvloop
from discord.commands import SlashCommandGroup
from discord.ext import commands
from disquest_utils import DisQuestUsers, lvl
from dotenv import load_dotenv

load_dotenv()

PASSWORD = os.getenv("Postgres_Password")
IP = os.getenv("Postgres_IP")
USER = os.getenv("Postgres_User")
DATABASE = os.getenv("Postgres_Database")
PORT = os.getenv("Postgres_Port")
CONNECTION_URI = f"postgresql+asyncpg://{USER}:{PASSWORD}@{IP}:{PORT}/{DATABASE}"

user = DisQuestUsers()


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
        await user.insUser(
            user_uuid=str(uuid.uuid4()),
            user_id=interaction.user.id,
            guild_id=interaction.guild_id,
            uri=CONNECTION_URI,
        )
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

    disquest = SlashCommandGroup("disquest", "Commands for Disquest")
    disquestRank = disquest.create_subgroup("rank", "Commands for Disquest")

    @disquest.command(name="mylvl")
    async def mylvl(self, ctx):
        """Displays your activity level!"""
        try:
            xp = await user.getUserXP(
                user_id=ctx.user.id, guild_id=ctx.guild.id, uri=CONNECTION_URI
            )
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 217, 254))
            embedVar.add_field(name="User", value=f"{ctx.author.mention}", inline=True)
            embedVar.add_field(
                name="LVL", value=f"{lvl.cur(dict(xp)['xp'])}", inline=True
            )
            embedVar.add_field(
                name="XP",
                value=f"{dict(xp)['xp']}/{lvl.next(dict(xp)['xp'])*100}",
                inline=True,
            )
            await ctx.respond(embed=embedVar)
        except TypeError:
            embedError = discord.Embed()
            embedError.description = "It seems like you haven't created a DisQuest account yet. Please run the command `/disquest-init` to first create your account."
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @disquest.command(name="init")
    async def disquestInit(self, ctx):
        """Initializes the database for DisQuest!"""
        embed = discord.Embed()
        embed.description = "Do you wish to initialize your DisQuest account? This is completely optional. Click on the buttons to confirm"
        await ctx.respond(embed=embed, view=View())

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @disquestRank.command(name="local")
    async def rank(self, ctx):
        """Displays the most active members of your server!"""
        getUserRank = await user.userLocalRank(
            guild_id=ctx.guild.id, uri=CONNECTION_URI
        )
        for i, items in enumerate(getUserRank):
            getUserInfo = await self.bot.get_or_fetch_user(dict(items)["user_id"])
            getUserRank[
                i
            ] = f"{i}. {getUserInfo.display_name} | XP. {dict(items)['xp']}\n"
        embedVar = discord.Embed(color=discord.Color.from_rgb(254, 255, 217))
        embedVar.description = f"**Server Rankings**\n{''.join(list(getUserRank))}"
        await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @disquestRank.command(name="global")
    async def grank(self, ctx):
        """Displays the most active members of all servers that this bot is connected to!"""
        getGlobalRank = await user.globalRank(uri=CONNECTION_URI)
        for i, items in enumerate(getGlobalRank):
            getUserInfo = await self.bot.get_or_fetch_user(dict(items)["user_id"])
            getGlobalRank[
                i
            ] = f"{i}. {getUserInfo.display_name} | XP. {dict(items)['xp']}\n"
        embedVar = discord.Embed(color=discord.Color.from_rgb(217, 255, 251))
        embedVar.description = f"**Global Rankings**\n{''.join(list(getGlobalRank))}"
        await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class DisQuestListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return
        reward = random.randint(0, 20)
        try:
            await user.addxp(
                offset=reward,
                user_id=ctx.author.id,
                guild_id=ctx.guild.id,
                uri=CONNECTION_URI,
            )
        except TypeError:
            pass

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(DisQuest(bot))
    bot.add_cog(DisQuestListener(bot))
