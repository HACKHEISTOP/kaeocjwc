#(©)CodeXBotz

import os
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

load_dotenv()

#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "7931405874:AAGodglFGX3zOG49z5dxMff_GpaNLgxZ9OE")
APP_ID = int(os.environ.get("APP_ID", "23713783")) #Your API ID from my.telegram.org
API_HASH = os.environ.get("API_HASH", "2daa157943cb2d76d149c4de0b036a99") #Your API Hash from my.telegram.org
#Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002493255368")) #Your db channel Id
OWNER_ID = int(os.environ.get("OWNER_ID", "5487643307")) # Owner id
#--------------------------------------------
PORT = os.environ.get("PORT", "8080")

#Database 
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://namanjain123eudhc:opmaster@cluster0.5iokvxo.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", "Cluster0")

#force sub channel id, if you want enable force sub
FORCE_SUB_CHANNEL1 = int(os.environ.get("FORCE_SUB_CHANNEL1", "-1002215102799"))
#put 0 to disable
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "0"))#put 0 to disable
FORCE_SUB_CHANNEL3 = int(os.environ.get("FORCE_SUB_CHANNEL3", "0"))#put 0 to disable
FORCE_SUB_CHANNEL4 = int(os.environ.get("FORCE_SUB_CHANNEL4", "0"))#put 0 to disable

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

#start message
START_PIC = os.environ.get("START_PIC", "https://i.ibb.co/PV7wZVd/x.jpg")
HELP_TXT = "<b><blockquote>ᴛʜɪs ɪs ᴀɴ ʟᴇᴄᴛᴜʀᴇ ʙᴏᴛ ᴡᴏʀᴋ ғᴏʀ ʜᴀᴄᴋʜᴇɪsᴛ\n\n❏ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs\n├/start : sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ\n├/about : ᴏᴜʀ Iɴғᴏʀᴍᴀᴛɪᴏɴ\n└/help : ʜᴇʟᴘ ʀᴇʟᴀᴛᴇᴅ ʙᴏᴛ\n\n sɪᴍᴘʟʏ ᴄʟɪᴄᴋ ᴏɴ ʟɪɴᴋ ᴀɴᴅ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ᴊᴏɪɴ ʙᴏᴛʜ ᴄʜᴀɴɴᴇʟs ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ᴛʜᴀᴛs ɪᴛ.....!\n\n ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ <a href=https://t.me/TEAM_OPTECH>𝗛𝗔𝗖𝗞𝗛𝗘𝗜𝗦𝗧</a></blockquote></b>"
ABOUT_TXT = "<b><blockquote>◈ ᴄʀᴇᴀᴛᴏʀ: <a href=https://t.me/HACKHEISTBOT>HACKHEIST</a>\n◈ ꜰᴏᴜɴᴅᴇʀ ᴏꜰ : <a href=https://yashyasag.github.io/hiddens_officials>𝗛𝗔𝗖𝗞𝗛𝗘𝗜𝗦𝗧 𝗪𝗘𝗕</a>\n◈ ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href=https://t.me/HACKHEISTBOT>HACKHEIST</a></blockquote></b>"
#--------------------------------------------
#--------------------------------------------
START_MSG = os.environ.get("START_MESSAGE", "<b>ʜᴇʟʟᴏ {first}\n\n<blockquote> ɪ ᴀᴍ ʟᴇᴄᴛᴜʀᴇ ᴘʀᴏᴠɪᴅᴇʀ ʙᴏᴛ, ɪ ᴄᴀɴ ᴘʀᴏᴠɪᴅᴇ ᴀʟʟ ʟᴇᴄᴛᴜʀᴇs 😈 ᴀɴᴅ ᴘᴅғs 😁</blockquote></b>")
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "ʜᴇʟʟᴏ {first}\n\n<b>ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ᴀɴᴅ ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ʀᴇʟᴏᴀᴅ button ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛᴇᴅ ʟᴇᴄᴛᴜʀᴇs/ᴘᴅғs</b>")

CMD_TXT = "<blockquote><b>HACKHEIST</b></blockquote>"
#--------------------------------------------
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", """<b>{previouscaption}</b>\n<b>━━━━━━━━━━━━━━━━━◇</b>\n<b>⛧ 🄱🅈 :-) </b><b><a href="https://yashyasag.github.io/hiddens">ℍ𝔸ℂ𝕂ℍ𝔼𝕀𝕊𝕋 😈</a></b> <b>♛</b>\n<b>━━━━━━━━━━━━━━━━━◇</b>\n<b>🙏 sʜᴀʀᴇ ᴀɴᴅ sᴜᴘᴘᴏʀᴛ ᴜs 👇</b>\n<b>—————————————————</b>\n<b><a href="https://yashyasag.github.io/hiddens">🚀 𝗠𝗢𝗥𝗘 𝗪𝗘𝗕𝗦𝗜𝗧𝗘𝗦 🌟</a></b>\n<b>—————————————————</b>""")
try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#Force sub message 

#set your Custom Caption here, Keep None for Disable Custom Caption
#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

# Auto delete time in seconds.
AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", "0"))
AUTO_DELETE_MSG = os.environ.get("AUTO_DELETE_MSG", "This file will be automatically deleted in {time} seconds. Please ensure you have saved any necessary content before this time.")
AUTO_DEL_SUCCESS_MSG = os.environ.get("AUTO_DEL_SUCCESS_MSG", "Your file has been successfully deleted. Thank you for using our service. ✅")

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌Don't send me messages directly I'm only File Share bot!"

ADMINS.append(OWNER_ID)
ADMINS.append(1250450587)

LOG_FILE_NAME = "filesharingbot.txt"

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
