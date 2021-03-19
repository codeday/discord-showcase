import logging
import os
import sys
import traceback
import atexit

import discord

from discord.ext import commands
from raygun4py import raygunprovider


def handle_exception(exc_type, exc_value, exc_traceback):
    cl = raygunprovider.RaygunSender(os.getenv("RAYGUN_TOKEN"))
    cl.send_exception(exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception

BOT_TOKEN = os.getenv('BOT_TOKEN')
intents = discord.Intents(messages=True, guilds=True, members=True, reactions=True)
bot = commands.Bot(command_prefix='s~', intents=intents)

initial_cogs = [
    'cogs.listen',
    'cogs.checkin',
    'cogs.pods',
    'cogs.reactions'
]

for cog in initial_cogs:
    try:
        bot.load_extension(cog)
        logging.info(f'Successfully loaded extension {cog}')
    except Exception as e:
        logging.exception(
            f'Failed to load extension {cog}.', exc_info=traceback.format_exc())


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    atexit.register(exit_handler)

def exit_handler():
    print('The application is ending!')
    session.commit()
    session.close()


bot.run(BOT_TOKEN, bot=True, reconnect=True)
