import discord
from discord.ext import commands
import asyncio
import uvloop

class edictHelpClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="edicthelp")
    async def edicthelp(self, ctx):
        embed = discord.Embed()
        embed.description = """
        edict is used to edit the json file that the bot uses to store everything\n
        its very powerful\n
        every word in the path is called a key\n
        u have to have the >arrows> that shows the program where to separate it\n
        if u have only one key then u dont need to worry abt the arrows\n
        if u wanna figure out what keys there are in a path do one of these\n
        ```\n
        beryl edict ---your path here--- keys 0\n
        ```\n
        u have to have something at the end or it will cause an error and do nothing\n
        if u dont know what path to type just type "self" it will show you places to go\n
        if u wanna print someones xp or something you can do this\n
        ```\n
        beryl edict users>---user id here--->xp print 0\n
        ```\n
        i am gonna write more here later\n
        important things i should have added earlier:\n
        actions:\n
        ```\n
        print: sends the whole thing to the channel\n
        dumps: sends the whole thing as a json string\n
        keys: sends only the keys\n
        type: sends the datatype at the path\n
        update: updates the dict with a json string\n
        append: appends to lists\n
        pop: remove things from a dict or list\n
        ```\n
        disable levelling:\n
        ```beryl edict self update {\"leveltrue\":false}```\n
        there are more but i am lazy and do not want to write more
        """
        await ctx.send(embed=embed)
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

        
def setup(bot):
    bot.add_cog(edictHelpClass(bot))