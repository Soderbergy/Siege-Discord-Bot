import os
from dotenv import load_dotenv
import discord

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Discord Intents setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Data file paths
DATA_FOLDER = "data"
SCORES_FILE = os.path.join(DATA_FOLDER, "scores.json")
SCOREBOARD_MSG_FILE = os.path.join(DATA_FOLDER, "scoreboard_msg.json")
PANIC_CONFIG_FILE = os.path.join(DATA_FOLDER, "panic_config.json")

# Channel IDs
TIMEOUT_CHANNEL_ID = 1365471631312683008
SCOREBOARD_CHANNEL_ID = 1365097159149490186
