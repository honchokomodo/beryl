import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv() 

Token = os.getenv("Beryl_Keys")

# PyCord should have slash cmds...

prefixes = 'beryl ', 'Beryl ', 'br '
client = commands.Bot(command_prefix=prefixes)
status = 'https://youtu.be/QPqf2coKBl8'

# Loads all Cogs
initial_extensions = [
    "Cogs.edictHelp",
    "Cogs.fun-stuff",
    "Cogs.tasks",
    "Cogs.useful-things",
    "Cogs.xp"
]
for extension in initial_extensions:
    client.load_extension(extension)

@client.event
async def on_ready():
    print('ready')
    await client.change_presence(activity=discord.Game(status))
    

client.run(Token)
