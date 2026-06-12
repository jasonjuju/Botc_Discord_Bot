import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

import botc_commands

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True


bot = commands.Bot(command_prefix='!', intents=intents)

# track messages that should grant the Player role on reaction
# map message id -> message object so we can edit the message when players join
role_messages = {}


async def _edit_role_message(payload, user_id: int, add: bool):
    """Fetch the original signup message (from cache or channel), then add or remove the member line and edit it.

    This function uses a mention `<@user_id>` to ensure removals match even if display names change.
    """
    message = role_messages.get(payload.message_id)
    if message is None:
        channel = bot.get_channel(payload.channel_id)
        if channel is not None:
            try:
                message = await channel.fetch_message(payload.message_id)
            except Exception:
                return
    if message is None:
        return

    lines = message.content.splitlines()

    # find index of the Players header (first line that startswith Players)
    header_index = None
    for i, line in enumerate(lines):
        if line.strip().lower().startswith('players'):
            header_index = i
            break

    if header_index is None:
        # nothing to do if header missing
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

        # remove any lines that reference this user id (mention or plain name)
        def line_matches(l: str) -> bool:
            return mention in l or l.strip().endswith(f"{user_id}")

        new_players = [l for l in players_section if not line_matches(l)]
        content = "\n".join(lines[: header_index + 1] + new_players)

    if content != message.content:
        try:
            message = await message.edit(content=content)
            role_messages[payload.message_id] = message
        except Exception:
            return

@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.command()
async def create(ctx):
    message = await ctx.send('Creating game!\nPlayers:')
    await message.add_reaction('✅')
    # remember this message so reactions to it can grant the role
    role_messages[message.id] = message


@bot.event
async def on_raw_reaction_add(payload):
    # ignore reactions from the bot itself
    if payload.user_id == bot.user.id:
        return

    if payload.message_id not in role_messages:
        return

    # only handle the check mark reaction
    if str(payload.emoji) != '✅':
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    member = guild.get_member(payload.user_id)
    if member is None:
        try:
            member = await guild.fetch_member(payload.user_id)
        except Exception:
            return

    role = discord.utils.get(guild.roles, name='Player')
    if role is None:
        return

    try:
        await member.add_roles(role, reason='Joined game via reaction')
    except Exception:
        pass
    else:
        # update the original message to include this player's username
        try:
            await _edit_role_message(payload, payload.user_id, True)
        except Exception:
            pass


@bot.event
async def on_raw_reaction_remove(payload):
    # ignore reactions from the bot itself
    if payload.user_id == bot.user.id:
        return

    if payload.message_id not in role_messages:
        return

    # only handle the check mark reaction
    if str(payload.emoji) != '✅':
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    member = guild.get_member(payload.user_id)
    if member is None:
        try:
            member = await guild.fetch_member(payload.user_id)
        except Exception:
            return

    role = discord.utils.get(guild.roles, name='Player')
    if role is None:
        return

    try:
        if role in member.roles:
            await member.remove_roles(role, reason='Left game via reaction removal')
    except Exception:
        pass

    try:
        await _edit_role_message(payload, payload.user_id, False)
    except Exception:
        print("Failed to update role message on reaction removal")


@bot.command()
async def startgame(ctx):
    await ctx.send('Hello!')
    await bot.add_cog(botc_commands.BotcCommands(bot))

@bot.command()
async def stop(ctx):
    await ctx.send('Goodbye!') 
    await bot.remove_cog('BotcCommands')

bot.run(token, log_handler=handler, log_level=logging.DEBUG)