import asyncio
import importlib
import os
from flask import Flask
from threading import Thread

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from AnonXMusic import LOGGER, app, userbot
from AnonXMusic.core.call import Anony
from AnonXMusic.misc import sudo
from AnonXMusic.plugins import ALL_MODULES
from AnonXMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# --- Render Port Binding (Flask Server) ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running!"

def run_web_server():
    # Render default port 10000 use karta hai agar PORT env na mile
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_web_server)
    t.daemon = True
    t.start()
# -----------------------------------------

async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()
    
    await sudo()
    
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass

    await app.start()
    
    for all_module in ALL_MODULES:
        importlib.import_module("AnonXMusic.plugins" + all_module)
    
    LOGGER("AnonXMusic.plugins").info("Successfully Imported Modules...")
    
    await userbot.start()
    await Anony.start()
    
    try:
        await Anony.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("AnonXMusic").error(
            "Please turn on the videochat of your log group\\channel.\\n\\nStopping Bot..."
        )
        # Yahan exit() ki jagah hum bot ko chalne denge taaki web server down na ho
        pass
    except:
        pass

    await Anony.decorators()
    
    # Flask server yahan start hoga
    keep_alive()
    LOGGER("AnonXMusic").info("Web Server Started for Render Port Binding...")

    await idle()
    await app.stop()
    LOGGER("AnonXMusic").info("Stopping AnonX Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
