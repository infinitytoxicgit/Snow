from pyrogram.types import InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle
from Oneforall import app
from Oneforall.utils.inline.start import btn


def help_pannel(_, START=None):

    upl = InlineKeyboardMarkup(
        [

            # ================= TOP SECTION =================

            [
                btn(
                    "ᴘʟᴀʏ 🎵",
                    5224565799888382217,
                    callback_data="help_callback hb11",
                    style=ButtonStyle.PRIMARY
                ),

                btn(
                    "ᴘɪɴɢ ⚡",
                    5224531289826157876,
                    callback_data="help_callback hb10",
                    style=ButtonStyle.PRIMARY
                ),
            ],

            [
                btn(
                    "ᴀᴅᴍɪɴ 🛡",
                    5224338222456283026,
                    callback_data="help_callback hb1",
                    style=ButtonStyle.PRIMARY
                ),

                btn(
                    "ɢʙᴀɴ 🚫",
                    5224496122633941486,
                    callback_data="help_callback hb7",
                    style=ButtonStyle.PRIMARY
                ),
            ],

            [
                btn(
                    "sᴏɴɢ 🎧",
                    5224306392453640289,
                    callback_data="help_callback hb14",
                    style=ButtonStyle.PRIMARY
                ),

                btn(
                    "ʟᴏᴏᴘ 🔁",
                    5224343488086173151,
                    callback_data="help_callback hb8",
                    style=ButtonStyle.PRIMARY
                ),
            ],

            [
                btn(
                    "ғᴜɴ ɢᴀᴍᴇs 🎮",
                    5224659060808250648,
                    callback_data="help_callback hb21",
                    style=ButtonStyle.PRIMARY
                ),
            ],

            # ================= GREEN SECTION =================

            [
                btn(
                    "ʙʀᴏᴀᴅᴄᴀsᴛ 📢",
                    5224524039921365315,
                    callback_data="help_callback hb3",
                    style=ButtonStyle.SUCCESS
                ),

                btn(
                    "ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ 🛠",
                    5224537882600955399,
                    callback_data="help_callback hb9",
                    style=ButtonStyle.SUCCESS
                ),
            ],

            [
                btn(
                    "sᴇᴇᴋ 🔍",
                    5224681093990478312,
                    callback_data="help_callback hb13",
                    style=ButtonStyle.SUCCESS
                ),

                btn(
                    "sʜᴜғғʟᴇ 🎼",
                    5219696148788307720,
                    callback_data="help_callback hb12",
                    style=ButtonStyle.SUCCESS
                ),
            ],

            [
                btn(
                    "ᴘᴏᴡᴇʀᴇᴅ ʙʏ ʀᴏᴏʜɪ ✨",
                    5222287908148371157,
                    url="https://t.me/Go_And_Love_Yourself_Brother",
                    style=ButtonStyle.SUCCESS
                ),
            ],

            # ================= NAVIGATION =================

[
    btn(
        "ɴᴇxᴛ",
        5462931610028510371,
        callback_data="mbot_cb",
        style=ButtonStyle.PRIMARY
    ),

    btn(
        "ʜᴏᴍᴇ",
        5796647601105276281,
        callback_data="settingsback_helper",
        style=ButtonStyle.SUCCESS
    ),

    btn(
        "ɴᴇxᴛ",
        5465144931230190889,
        callback_data="mbot_cb",
        style=ButtonStyle.PRIMARY
    ),
],

            # ================= CLOSE =================

            [
                btn(
                    "ᴄʟᴏsᴇ",
                    5210952531676504517,
                    callback_data="close",
                    style=ButtonStyle.DANGER
                ),
            ],

        ]
    )

    return upl


def help_back_markup(_):

    upl = InlineKeyboardMarkup(
        [
            [
                btn(
                    "ʙᴀᴄᴋ",
                    5210952531676504517,
                    callback_data="settings_back_helper",
                    style=ButtonStyle.DANGER,
                ),
            ]
        ]
    )

    return upl


def private_help_panel(_):

    buttons = [
        [
            btn(
                "ᴏᴘᴇɴ ʜᴇʟᴘ 📚",
                5220035141967046212,
                url=f"https://t.me/{app.username}?start=help",
                style=ButtonStyle.PRIMARY,
            ),
        ],
    ]

    return buttons