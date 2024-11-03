import asyncio
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from config import LOG_GROUP_ID
from ANNIEMUSIC import app  # Ensure ANNIEMUSIC is imported correctly

# Function to send a message with a photo and a keyboard
async def send_help_message(client, chat_id):
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
        chat_id=chat_id,
        photo=photo_url,
        caption=help_text,
        reply_markup=keyboard,
    )

# Handle /help command in group only
@app.on_message(filters.command("help") & filters.group)
async def help_command(client, message: Message):
    try:
        await send_help_message(client, message.chat.id)
    except Exception as e:
        print(f"Error sending help message: {e}")

# Function to send a welcome message with buttons
async def send_start_message(client, chat_id):
    update_url = "https://t.me/kittyxupdates"  # Replace with your update URL
    support_url = "https://t.me/grandxmasti"  # Replace with your support URL
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
        chat_id=chat_id,
        text=start_text,
        reply_markup=keyboard,
    )

# Handle /start command in group only
@app.on_message(filters.command("start") & filters.group)
async def start_command(client, message: Message):
    try:
        await send_start_message(client, message.chat.id)
    except Exception as e:
        print(f"Error sending start message: {e}")

# Run the bot until interrupted
if __name__ == "__main__":
    asyncio.run(app.run())
