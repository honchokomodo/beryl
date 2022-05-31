import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
load_dotenv()

Token = os.getenv("Beryl_Keys")

# PyCord should have slash cmds...
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] | %(asctime)s >> %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)

prefixes = "beryl ", "Beryl ", "br "
client = commands.Bot(command_prefix=".", intents=intents)
status = "https://youtu.be/QPqf2coKBl8"

# Loads all Cogs
initial_extensions = [
    "Cogs.fun-stuff",
    "Cogs.useful-things",
    "Cogs.edictHelp",
    "Cogs.xp",
]
for extension in initial_extensions:
    client.load_extension(extension)


@client.event
async def on_ready():
    logging.info("Beryl is ready!")
    await client.change_presence(activity=discord.Game(status))


client.run(Token)
