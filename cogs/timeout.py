import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from utils import config, logging_setup as log

class TimeoutCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="timeout", description="Send someone to timeout VC for 30 seconds!")
    @app_commands.describe(user="User to time out")
    async def timeout(self, interaction: discord.Interaction, user: discord.Member):
        timeout_vc = interaction.guild.get_channel(config.TIMEOUT_CHANNEL_ID)
        if not timeout_vc or not isinstance(timeout_vc, discord.VoiceChannel):
            await interaction.response.send_message("Timeout channel not found!")
            return

        if not user.voice or not user.voice.channel:
            await interaction.response.send_message(f"{user.display_name} is not in a voice channel!")
            return

        origin_channel = user.voice.channel
        try:
            await user.move_to(timeout_vc)
            await interaction.response.send_message(f"{user.mention} has been sent to the timeout corner! 🕒 (30s)")
            log.log.info("%s sent %s to timeout VC.", interaction.user, user.display_name)
            await asyncio.sleep(30)
            await user.move_to(origin_channel)
            log.log.info("%s returned from timeout VC.", user.display_name)
        except Exception as e:
            log.log.error("Timeout error: %s", e)
            await interaction.followup.send(f"Could not move {user.display_name} back. (Maybe they left or permissions issue?)")

async def setup(bot):
    await bot.add_cog(TimeoutCog(bot))
