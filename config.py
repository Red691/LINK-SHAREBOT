from ast import pattern
import os
from os import environ
import logging
from logging.handlers import RotatingFileHandler

TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
BOT_USERNAME = 'REx'
APP_ID = int(os.environ.get("APP_ID", ""))
API_HASH = os.environ.get("API_HASH", "")
OWNER_ID = int(os.environ.get("OWNER_ID", ""))
PORT = os.environ.get("PORT", "8080")
DB_URL = os.environ.get("DB_URI", "")
DB_NAME = os.environ.get("DB_NAME", "RexBots")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "40"))
COMMAND_PHOTO = os.environ.get("COMMAND_PHOTO", "https://ibb.co/DHqBS4V7")  # Replace with your photo URL
START_PIC = os.environ.get("START_PIC", "https://ibb.co/CsPWqnR4")
START_MSG = os.environ.get("START_MESSAGE", "Hᴇʟʟᴏ {mention} ~\n\n <i><b><blockquote>Iᴀᴍ ᴀ ᴀᴅᴠᴀɴᴄᴇ ʟɪɴᴋ sʜᴀʀᴇ ʙᴏᴛ ᴛʜʀᴏᴜɢʜ ᴡʜɪᴄʜ ʏᴏᴜ ᴄᴀɴ ɢᴇᴛ ᴛʜᴇ ʟɪɴᴋs ᴏғ sᴘᴇᴄɪғɪᴄ ᴄʜᴀɴɴᴇʟs ᴡʜɪᴄʜ sᴀᴠᴇ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟs ғʀᴏᴍ ᴄᴏᴘʏʀɪɡʜᴛ.</blockquote></b></i>")
ABOUT_TXT = os.environ.get("HELP_MESSAGE", "<i><b><blockquote>◈ ᴄʀᴇᴀᴛᴏʀ: <a href=https://t.me/RexBots_Official>RexBots</a>\n◈ ꜰᴏᴜɴᴅᴇʀ ᴏꜰ : <a href=https://t.me/RexBots_Official>RexBOTS</a>\n◈ ᴅᴇᴠᴇʟᴏᴘᴇʀ: <a href='https://t.me/about_zani/117'>ZANI</a>\n◈ ᴅᴀᴛᴀʙᴀsᴇ: <a href='https://www.mongodb.com/docs/'>ᴍᴏɴɢᴏ ᴅʙ</a>\n» ᴅᴇᴠᴇʟᴏᴘᴇʀ: <a href='https://t.me/about_zani/179'>ZANI</a></blockquote></b></i>")
HELP_TXT =  os.environ.get("HELP_MESSAGE", "⁉️ Hᴇʟʟᴏ {mention} ~\n\n <b><blockquote expandable>➪ I ᴀᴍ ᴀ ᴘʀɪᴠᴀᴛᴇ ʟɪɴᴋ sʜᴀʀɪɴɢ ʙᴏᴛ, ᴍᴇᴀɴᴛ ᴛᴏ ᴘʀᴏᴠɪᴅᴇ ʟɪɴᴋ ғᴏʀ sᴘᴇᴄɪғɪᴄ ᴄʜᴀɴɴᴇʟs.\n\n ➪ Iɴ ᴏʀᴅᴇʀ ᴛᴏ ɢᴇᴛ ᴛʜᴇ ʟɪɴᴋs ʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ ᴊᴏɪɴ ᴛʜᴇ ᴀʟʟ ᴍᴇɴᴛɪᴏɴᴇᴅ ᴄʜᴀɴɴᴇʟ ᴛʜᴀᴛ ɪ ᴘʀᴏᴠɪᴅᴇ ʏᴏᴜ ᴛᴏ ᴊᴏɪɴ. Yᴏᴜ ᴄᴀɴ ɴᴏᴛ ᴀᴄᴄᴇss ᴏʀ ɢᴇᴛ ᴛʜᴇ ғɪʟᴇs ᴜɴʟᴇss ʏᴏᴜ ᴊᴏɪɴᴇᴅ ᴀʟʟ ᴄʜᴀɴɴᴇʟs.\n\n ‣ /help - Oᴘᴇɴ ᴛʜɪs ʜᴇʟᴘ ᴍᴇssᴀɢᴇ !</blockquote></b>")
FSUB_PIC = os.environ.get("FSUB_PIC", "https://ibb.co/DHqBS4V7")
FSUB_LINK_EXPIRY = 300
LOG_FILE_NAME = "Rexbots.txt"
DATABASE_CHANNEL = int(os.environ.get("DATABASE_CHANNEL", ""))

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
