import asyncio
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

import botc_commands
from botc_commands import SetupCommands

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def main():
    await bot.add_cog(SetupCommands(bot))
    await bot.start(token) #, log_handler=handler, log_level=logging.DEBUG


@bot.event
async def on_ready():
    print('Bot is ready.')


@bot.command()
async def startgame(ctx):
    await ctx.send('Hello!')


@bot.command()
async def stop(ctx):
    await ctx.send('Goodbye!')
    await bot.remove_cog('SetupCommands')

if __name__ == "__main__":
    asyncio.run(main())