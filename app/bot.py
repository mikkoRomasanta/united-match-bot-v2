import os
import scraper
import bot_commands
import notify as nt
import asyncio
from discord.ext import commands, tasks
from dotenv import load_dotenv


load_dotenv()

#BOT SETTINGS
bot = commands.Bot(command_prefix='!', 
                   case_insensitive=True)

#COMMANDS
@bot.command()
async def GG(ctx):
    await ctx.send('MU!')
    
@bot.command()
async def cmd(ctx):
    cmds = bot_commands.send_commands()
    
    await ctx.send(cmds)

@bot.command()
async def table(ctx,arg=''):
    table = scraper.send_table(arg)

    await ctx.send(table)

@bot.command()
async def sched(ctx):
    fixtures = scraper.send_fixtures()

    await ctx.send(fixtures)
    
@tasks.loop(hours=1)
async def notify_next_match():
    #set targets
    channel_id = int(os.getenv('TARGET_CHANNEL_ID'))
    role_id = int(os.getenv('TARGET_ROLE_ID'))
    channel = bot.get_channel(channel_id)
    
    data = nt.check_date_difference()
    delay = data["delay"]
    data["role"] = role_id
    
    if delay != 0:
        notify = nt.send_notification(data)
        await channel.send(notify)
        #sleep task if notification is sent.
        await asyncio.sleep(delay)
    
@notify_next_match.before_loop
async def before():
    await bot.wait_until_ready()

#RUN BOT
notify_next_match.start()
bot.run(os.getenv('DISCORD_BOT_TOKEN'))