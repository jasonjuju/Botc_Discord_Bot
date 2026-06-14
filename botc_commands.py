import discord
from discord.ext import commands

SIGNUP_EMOJI = "✅"

player_role = "Player"

class BotcCommands(commands.Cog):
    def __init__(self, bot, players):
        self.bot = bot
        self.players = players
        self.signup_message_id = None
        self.signup_role_id = None

        print(players)


    @commands.command(name='play')
    async def pla_command(self, ctx):
        await ctx.send('Playing!')


class SetupCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = set()
        self.role_messages = {}

    def get_players(self):
        return self.players

    async def _edit_role_message(self, payload, user_id: int, add: bool):
        message = self.role_messages.get(payload.message_id)
        if message is None:
            channel = self.bot.get_channel(payload.channel_id)
            if channel is not None:
                try:
                    message = await channel.fetch_message(payload.message_id)
                except Exception:
                    return
        if message is None:
            return

        lines = message.content.splitlines()
        header_index = None
        for i, line in enumerate(lines):
            if line.strip().lower().startswith('players'):
                header_index = i
                break

        if header_index is None:
            return

        players_section = lines[header_index + 1 :]
        mention = f"<@{user_id}>"
        if add:
            entry = f"- {mention}"
            if entry not in players_section:
                new_content_lines = lines[: header_index + 1] + players_section + [entry]
                content = "\n".join(new_content_lines)
            else:
                content = message.content
        else:
            def line_matches(l: str) -> bool:
                return mention in l or l.strip().endswith(f"{user_id}")

            new_players = [l for l in players_section if not line_matches(l)]
            content = "\n".join(lines[: header_index + 1] + new_players)

        if content != message.content:
            try:
                message = await message.edit(content=content)
                self.role_messages[payload.message_id] = message
            except Exception:
                return

    @commands.command(name='create')
    async def create(self, ctx):
        message = await ctx.send('Creating game!\nPlayers:')
        await message.add_reaction(SIGNUP_EMOJI)
        self.role_messages[message.id] = message

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        if payload.emoji.name != SIGNUP_EMOJI and str(payload.emoji) != SIGNUP_EMOJI:
            return

        if payload.message_id not in self.role_messages:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return

        member = guild.get_member(payload.user_id)
        if member is None:
            try:
                member = await guild.fetch_member(payload.user_id)
            except Exception:
                return

        role = discord.utils.get(guild.roles, name=player_role)
        if role is None:
            return

        try:
            await member.add_roles(role, reason='Joined game via reaction')
        except Exception:
            pass
        
        self.players.add(payload.user_id)
        await self._edit_role_message(payload, payload.user_id, True)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        if payload.emoji.name != SIGNUP_EMOJI and str(payload.emoji) != SIGNUP_EMOJI:
            return

        if payload.message_id not in self.role_messages:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return

        member = guild.get_member(payload.user_id)
        if member is None:
            try:
                member = await guild.fetch_member(payload.user_id)
            except Exception:
                return

        role = discord.utils.get(guild.roles, name=player_role)
        if role is None:
            return

        try:
            if role in member.roles:
                await member.remove_roles(role, reason='Left game via reaction removal')
        except Exception:
            pass

        self.players.discard(payload.user_id)
        await self._edit_role_message(payload, payload.user_id, False)


    #run a test game with 8 players
    @commands.command(name='runtest')
    async def runtest(self, ctx):
        self.players = [f"Player {i}" for i in range(1, 9)]
        content = "Creating game!\nPlayers:\n" + "\n".join(f"- {name}" for name in self.players)
        message = await ctx.send(content)
        self.role_messages[message.id] = message

    @commands.command(name='loadgame')
    async def loadgame(self, ctx):
        players = self.get_players()
        if not players:
            await ctx.send("No players have joined the game yet.")
            return
        

        await self.bot.add_cog(BotcCommands(self.bot, players))

        await self.bot.remove_cog('SetupCommands')


#day commands

#night commands

#voting commands