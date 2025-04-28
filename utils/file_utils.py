import os
import json
from utils import config
from utils import logging_setup as log

# ===== SCOREBOARD FILES =====
def load_scores():
    if os.path.exists(config.SCORES_FILE):
        try:
            with open(config.SCORES_FILE, "r") as f:
                data = json.load(f)
                log.log.info("Loaded scores from file.")
                return data.get("attack", 0), data.get("defend", 0)
        except (json.JSONDecodeError, ValueError):
            log.log.warning("Score file corrupted, resetting scores.")
            return 0, 0
    return 0, 0

def save_scores(attack, defend):
    with open(config.SCORES_FILE, "w") as f:
        json.dump({"attack": attack, "defend": defend}, f)
    log.log.info("Saved scores: Attack=%s, Defend=%s", attack, defend)

def save_scoreboard_msg_id(msg_id):
    with open(config.SCOREBOARD_MSG_FILE, "w") as f:
        json.dump({"msg_id": msg_id}, f)
    log.log.info("Saved scoreboard message ID: %s", msg_id)

def load_scoreboard_msg_id():
    if os.path.exists(config.SCOREBOARD_MSG_FILE):
        try:
            with open(config.SCOREBOARD_MSG_FILE, "r") as f:
                data = json.load(f)
                return data.get("msg_id", None)
        except (json.JSONDecodeError, ValueError):
            return None
    return None

# ===== PANIC CONFIG FILES =====
def load_panic_config():
    if os.path.exists(config.PANIC_CONFIG_FILE):
        try:
            with open(config.PANIC_CONFIG_FILE, "r") as f:
                data = json.load(f)
                log.log.info("Loaded panic config.")
                return data.get("target_user_id"), data.get("panic_channel_id")
        except (json.JSONDecodeError, ValueError):
            log.log.warning("Panic config corrupted, resetting.")
            return None, None
    return None, None

def save_panic_config(target_user_id, panic_channel_id):
    with open(config.PANIC_CONFIG_FILE, "w") as f:
        json.dump({
            "target_user_id": target_user_id,
            "panic_channel_id": panic_channel_id
        }, f)
    log.log.info("Saved panic config: TargetUser=%s, PanicChannel=%s", target_user_id, panic_channel_id)
