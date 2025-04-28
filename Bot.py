from discord.ext import commands
from utils import config, logging_setup
import asyncio

bot = commands.Bot(command_prefix="!", intents=config.intents)

async def load_extensions():
    extensions = [
        "cogs.siegeai",
        "cogs.scoreboard",
        "cogs.panic",
        "cogs.massnick",
        "cogs.roast",
        "cogs.timeout"
    ]
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            logging_setup.log.info(f"Loaded extension: {ext}")
        except Exception as e:
            logging_setup.log.error(f"Failed to load {ext}: {e}")

@bot.event
async def on_ready():
    logging_setup.log.info(f"{bot.user} is online!")
    await bot.tree.sync()
    logging_setup.log.info(f"Slash commands synced.")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(config.DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
