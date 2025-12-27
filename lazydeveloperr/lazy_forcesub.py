from pyrogram.errors import ChatAdminRequired
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client,  __version__, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import ChatAdminRequired,UserNotParticipant
from config import *
logger = logging.getLogger(__name__)

async def lazy_channel_user(client: Client, user_id: int):
    required_channels = [FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL2, FORCE_SUB_CHANNEL3]
    for channel in required_channels:
        try:
            # Check if the user is a member of the channel
            member = await client.get_chat_member(channel, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except Exception:
            return False
    return True

async def is_subscribed(bot, query):
    required_channels = [FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL2, FORCE_SUB_CHANNEL3]
    for channels in required_channels:
        try:
            user = await bot.get_chat_member(channels, query.from_user.id)
        except UserNotParticipant:
            pass
        except Exception as e:
            logger.exception(e)
        else:
            if user.status != enums.ChatMemberStatus.BANNED:
                return True
    return False

async def lazy_force_sub(client: Client, message: Message):
    try:
        invite_link = await client.create_chat_invite_link(int(FORCE_SUB_CHANNEL), creates_join_request=True)
        invite_link2 = await client.create_chat_invite_link(int(FORCE_SUB_CHANNEL2), creates_join_request=True)
        invite_link3 = await client.create_chat_invite_link(int(FORCE_SUB_CHANNEL3), creates_join_request=True)
    except ChatAdminRequired:
        logger.error("Hey Sona, Ek dfa check kr lo ki auth Channel mei Add hu ya nhi...!")
        return
    buttons = [
        
            [InlineKeyboardButton(text="📌ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ1", url=invite_link.invite_link)],
            [InlineKeyboardButton(text="📌ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ2", url=invite_link2.invite_link)],
            [InlineKeyboardButton(text="📌ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ3", url=invite_link3.invite_link)],
        
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text='↺ʀᴇʟᴏᴀᴅ',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )

# # Using the channel_user check and force_sub call
# @Bot.on_message(filters.command("start"))
# async def start_handler(client: Client, message: Message):
#     if not await channel_user(client, message.from_user.id):
#         return await force_sub(client, message)
#     # Proceed with the rest of the command if user is a member
#     await message.reply("Welcome! You have access to this bot.")
