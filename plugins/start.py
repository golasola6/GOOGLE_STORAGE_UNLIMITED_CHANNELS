import os, asyncio, humanize
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait,ChatAdminRequired, UserIsBlocked, InputUserDeactivated, PeerIdInvalid
from bot import Bot
from config import *
from helper_func import subscribed, encode, decode, get_messages
from database.database import db
logger = logging.getLogger(__name__)
import time
import logging 
from lazydeveloperr.lazy_forcesub import is_subscribed, lazy_force_sub
import datetime
neha_delete_time = FILE_AUTO_DELETE
neha = neha_delete_time
file_auto_delete = humanize.naturaldelta(neha)
from utils import temp

@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    user = message.from_user
    # if not await db.is_user_exist(user.id):
    #     await db.add_user(user.id)
    id = message.from_user.id
    user_id = message.from_user.id
    if not await db.is_user_exist(id):
        await db.add_user(id)
    # if (FORCE_SUB_CHANNEL or FORCE_SUB_CHANNEL2 or FORCE_SUB_CHANNEL3) and not await is_subscribed(client, message):
    #     # User is not subscribed to any of the required channels, trigger force_sub logic
    #     return await lazy_force_sub(client, message)
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
            file_id = base64_string
        except IndexError:
            return

        channel_id = await db.get_locked_files(file_id)

        if not channel_id:
            await message.reply("❌ No channels linked with this file.")
            return
        # reset old channel
        # temp.ASSIGNED_CHANNEL[user_id] = []
        # assign new channel
        # temp.ASSIGNED_CHANNEL.pop(user_id, None)
        print(f"all channels associated with this file is : {channel_id}")
        temp.ASSIGNED_CHANNEL[user_id] = channel_id 

        temp.FILE_ID[id] = {"LAZY_FILE": base64_string}
        
        buttons = []
        for ch in temp.ASSIGNED_CHANNEL[user_id]:
            invite_link = await client.create_chat_invite_link(
                int(ch),
                creates_join_request=True
            )

            buttons.append([
                InlineKeyboardButton(
                    text=" • ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •",
                    url=invite_link.invite_link
                )
            ])  
        lazybuttons = InlineKeyboardMarkup(buttons)

        print(f"temp.FILE_ID[id] : {temp.FILE_ID[id]}")
        print(f"temp.ASSIGNED_CHANNEL : {temp.ASSIGNED_CHANNEL} ")
        lazymsg = await client.send_message(
            chat_id=message.from_user.id , 
            text=f"PLease unlock the file by joining this channel 👇", 
            reply_markup=lazybuttons
            )
        temp.LOCAL_MSG[id] = lazymsg  

        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('⚡️ ᴍᴏᴠɪᴇs', url='https://t.me/moviesimplyfytuber'),
                    InlineKeyboardButton('🍁 ᴄʀɪᴄᴋᴇᴛ ɴᴇᴡꜱ​​​​​', url='https://telegram.me/cricketediting')
                ],
                [
                    InlineKeyboardButton('🍿.  ꜰʀᴇᴇ ᴀᴘᴘꜱ​  .🚀', url='https://telegram.me/simplifytuberyt')
                ]
            ]
        )
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            disable_web_page_preview=True,
            quote=True
        )
        return


# @Bot.on_message(filters.private & filters.command(["broadcast", "users"]) & filters.user(ADMINS))  
# async def broadcast(c, m):
#     if m.text == "/users":
#         total_users = await Data.count_documents({})
#         return await m.reply(f"Total Users: {total_users}")
#     b_msg = m.reply_to_message
#     sts = await m.reply_text("Broadcasting your messages...")
#     users = Data.find({})
#     total_users = await Data.count_documents({})
#     done = 0
#     failed = 0
#     success = 0
#     start_time = time.time()
#     async for user in users:
#         user_id = int(user['id'])
#         try:
#             await b_msg.copy(chat_id=user_id)
#             success += 1
#         except FloodWait as e:
#             await asyncio.sleep(e.value)
#             await b_msg.copy(chat_id=user_id)
#             success += 1
#         except InputUserDeactivated:
#             await Data.delete_many({'id': user_id})
#             failed += 1
#         except UserIsBlocked:
#             failed += 1
#         except PeerIdInvalid:
#             await Data.delete_many({'id': user_id})
#             failed += 1
#         except Exception as e:
#             failed += 1
#         done += 1
#         if not done % 20:
#             await sts.edit(f"Broadcast in progress:\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nFailed: {failed}")    
#     time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
#     await sts.delete()
#     await m.reply_text(f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nFailed: {failed}", quote=True)


# @Bot.on_message(filters.private & (filters.document | filters.video | filters.audio) & ~filters.command(['start','users','broadcast','batch','genlink','stats']))
# async def channel_post(client: Client, message: Message):
#     # user = message.from_user
#     # if not await db.is_user_exist(user.id):
#     #     await db.add_user(user.id) 
#     id = message.from_user.id
    
#     if not await Data.find_one({'id': id}): await Data.insert_one({'id': id})


#     if (FORCE_SUB_CHANNEL or FORCE_SUB_CHANNEL2 or FORCE_SUB_CHANNEL3) and not await is_subscribed(client, message):
#         # User is not subscribed to any of the required channels, trigger force_sub logic
#         return await lazy_force_sub(client, message)

#     reply_text = await message.reply_text("Please Wait...!", quote = True)
#     try:
#         post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
#     except FloodWait as e:
#         await asyncio.sleep(e.x)
#         post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
#     except Exception as e:
#         print(e)
#         await reply_text.edit_text("Something went Wrong..!")
#         return
#     converted_id = post_message.id * abs(client.db_channel.id)
#     string = f"get-{converted_id}"
#     base64_string = await encode(string)
#     link = f"https://t.me/{client.username}?start={base64_string}"

#     reply_markup = InlineKeyboardMarkup([
#         [InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')],
#         [InlineKeyboardButton("🚀 Rename", callback_data='rename')]
#         ])

#     await reply_text.edit(f"<b>Here is your link</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview = True)

#     if not DISABLE_CHANNEL_BUTTON:
#         await post_message.edit_reply_markup(reply_markup)

# @Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
# async def new_post(client: Client, message: Message):

#     if DISABLE_CHANNEL_BUTTON:
#         return

#     converted_id = message.id * abs(client.db_channel.id)
#     string = f"get-{converted_id}"
#     base64_string = await encode(string)
#     link = f"https://t.me/{client.username}?start={base64_string}"
#     reply_markup = InlineKeyboardMarkup([
#         [InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')],
#         [InlineKeyboardButton("🚀 Rename", callback_data="rename")]
#         ])
#     try:
#         await message.edit_reply_markup(reply_markup)
#     except Exception as e:
#         print(e)
#         pass

         
# async def send_msg(user_id, message):
#     try:
#         await message.copy(chat_id=int(user_id))
#         return 200
#     except FloodWait as e:
#         await asyncio.sleep(e.value)
#         return send_msg(user_id, message)
#     except InputUserDeactivated:
#         logger.info(f"{user_id} : deactivated")
#         return 400
#     except UserIsBlocked:
#         logger.info(f"{user_id} : blocked the bot")
#         return 400
#     except PeerIdInvalid:
#         logger.info(f"{user_id} : user id invalid")
#         return 400
#     except Exception as e:
#         logger.error(f"{user_id} : {e}")
#         return 500
 

# Function to handle file deletion
async def delete_files(messages, client, k):
    await asyncio.sleep(FILE_AUTO_DELETE)  # Wait for the duration specified in config.py
    
    for msg in messages:
        try:
            await client.delete_messages(chat_id=msg.chat.id, message_ids=[msg.id])
        except Exception as e:
            print(f"The attempt to delete the media {msg.id} was unsuccessful: {e}")

    # Safeguard against k.command being None or having insufficient parts
    command_part = k.command[1] if k.command and len(k.command) > 1 else None

    if command_part:
        button_url = f"https://t.me/{client.username}?start={command_part}"
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("ɢᴇᴛ ғɪʟᴇ ᴀɢᴀɪɴ!", url=button_url)]
            ]
        )
    else:
        keyboard = None

    # Edit message with the button
    await k.edit_text("<b><i>Your Video / File Is Successfully Deleted ✅</i></b>", reply_markup=keyboard)
