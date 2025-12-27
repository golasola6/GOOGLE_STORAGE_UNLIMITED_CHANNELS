
import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from database.database import db
from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON, FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL2, FORCE_SUB_CHANNEL3
from helper_func import encode
from lazydeveloperr.lazy_forcesub import lazy_force_sub, is_subscribed
from config import *
from utils import get_shortlink 
from motor.motor_asyncio import AsyncIOMotorClient  
Dbclient = AsyncIOMotorClient(DB_URI)
Cluster = Dbclient['Cluster0']
Data = Cluster['users']

@Bot.on_message(filters.private & (filters.document | filters.video | filters.audio) & filters.user(ADMINS) & ~filters.command(['start','users','broadcast','batch','genlink','stats', 'reset_locked']))
async def channel_post(client: Client, message: Message):
    # user = message.from_user
    # if not await db.is_user_exist(user.id):
    #     await db.add_user(user.id)
    id = message.from_user.id
    if not await db.is_user_exist(id):
        await db.add_user(id)

    # if (FORCE_SUB_CHANNEL or FORCE_SUB_CHANNEL2 or FORCE_SUB_CHANNEL3) and not await is_subscribed(client, message):
    #     # User is not subscribed to any of the required channels, trigger force_sub logic
    #     return await lazy_force_sub(client, message)

    reply_text = await message.reply_text("Please Wait...!", quote = True)
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return
    converted_id = post_message.id * abs(client.db_channel.id)
    print(f"post id : {post_message.id}")
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    file_id = base64_string
    print(f"base64_string : {base64_string}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    lazydeveloperr = await get_shortlink(id, link)
    
    print(link)
    print(lazydeveloperr)
    # ========================================================
    # channel = await client.ask(
    #     chat_id=message.chat.id,
    #     text="💡 Please send the channel ID to connect the file : "
    # )

    # # Validate integer
    # if not channel.text.lstrip("-").isdigit():
    #     await message.reply("❌ Invalid Channel ID! Process stopped.")
    #     return

    # channel_id = int(channel.text)
    
    # await db.save_locked_file(file_id, channel_id)
    # await channel.delete()
    # =======================================================

    msg = await client.ask(
        chat_id=message.chat.id,
        text="💡 Send channel IDs separated by space:"
    )

    raw_ids = msg.text.strip().split()
    channel_ids = []

    for ch in raw_ids:
        if ch.lstrip("-").isdigit():
            channel_ids.append(int(ch))
        else:
            await message.reply(f"❌ Invalid Channel ID: `{ch}`")
            await msg.delete()
            return

    await db.save_locked_file(file_id, channel_ids)
    await msg.delete()

    reply_markup = InlineKeyboardMarkup([
        # [InlineKeyboardButton("🏮 Share Shortlink 🔥", url=f'https://telegram.me/share/url?url={lazydeveloperr}')],
        [InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')],
        [InlineKeyboardButton("🚀 Rename", callback_data='rename')]
        ])

    await reply_text.edit(f"✅ <b>{len(channel_ids)} channels</b> linked to this file.\n\n<b>Here is your link</b>\n\n{link}\n\n🏮 Share Shortlink 🔥 : {lazydeveloperr}", reply_markup=reply_markup, disable_web_page_preview = True)

    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)

@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    print(f"Converted ID : {converted_id}")
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')],
        [InlineKeyboardButton("🚀 Rename", callback_data="rename")]
        ])
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass


