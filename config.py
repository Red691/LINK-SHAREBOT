from ast import pattern
import os
from os import environ
import logging
from logging.handlers import RotatingFileHandler

TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "7280187591:AAE-Lh16r1noxlMGeRn0y7SYhj3XjkT6NOs")
BOT_USERNAME = 'New_Movie_filter_bot'
APP_ID = int(os.environ.get("APP_ID", "20594537"))
API_HASH = os.environ.get("API_HASH", "c505a4e5bb7d482197875888af544f17")
OWNER_ID = int(os.environ.get("OWNER_ID", "5770911041"))
PORT = os.environ.get("PORT", "8080")
DB_URL = os.environ.get("DB_URI", "mongodb+srv://reelcraft99:reelcraft999@cluster0.f0sv73o.mongodb.net/?appName=Cluster0")
DB_NAME = os.environ.get("DB_NAME", "Sensei_links")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "40"))
COMMAND_PHOTO = os.environ.get("COMMAND_PHOTO", "http://ibb.co/TDy4j0Zm")  # Replace with your photo URL
START_PIC = os.environ.get("START_PIC", "https://files.catbox.moe/c5dtav.jpg")
START_MSG = os.environ.get("START_MESSAGE", "Hᴇʟʟᴏ {mention} ~\n\n <i><b><blockquote>Iᴀᴍ ᴀ ᴀᴅᴠᴀɴᴄᴇ ʟɪɴᴋ sʜᴀʀᴇ ʙᴏᴛ ᴛʜʀᴏᴜɢʜ ᴡʜɪᴄʜ ʏᴏᴜ ᴄᴀɴ ɢᴇᴛ ᴛʜᴇ ʟɪɴᴋs ᴏғ sᴘᴇᴄɪғɪᴄ ᴄʜᴀɴɴᴇʟs ᴡʜɪᴄʜ sᴀᴠᴇ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟs ғʀᴏᴍ ᴄᴏᴘʏʀɪɡʜᴛ.</blockquote></b></i>")
ABOUT_TXT = os.environ.get("HELP_MESSAGE", "<i><b><blockquote>◈ ᴄʀᴇᴀᴛᴏʀ: <a href=https://t.me/Noting_else_bro>Nᴏᴛʜɪɴɢ 😑</a>\n◈ ꜰᴏᴜɴᴅᴇʀ ᴏꜰ : <a href=https://t.me/RexBots_Official>Nᴏᴛʜɪɴɢ 😑</a>\n◈ Cʜᴀɴɴᴇʟ: <a href='https://t.me/Anime_sensei_official'>Aɴɪᴍᴇ ᴄʜᴀɴɴᴇʟ</a>\n◈ ᴅᴀᴛᴀʙᴀsᴇ: <a href='https://www.mongodb.com/docs/'>ᴍᴏɴɢᴏ ᴅʙ</a>\n» Rᴇᴘᴏ ʟɪɴᴋ: <a href='https://t.me/Promotion_wala'>Click Here</a></blockquote></b></i>")
HELP_TXT =  os.environ.get("HELP_MESSAGE", "⁉️ Hᴇʟʟᴏ {mention} ~\n\n <b><blockquote expandable>➪ I ᴀᴍ ᴀ ᴘʀɪᴠᴀᴛᴇ ʟɪɴᴋ sʜᴀʀɪɴɢ ʙᴏᴛ, ᴍᴇᴀɴᴛ ᴛᴏ ᴘʀᴏᴠɪᴅᴇ ʟɪɴᴋ ғᴏʀ sᴘᴇᴄɪғɪᴄ ᴄʜᴀɴɴᴇʟs.\n\n ➪ Iɴ ᴏʀᴅᴇʀ ᴛᴏ ɢᴇᴛ ᴛʜᴇ ʟɪɴᴋs ʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ ᴊᴏɪɴ ᴛʜᴇ ᴀʟʟ ᴍᴇɴᴛɪᴏɴᴇᴅ ᴄʜᴀɴɴᴇʟ ᴛʜᴀᴛ ɪ ᴘʀᴏᴠɪᴅᴇ ʏᴏᴜ ᴛᴏ ᴊᴏɪɴ. Yᴏᴜ ᴄᴀɴ ɴᴏᴛ ᴀᴄᴄᴇss ᴏʀ ɢᴇᴛ ᴛʜᴇ ғɪʟᴇs ᴜɴʟᴇss ʏᴏᴜ ᴊᴏɪɴᴇᴅ ᴀʟʟ ᴄʜᴀɴɴᴇʟs.\n\n!</blockquote></b>")
FSUB_PIC = os.environ.get("FSUB_PIC", "https://ibb.co/DHqBS4V7")
FSUB_LINK_EXPIRY = 300
LOG_FILE_NAME = "Rexbots.txt"
DATABASE_CHANNEL = int(os.environ.get("DATABASE_CHANNEL", "-1003642299475"))

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
