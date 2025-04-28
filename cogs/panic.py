import discord
from discord.ext import commands
from discord import app_commands
from utils import file_utils, config, logging_setup as log

class PanicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_user_id, self.panic_channel_id = file_utils.load_panic_config()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.id == self.target_user_id and after.channel and (before.channel != after.channel):
            source_channel = after.channel
            panic_channel = member.guild.get_channel(self.panic_channel_id)
            if panic_channel is None:
                log.log.warning("Panic channel not found!")
                return

            for m in source_channel.members:
                if m.id != self.target_user_id and not m.bot:
                    try:
                        await m.move_to(panic_channel)
                        log.log.info("Panic! Moved %s to %s", m.display_name, panic_channel)
                    except Exception as e:
                        log.log.warning("Couldn't move %s: %s", m.display_name, e)

    @app_commands.command(name="panicset", description="Set the target user and panic channel for panic mode.")
    @app_commands.describe(
        user="The user to run from",
        channel="The voice channel to move everyone to"
    )
    async def panicset(self, interaction: discord.Interaction, user: discord.Member, channel: discord.VoiceChannel):
        self.target_user_id = user.id
        self.panic_channel_id = channel.id
        file_utils.save_panic_config(self.target_user_id, self.panic_channel_id)
        log.log.info("/panicset used by %s: TargetUser=%s, PanicChannel=%s", interaction.user, user, channel)
        await interaction.response.send_message(
            f"🔄 Panic mode updated!\nTarget user: {user.mention}\nPanic channel: {channel.mention}",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(PanicCog(bot))