import asyncio
import importlib
from pyrogram import filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

import config
from config import BANNED_USERS
from ANNIEMUSIC import HELPABLE, LOGGER, app, userbot
from ANNIEMUSIC.core.call import MOON
from ANNIEMUSIC.plugins import ALL_MODULES
from ANNIEMUSIC.utils.database import get_banned_users, get_gbanned

# Reload modules if needed
for module in ALL_MODULES:
    importlib.import_module(f"ANNIEMUSIC.plugins.{module}")

# Handle /help command in group only
@app.on_message(filters.command("help"))
async def help_command(client, message: Message):
    if message.chat.type not in ["group", "supergroup"]:
        return  # Ignore if the chat is not a group

    help_url = "https://t.me/musicXanime_bot?startgroup=true"  # Replace with your help URL
    button_text = "Click me for help!"
    photo_url = "https://files.catbox.moe/6iv99c.jpg"  # Replace with your image URL

    help_text = (
        "Here's how I can help you! Please click the button below to view all available commands."
    )

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(button_text, url=help_url)]]
    )

    await client.send_photo(
        chat_id=message.chat.id,
        photo=photo_url,
        caption=help_text,
        reply_markup=keyboard,
    )

# Handle /start command in group only
@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
    if message.chat.type not in ["group", "supergroup"]:
        return  # Ignore if the chat is not a group

    update_url = "https://t.me/kittyxupdates"  # Replace with your update URL
    support_url = "https://t.me/grandxmasti" # Replace with your support URL
    photo_url = "https://files.catbox.moe/6iv99c.jpg"
  
    start_text = (
        "Welcome! Use the buttons below to check updates or get support."
    )

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Update", url=update_url)],
            [InlineKeyboardButton("Support", url=support_url)]
        ]
    )

    await client.send_message(
        chat_id=message.chat.id,
        text=start_text,
        photo=photo_url,
        reply_markup=keyboard,
    )

# Initialize and start the bot
async def start_bot():
    await app.start()
    LOGGER.info("Bot started and running!")
    
    for module in ALL_MODULES:
        importlib.reload(importlib.import_module(f"ANNIEMUSIC.plugins.{module}"))
        
    await idle()

if __name__ == "__main__":
    asyncio.run(start_bot())
