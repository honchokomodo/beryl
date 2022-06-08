import asyncio
import datetime
import logging
import os
import re

import discord
import ffmpeg
import uvloop
from discord.commands import Option, slash_command
from discord.ext import commands

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] | %(asctime)s >> %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)


def days_until(month, day):
    try:
        today = datetime.date.today()
        year = today.year
        dt = datetime.date(year, month, day) - today
        if 0 <= dt.days:
            return dt.days
        return (datetime.date(year + 1, month, day) - today).days
    except TypeError:
        return 999


cooldown = {}
countcooldown = 0
countresponse = {}


class usefulThings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="ffmpegcve", description="Apparently convert video files to mp4"
    )
    async def ffmpegcve(
        self,
        ctx,
        *,
        video_file: Option(discord.Attachment, "The file to convert to mp4"),
    ):
        try:
            await video_file.save(fp="video")
            await ctx.respond("converting to mp4...")
            ffmpeg.input("video").output("ffmpeg.mp4").run()
            os.system("rm video")
            await ctx.respond("sending...")
            await ctx.respond(file=discord.File(r"ffmpeg.mp4"))
        except Exception as e:
            embedError = discord.Embed()
            embedError.description = "Something went wrong. Please try again"
            embedError.add_field(name="Error", value=e, inline=True)
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @slash_command(
        name="youtubedltte",
        description="Apparently downloads tiktok videos and sends it",
    )
    async def youtubedltte(
        self, ctx, url: Option(str, "The url of the video to download")
    ):
        try:
            ttfilter = re.compile(r"^https:\/\/vm.tiktok.com\/\w+\/$")
            if ttfilter.match(url):
                await ctx.send("downloading...")
                os.system(f"youtube-dl {url} -o youtubedl.mp4")
                file_size = os.path.getsize("youtubedl.mp4")
                await ctx.send(f"file size: {file_size} max 8000000")
                if file_size > 8000000:
                    await ctx.send("didnt even try sending video. file too big")
                else:
                    await ctx.send("sending...")
                    await ctx.send(file=discord.File(r"youtubedl.mp4"))
                os.system("rm youtubedl.mp4")
            else:
                await ctx.send(
                    r"link does not match regex `^https:\/\/vm.tiktok.com\/\w+\/$`. video was not downloaded"
                )
        except Exception as e:
            embedError = discord.Embed()
            embedError.description = "Something went wrong. Please try again"
            embedError.add_field(name="Error", value=e, inline=True)
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @slash_command(
        name="ping",
        description="The Lag-o-meter, often lies",
        guild_ids=[978909341665079366],
    )
    async def pingChecker(self, ctx):
        embed = discord.Embed()
        embed.description = f"Bot Latency: {round(self.bot.latency * 1000)}ms"
        await ctx.respond(embed=embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    # @commands.command(
    #     help='(path, action=print): hypixel api things. action can also be "keys"'
    # )
    # async def dump_count(self, ctx, path, action="print"):
    #     global countresponse, countcooldown

    #     if time.time() >= countcooldown + 60:
    #         # please use aiohttp for this instead
    #         r = requests.get(
    #             "https://api.hypixel.net/counts?key=" + keys["hypixelapikey"]
    #         )
    #         countcooldown = time.time()
    #         countresponse = orjson.loads(r.text)

    #     pathlist = path.split(">")
    #     a_key = countresponse
    #     if path != "self":
    #         for i in pathlist[0:-1]:
    #             a_key = a_key[i]
    #     else:
    #         pathlist = ["a"]
    #         a_key = {"a": countresponse}

    #     response = ""

    #     if action == "print":
    #         response = a_key[pathlist[-1]]
    #     if action == "keys":
    #         response = [i for i in a_key[pathlist[-1]]]

    #     await ctx.send(f"```json\n{orjson.dumps(response, indent=2)}\n```")

    # asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    # @dump_count.error
    # async def dump_count_error(self, ctx, error):
    #     await ctx.send(error)

    # asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(usefulThings(bot))
