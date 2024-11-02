#
# Copyright (C) 2024 by Moonshining1@Github, < https://github.com/Moonshining1 >.
#
# This file is part of < https://github.com/Moonshining1/ANNIE-MUSIC > project,
# and is released under the MIT License.
# Please see < https://github.com/Moonshining1/ANNIE-MUSIC/blob/master/LICENSE >
#
# All rights reserved.
#
import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch
from config import YOUTUBE_IMG_URL

# Utility functions
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight))

def truncate(text):
    words = text.split(" ")
    text1, text2 = "", ""
    for word in words:
        if len(text1) + len(word) < 30:
            text1 += " " + word
        elif len(text2) + len(word) < 30:
            text2 += " " + word
    return [text1.strip(), text2.strip()]

def crop_center_circle(img, output_size, border, crop_scale=1.5):
    half_width, half_height = img.size[0] / 2, img.size[1] / 2
    larger_size = int(output_size * crop_scale)
    img = img.crop((
        half_width - larger_size / 2,
        half_height - larger_size / 2,
        half_width + larger_size / 2,
        half_height + larger_size / 2
    ))
    img = img.resize((output_size - 2 * border, output_size - 2 * border))

    final_img = Image.new("RGBA", (output_size, output_size), "white")
    mask_main = Image.new("L", (output_size - 2 * border, output_size - 2 * border), 0)
    draw_main = ImageDraw.Draw(mask_main)
    draw_main.ellipse((0, 0, output_size - 2 * border, output_size - 2 * border), fill=255)
    final_img.paste(img, (border, border), mask_main)

    mask_border = Image.new("L", (output_size, output_size), 0)
    draw_border = ImageDraw.Draw(mask_border)
    draw_border.ellipse((0, 0, output_size, output_size), fill=255)
    
    return Image.composite(final_img, Image.new("RGBA", final_img.size, (0, 0, 0, 0)), mask_border)

# Main function to generate thumbnail
async def get_thumb(videoid):
    # Check if cached thumbnail exists
    if os.path.isfile(f"cache/{videoid}_v4.png"):
        return f"cache/{videoid}_v4.png"
    
    try:
        # Search video on YouTube
        query = f"https://www.youtube.com/watch?v={videoid}"
        results = VideosSearch(query, limit=1)
        for result in (await results.next())["result"]:
            title = re.sub(r"\W+", " ", result.get("title", "Unsupported Title")).title()
            duration = result.get("duration", "Unknown Mins")
            thumbnail_url = result["thumbnails"][0]["url"].split("?")[0]
            views = result.get("viewCount", {}).get("short", "Unknown Views")
            channel = result.get("channel", {}).get("name", "Unknown Channel")
        
        # Download thumbnail image
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail_url) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        youtube_img = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube_img)
        image2 = image1.convert("RGBA")
        background = ImageEnhance.Brightness(image2.filter(ImageFilter.BoxBlur(20))).enhance(0.6)

        # Draw details on the thumbnail
        draw = ImageDraw.Draw(background)
        arial = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font2.ttf", 30)
        title_font = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font3.ttf", 45)
        circle_thumbnail = crop_center_circle(youtube_img, 400, 20).resize((400, 400))

        # Positions and text for overlay
        circle_position = (120, 160)
        text_x_position = 565
        background.paste(circle_thumbnail, circle_position, circle_thumbnail)

        title1 = truncate(title)
        draw.text((text_x_position, 180), title1[0], fill=(255, 255, 255), font=title_font)
        draw.text((text_x_position, 230), title1[1], fill=(255, 255, 255), font=title_font)
        draw.text((text_x_position, 320), f"{channel} | {views[:23]}", (255, 255, 255), font=arial)

        # Duration line and play icons
        line_length = 580
        red_length = int(line_length * 0.6)
        draw.line([(text_x_position, 380), (text_x_position + red_length, 380)], fill="red", width=9)
        draw.line([(text_x_position + red_length, 380), (text_x_position + line_length, 380)], fill="white", width=8)
        draw.ellipse([(text_x_position + red_length - 10, 370), (text_x_position + red_length + 10, 390)], fill="red")

        draw.text((text_x_position, 400), "00:00", (255, 255, 255), font=arial)
        draw.text((1080, 400), duration, (255, 255, 255), font=arial)
        play_icons = Image.open("ANNIEMUSIC/assets/thumb/play_icons.png").resize((580, 62))
        background.paste(play_icons, (text_x_position, 450), play_icons)

        # Clean up and save
        os.remove(f"cache/thumb{videoid}.png")
        background.save(f"cache/{videoid}_v4.png")
        return f"cache/{videoid}_v4.png"

    except Exception:
        return YOUTUBE_IMG_URL
                    
                                
