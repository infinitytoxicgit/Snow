import asyncio
import speedtest

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

from Oneforall import app
from Oneforall.misc import SUDOERS


# SPEEDTEST FUNCTION
def run_speedtest():

    test = speedtest.Speedtest()

    test.get_best_server()

    test.download()

    test.upload()

    try:
        test.results.share()
    except:
        pass

    return test.results.dict()


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


# COMMAND
@app.on_message(
    filters.command(
        ["speedtest", "spt"]
    ) & SUDOERS
)
async def speedtest_function(
    client,
    message: Message
):

    m = await message.reply_text(
        "⚡ Running Speed Test..."
    )

    try:

        loop = asyncio.get_event_loop()

        result = await loop.run_in_executor(
            None,
            run_speedtest
        )

        # SPEEDS
        download = round(
            result["download"] / 1024 / 1024,
            2
        )

        upload = round(
            result["upload"] / 1024 / 1024,
            2
        )

        ping = result.get(
            "ping",
            "N/A"
        )

        # CLIENT
        client_data = result.get(
            "client",
            {}
        )

        isp = client_data.get(
            "isp",
            "Unknown"
        )

        country = client_data.get(
            "country",
            "Unknown"
        )

        # SERVER
        server_data = result.get(
            "server",
            {}
        )

        server = server_data.get(
            "name",
            "Unknown"
        )

        sponsor = server_data.get(
            "sponsor",
            "Unknown"
        )

        latency = server_data.get(
            "latency",
            "Unknown"
        )

        caption = f"""
╭───────────────⭓
│ ⚡ SPEED TEST
├───────────────
│ 📥 Download: {download} Mbps
│ 📤 Upload: {upload} Mbps
│ 🏓 Ping: {ping} ms
├───────────────
│ 🌍 ISP: {isp}
│ 🇮🇳 Country: {country}
├───────────────
│ 🖥 Server: {server}
│ 🏢 Sponsor: {sponsor}
│ ⚡ Latency: {latency}
╰───────────────⭓
"""

        # SHARE IMAGE
        share = result.get("share")

        if share:

            await message.reply_photo(
                photo=share,
                caption=caption
            )

        else:

            await message.reply_text(
                caption
            )

        try:
            await m.delete()
        except:
            pass

    except Exception as e:

        await safe_edit(
            m,
            f"❌ Error:\n`{e}`"
        )