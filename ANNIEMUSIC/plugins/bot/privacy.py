#
# Copyright (C) 2024 by Moonshining1@Github, < https://github.com/Moonshining1 >.
#
# This file is part of < https://github.com/Moonshining1/ANNIE-MUSIC > project,
# and is released under the MIT License.
# Please see < https://github.com/Moonshining1/ANNIE-MUSIC/blob/master/LICENSE >
#
# All rights reserved.
#

from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from ANNIEMUSIC import app


@app.on_message(filters.command("privacy"))
async def privacy(client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("View Privacy Policy", url=config.PRIVACY_LINK)]]
    )
    TEXT = f"""
🔒 **Privacy Policy for {client.me.mention} !**

Your privacy is important to us. To learn more about how we collect, use, and protect your data, please review our Privacy Policy here: [Privacy Policy]({config.PRIVACY_LINK}).

If you have any questions or concerns, feel free to reach out to our [Support Team]({config.SUPPORT_GROUP}).
    """

    await message.reply_text(
        TEXT,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
