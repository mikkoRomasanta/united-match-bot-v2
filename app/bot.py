import os
import scraper
import bot_commands
import notify as nt
from discord.ext import commands, tasks
from dotenv import load_dotenv
import logging
import logging.config
import datetime as dt


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
    
@tasks.loop(minutes=30)
async def notify_next_match():
    global notify_delay
    
    logging.info(f'[{dt.datetime.now()}] Running task. '
                 f'notify_delay: {notify_delay}')
    
    if notify_delay > 0:
        notify_delay -= .2 #skip 6x after sending notification
    elif notify_delay < 0:
        notify_delay = 0
    else:
        #set targets
        channel_id = int(os.getenv('TARGET_CHANNEL_ID'))
        role_id = int(os.getenv('TARGET_ROLE_ID'))
        channel = bot.get_channel(channel_id)
    
        data = nt.check_date_difference()
            
        logging.info(f'Receiving data. \n{data} \n')
        #Run notification
        if data['notify'] != False:
            notify_delay = 1
            data["role"] = role_id
            notify = nt.send_notification(data)
            logging.info(f'Sending notification. \n'
                         f'data: {notify}'
                         )
            
            await channel.send(notify)
    
@notify_next_match.before_loop
async def before():
    #set global
    global notify_delay
    notify_delay = 0
    
    logging.config.fileConfig("../logging.conf", disable_existing_loggers=False,
                              defaults={'logfilename': '../bot.log'})
    
    await bot.wait_until_ready()

#RUN BOT
notify_next_match.start()
bot.run(os.getenv('DISCORD_BOT_TOKEN'))