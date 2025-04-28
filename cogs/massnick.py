import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio
from utils import constants, logging_setup as log

class MassNickCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="massnick", description="Temporarily change everyone's nick in a VC to something dumb!")
    @app_commands.describe(channel="The voice channel to meme-ify")
    async def massnick(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        members = [m for m in channel.members if not m.bot]
        if not members:
            await interaction.response.send_message("No real users in that channel!")
            return

        old_nicks = {}
        new_nicks = random.sample(constants.MEME_NICKS * ((len(members) // len(constants.MEME_NICKS)) + 1), len(members))
        await interaction.response.send_message(f"Changing nicknames for 60 seconds...")

        log.log.info("/massnick used by %s in %s on %d users", interaction.user, channel, len(members))
        for member, newnick in zip(members, new_nicks):
            try:
                old_nicks[member.id] = member.nick
                await member.edit(nick=newnick)
                log.log.info("Changed %s's nickname to %s", member.display_name, newnick)
            except Exception as e:
                log.log.warning("Couldn't change %s's nickname: %s", member.display_name, e)

        await asyncio.sleep(60)

        for member in members:
            try:
                await member.edit(nick=old_nicks.get(member.id))
                log.log.info("Restored %s's nickname", member.display_name)
            except Exception:
                pass

async def setup(bot):
    await bot.add_cog(MassNickCog(bot))