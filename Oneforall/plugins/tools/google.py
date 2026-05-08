import logging

from duckduckgo_search import DDGS
from googlesearch import search
from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from SafoneAPI import SafoneAPI
from Oneforall import app

logging.basicConfig(level=logging.INFO)


# GOOGLE + DUCKDUCKGO SEARCH
@app.on_message(filters.command(["google", "gle"]))
async def google_search(client, message):

    if len(message.command) < 2 and not message.reply_to_message:

        return await message.reply_text(
            "**Usage:**\n`/google roohi`"
        )

    # QUERY
    if (
        message.reply_to_message
        and message.reply_to_message.text
    ):

        query = message.reply_to_message.text

    else:

        query = " ".join(message.command[1:])

    msg = await message.reply_text(
        "🔎 **Searching Multiple Browsers...**"
    )

    text = (
        "╭───────────────⭓\n"
        "│ 🔍 **SEARCH RESULTS**\n"
        "├───────────────\n"
        f"│ 📝 Query: `{query}`\n"
        "╰───────────────⭓\n\n"
    )

    found = False

    try:

        # GOOGLE SEARCH
        google_results = list(
            search(
                query,
                num_results=3,
                sleep_interval=2
            )
        )

        if google_results:

            text += "🌐 **Google Results**\n\n"

            for index, link in enumerate(
                google_results,
                start=1
            ):

                text += (
                    f"➤ {index}. {link}\n\n"
                )

            found = True

    except Exception as e:

        logging.exception(e)

    try:

        # DUCKDUCKGO SEARCH
        ddg_results = []

        with DDGS() as ddgs:

            results = ddgs.text(
                query,
                max_results=3
            )

            for r in results:
                ddg_results.append(r)

        if ddg_results:

            text += "🦆 **DuckDuckGo Results**\n\n"

            for index, result in enumerate(
                ddg_results,
                start=1
            ):

                title = result.get(
                    "title",
                    "No Title"
                )

                href = result.get(
                    "href",
                    ""
                )

                text += (
                    f"➤ [{title}]({href})\n\n"
                )

            found = True

    except Exception as e:

        logging.exception(e)

    if not found:

        return await msg.edit(
            "❌ No results found."
        )

    buttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                "🔍 Search Again",
                switch_inline_query_current_chat=""
            )
        ]]
    )

    await msg.edit(
        text,
        disable_web_page_preview=True,
        reply_markup=buttons
    )


# PLAY STORE SEARCH
@app.on_message(filters.command(["app", "apps"]))
async def playstore_search(client, message):

    if len(message.command) < 2 and not message.reply_to_message:

        return await message.reply_text(
            "**Usage:**\n`/app Spotify`"
        )

    # QUERY
    if (
        message.reply_to_message
        and message.reply_to_message.text
    ):

        query = message.reply_to_message.text

    else:

        query = " ".join(message.command[1:])

    msg = await message.reply_text(
        "📱 **Searching Play Store...**"
    )

    try:

        data = await SafoneAPI().apps(
            query,
            1
        )

        if (
            not data
            or "results" not in data
        ):

            return await msg.edit(
                "❌ No app found."
            )

        result = data["results"][0]

        title = result.get(
            "title",
            "Unknown"
        )

        developer = result.get(
            "developer",
            "Unknown"
        )

        description = result.get(
            "description",
            "No description"
        )

        link = result.get(
            "link",
            ""
        )

        icon = result.get(
            "icon",
            ""
        )

        app_id = result.get(
            "id",
            "Unknown"
        )

        caption = (
            "╭───────────────⭓\n"
            "│ 📱 **PLAY STORE APP**\n"
            "├───────────────\n"
            f"│ 🏷 Name: [{title}]({link})\n"
            f"│ 🆔 ID: `{app_id}`\n"
            f"│ 👨‍💻 Dev: {developer}\n"
            "╰───────────────⭓\n\n"
            f"📝 **Description:**\n{description}"
        )

        buttons = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(
                    "📥 Open In Play Store",
                    url=link
                )
            ]]
        )

        if icon:

            await message.reply_photo(
                photo=icon,
                caption=caption,
                reply_markup=buttons
            )

        else:

            await message.reply_text(
                caption,
                reply_markup=buttons,
                disable_web_page_preview=True
            )

        await msg.delete()

    except Exception as e:

        logging.exception(e)

        await msg.edit(
            f"❌ Error:\n`{e}`"
        )