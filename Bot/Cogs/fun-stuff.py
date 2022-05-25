import asyncio
import random
from hashlib import sha1

import uvloop
from discord.ext import commands


def is_love_in_the_air(percentage):
    if percentage < 20:
        return "smells like hatred!"
    if percentage < 40:
        return "best stay apart!"
    if percentage < 60:
        return "let's stay friends!"
    if percentage < 85:
        return "the air buzzes with love!"
    return "true love is in the air!"


class fun_stuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="ship", help="(person_a, person_b, show_hash=" "): the love calculator"
    )
    async def ship(self, ctx, person_a, person_b, show_hash=""):
        a = person_a + person_b
        hashstr = sha1(bytes(a, "utf-8")).hexdigest()
        shash = f"\nSHA1 HASH: {hashstr}" if show_hash == "SHOW_HASH" else ""
        percentage = round(int(hashstr, 16) / 2**160 * 100, 2)
        yeah = is_love_in_the_air(percentage)
        await ctx.send(f"Their love is {percentage}%. {yeah}{shash}")

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @commands.command(name="sex", help="(person): the sex calculator")
    async def sex(self, ctx, person):
        sexsuccessresponses = [
            "You have successfully fucked {}! You were very submissive and breedable",
            "Ou la la! You successfully sexed {}! You were so breedable you bore their twins!",
        ]
        sexfailureresponses = [
            "You did not fuck {}. You were too dominant and unbreedable"
        ]
        if random.randint(0, 1):
            await ctx.send(random.choice(sexsuccessresponses).format(person))
        else:
            await ctx.send(random.choice(sexfailureresponses).format(person))

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @commands.command(help="(things): just says things")
    async def say(self, ctx, things):
        print(f"{ctx.author.name} used say with arg {things}")
        await ctx.send(things.replace("@", ""))

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @commands.command(help="(length=16): funne!")
    async def laugh(self, ctx, length=16):
        laughter = "".join(
            [random.choice("ASDFGHJKL") for _ in range(min(length, 2001))]
        )
        await ctx.send(laughter)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @commands.command(help="(floor, ceil): sends a random int between floor and ceil")
    async def randint(self, ctx, floor, ceil):
        await ctx.send(random.randint(int(floor), int(ceil)))

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @say.error
    async def say_error(self, ctx, error):
        await ctx.send(error)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @sex.error
    async def sex_error(self, ctx, error):
        await ctx.send(error)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @randint.error
    async def randint_error(self, ctx, error):
        await ctx.send(error)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @laugh.error
    async def laugh_error(self, ctx, error):
        await ctx.send(error)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @ship.error
    async def ship_error(self, ctx, error):
        await ctx.send(error)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(fun_stuff(bot))
