from pyrogram import filters
import os
import re
import requests
import yt_dlp

from pyrogram.types import Message
from Oneforall import app


URL_PATTERN = r"(https?://(www\.)?(youtube\.com|youtu\.be|instagram\.com)/[^\s]+)"


# DOWNLOAD FUNCTION
def download_video(url: str):

    try:

        path = "downloads"

        os.makedirs(path, exist_ok=True)

        url = url.split("?")[0]

        # INSTAGRAM
        if "instagram.com" in url:

            try:

                api = (
                    "https://api.agatz.xyz/api/instagram"
                    f"?url={url}"
                )

                response = requests.get(
                    api,
                    timeout=30
                ).json()

                video_url = None

                if response.get("data"):

                    data = response["data"]

                    if isinstance(data, list):
                        video_url = data[0].get("url")
                    else:
                        video_url = data.get("url")

                if video_url:

                    file_path = (
                        f"{path}/instagram_video.mp4"
                    )

                    video = requests.get(
                        video_url,
                        stream=True,
                        timeout=60
                    )

                    with open(file_path, "wb") as f:
                        for chunk in video.iter_content(
                            chunk_size=1024
                        ):
                            if chunk:
                                f.write(chunk)

                    return file_path

            except Exception as e:
                print("INSTAGRAM API ERROR:", e)

        # YOUTUBE
        ydl_opts = {

            "outtmpl": f"{path}/%(title).50s.%(ext)s",

            "format": (
                "bestvideo+bestaudio/"
                "best"
            ),

            "merge_output_format": "mp4",

            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "geo_bypass": True,

            "http_headers": {
                "User-Agent": (
                    "Mozilla/5.0"
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

            file_path = ydl.prepare_filename(
                info
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

        print("DOWNLOAD ERROR:", e)

        return None


# AUTO DOWNLOADER
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

    status = await message.reply_text(
        "⚡ **Downloading...**"
    )

    try:

        file_path = download_video(url)

        if (
            not file_path
            or not os.path.exists(file_path)
        ):

            return await status.edit(
                "❌ Download Failed"
            )

        await status.edit(
            "📤 Uploading..."
        )

        await message.reply_video(
            video=file_path,
            caption=(
                "✅ **Download Complete**"
            )
        )

        try:
            os.remove(file_path)
        except:
            pass

        await status.delete()

    except Exception as e:

        await status.edit(
            f"❌ Error:\n`{e}`"
        )