import asyncio
import json
import math
import random
import time

import uvloop
from discord.ext import commands

with open("mmmm_a_thicccyyy.json") as mmmm_a_thicccyyy:
    data = json.loads(mmmm_a_thicccyyy.read())

cooldown = {}
countcooldown = 0
countresponse = {}


class xpUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def givexp(self, ctx):
        guild_id = f"{ctx.guild.id}"
        author_id = f"{ctx.author.id}"
        try:
            int(data[guild_id]["users"][author_id]["xp"])
        except ValueError:
            print("it is not a number or something")
            return

        pre_level = math.floor(math.log(data[guild_id]["users"][author_id]["xp"], 1.1))
        try:
            if author_id not in cooldown[guild_id]:
                data[guild_id]["users"][author_id]["xp"] += random.randint(
                    1000000, 1200000
                )
                cooldown[guild_id].append(author_id)
        except KeyError:
            data[guild_id]["users"][author_id]["xp"] += random.randint(1000000, 1200000)
            cooldown.update({guild_id: [author_id]})
        post_xp = data[guild_id]["users"][author_id]["xp"]
        post_level = math.floor(math.log(post_xp, 1.1))
        if pre_level < post_level:
            try:
                # Probably not a good idea to send level up                # If you are getting the bot verifed on discords.bots.gg
                channel = self.bot.get_channel(int(data[guild_id]["levelchannel"]))
                await channel.send(
                    f"congrats **{ctx.author.name}** you are now level **{post_level}** with **{post_xp}** xp"
                )
            except KeyError:
                await ctx.channel.send(
                    f"congrats **{ctx.author.name}** you are now level **{post_level}** with **{post_xp}** xp"
                )
        try:
            levelroles2 = data[guild_id]["levelroles"]
            for roleid in levelroles2:
                role = ctx.guild.get_role(int(roleid))
                if post_level >= levelroles2[roleid]:
                    await ctx.author.add_roles(role)
                else:
                    await ctx.author.remove_roles(role)
        except KeyError:
            pass

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @commands.Cog.listener()
    async def on_message(self, ctx):
        global cooldown

        if ctx.author == self.bot.user:
            return
        if ctx.author.bot:
            return

        try:
            guild_id = f"{ctx.guild.id}"
        except AttributeError:
            await self.bot.process_commands(ctx)
            return
        author_id = f"{ctx.author.id}"

        try:
            print(f'{time.time()}: {data[guild_id]["users"][author_id]}')
            data[guild_id].update({"name": ctx.guild.name})
            data[guild_id]["users"][author_id].update({"name": ctx.author.name})
        except KeyError:
            try:
                print(data[guild_id]["users"])
            except KeyError:
                try:
                    print(data[guild_id])
                except KeyError:
                    print("could not find the guild. making one")
                    data.update(
                        {guild_id: {"name": ctx.guild.name, "leveltrue": False}}
                    )
                print("could not find a list of users. making one")
                data[guild_id].update({"users": {}})
            print("could not find the user. making one")
            data[guild_id]["users"].update(
                {author_id: {"name": ctx.author.name, "xp": 1}}
            )
        decision = data[guild_id]["leveltrue"]
        try:
            if ctx.channel.id in data[guild_id]["nolevels"]:
                decision = False
        except KeyError:
            pass
        finally:
            if decision:
                utils = xpUtils()
                await utils.givexp(ctx)

        await self.bot.process_commands(ctx)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(xpUtils(bot))
