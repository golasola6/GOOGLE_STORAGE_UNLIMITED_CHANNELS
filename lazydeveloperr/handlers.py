# (c) @LazyDeveloperr

import asyncio
from config import *
from pyrogram import Client
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram.errors import FloodWait
from base64 import standard_b64encode, standard_b64decode
from helper_func import encode

def str_to_b64(__str: str) -> str:
    str_bytes = __str.encode('ascii')
    bytes_b64 = standard_b64encode(str_bytes)
    b64 = bytes_b64.decode('ascii')
    return b64


async def forward_to_channel(bot: Client, message: Message, editable: Message):
    try:
        __SENT = await message.forward(CHANNEL_ID)
        return __SENT
    except FloodWait as sl:
        if sl.value > 45:
            await asyncio.sleep(sl.value)
            await bot.send_message(
                chat_id=int(LOG_CHANNEL),
                text=f"#FloodWait:\nGot FloodWait of `{str(sl.value)}s` from `{str(editable.chat.id)}` !!",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Ban User", callback_data=f"ban_user_{str(editable.chat.id)}")]
                    ]
                )
            )
        return await forward_to_channel(bot, message, editable)


async def save_batch_media_in_channel(bot: Client, editable: Message, message_ids: list):
    try:
        message_ids_str = ""
        for message in (await bot.get_messages(chat_id=editable.chat.id, message_ids=message_ids)):
            sent_message = await forward_to_channel(bot, message, editable)
            if sent_message is None:
                continue
            message_ids_str += f"{str(sent_message.id)} "
            await asyncio.sleep(2)
        # SaveMessage = await bot.send_message(
        #     chat_id=CHANNEL_ID,
        #     text=message_ids_str,
        #     disable_web_page_preview=True,
        #     reply_markup=InlineKeyboardMarkup([[
        #         InlineKeyboardButton("Delete Batch", callback_data="closeMessage")
        #     ]])
        # )
        try:
            post_message = await message.copy(chat_id = bot.db_channel.id, disable_notification=True)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            post_message = await message.copy(chat_id = bot.db_channel.id, disable_notification=True)
        except Exception as e:
            print(e)
            await bot.edit_text("Something went Wrong..!")
            return
        converted_id = post_message.id * abs(bot.db_channel.id)
        string = f"get-{converted_id}"
        base64_string = await encode(string)
        link = f"https://t.me/{bot.username}?start={base64_string}"

        share_link = f"https://t.me/{bot.username}?start=LazyDeveloperr_{str_to_b64(str(SaveMessage.id))}"

        await editable.edit(
            f"Here is your batch link: {link} \n\n link 2: {share_link}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⚡️ Open Link ⚡️", url=link)]]
            ),
            disable_web_page_preview=True
        )

        await bot.send_message(
            chat_id=int(LOG_CHANNEL),
            text=f"#BATCH_SAVE:\n\n[{editable.reply_to_message.from_user.first_name}](tg://user?id={editable.reply_to_message.from_user.id}) Got Batch Link!",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✧ Open Link", url=link)]])
        )
        # ✧ Bina soche smjhe code edit mt krna wrna error dhundne mei umrr beet jaayega.
        # ✧ source code upgraded by The sir LazyDeveloper 
        # ✧ Don't remove credit ✧ @LazyDeveloper ✧

    except Exception as err:
        await editable.edit(f"ꜱᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ...\n\nError `{err}`")
        await bot.send_message(
            chat_id=int(LOG_CHANNEL),
            text=f"#ERROR_TRACEBACK:\nGot Error from `{str(editable.chat.id)}` !!\n\nTraceback: `{err}`",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Ban User", callback_data=f"ban_user_{str(editable.chat.id)}")]
                ]
            )
        )
