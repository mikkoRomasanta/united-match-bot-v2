import os
import scraper
import bot_commands
from discord.ext import commands
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


#RUN BOT
bot.run(os.getenv('DISCORD_BOT_TOKEN'))