import logging
import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Set up needed intents
intents = discord.Intents.default()
intents.message_content = True

load_dotenv()

Token = os.getenv("Beryl_Keys")

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] | %(asctime)s >> %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)

client = commands.Bot(command_prefix=["beryl ", "Beryl ", "br "], intents=intents)
status = "https://youtu.be/QPqf2coKBl8"

# Loads all Cogs
path = Path(__file__).parents[0]
cogsList = os.listdir(os.path.join(path, "Cogs"))
for items in cogsList:
    if items.endswith(".py"):
        client.load_extension(f"Cogs.{items[:-3]}")


@client.event
async def on_ready():
    logging.info("Beryl is ready!")
    await client.change_presence(activity=discord.Game(status))


client.run(Token)
