import asyncio
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

import botc_commands
from botc_commands import SetupCommands
from botc_session import game_session


        



load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def main():
    session = game_session()

    await bot.add_cog(SetupCommands(bot, session))
    await bot.start(token)

@bot.event
async def on_ready():
    print('Bot is ready.')


@bot.command()
async def startgame(ctx):
    await ctx.send('Hello!')


@bot.command()
async def stop(ctx):
    for cog_name in list(bot.cogs):
        await bot.remove_cog(cog_name)

    await ctx.send('Goodbye!')

if __name__ == "__main__":
    asyncio.run(main())