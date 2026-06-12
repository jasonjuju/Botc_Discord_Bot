import discord
from discord.ext import commands

SIGNUP_EMOJI = "✅"

player_role = "Player"

class BotcCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = set()
        self.signup_message_id = None
        self.signup_role_id = None

    


    @commands.command(name='play')
    async def pla_command(self, ctx):
        await ctx.send('Playing!')


    



#day commands

#night commands

#voting commands