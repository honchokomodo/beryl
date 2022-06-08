import asyncio
import os
import re

import aiohttp
import discord
import ffmpeg
import orjson
import simdjson
import uvloop
from discord.commands import Option, slash_command
from discord.ext import commands

parser = simdjson.Parser()
hypixel_api_key = os.getenv("Hypixel_API_Key")


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

    @slash_command(name="ping", description="The Lag-o-meter, often lies")
    async def pingChecker(self, ctx):
        embed = discord.Embed()
        embed.description = f"Bot Latency: {round(self.bot.latency * 1000)}ms"
        await ctx.respond(embed=embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @slash_command(
        name="hypixel-count",
        description="Returns the amount of players in each game server",
    )
    async def player_count(self, ctx):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"key": hypixel_api_key}
            async with session.get(
                "https://api.hypixel.net/counts", params=params
            ) as response:
                status = await response.content.read()
                statusMain = parser.parse(status, recursive=True)
                try:
                    embedVar = discord.Embed(
                        title="Games Player Count",
                        color=discord.Color.from_rgb(186, 193, 255),
                    )
                    for k, v in statusMain["games"].items():
                        embedVar.add_field(name=k, value=v["players"], inline=True)
                    await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "The command broke. Please try again."
                    embedVar.add_field(name="Reason", value=str(e), inline=False)
                    await ctx.respond(embed=embedVar)


def setup(bot):
    bot.add_cog(usefulThings(bot))
