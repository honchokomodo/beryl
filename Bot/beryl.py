import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

Token = os.getenv("Beryl_Keys")

# PyCord should have slash cmds...

prefixes = "beryl ", "Beryl ", "br "
client = commands.Bot(command_prefix=".")
status = "https://youtu.be/QPqf2coKBl8"

# Loads all Cogs
initial_extensions = [
    "Cogs.fun-stuff",
    "Cogs.useful-things",
]
for extension in initial_extensions:
    client.load_extension(extension)


@client.event
async def on_ready():
    print("ready")
    await client.change_presence(activity=discord.Game(status))


client.run(Token)
