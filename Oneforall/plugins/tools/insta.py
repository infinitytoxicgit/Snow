import asyncio
import os
import random
import re
import requests
import yt_dlp

from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from Oneforall import app


URL_PATTERN = r"(https?://[^\s]+)"


USER_AGENTS = [

    "Mozilla/5.0 (Linux; Android 14)",

    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
]


# WORKING APIs
INSTAGRAM_APIS = [

    "https://api.vreden.my.id/api/igdl?url={url}",

    "https://api.botcahx.eu.org/api/dowloader/igdl?url={url}&apikey=Admin",

    "https://api.agatz.xyz/api/instagram?url={url}"
]


# SAFE EDIT
async def safe_edit(msg, text):

    try:
        await msg.edit_text(text)

    except FloodWait as e:

        await asyncio.sleep(e.value)

        try:
            await msg.edit_text(text)
        except:
            pass

    except:
        pass


# API DOWNLOAD
def api_instagram_download(url):

    for api in INSTAGRAM_APIS:

        try:

            api_url = api.format(
                url=url
            )

            response = requests.get(
                api_url,
                headers={
                    "User-Agent":
                        random.choice(
                            USER_AGENTS
                        )
                },
                timeout=30
            )

            if response.status_code != 200:
                continue

            try:
                data = response.json()
            except:
                continue

            video_url = None

            # data
            if data.get("data"):

                d = data["data"]

                if isinstance(d, list):

                    first = d[0]

                    if isinstance(first, dict):

                        video_url = (
                            first.get("url")
                            or first.get("video")
                        )

                    else:

                        video_url = first

                elif isinstance(d, dict):

                    video_url = (
                        d.get("url")
                        or d.get("video")
                    )

            # result
            if (
                not video_url
                and data.get("result")
            ):

                d = data["result"]

                if isinstance(d, list):

                    first = d[0]

                    if isinstance(first, dict):

                        video_url = (
                            first.get("url")
                            or first.get("video")
                        )

                    else:

                        video_url = first

                elif isinstance(d, dict):

                    video_url = (
                        d.get("url")
                        or d.get("video")
                    )

            if not video_url:
                continue

            path = "downloads"

            os.makedirs(
                path,
                exist_ok=True
            )

            file_path = (
                f"{path}/ig_"
                f"{random.randint(1000,9999)}.mp4"
            )

            r = requests.get(
                video_url,
                stream=True,
                timeout=60,
                headers={
                    "User-Agent":
                        random.choice(
                            USER_AGENTS
                        )
                }
            )

            with open(
                file_path,
                "wb"
            ) as f:

                for chunk in r.iter_content(
                    chunk_size=1024
                ):

                    if chunk:
                        f.write(chunk)

            if os.path.exists(file_path):

                return file_path

        except Exception as e:

            print(
                "API ERROR:",
                e
            )

    return None


# YTDLP FALLBACK
def ytdlp_download(url):

    try:

        path = "downloads"

        os.makedirs(
            path,
            exist_ok=True
        )

        ydl_opts = {

            "outtmpl":
                f"{path}/%(title).50s.%(ext)s",

            "format":
                "best[ext=mp4]/best",

            "quiet": True,

            "no_warnings": True,

            "noplaylist": True,

            "geo_bypass": True,

            "retries": 5,

            "extractor_retries": 5,

            "http_headers": {

                "User-Agent":
                    random.choice(
                        USER_AGENTS
                    )
            }
        }

        with yt_dlp.YoutubeDL(
            ydl_opts
        ) as ydl:

            info = ydl.extract_info(
                url,
                download=True
            )

            file_path = (
                ydl.prepare_filename(
                    info
                )
            )

        if os.path.exists(file_path):

            return file_path

    except Exception as e:

        print(
            "YTDLP ERROR:",
            e
        )

    return None


# MAIN DOWNLOADER
def download_video(url):

    # Instagram APIs first
    if "instagram.com" in url:

        file_path = (
            api_instagram_download(
                url
            )
        )

        if file_path:
            return file_path

    # Fallback
    return ytdlp_download(url)


# PROCESS
async def process_download(
    message,
    url
):

    status = await message.reply_text(
        "⚡ Downloading..."
    )

    try:

        file_path = download_video(
            url
        )

        if (
            not file_path
            or not os.path.exists(
                file_path
            )
        ):

            return await safe_edit(
                status,
                "❌ Download Failed"
            )

        await safe_edit(
            status,
            "📤 Uploading..."
        )

        buttons = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(
                    "🔗 Open Link",
                    url=url
                )
            ]]
        )

        await message.reply_video(
            video=file_path,
            caption="✅ Download Complete",
            reply_markup=buttons
        )

        try:
            os.remove(file_path)
        except:
            pass

        try:
            await status.delete()
        except:
            pass

    except Exception as e:

        await safe_edit(
            status,
            f"❌ Error:\n`{e}`"
        )


# AUTO
@app.on_message(
    filters.text &
    filters.regex(URL_PATTERN)
)
async def auto_downloader(
    client,
    message: Message
):

    match = re.search(
        URL_PATTERN,
        message.text
    )

    if not match:
        return

    url = match.group(0)

    if (
        "instagram.com" not in url
        and "youtube.com" not in url
        and "youtu.be" not in url
    ):
        return

    await process_download(
        message,
        url
    )


# COMMANDS
@app.on_message(
    filters.command(
        [
            "ig",
            "insta",
            "instagram"
        ]
    )
)
async def insta_command(
    client,
    message: Message
):

    if len(message.command) < 2:

        return await message.reply_text(
            "Usage:\n/ig link"
        )

    url = message.command[1]

    await process_download(
        message,
        url
    )