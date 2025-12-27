from pyrogram import Client, filters, enums
from pyrogram.types import ChatJoinRequest
from database.database import db
from config import * 
import logging
import asyncio
from pyrogram.enums import ParseMode
#5 => verification_steps ! [Youtube@LazyDeveloperr]
logger = logging.getLogger(__name__)
from utils import temp 
from helper_func import decode, get_messages
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_chat_join_request() # Fetch channels dynamically
async def join_reqs(client, message):
    try:
        channel_id = message.chat.id
        user_id = message.from_user.id

        # user ke assigned channels hi check karo
        assigned = temp.ASSIGNED_CHANNEL.get(user_id)
        if not assigned:
            return

        # ✅ save join in DB
        await db.save_user_join(user_id, channel_id)

        # get all joined channels
        joined_channels = await db.get_user_joins(user_id)

        # 🔍 check if all assigned channels joined
        if set(assigned).issubset(set(joined_channels)):  
            file_id = temp.FILE_ID[user_id]["LAZY_FILE"]
            print(f"file id in req  = {file_id}")
            # print(f"base64_string on start : {base64_string}")
            string = await decode(file_id)
            argument = string.split("-")
            ids = []
            if len(argument) == 3:
                try:
                    start = int(int(argument[1]) / abs(client.db_channel.id))
                    end = int(int(argument[2]) / abs(client.db_channel.id))
                    ids = range(start, end + 1) if start <= end else list(range(start, end - 1, -1))
                except Exception as e:
                    print(f"Error decoding IDs: {e}")
                    return

            elif len(argument) == 2:
                try:
                    ids = [int(int(argument[1]) / abs(client.db_channel.id))]
                except Exception as e:
                    print(f"Error decoding ID: {e}")
                    return

            temp_msg = await client.send_message(
                user_id,
                "⏳ Wait a sec, preparing your file..."
            )
            print(f"ids -=> {ids}")
            try:
                messages = await get_messages(client, ids)
            except Exception as e:
                print(f"Error getting messages: {e}")
                return
            finally:
                await temp_msg.delete()

            lazy_msgs = []  # List to keep track of sent messages

            for msg in messages:
                caption = (CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, 
                                                filename=msg.document.file_name) if bool(CUSTOM_CAPTION) and bool(msg.document)
                        else ("" if not msg.caption else msg.caption.html))

                reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None

                try:
                    copied_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, 
                                                reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    lazy_msgs.append(copied_msg)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    copied_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, 
                                                reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    lazy_msgs.append(copied_msg)
                except Exception as e:
                    print(f"Failed to send message: {e}")
                    pass

            k = await client.send_message(chat_id=message.from_user.id, 
                                        text=f"<b><i>This File is deleting automatically in {FILE_AUTO_DELETE}. Forward in your Saved Messages..!</i></b>")

            # 🧼 CLEANUP
            temp.ASSIGNED_CHANNEL.pop(user_id, None)
            temp.FILE_ID.pop(user_id, None)
            temp.LOCAL_MSG.pop(user_id, None)
            # Schedule the file deletion
            asyncio.create_task(delete_files(lazy_msgs, client, k))
    except Exception as lazydeveloper:
        logging.info(f"Error: {lazydeveloper}")


@Client.on_message(filters.command("delreq") & filters.private & filters.user(ADMINS))
async def del_requests(client, message):
    await db.del_join_req()    
    await message.reply("<b>⚙ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ᴄʜᴀɴɴᴇʟ ʟᴇғᴛ ᴜꜱᴇʀꜱ ᴅᴇʟᴇᴛᴇᴅ</b>")

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

@Client.on_message(filters.command("reset_locked") & filters.private)
async def reset_locked_files(client, message):
    # Only admin allowed
    if message.from_user.id not in ADMINS:
        return await message.reply("❌ You are not authorized to use this command.")

    # Delete all locked records
    result = await db.locked_files.delete_many({})

    # Reset temp memory
    temp.FILE_ID.clear()
    temp.ASSIGNED_CHANNEL.clear()

    await message.reply(
        f"✅ All locked files have been reset.\n"
        f"🗑 Deleted entries: {result.deleted_count}"
    )
