import discord
from discord.ext import commands
import os
import json
import orjson
import asyncio
import random
import math
import time
from hashlib import sha1
import datetime
from dotenv import load_dotenv

load_dotenv() 

Token = os.getenv("Beryl_Keys")

# PyCord should have slash cmds...

prefixes = 'beryl ', 'Beryl ', 'br '
client = commands.Bot(command_prefix=prefixes)
status = 'https://youtu.be/QPqf2coKBl8'
with open('mmmm_a_thicccyyy.json') as mmmm_a_thicccyyy:
    data = json.loads(mmmm_a_thicccyyy.read())
with open('penis_pleasure_18.json') as sensitive_things:
    keys = json.loads(sensitive_things.read())
cooldown = {}
countcooldown = 0
countresponse = {}

async def givexp(message):
    guild_id = f'{message.guild.id}'
    author_id = f'{message.author.id}'
    try:
        int(data[guild_id]["users"][author_id]["xp"])
    except ValueError:
        print('it is not a number or something')
        return

    pre_level = math.floor(math.log(data[guild_id]["users"][author_id]["xp"], 1.1))
    try:
        if author_id not in cooldown[guild_id]:
            data[guild_id]["users"][author_id]["xp"] += random.randint(1000000, 1200000)
            cooldown[guild_id].append(author_id)
    except KeyError:
        data[guild_id]["users"][author_id]["xp"] += random.randint(1000000, 1200000)
        cooldown.update({guild_id: [author_id]})
    post_xp = data[guild_id]["users"][author_id]["xp"]
    post_level = math.floor(math.log(post_xp, 1.1))
    if pre_level < post_level:
        try:
            # Probably not a good idea to send level up messages 
            # If you are getting the bot verifed on discords.bots.gg
            channel = client.get_channel(int(data[guild_id]["levelchannel"]))
            await channel.send(
                f'congrats **{message.author.name}** you are now level **{post_level}** with **{post_xp}** xp')
        except KeyError:
            await message.channel.send(
                f'congrats **{message.author.name}** you are now level **{post_level}** with **{post_xp}** xp')
    try:
        levelroles2 = data[guild_id]["levelroles"]
        for roleid in levelroles2:
            role = message.guild.get_role(int(roleid))
            if post_level >= levelroles2[roleid]:
                await message.author.add_roles(role)
            else:
                await message.author.remove_roles(role)
    except KeyError:
        pass


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


async def cele():
    for i in data:
        try:
            ec = data[i]['events_channel']
            ec = client.get_channel(ec)
            data2 = [ii[1] for ii in data[i]['events'].items()]
            data3 = [iii for iii in data2 if days_until(iii['month'], iii['day']) == 0 and not iii['passed']]
            printable = []
            for n, iv in enumerate(data3):
                printable.append(f'{iv["name"]}:\n'
                                 f'{iv["on_start"]}\n'
                                 f'-----\n')
            # noinspection PyBroadException
            try:
                if len(printable) > 0:
                    await ec.send(f'there are events today!\n'
                                  f'{"".join(printable)}')
            except Exception as _:
                pass
        except KeyError:
            pass

    for vi in data:
        try:
            for vii in data[vi]['events']:
                data[vi]['events'][vii]['passed'] = days_until(data[vi]['events'][vii]['month'], data[vi]['events'][vii]['day']) == 0
        except KeyError:
            pass


async def every_minute():
    global cooldown
    while not client.is_closed():
        await asyncio.sleep(60)

        cooldown = {}
        await cele()


async def every_hour():
    while not client.is_closed():
        await asyncio.sleep(3600)
        f = open('mmmm_a_thicccyyy.json', 'w')
        f.write(json.dumps(data, indent=2))
        f.close()
        print('saved')




@client.event
async def on_ready():
    print('ready')
    await client.change_presence(activity=discord.Game(status))


@client.event
async def on_message(message):
    global cooldown

    if message.author == client.user:
        return
    if message.author.bot:
        return

    try:
        guild_id = f'{message.guild.id}'
    except AttributeError:
        await client.process_commands(message)
        return
    author_id = f'{message.author.id}'

    try:
        print(f'{time.time()}: {data[guild_id]["users"][author_id]}')
        data[guild_id].update({"name": message.guild.name})
        data[guild_id]["users"][author_id].update({"name": message.author.name})
    except KeyError:
        try:
            print(data[guild_id]["users"])
        except KeyError:
            try:
                print(data[guild_id])
            except KeyError:
                print('could not find the guild. making one')
                data.update({guild_id: {"name": message.guild.name, "leveltrue": False}})
            print('could not find a list of users. making one')
            data[guild_id].update({"users": {}})
        print('could not find the user. making one')
        data[guild_id]["users"].update({author_id: {"name": message.author.name, "xp": 1}})
    decision = data[guild_id]["leveltrue"]
    try:
        if message.channel.id in data[guild_id]["nolevels"]:
            decision = False
    except KeyError:
        pass
    finally:
        if decision:
            await givexp(message)

    await client.process_commands(message)


client.loop.create_task(every_minute())
client.loop.create_task(every_hour())
client.run(Token)
