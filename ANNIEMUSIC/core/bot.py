# Copyright (C) 2024 by Moonshining1@Github, <https://github.com/Moonshining1>.
# This file is part of <https://github.com/Moonshining1/ANNIE-MUSIC> project,
# and is released under the "GNU v3.0 License Agreement".
# Please see <https://github.com/Moonshining1/ANNIE-MUSIC/blob/master/LICENSE>
# All rights reserved.

import asyncio
import threading
import uvloop
from flask import Flask
from pyrogram import Client, idle
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    BotCommand,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
import config
from ..logging import LOGGER

# Install uvloop for better performance
uvloop.install()

# Flask app initialization
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run():
    app.run(host="0.0.0.0", port=8000, debug=False)

# ANNIEBot Class
class ANNIEBot(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot")
        super().__init__(
            "ANNIEMUSIC",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = get_me.first_name + " " + (get_me.last_name or "")
        self.mention = get_me.mention

        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="+ Add me to your clan darlo +",
                        url=f"https://t.me/{self.username}?startgroup=true",
                    )
                ]
            ]
        )

        if config.LOG_GROUP_ID:
            await self.send_startup_message(button)

        if config.SET_CMDS:
            await self.set_commands()

        await self.check_admin_status()

        LOGGER(__name__).info(f"MusicBot Started as {self.name}")

    async def send_startup_message(self, button):
        try:
            await self.send_photo(
                config.LOG_GROUP_ID,
                photo=config.START_IMG_URL,
                caption=(
                    f"✨ <b>{self.mention}</b> is alive 🖤!\n\n"
                    f"<b>System Stats:</b>\n"
                    f"✨  Uptime: 3.11.5\n"
                    f"☁️  Ram: 13.15\n"
                    f"❄️  Cpu: 1.34.0\n"
                    f"🔮  Disk: 2.0.106\n\n"
                    f"<i>Made {self.mention} with love by ᴅᴇᴠᴇʟᴏᴘᴇʀs✨🥀</i>"
                ),
                reply_markup=button,
            )
        except pyrogram.errors.ChatWriteForbidden as e:
            LOGGER(__name__).error(f"Bot cannot write to the log group: {e}")
            await self.send_message_fallback()

    async def send_message_fallback(self):
        try:
            await self.send_message(
                config.LOG_GROUP_ID,
                f"✨ <b>{self.mention}</b> is alive 🖤!\n\n"
                f"<b>System Stats:</b>\n"
                f"✨  Uptime: 3.11.5\n"
                f"☁️  Ram: 13.15\n"
                f"❄️  Cpu: 1.34.0\n"
                f"🔮  Disk: 2.0.106\n\n"
                f"<i>Made {self.mention} with love by ᴅᴇᴠᴇʟᴏᴘᴇʀs✨🥀</i>",
                reply_markup=button,
            )
        except Exception as e:
            LOGGER(__name__).error(f"Failed to send message in log group: {e}")

    async def set_commands(self):
        commands = [
            BotCommand("start", "Start the bot"),
            BotCommand("help", "Get the help menu"),
            BotCommand("ping", "Check if the bot is alive or dead"),
            BotCommand("play", "Start playing requested song"),
            BotCommand("stop", "Stop the current song"),
            BotCommand("pause", "Pause the current song"),
            BotCommand("resume", "Resume the paused song"),
            BotCommand("queue", "Check the queue of songs"),
            BotCommand("skip", "Skip the current song"),
            BotCommand("volume", "Adjust the music volume"),
            BotCommand("lyrics", "Get lyrics of the song"),
        ]

        await self.set_bot_commands(commands, scope=BotCommandScopeAllPrivateChats())

        admin_commands = [
            BotCommand("start", "❥ Start the bot"),
            BotCommand("ping", "❥ Check the ping"),
            BotCommand("help", "❥ Get help"),
            BotCommand("vctag", "❥ Tag all for voice chat"),
            BotCommand("stopvctag", "❥ Stop tagging for VC"),
            BotCommand("tagall", "❥ Tag all members by text"),
            BotCommand("cancel", "❥ Cancel the tagging"),
            BotCommand("settings", "❥ Get the settings"),
            BotCommand("reload", "❥ Reload the bot"),
            BotCommand("play", "❥ Play the requested song"),
            BotCommand("vplay", "❥ Play video along with music"),
            BotCommand("end", "❥ Empty the queue"),
            BotCommand("playlist", "❥ Get the playlist"),
            BotCommand("stop", "❥ Stop the song"),
            BotCommand("lyrics", "❥ Get the song lyrics"),
            BotCommand("song", "❥ Download the requested song"),
            BotCommand("video", "❥ Download the requested video song"),
            BotCommand("gali", "❥ Reply with fun"),
            BotCommand("shayri", "❥ Get a shayari"),
            BotCommand("love", "❥ Get a love shayari"),
            BotCommand("sudolist", "❥ Check the sudo list"),
            BotCommand("owner", "❥ Check the owner"),
            BotCommand("update", "❥ Update bot"),
            BotCommand("gstats", "❥ Get stats of the bot"),
            BotCommand("repo", "❥ Check the repo"),
        ]

        await self.set_bot_commands(admin_commands, scope=BotCommandScopeAllChatAdministrators())

    async def check_admin_status(self):
        try:
            chat_member_info = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
            if chat_member_info.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error("Please promote Bot as Admin in Logger Group")
        except Exception as e:
            LOGGER(__name__).error(f"Error occurred while checking bot status: {e}")

# Define the async boot function
async def anony_boot():
    bot = ANNIEBot()
    await bot.start()
    await idle()

if __name__ == "__main__":
    LOGGER(__name__).info("Starting Flask server...")

    # Start Flask server in a new thread
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()

    LOGGER(__name__).info("Starting ANNIEBot...")

    # Run the bot
    asyncio.run(anony_boot())

    LOGGER(__name__).info("Stopping ANNIEBot...")
