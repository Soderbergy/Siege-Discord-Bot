import discord
from discord.ext import commands
from discord import app_commands
from utils import file_utils, config, logging_setup as log

class ScoreboardView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.attack_count, self.defend_count = file_utils.load_scores()

    @discord.ui.button(label="Attack +1", style=discord.ButtonStyle.red, custom_id="attack_button")
    async def attack(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.attack_count += 1
        file_utils.save_scores(self.attack_count, self.defend_count)
        await interaction.response.edit_message(embed=self.make_embed(), view=self)

    @discord.ui.button(label="Defend +1", style=discord.ButtonStyle.blurple, custom_id="defend_button")
    async def defend(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.defend_count += 1
        file_utils.save_scores(self.attack_count, self.defend_count)
        await interaction.response.edit_message(embed=self.make_embed(), view=self)

    def make_embed(self):
        embed = discord.Embed(
            title="Nelms Attack/Defend First Tracker",
            description="Keep track of who’s attacking and defending first!",
            color=discord.Color.gold()
        )
        embed.add_field(name="Attacks First", value=str(self.attack_count), inline=True)
        embed.add_field(name="Defends First", value=str(self.defend_count), inline=True)
        return embed

class ScoreboardCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.setup_scoreboard()

    async def setup_scoreboard(self):
        channel = self.bot.get_channel(config.SCOREBOARD_CHANNEL_ID)
        if channel is None:
            log.log.error("Couldn't find the scoreboard channel! Check the ID.")
            return

        view = ScoreboardView()
        embed = view.make_embed()
        msg_id = file_utils.load_scoreboard_msg_id()
        scoreboard_msg = None

        if msg_id:
            try:
                scoreboard_msg = await channel.fetch_message(msg_id)
                await scoreboard_msg.edit(embed=embed, view=view)
                log.log.info("Scoreboard message updated.")
            except Exception as e:
                log.log.warning("Couldn't fetch or edit scoreboard message: %s", e)

        if scoreboard_msg is None:
            scoreboard_msg = await channel.send(embed=embed, view=view)
            file_utils.save_scoreboard_msg_id(scoreboard_msg.id)
            log.log.info("Posted a new scoreboard message.")

async def setup(bot):
    await bot.add_cog(ScoreboardCog(bot))