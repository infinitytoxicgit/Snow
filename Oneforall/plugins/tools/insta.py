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


# URL PATTERN
URL_PATTERN = r"(https?://[^\s]+)"


# USER AGENTS
USER_AGENTS = [

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0 Safari/537.36",

    "Mozilla/5.0 (Linux; Android 14) Chrome/123.0 Mobile Safari/537.36",

    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) Safari/604.1",

    "Mozilla/5.0 (X11; Linux x86_64) Firefox/126.0"
]


# MULTIPLE INSTAGRAM APIs
INSTAGRAM_APIS = [

    "https://api.neoxr.eu/api/ig?url={url}&apikey=mcandy",

    "https://api.agatz.xyz/api/instagram?url={url}",

    "https://api.ryzendesu.vip/api/downloader/instagram?url={url}",

    "https://api.betabotz.eu.org/api/download/igdowloader?url={url}&apikey=BetaBotz"
]


# SAFE EDIT
async def safe_edit(message, text):

    try:

        await message.edit_text(text)

    except FloodWait as e:

        await asyncio.sleep(e.value)

        await message.edit_text(text)

    except:
        pass


# DOWNLOAD FUNCTION
def download_video(url: str):

    try:

        path = "downloads"

        os.makedirs(path, exist_ok=True)

        url = url.split("?")[0]

        # INSTAGRAM APIs
        if "instagram.com" in url:

            for api in INSTAGRAM_APIS:

                try:

                    api_url = api.format(
                        url=url
                    )

                    headers = {

                        "User-Agent":
                            random.choice(
                                USER_AGENTS
                            )
                    }

                    response = requests.get(
                        api_url,
                        headers=headers,
                        timeout=30
                    )

                    if response.status_code != 200:
                        continue

                    try:
                        data = response.json()
                    except:
                        continue

                    video_url = None

                    # DATA
                    if data.get("data"):

                        result = data["data"]

                        if isinstance(
                            result,
                            list
                        ):

                            first = result[0]

                            if isinstance(
                                first,
                                dict
                            ):

                                video_url = (
                                    first.get("url")
                                    or first.get("video")
                                )

                            else:

                                video_url = first

                        elif isinstance(
                            result,
                            dict
                        ):

                            video_url = (
                                result.get("url")
                                or result.get("video")
                            )

                    # RESULT
                    if (
                        not video_url
                        and data.get("result")
                    ):

                        result = data["result"]

                        if isinstance(
                            result,
                            list
                        ):

                            first = result[0]

                            if isinstance(
                                first,
                                dict
                            ):

                                video_url = (
                                    first.get("url")
                                    or first.get("video")
                                )

                            else:

                                video_url = first

                        elif isinstance(
                            result,
                            dict
                        ):

                            video_url = (
                                result.get("url")
                                or result.get("video")
                            )

                    # DOWNLOAD
                    if video_url:

                        file_path = (
                            f"{path}/instagram_"
                            f"{random.randint(1,9999)}.mp4"
                        )

                        video = requests.get(
                            video_url,
                            headers=headers,
                            stream=True,
                            timeout=60
                        )

                        with open(
                            file_path,
                            "wb"
                        ) as f:

                            for chunk in (
                                video.iter_content(
                                    chunk_size=1024
                                )
                            ):

                                if chunk:
                                    f.write(chunk)

                        if os.path.exists(
                            file_path
                        ):

                            return file_path

                except Exception as e:

                    print(
                        "API ERROR:",
                        e
                    )

        # YOUTUBE / FALLBACK
        ydl_opts = {

            "outtmpl":
                f"{path}/%(title).50s.%(ext)s",

            "format":
                "bestvideo+bestaudio/best",

            "merge_output_format":
                "mp4",

            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "geo_bypass": True,

            "sleep_interval_requests": 3,

            "extractor_retries": 10,

            "retries": 10,

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

            if not file_path.endswith(
                ".mp4"
            ):

                file_path = (
                    os.path.splitext(
                        file_path
                    )[0]
                    + ".mp4"
                )

        return file_path

    except Exception as e:

        print(
            "DOWNLOAD ERROR:",
            e
        )

        return None


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
            caption=(
                "✅ Download Complete"
            ),
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

    except FloodWait as e:

        await asyncio.sleep(
            e.value
        )

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
async def instagram_command(
    client,
    message: Message
):

    if len(message.command) < 2:

        return await message.reply_text(
            "Usage:\n/ig instagram_link"
        )

    url = message.command[1]

    await process_download(
        message,
        url
    )


__MODULE__ = "Downloader"