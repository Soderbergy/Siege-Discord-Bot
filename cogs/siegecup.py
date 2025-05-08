import discord
from discord.ext import commands
from discord import app_commands

MAX_SIGNUPS = 5
SIGNUP_EMOJI = "✅"

class SiegeCupSignup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.attendees = []
        self.signup_message_id = None

    @app_commands.command(name="siegecup", description="Post a Siege Cup signup embed.")
    async def siegecup(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🏆 Siege Cup Sign-Ups Open!",
            description="Click the ✅ reaction below to join the roster.\nMax players: 5",
            color=discord.Color.gold()
        )
        embed.add_field(name="Confirmed Players", value="*(None yet)*", inline=False)
        message = await interaction.channel.send(embed=embed)
        self.signup_message_id = message.id
        await message.add_reaction(SIGNUP_EMOJI)
        await interaction.response.send_message("Siege Cup signup posted!", ephemeral=True)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id != self.signup_message_id or str(payload.emoji) != SIGNUP_EMOJI:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if member.bot:
            return  # Ignore bots

        display_name = member.nick or member.name

        if display_name in self.attendees:
            return  # Already signed up

        if len(self.attendees) >= MAX_SIGNUPS:
            try:
                channel = guild.get_channel(payload.channel_id)
                msg = await channel.fetch_message(payload.message_id)
                await msg.remove_reaction(payload.emoji, member)
            except Exception:
                pass
            return

        self.attendees.append(display_name)

        # Update the embed message
        channel = guild.get_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        embed = msg.embeds[0]
        embed.set_field_at(0, name="Confirmed Players", value="\n".join(self.attendees), inline=False)
        await msg.edit(embed=embed)

async def setup(bot):
    await bot.add_cog(SiegeCupSignup(bot))