import discord
from discord.ext import commands
import os
import json
import asyncio
import random
import math
import time
import requests
import re
from hashlib import sha1
import datetime
from dotenv import load_dotenv

load_dotenv() # Create a .env file and store all Tokens, API keys, and other sensitive info there. 


# from discord_slash import SlashCommand

prefixes = 'beryl ', 'Beryl ', 'br '
client = commands.Bot(command_prefix=prefixes)
# slash = SlashCommand(client)
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


@client.command(help='(): ahtynjrghtbshtrnsrthjnbsbthrgsa')
async def testcommand(ctx):
    await ctx.send('shut up')


@client.command(help='(): not done!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
async def edicthelp(ctx):
    await ctx.send(f'edict is used to edit the json file that the bot uses to store everything\n'
                   f'its very powerful\n'
                   f'every word in the path is called a key\n'
                   f'u have to have the >arrows> that shows the program where to separate it\n'
                   f'if u have only one key then u dont need to worry abt the arrows\n'
                   f'if u wanna figure out what keys there are in a path do one of these\n'
                   f'```\n'
                   f'beryl edict ---your path here--- keys 0\n'
                   f'```\n'
                   f'u have to have something at the end or it will cause an error and do nothing\n'
                   f'if u dont know what path to type just type "self" it will show you places to go\n'
                   f'if u wanna print someones xp or something you can do this\n'
                   f'```\n'
                   f'beryl edict users>---user id here--->xp print 0\n'
                   f'```\n'
                   f'i am gonna write more here later\n'
                   f'important things i should have added earlier:\n'
                   f'actions:\n'
                   f'```\n'
                   f'print: sends the whole thing to the channel\n'
                   f'dumps: sends the whole thing as a json string\n'
                   f'keys: sends only the keys\n'
                   f'type: sends the datatype at the path\n'
                   f'update: updates the dict with a json string\n'
                   f'append: appends to lists\n'
                   f'pop: remove things from a dict or list\n'
                   f'```\n'
                   f'disable levelling:\n'
                   r'```beryl edict self update {\"leveltrue\":false}```' + '\n'
                                                                            f'there are more but i am lazy and do not want to write more\n')


class useful_things(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    
    @commands.command(help='(): save userdata')
    async def write(self, ctx):
        if ctx.author.id != 301774808167743489: # THIS IS HORRIBLE CHANGE THIS ASAP
            await ctx.send('you are not the bot host')
            return
        f = open('mmmm_a_thicccyyy.json', 'w')
        f.write(json.dumps(data, indent=2))
        f.close()
        print('saved')
        await ctx.send('saved')
    
    @write.error
    async def write_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(help='(): converts video files to mp4')
    async def ffmpegcve(self, ctx):
        url = ctx.message.attachments[0].url
        await ctx.send('downloading...')
        r = requests.get(url)
        os.system('touch video')
        with open('video', 'wb') as v:
            v.write(r.content)
        await ctx.send('converting to mp4...')
        os.system('ffmpeg -i video ffmpeg.mp4 -y')
        os.system('rm video')
        await ctx.send('sending...')
        await ctx.send(file=discord.File(r'ffmpeg.mp4'))
    
    @ffmpegcve.error
    async def ffmpegcve_error(self, ctx, error):
        await ctx.send(error)
        
    @commands.command(help='(): downloads tiktok videos and sends it')
    async def youtubedltte(self, ctx, url):
        ttfilter = re.compile(r'https:\/\/vm.tiktok.com\/\w+\/')
        if ttfilter.match(url):
            await ctx.send('downloading...')
            os.system(f'youtube-dl {url} -o youtubedl.mp4')
            for i in range(4):
                await ctx.send(f'sending... try: {i}')
                try:
                    await ctx.send(file=discord.File(r'youtubedl.mp4'))
                    os.system('rm youtubedl.mp4')
                    return
                except:
                    await ctx.send('video file too large. scaling down')
                    os.system('ffmpeg -i youtubedl.mp4 youtubedl.mp4 -vf scale="(iw/2)+mod(iw,2):(ih/2)+mod(ih,2)" -y')
            await ctx.send('could not send video')
            os.system('rm youtubedl.mp4')
        else:
            await ctx.send(r'link does not match regex `https:\/\/vm.tiktok.com\/\w+\/`. video was not downloaded')
    
    @youtubedltte.error
    async def youtubedltte_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(help='(): lists upcoming events')
    async def events(self, ctx):
        data2 = [i[1] for i in data[f'{ctx.guild.id}']['events'].items()]
        data3 = sorted(data2, key=lambda a: days_until(a['month'], a['day']))
        printable = []
        for n, i in enumerate(data3):
            printable.append(
                f'{n:>3} -> in {days_until(i["month"], i["day"]):>4} days on {i["month"]:>2}/{i["day"]:<2}: {i["name"]}\n')
        await ctx.send(f'```cs\n{"".join(printable)}\n```')

    @events.error
    async def events_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(help='(): initializes the event list for you')
    async def events_setup(self, ctx):
        try:
            print(data[f'{ctx.guild.id}']['events'])
            await ctx.send(f'there is already an events dict. nothing happened')
        except KeyError:
            data[f'{ctx.guild.id}'].update({'events': {}})
            await ctx.send(f'events entry added to dict. access with:\n'
                           f'```beryl edict events print 0```')

    @commands.command(
        help='(month, day, name, *desc): adds an entry to the events list. one on entry per user, can be bypassed by edict')
    async def events_update(self, ctx, month, day, name, *desc):
        entry = data[f'{ctx.guild.id}']['events']
        entry.update({f'{ctx.author.id}': {}})
        await ctx.send(f'event entry {ctx.author.id} initialized')
        entry = entry[f'{ctx.author.id}']
        desc2 = [f'{i} ' for i in desc]
        entry.update({'month': int(month), 'day': int(day), 'name': name, 'on_start': ''.join(desc2), 'passed': False})
        await ctx.send(f'event entry populated with data\n'
                       f'```json\n'
                       f'{json.dumps(entry, indent=2)}\n'
                       f'```\n'
                       f'if this info is wrong then redo the command with whatever changes you need')

    @events_update.error
    async def events_update_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(help='(month, day): sends the number of days until something')
    async def daycountdown(self, ctx, month, day):
        month = int(month)
        monthstr = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'][month - 1]
        day = int(day)
        dt = days_until(month, day)
        await ctx.send(f'{monthstr} {day} is in {dt} days')

    @daycountdown.error
    async def daycountdown_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(help='(): the lagometer, often lies')
    async def ping(self, ctx):
        t = await ctx.send(f'from client.latency: {round(client.latency * 1000)} (this number will probably be inaccurate)')
        ms = (t.created_at - ctx.message.created_at).total_seconds() * 1000
        await ctx.send(f'from message.created_at: {round(ms)}. disclaimer: this command only gets my (honchokomodo) ping')

    @commands.command(help='(path, action, value): does json things')
    async def edict(self, ctx, path, action, *value):
        pathlist = path.split('>')
        a_key = data[f'{ctx.guild.id}']
        if path != 'self':
            for i in pathlist[0:-1]:
                a_key = a_key[i]
        else:
            pathlist = [f'{ctx.guild.id}']
            a_key = data

        value = ''.join([f'{i} ' for i in value])

        perm = ctx.author.guild_permissions.administrator
        try:
            if action == 'print':
                return await ctx.send(a_key[pathlist[-1]])
            if action == 'dumps':
                return await ctx.send(f'```json\n{json.dumps(a_key[pathlist[-1]], indent=2)}\n```')
            if action == 'keys':
                return await ctx.send([i for i in a_key[pathlist[-1]]])
            if action == 'type':
                return await ctx.send(type(a_key[pathlist[-1]]))
            if action == 'update' and perm:
                a_key[pathlist[-1]].update(json.loads(value))
                return await ctx.send('aight dude')
            if action == 'append' and perm:
                a_key[pathlist[-1]].append(json.loads(value))
                return await ctx.send('aight dude')
            if action == 'pop' and perm:
                if type(a_key) == dict:
                    a_key.pop(pathlist[-1])
                    return await ctx.send('aight dude')
                if type(a_key) == list:
                    a_key.pop(int(pathlist[-1]))
                    return await ctx.send('aight dude')

        except Exception as e:
            await(ctx.send(e))

    @edict.error
    async def edict_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(help='(num=10): the leaderboard')
    async def top(self, ctx, num=10):
        data2 = [i[1] for i in data[f"{ctx.guild.id}"]["users"].items()]
        users_sorted = sorted(data2, key=lambda a: a["xp"] if type(a["xp"]) == int else 0, reverse=True)
        printable = []
        for n, i in enumerate(users_sorted[:num]):
            # noinspection PyBroadException
            try:
                le = math.floor(math.log(i['xp'], 1.1))
            except Exception as _:
                le = '???'
            printable.append(f"{n:>3} -> {i['name'][:20]:^20} | Level {le:>3} | {i['xp']:>10} xp\n")
        await ctx.send(f'```cs\n{"".join(printable)}\nthanks to Vedant36 for the help!```')

    @top.error
    async def top_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(help='(): prints your level')
    async def level(self, ctx):
        xp = data[f"{ctx.guild.id}"]["users"][f'{ctx.author.id}']["xp"]
        lv = math.floor(math.log(xp, 1.1))
        dt = math.floor(1.1 ** (lv + 1) - xp)
        await ctx.send(f'you are level {lv} with {xp} xp. you need {dt} more xp (around {dt/1100000} mins/msgs) to level up')

    @commands.command(help='(path, action=print): hypixel api things. action can also be \"keys\"')
    async def dump_count(self, ctx, path, action='print'):
        global countresponse, countcooldown

        if time.time() >= countcooldown + 60:
            r = requests.get('https://api.hypixel.net/counts?key=' + keys['hypixelapikey'])
            countcooldown = time.time()
            countresponse = json.loads(r.text)

        pathlist = path.split('>')
        a_key = countresponse
        if path != 'self':
            for i in pathlist[0:-1]:
                a_key = a_key[i]
        else:
            pathlist = ['a']
            a_key = {'a': countresponse}

        response = ''

        if action == 'print':
            response = a_key[pathlist[-1]]
        if action == 'keys':
            response = [i for i in a_key[pathlist[-1]]]

        await ctx.send(f'```json\n{json.dumps(response, indent=2)}\n```')

    @dump_count.error
    async def dump_count_error(self, ctx, error):
        await ctx.send(error)


class fun_stuff(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(help='(person_a, person_b, show_hash=''): the love calculator')
    async def ship(self, ctx, person_a, person_b, show_hash=''):
        a = person_a + person_b
        hashstr = sha1(bytes(a, 'utf-8')).hexdigest()
        shash = f'\nSHA1 HASH: {hashstr}' if show_hash == 'SHOW_HASH' else ''
        percentage = round(int(hashstr, 16) / 2 ** 160 * 100, 2)
        yeah = is_love_in_the_air(percentage)
        await ctx.send(f'Their love is {percentage}%. {yeah}{shash}')

    @ship.error
    async def ship_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(help='(person): the sex calculator')
    async def sex(self, ctx, person):
        sexsuccessresponses = [
            'You have successfully fucked {}! You were very submissive and breedable',
            'Ou la la! You successfully sexed {}! You were so breedable you bore their twins!'
        ]
        sexfailureresponses = [
            'You did not fuck {}. You were too dominant and unbreedable'
        ]
        if random.randint(0, 1):
            await ctx.send(random.choice(sexsuccessresponses).format(person))
        else:
            await ctx.send(random.choice(sexfailureresponses).format(person))

    @sex.error
    async def sex_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(help='(things): just says things')
    async def say(self, ctx, things):
        print(f'{ctx.author.name} used say with arg {things}')
        await ctx.send(things.replace('@', ''))

    @say.error
    async def say_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(help='(floor, ceil): sends a random int between floor and ceil')
    async def randint(self, ctx, floor, ceil):
        await ctx.send(random.randint(int(floor), int(ceil)))

    @randint.error
    async def randint_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(help='(length=16): funne!')
    async def laugh(self, ctx, length=16):
        laughter = ''.join([random.choice('ASDFGHJKL') for _ in range(min(length, 2001))])
        await ctx.send(laughter)

    @laugh.error
    async def laugh_error(self, ctx, error):
        await ctx.send(error)


client.add_cog(useful_things(client))
client.add_cog(fun_stuff(client))
client.loop.create_task(every_minute())
client.loop.create_task(every_hour())
client.run(keys['botkey'])
