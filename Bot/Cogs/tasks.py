from discord.ext import commands, tasks
import asyncio
import orjson
import datetime
import asyncio
import uvloop

with open('mmmm_a_thicccyyy.json') as mmmm_a_thicccyyy:
    data = orjson.loads(mmmm_a_thicccyyy.read())
    
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
        
class tasksUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.every_minute.start()
        self.every_hour.start()
        
    
    
    async def cele(self):
        for i in data:
            try:
                ec = data[i]['events_channel']
                ec = self.bot.get_channel(ec)
                data2 = [ii[1] for ii in data[i]['events'].items()]
                data3 = [iii for iii in data2 if days_until(iii['month'], iii['day']) == 0 and not iii['passed']]
                printable = []
                for _, iv in enumerate(data3):
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
            
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @tasks.loop()   
    async def every_minute(self):
        global cooldown
        while not self.bot.is_closed():
            await asyncio.sleep(60)

            cooldown = {}
            tasks = tasksUtils()
            await tasks.cele()
            
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


    @tasks.loop()
    async def every_hour(self):
        while not self.bot.is_closed():
            await asyncio.sleep(3600)
            f = open('mmmm_a_thicccyyy.json', 'w')
            f.write(orjson.dumps(data, indent=2))
            f.close()
            print('saved')
            
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

            
def setup(bot):
    bot.add_cog(tasksUtils(bot))