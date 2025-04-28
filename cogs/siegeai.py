import discord
from discord.ext import commands
from discord import app_commands
import openai
from utils import config, logging_setup as log

class SiegeAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
        self.system_prompt = (
            "You are a Discord bot that only responds with answers, jokes, roasts, strategies, or memes "
            "about Rainbow Six Siege. Never break character. If someone asks about anything else, steer it "
            "back to Siege, make a Siege meme, or refuse in a Siege-themed way."
        )

    @app_commands.command(name="siegeai", description="Ask SiegeBot anything (only Siege-related answers allowed!)")
    @app_commands.describe(prompt="Ask anything about Siege operators, memes, strats, or loadouts")
    async def siegeai(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=350,
                temperature=0.9,
            )
            reply = response.choices[0].message.content
            formatted = (
                f"**You asked:**\n> {prompt}\n\n"
                f"**SiegeBot says:**\n{reply}"
            )
            await interaction.followup.send(formatted[:2000])
        except Exception as e:
            await interaction.followup.send(f"Error fetching Siege wisdom: {e}")

async def setup(bot):
    await bot.add_cog(SiegeAI(bot))
