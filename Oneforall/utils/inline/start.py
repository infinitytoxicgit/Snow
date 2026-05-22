import random
from pyrogram.types import InlineKeyboardButton
from pyrogram.enums import ButtonStyle
import config
from Oneforall import app

def btn(text, emoji_id, style=ButtonStyle.DEFAULT, **kwargs):
    """
    Har button ke liye specific emoji_id use karega.
    """
    try:
        return InlineKeyboardButton(
            text=text,
            icon_custom_emoji_id=emoji_id,
            style=style,
            **kwargs
        )
    except TypeError:
        # Fallback for older versions
        return InlineKeyboardButton(text=text, **kwargs)

def start_panel(_):
    buttons = [
        [
            # Add to Group - 💞 (5438224604499819092)
            btn(_["S_B_1"], 5438224604499819092, url=f"https://t.me/{app.username}?startgroup=true", style=ButtonStyle.SUCCESS),
            # Support - 💜 (6026236216079290036)
            btn(_["S_B_2"], 6026236216079290036, url=config.SUPPORT_CHAT, style=ButtonStyle.DANGER),
        ],
    ]
    return buttons

def private_panel(_):
    buttons = [
        [
            # Add to Group - 🥰 (5436346075998864232)
            btn(_["S_B_3"], 5436346075998864232, url=f"https://t.me/{app.username}?startgroup=true", style=ButtonStyle.SUCCESS)
        ],
        [
            # Profile - 💜 (6026236216079290036)
            btn("˹ 𓆩Q֟፝υєєη𓆪 ˼", 6026236216079290036, url="https://t.me/theinfinitynetwork", style=ButtonStyle.DANGER),
            # Support - 💞 (5438224604499819092)
            btn(_["S_B_2"], 5438224604499819092, url=config.SUPPORT_CHAT, style=ButtonStyle.PRIMARY),
        ],
        [
            # Help/Settings - ✅ (6001604106190330097)
            btn(_["S_B_4"], 6001604106190330097, callback_data="settings_back_helper", style=ButtonStyle.PRIMARY)
        ],
        [
            # Channel - 👑 (6089090515540644835)
            btn(_["S_B_6"], 6089090515540644835, url=config.SUPPORT_CHANNEL, style=ButtonStyle.PRIMARY),
            # Other Channel - 💜 (6026236216079290036)
            btn(_["S_B_5"], 6026236216079290036, url="tg://openmessage?user_id=8569102770", style=ButtonStyle.DANGER)
        ],
        [
            # Website Button - 🎵 (6026256492619895014)
            btn("「 ⌯ ᴜᴘᴘєʀϻσσɴ ᴛᴜηєꜱ ⌯ 」", 6026256492619895014, url="https://uppermooninfinity.jo3.org/", style=ButtonStyle.SUCCESS)
        ],
    ]
    return buttons