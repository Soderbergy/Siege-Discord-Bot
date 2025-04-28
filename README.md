# SiegeBot

A spicy Discord bot for Rainbow Six Siege fans, packed with:
- Siege-only AI responses
- Attack/Defend score tracking
- Voice channel "panic mode"
- Mass nickname memes
- Roasty toasty friend roasting

---

## 🛠 Setup Instructions

1. **Clone the project**
```bash
git clone <your-repo-url>
cd siege-bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Create a `.env` file** (in the project root)
```plaintext
DISCORD_TOKEN=your_discord_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

4. **Prepare your `data/` folder**
- Place empty (or copied) `panic_config.json`, `scores.json`, `scoreboard_msg.json` into a `/data` folder.

Example structure:
```plaintext
siegebot/
├── Bot.py
├── cogs/
├── utils/
├── data/
│   ├── panic_config.json
│   ├── scores.json
│   ├── scoreboard_msg.json
├── requirements.txt
├── README.md
```

5. **Run the bot**
```bash
python Bot.py
```

The bot will auto-sync slash commands and get ready to meme, roast, and panic!

---

## 📜 Commands Cheat Sheet
| Slash Command | What it does |
|:---|:---|
| `/siegeai [prompt]` | Ask SiegeBot anything (about Siege only!) |
| `/operator [team]` | Get a random attacker or defender |
| `/panicset [user] [channel]` | Set panic mode target user and channel |
| `/massnick [channel]` | Meme everyone's nickname for 60 seconds |
| `/timeout [user]` | Send someone to timeout VC for 30s |
| `/roast [user]` | Drop a spicy roast on someone |

---

## 🧹 Features
- Modular Cogs
- Fancy color-logging
- OpenAI siege-only chatting
- Data saved in JSON files for easy backup

---

## 🎖 Credits
Built by Levii Soderberg with caffeine, bad aim, and Siege memes. 🌈🎮