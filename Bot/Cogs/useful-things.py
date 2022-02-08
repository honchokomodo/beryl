import requests
from discord.ext import commands
import orjson
import discord
import os
import datetime
import time
import math
import re
import asyncio
import uvloop

with open('mmmm_a_thicccyyy.json') as mmmm_a_thicccyyy:
    data = orjson.loads(mmmm_a_thicccyyy.read())
with open('penis_pleasure_18.json') as sensitive_things:
    keys = orjson.loads(sensitive_things.read())
    
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
        
cooldown = {}
countcooldown = 0
countresponse = {}

class usefulThings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(help='(): save userdata')
    async def write(self, ctx):
        if ctx.author.id != 301774808167743489: # THIS IS HORRIBLE CHANGE THIS ASAP
            await ctx.send('you are not the bot host')
            return
        f = open('mmmm_a_thicccyyy.json', 'w')
        f.write(orjson.dumps(data, indent=2))
        f.close()
        print('saved')
        await ctx.send('saved')
        
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    
    @write.error
    async def write_error(self, ctx, error):
        await ctx.send(error)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


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
        
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    
    @ffmpegcve.error
    async def ffmpegcve_error(self, ctx, error):
        await ctx.send(error)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

        
    @commands.command(help='(): downloads tiktok videos and sends it')
    async def youtubedltte(self, ctx, url):
        ttfilter = re.compile(r'^https:\/\/vm.tiktok.com\/\w+\/$')
        if ttfilter.match(url):
            await ctx.send('downloading...')
            os.system(f'youtube-dl {url} -o youtubedl.mp4')
            file_size = os.path.getsize('youtubedl.mp4')
            await ctx.send(f'file size: {file_size} max 8000000')
            if file_size > 8000000:
                await ctx.send('didnt even try sending video. file too big')
            else:
                await ctx.send('sending...')
                await ctx.send(file=discord.File(r'youtubedl.mp4'))
            os.system('rm youtubedl.mp4')
        else:
            await ctx.send(r'link does not match regex `^https:\/\/vm.tiktok.com\/\w+\/$`. video was not downloaded')
            
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    
    @youtubedltte.error
    async def youtubedltte_error(self, ctx, error):
        await ctx.send(error)
        
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


    @commands.command(help='(): lists upcoming events')
    async def events(self, ctx):
        data2 = [i[1] for i in data[f'{ctx.guild.id}']['events'].items()]
        data3 = sorted(data2, key=lambda a: days_until(a['month'], a['day']))
        printable = []
        for n, i in enumerate(data3):
            printable.append(
                f'{n:>3} -> in {days_until(i["month"], i["day"]):>4} days on {i["month"]:>2}/{i["day"]:<2}: {i["name"]}\n')
        await ctx.send(f'```cs\n{"".join(printable)}\n```')
        
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


    @events.error
    async def events_error(self, ctx, error):
        await ctx.send(error)
        
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


    @commands.command(help='(): initializes the event list for you')
    async def events_setup(self, ctx):
        try:
            print(data[f'{ctx.guild.id}']['events'])
            await ctx.send(f'there is already an events dict. nothing happened')
        except KeyError:
            data[f'{ctx.guild.id}'].update({'events': {}})
            await ctx.send(f'events entry added to dict. access with:\n'
                           f'```beryl edict events print 0```')
            
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


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
                       f'{orjson.dumps(entry, indent=2)}\n'
                       f'```\n'
                       f'if this info is wrong then redo the command with whatever changes you need')

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


    @events_update.error
    async def events_update_error(self, ctx, error):
        await ctx.send(error)
        
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


    @commands.command(help='(month, day): sends the number of days until something')
    async def daycountdown(self, ctx, month, day):
        month = int(month)
        monthstr = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'][month - 1]
        day = int(day)
        dt = days_until(month, day)
        await ctx.send(f'{monthstr} {day} is in {dt} days')
        
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


    @daycountdown.error
    async def daycountdown_error(self, ctx, error):
        await ctx.send(error)
        
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


    @commands.command(help='(): the lagometer, often lies')
    async def ping(self, ctx):
        t = await ctx.send(f'from client.latency: {round(self.bot.latency * 1000)} (this number will probably be inaccurate)')
        ms = (t.created_at - ctx.message.created_at).total_seconds() * 1000
        await ctx.send(f'from message.created_at: {round(ms)}. disclaimer: this command only gets my (honchokomodo) ping')
        
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


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
                return await ctx.send(f'```json\n{orjson.dumps(a_key[pathlist[-1]], indent=2)}\n```')
            if action == 'keys':
                return await ctx.send([i for i in a_key[pathlist[-1]]])
            if action == 'type':
                return await ctx.send(type(a_key[pathlist[-1]]))
            if action == 'update' and perm:
                a_key[pathlist[-1]].update(orjson.loads(value))
                return await ctx.send('aight dude')
            if action == 'append' and perm:
                a_key[pathlist[-1]].append(orjson.loads(value))
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
            
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


    @edict.error
    async def edict_error(self, ctx, error):
        await ctx.send(error)
        
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


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

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @top.error
    async def top_error(self, ctx, error):
        await ctx.send(error)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @commands.command(help='(): prints your level')
    async def level(self, ctx):
        xp = data[f"{ctx.guild.id}"]["users"][f'{ctx.author.id}']["xp"]
        lv = math.floor(math.log(xp, 1.1))
        dt = math.floor(1.1 ** (lv + 1) - xp)
        await ctx.send(f'you are level {lv} with {xp} xp. you need {dt} more xp (around {dt/1100000} mins/msgs) to level up')
        
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


    @commands.command(help='(path, action=print): hypixel api things. action can also be \"keys\"')
    async def dump_count(self, ctx, path, action='print'):
        global countresponse, countcooldown

        if time.time() >= countcooldown + 60:
            # please use aiohttp for this instead
            r = requests.get('https://api.hypixel.net/counts?key=' + keys['hypixelapikey'])
            countcooldown = time.time()
            countresponse = orjson.loads(r.text)

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

        await ctx.send(f'```json\n{orjson.dumps(response, indent=2)}\n```')
        
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


    @dump_count.error
    async def dump_count_error(self, ctx, error):
        await ctx.send(error)
        
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

        
def setup(bot):
    bot.add_cog(usefulThings(bot))