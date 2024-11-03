import asyncio
from pyrogram import filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from config import LOG_GROUP_ID
from ANNIEMUSIC import app  # Ensure ANNIEMUSIC is imported correctly

# Handle /help command in group only
@ANNIEMUSIC.on_message(filters.command("help"))
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
@ANNIEMUSIC.on_message(filters.command("start"))
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
        reply_markup=keyboard,
    )
