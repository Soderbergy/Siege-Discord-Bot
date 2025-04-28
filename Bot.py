import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord import app_commands
import json
import os
import random
import asyncio
import logging
import colorlog
import openai
from openai import OpenAI

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ------------- LOGGING SETUP -------------
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'bold_red',
    }
))

log = colorlog.getLogger('siege-bot')
log.addHandler(handler)
log.setLevel(logging.INFO)


# ------------- DISCORD INTENTS & BOT -------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ------------- FILE PATHS & IDs -------------
SCORES_FILE = "scores.json"
SCOREBOARD_MSG_FILE = "scoreboard_msg.json"
PANIC_CONFIG_FILE = "panic_config.json"
TIMEOUT_CHANNEL_ID = 1365471631312683008  # <--- Set your timeout VC ID here!
SCOREBOARD_CHANNEL_ID = 1365097159149490186  # <--- Scoreboard channel ID

# ------------- MEME NICKNAMES -------------
MEME_NICKS = [
    "Toilet Duck", "Lord Chonka", "CrouchSpammer9000", "ProneBone", "PingZero",
    "1Tap Wonder", "NPC Energy", "Breach Goblin", "Team Flash", "Friendly Fire",
    "Spawnpeek Pro", "Ace Ace Baby", "Campfire Camper", "Tactical T-Rex",
    "DroneZone", "Yeet Supreme", "Flashbang Fiend", "Mr. Potato Aim", "Jackal Snack","Wallbang Walter",
    "Peeker’s Disadvantage", "NoScope Nelly", "Stunlocked", "Cav Main Pain", "Ranked Reject", "Reinforce Andy", "Breach Breather",
    "Flashbanged Frank", "Plant Denier", "Pixel Peek Pete", "Sound Cue Sally", "Spawn Peek Freak", "Ping Diff", "Clutch Potato",
    "Teamkill Timmy", "One Tap Flap", "Map Knowledge? Nah", "Copper Vibes", "Thermite Enthusiast", "Drone Zone Tony", "Mic Static",
    "WubWub Warden", "Tachanka’s Child", "Default Cam Stan", "Head Glitch Gary", "Shaky Aim", "Mousepad Magician", "Iron Sight Icon",
    "Drone Destroyer", "Mouse DPI Overlord", "Mute Button Abuser", "Claymore Claire", "IQless", "Misthrown Maestro", "Bomb Site Tourist",
    "Oven Mitts (for aim)", "No Callouts", "Gadget Recycler", "Pick Diff Dan", "Mag Dump Danny", "Last Alive Larry", "Dead Weight Donny",
    "Random Queue Hero","Lobby Legend", "Meme Dream", "Friendly Fire Freddy", "Free Elo Felicia", "Stuck on Drone", "TK Specialist",
    "Mute All Mark", "Ash Rush Ashley"
]

# ------------- OPERATOR LISTS -------------
ATTACKERS = [
    "Sledge", "Thatcher", "Ash", "Thermite", "Montagne", "Twitch", "Glaz",
    "Fuze", "Blitz", "IQ", "Buck", "Blackbeard", "Capitão", "Hibana",
    "Jackal", "Ying", "Zofia", "Dokkaebi", "Lion", "Finka", "Maverick",
    "Nomad", "Gridlock", "Nøkk", "Amaru", "Kali", "Iana", "Ace", "Zero",
    "Flores", "Osa", "Sens", "Grim", "Brava", "Ram"
    ]
DEFENDERS = [
    "Smoke", "Mute", "Castle", "Pulse", "Doc", "Rook", "Kapkan", "Tachanka",
    "Jäger", "Bandit", "Frost", "Valkyrie", "Caveira", "Echo", "Mira",
    "Lesion", "Ela", "Vigil", "Maestro", "Alibi", "Clash", "Kaid", "Mozzie",
    "Warden", "Goyo", "Wamai", "Oryx", "Melusi", "Aruni", "Thunderbird",
    "Thorn", "Azami", "Solis", "Fenrir", "Tubarao"
]
ALL_OPS = ATTACKERS + DEFENDERS

# ------------- ROASTS -------------
ROASTS = [
     "You're the reason we need drone economy.",
    "I'd tell you to aim higher, but you might hit a teammate.",
    "You're like a stun grenade: everyone's annoyed when you show up.",
    "If potato aim was a competition, you'd still miss.",
    "You get more kills with your mic than your gun.",
    "I've seen drones with better movement.",
    "You're proof that spawnpeeking isn't for everyone.",
    "Are you trying to plant or just sightseeing?",
    "Your aim is so shaky, I thought you were on dial-up.",
    "You're a walking entry frag. For the other team.",
    "You must be running dial-up. Your aim’s always lagging behind.",
    "Your favorite operator must be the bench.",
    "If you were a gadget, you’d be a default cam—out in the open and ignored.",
    "You aim like you’re playing whack-a-mole at the arcade.",
    "Your callouts are like your aim—completely off.",
    "If confusion was a strat, you’d be the team captain.",
    "You could get spawnpeeked in T-Hunt.",
    "I’ve seen claymores with better placement.",
    "Your drone work is top tier—if only you played the rest of the game.",
    "Your best play was uninstalling the game.",
    "You reload after every shot, don’t you?",
    "Your utility usage is as empty as your scoreboard.",
    "The only thing you clear is your own team.",
    "You’re the human embodiment of a misthrown smoke.",
    "You’d lose a gunfight to a security camera.",
    "You’re not bottom fragging—you’re anchoring the team’s morale.",
    "When you queue up, the enemy team wins the lottery.",
    "At least your deaths give us time to check TikTok.",
    "You hear more footsteps in your head than in the game.",
    "Even Tachanka has higher stats.",
    "Your FOV is set to potato.",
    "I’d roast your stats, but it’d be bullying.",
    "You have ‘insert coin to continue’ energy.",
    "If you get banned for toxicity, it’ll be for your gameplay.",
    "Your best strat is accidental.",
    "Your bullets do less damage than harsh language.",
    "If you’re clutching, the enemy’s AFK.",
    "You miss so much, you’re banned from dodgeball.",
    "Callouts: 0, Deaths: 7, Vibes: Immaculate.",
    "You’re more lost than a drone in a Mozzie trap."
]

# ========== SCOREBOARD UTILS ==========
def load_scores():
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "r") as f:
                data = json.load(f)
                log.info("Loaded scores from file.")
                return data.get("attack", 0), data.get("defend", 0)
        except (json.JSONDecodeError, ValueError):
            log.warning("Score file corrupted, resetting scores.")
            return 0, 0
    return 0, 0

def save_scores(attack, defend):
    with open(SCORES_FILE, "w") as f:
        json.dump({"attack": attack, "defend": defend}, f)
    log.info("Saved scores: Attack=%s, Defend=%s", attack, defend)

def save_scoreboard_msg_id(msg_id):
    with open(SCOREBOARD_MSG_FILE, "w") as f:
        json.dump({"msg_id": msg_id}, f)
    log.info("Saved scoreboard message ID: %s", msg_id)

def load_scoreboard_msg_id():
    if os.path.exists(SCOREBOARD_MSG_FILE):
        try:
            with open(SCOREBOARD_MSG_FILE, "r") as f:
                data = json.load(f)
                return data.get("msg_id", None)
        except (json.JSONDecodeError, ValueError):
            return None
    return None

# ========== PANIC CONFIG UTILS ==========
def load_panic_config():
    if os.path.exists(PANIC_CONFIG_FILE):
        try:
            with open(PANIC_CONFIG_FILE, "r") as f:
                data = json.load(f)
                log.info("Loaded panic config.")
                return data.get("target_user_id"), data.get("panic_channel_id")
        except (json.JSONDecodeError, ValueError):
            log.warning("Panic config corrupted, resetting.")
            return None, None
    return None, None

def save_panic_config(target_user_id, panic_channel_id):
    with open(PANIC_CONFIG_FILE, "w") as f:
        json.dump({
            "target_user_id": target_user_id,
            "panic_channel_id": panic_channel_id
        }, f)
    log.info("Saved panic config: TargetUser=%s, PanicChannel=%s", target_user_id, panic_channel_id)

# ========== DISCORD VIEWS ==========
class ScoreboardView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.attack_count, self.defend_count = load_scores()

    @discord.ui.button(label="Attack +1", style=discord.ButtonStyle.red, custom_id="attack_button")
    async def attack(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.attack_count += 1
        save_scores(self.attack_count, self.defend_count)
        await interaction.response.edit_message(embed=self.make_embed(), view=self)

    @discord.ui.button(label="Defend +1", style=discord.ButtonStyle.blurple, custom_id="defend_button")
    async def defend(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.defend_count += 1
        save_scores(self.attack_count, self.defend_count)
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

# ========== SLASH COMMANDS ==========
@bot.tree.command(name="operator", description="Get a random Siege operator for your team!")
@app_commands.describe(team="Attack or Defend")
@app_commands.choices(team=[
    app_commands.Choice(name="Attack", value="attack"),
    app_commands.Choice(name="Defend", value="defend"),
])
async def operator(interaction: discord.Interaction, team: app_commands.Choice[str]):
    op = random.choice(ATTACKERS if team.value == "attack" else DEFENDERS)
    log.info("/operator used by %s - %s got %s", interaction.user, team.value, op)
    await interaction.response.send_message(
        f"{'🔺' if team.value == 'attack' else '🛡️'} **{team.value.title()}:** `{op}`"
    )

@bot.tree.command(name="panicset", description="Set the target user and panic channel for panic mode.")
@discord.app_commands.describe(
    user="The user to run from",
    channel="The voice channel to move everyone to"
)
async def panicset(interaction: discord.Interaction, user: discord.Member, channel: discord.VoiceChannel):
    global TARGET_USER_ID, PANIC_CHANNEL_ID
    TARGET_USER_ID = user.id
    PANIC_CHANNEL_ID = channel.id
    save_panic_config(TARGET_USER_ID, PANIC_CHANNEL_ID)
    log.info("/panicset used by %s: TargetUser=%s, PanicChannel=%s", interaction.user, user, channel)
    await interaction.response.send_message(
        f"🔄 Panic mode updated!\nTarget user: {user.mention}\nPanic channel: {channel.mention}",
        ephemeral=True
    )

@bot.tree.command(name="massnick", description="Temporarily change everyone's nick in a VC to something dumb!")
@app_commands.describe(channel="The voice channel to meme-ify")
async def massnick(interaction: discord.Interaction, channel: discord.VoiceChannel):
    members = [m for m in channel.members if not m.bot]
    if not members:
        await interaction.response.send_message("No real users in that channel!")
        return

    old_nicks = {}
    new_nicks = random.sample(MEME_NICKS * ((len(members) // len(MEME_NICKS)) + 1), len(members))
    await interaction.response.send_message(f"Changing nicknames for 60 seconds...")

    log.info("/massnick used by %s in %s on %d users", interaction.user, channel, len(members))
    for member, newnick in zip(members, new_nicks):
        try:
            old_nicks[member.id] = member.nick
            await member.edit(nick=newnick)
            log.info("Changed %s's nickname to %s", member.display_name, newnick)
        except Exception as e:
            log.warning("Couldn't change %s's nickname: %s", member.display_name, e)

    await asyncio.sleep(60)
    for member in members:
        try:
            await member.edit(nick=old_nicks[member.id])
            log.info("Restored %s's nickname", member.display_name)
        except Exception:
            pass

@bot.tree.command(name="timeout", description="Send someone to timeout VC for 30 seconds!")
@app_commands.describe(user="User to time out")
async def timeout(interaction: discord.Interaction, user: discord.Member):
    timeout_vc = interaction.guild.get_channel(TIMEOUT_CHANNEL_ID)
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
        log.info("%s sent %s to timeout VC.", interaction.user, user.display_name)
        await asyncio.sleep(30)
        await user.move_to(origin_channel)
        log.info("%s returned from timeout VC.", user.display_name)
    except Exception as e:
        log.error("Timeout error: %s", e)
        await interaction.followup.send(f"Could not move {user.display_name} back. (Maybe they left or permissions issue?)")

@bot.tree.command(name="roast", description="Send a friendly roast to someone!")
@app_commands.describe(user="The target of your roast")
async def roast(interaction: discord.Interaction, user: discord.Member):
    roast = random.choice(ROASTS)
    log.info("/roast used by %s on %s", interaction.user, user)
    await interaction.response.send_message(f"{user.mention} {roast}")

# ========== EVENTS ==========
@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == TARGET_USER_ID and after.channel is not None and (before.channel != after.channel):
        source_channel = after.channel
        panic_channel = member.guild.get_channel(PANIC_CHANNEL_ID)
        if panic_channel is None:
            log.warning("Panic channel not found!")
            return

        for m in source_channel.members:
            if m.id != TARGET_USER_ID and not m.bot:
                try:
                    await m.move_to(panic_channel)
                    log.info("Panic! Moved %s to %s", m.display_name, panic_channel)
                except Exception as e:
                    log.warning("Couldn't move %s: %s", m.display_name, e)

@bot.event
async def on_ready():
    log.info("%s is online and ready to track your glorious battles!", bot.user)
    try:
        synced = await bot.tree.sync()
        log.info("Synced %d slash command(s).", len(synced))
    except Exception as e:
        log.error("Slash command sync error: %s", e)

    channel = bot.get_channel(SCOREBOARD_CHANNEL_ID)
    if channel is None:
        log.error("Couldn't find the channel! Double-check the channel ID.")
        return

    view = ScoreboardView()
    embed = view.make_embed()
    msg_id = load_scoreboard_msg_id()
    scoreboard_msg = None

    if msg_id:
        try:
            scoreboard_msg = await channel.fetch_message(msg_id)
            await scoreboard_msg.edit(embed=embed, view=view)
            log.info("Scoreboard message updated.")
        except Exception as e:
            log.warning("Couldn't fetch or edit scoreboard message: %s", e)

    if scoreboard_msg is None:
        scoreboard_msg = await channel.send(embed=embed, view=view)
        save_scoreboard_msg_id(scoreboard_msg.id)
        log.info("Posted a new scoreboard message.")

# ================== SIEGE AI ===============================
client = OpenAI(api_key=OPENAI_API_KEY)

SIEGE_AI_SYSTEM_PROMPT = (
    "You are a Discord bot that only responds with answers, jokes, roasts, strategies, or memes "
    "about Rainbow Six Siege. Never break character. If someone asks about anything else, steer it "
    "back to Siege, make a Siege meme, or refuse in a Siege-themed way."
)

@bot.tree.command(name="siegeai", description="Ask SiegeBot anything (only Siege-related answers allowed!)")
@app_commands.describe(prompt="Ask anything about Siege operators, memes, strats, or loadouts")
async def siegeai(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": SIEGE_AI_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=350,
            temperature=0.9,
        )
        reply = response.choices[0].message.content
        # Formatting
        formatted = (
            f"**You asked:**\n> {prompt}\n\n"
            f"**SiegeBot says:**\n{reply}"
        )
        await interaction.followup.send(formatted[:2000])  # Discord message limit
    except Exception as e:
        await interaction.followup.send(f"Error fetching Siege wisdom: {e}")


# ========== RUN ==========
bot.run(DISCORD_TOKEN)