import discord
from discord.ext import commands
from discord import app_commands
import random
from utils import constants, logging_setup as log

class RoastCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roast", description="Send a friendly roast to someone!")
    @app_commands.describe(user="The target of your roast")
    async def roast(self, interaction: discord.Interaction, user: discord.Member):
        roast = random.choice(constants.ROASTS)
        log.log.info("/roast used by %s on %s", interaction.user, user)
        await interaction.response.send_message(f"{user.mention} {roast}")

async def setup(bot):
    await bot.add_cog(RoastCog(bot))