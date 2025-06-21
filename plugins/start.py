#(©)CodeXBotz

import os
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant
from bot import Bot
from helper_func import subscribed,decode, get_messages, delete_file
from database.database import add_user, del_user, full_userbase, present_user, get_force_sub_channels, add_force_sub_channel, remove_force_sub_channel, set_channel_join_request
from config import *

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    text = message.text
    if len(text)>7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start,end+1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply(
            f"<b> 𝗪𝗮𝗶𝘁 𝗕𝗵𝗮𝗶 🥺.. </b>"
            )
        
        try:
            messages = await get_messages(client, ids)
            
        except Exception as e:
            await temp_msg.edit(f"Something went wrong: {str(e)}")
            return
        await temp_msg.delete()

        codeflix_msgs = []
        
        for msg in messages:
            # Initialize filename and media_type with safe defaults
            filename = "Unknown"
            media_type = "Unknown"

            # Determine the media type and filename
            if msg.video:
                media_type = "Video"
                filename = msg.video.file_name if msg.video.file_name else "Unnamed Video"
            elif msg.document:
                filename = msg.document.file_name if msg.document.file_name else "Unnamed Document"
                media_type = "PDF" if filename.endswith(".pdf") else "Document"
            elif msg.photo:
                media_type = "Image"
                filename = "Image"
            elif msg.text:
                media_type = "Text"
                filename = "Text Content"

    # Generate caption
            caption = (
                CUSTOM_CAPTION.format(
                    previouscaption=(msg.caption.html if msg.caption else "𝗛𝗔𝗖𝗞𝗛𝗘𝗜𝗦𝗧 🔥"),
                    filename=filename,
                    mediatype=media_type,
                )
                if bool(CUSTOM_CAPTION)
                else (msg.caption.html if msg.caption else "")
            )

            reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None


            try:
                # Use protect_content=True for new format, PROTECT_CONTENT for old format
                protect_content = PROTECT_CONTENT
                copied_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=protect_content
                )
                await asyncio.sleep(0.5)
                codeflix_msgs.append(copied_msg)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                copied_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=protect_content
                )
                codeflix_msgs.append(copied_msg)
            except Exception as e:
                await message.reply_text(f"Error copying message: {str(e)}")
        
            await asyncio.sleep(0.4)

        if AUTO_DELETE_TIME > 0:
            notification_msg = await message.reply(
                f"<b>Tʜɪs Fɪʟᴇ ᴡɪʟʟ ʙᴇ Dᴇʟᴇᴛᴇᴅ ɪɴ  {get_exp_time(FILE_AUTO_DELETE)}"
                f"<blockquote><b>ʙᴜᴛ ᴅᴏɴ'ᴛ ᴡᴏʀʀʏ 😁 ᴀғᴛᴇʀ ᴅᴇʟᴇᴛᴇᴅ ʏᴏᴜ ᴄᴀɴ ᴀɢᴀɪɴ ᴀᴄᴄᴇss ᴛʜʀᴏᴜɢʜ ᴏᴜʀ ᴡᴇʙsɪᴛᴇs 😘</b></blockquote>"
                f"<b> <a href=https://yashyasag.github.io/hiddens_officials>🌟 𝗢𝗧𝗛𝗘𝗥 𝗪𝗘𝗕𝗦𝗜𝗧𝗘𝗦 🌟</a></b>"
            )

            await asyncio.sleep(AUTO_DELETE_TIME)

            for snt_msg in codeflix_msgs:    
                if snt_msg:
                    try:    
                        await snt_msg.delete()  
                    except Exception as e:
                        print(f"Error deleting message {snt_msg.id}: {e}")

            try:
                reload_url = (
                    "https://yashyasag.github.io/hiddens_officials"
                    if message.command and len(message.command) > 1
                    else None
                )
                keyboard = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("ɢᴇᴛ ғɪʟᴇ ᴀɢᴀɪɴ!", url=reload_url)]]
                ) if reload_url else None

                await notification_msg.edit(
                    "<blockquote><b>ʏᴏᴜʀ ʟᴇᴄᴛᴜʀᴇs / ᴘᴅғ ɪs  ᴅᴇʟᴇᴛᴇᴅ !!\n</b></blockquote>"
                    "<b>ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ᴅᴇʟᴇᴛᴇᴅ ʟᴇᴄᴛᴜʀᴇs / ᴘᴅғ 👇</b>\n\n"
                    "<b> <a href=https://yashyasag.github.io/hiddens_officials>🌟 𝗢𝗧𝗛𝗘𝗥 𝗪𝗘𝗕𝗦𝗜𝗧𝗘𝗦 🌟</a></b>",
                    reply_markup=keyboard
                )
            except Exception as e:
                print(f"Error updating notification with 'Get File Again' button: {e}")
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                    [InlineKeyboardButton("• 𝗠𝗔𝗜𝗡 𝗪𝗘𝗕𝗦𝗜𝗧𝗘 •", url="https://yashyasag.github.io/hiddens_officials")],

    [
                    InlineKeyboardButton("• ᴀʙᴏᴜᴛ", callback_data = "about"),
                    InlineKeyboardButton('ʜᴇʟᴘ •', callback_data = "help")

    ]
            ]
        )
        if START_PIC:  # Check if START_PIC has a value
            await message.reply_photo(
                photo=START_PIC,
                caption=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=None if not message.from_user.username else '@' + message.from_user.username,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                quote=True
            )
        else:  # If START_PIC is empty, send only the text
            await message.reply_text(
                text=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=None if not message.from_user.username else '@' + message.from_user.username,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                quote=True
            )
        return

    
#=====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""

#=====================================================================================##

@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    # Initialize buttons list
    buttons = []

    # Check if the first and second channels are both set
    if FORCE_SUB_CHANNEL1 and FORCE_SUB_CHANNEL2:
        buttons.append([
            InlineKeyboardButton(text="🌟𝗝𝗼𝗶𝗻 𝟭𝘀𝘁🌟", url=client.invitelink1),
            InlineKeyboardButton(text="👻𝗝𝗼𝗶𝗻 𝟮𝗻𝗱👻", url=client.invitelink2),
        ])
    # Check if only the first channel is set
    elif FORCE_SUB_CHANNEL1:
        buttons.append([
            InlineKeyboardButton(text="🌟𝗝𝗼𝗶𝗻 𝟭𝘀𝘁🌟", url=client.invitelink1)
        ])
    # Check if only the second channel is set
    elif FORCE_SUB_CHANNEL2:
        buttons.append([
            InlineKeyboardButton(text="👻𝗝𝗼𝗶𝗻 𝟮𝗻𝗱👻", url=client.invitelink2)
        ])

    # Check if the third and fourth channels are set
    if FORCE_SUB_CHANNEL3 and FORCE_SUB_CHANNEL4:
        buttons.append([
            InlineKeyboardButton(text="‼️𝗝𝗼𝗶𝗻 𝟯𝗿𝗱‼️", url=client.invitelink3),
            InlineKeyboardButton(text="‼️𝗝𝗼𝗶𝗻 𝟰𝘁𝗵‼️", url=client.invitelink4),
        ])
    # Check if only the first channel is set
    elif FORCE_SUB_CHANNEL3:
        buttons.append([
            InlineKeyboardButton(text="‼️𝗝𝗼𝗶𝗻 𝟯𝗿𝗱‼️", url=client.invitelink3)
        ])
    # Check if only the second channel is set
    elif FORCE_SUB_CHANNEL4:
        buttons.append([
            InlineKeyboardButton(text="‼️𝗝𝗼𝗶𝗻 𝟰𝘁𝗵‼️", url=client.invitelink4)
        ])

    # Append "Try Again" button if the command has a second argument
    try:
        buttons.append([
            InlineKeyboardButton(
                text="♻️ 𝐓𝐑𝐘 𝐀𝐆𝐀𝐈𝐍 ♻️",
                url=f"https://t.me/{client.username}?start={message.command[1]}"
            )
        ])
    except IndexError:
        pass  # Ignore if no second argument is present

    await message.reply_photo(
        photo=FORCE_PIC,
        caption=FORCE_MSG.format(
        first=message.from_user.first_name,
        last=message.from_user.last_name,
        username=None if not message.from_user.username else '@' + message.from_user.username,
        mention=message.from_user.mention,
        id=message.from_user.id
    ),
    reply_markup=InlineKeyboardMarkup(buttons)#,
    #message_effect_id=5104841245755180586  # Add the effect ID here
)

# Management commands
@Bot.on_message(filters.private & filters.command('addforcesub') & filters.user(ADMINS))
async def add_force_sub(client: Client, message: Message):
    try:
        parts = message.text.split(" : ", 1)
        if len(parts) != 2:
            raise IndexError
        name, channel_id = parts
        name = name.strip()[len("/addforcesub"):].strip()
        channel_id = channel_id.strip()
        if await add_force_sub_channel(name, channel_id):
            await message.reply(f"Added {name} ({channel_id}) to force-subscribe channels.")
        else:
            await message.reply(f"{channel_id} is already in the force-subscribe list.")
    except IndexError:
        await message.reply("Usage: /addforcesub : <name> : <channel_id_or_username>")
    except Exception as e:
        await message.reply(f"Error: {str(e)}")

@Bot.on_message(filters.private & filters.command('removeforcesub') & filters.user(ADMINS))
async def remove_force_sub(client: Client, message: Message):
    try:
        channel_id = message.command[1]
        if await remove_force_sub_channel(channel_id):
            await message.reply(f"Removed {channel_id} from force-subscribe channels.")
        else:
            await message.reply(f"{channel_id} is not in the force-subscribe list.")
    except IndexError:
        await message.reply("Usage: /removeforcesub <channel_id_or_username>")
    except Exception as e:
        await message.reply(f"Error: {str(e)}")

@Bot.on_message(filters.private & filters.command('setjoinrequest') & filters.user(ADMINS))
async def set_join_request(client: Client, message: Message):
    try:
        parts = message.text.split(" : ", 2)
        if len(parts) != 3:
            raise IndexError
        _, channel_id, value = parts
        channel_id = channel_id.strip()
        value = value.strip().lower() == "true"
        if await set_channel_join_request(channel_id, value):
            await message.reply(f"JOIN_REQUEST for {channel_id} set to {value}")
        else:
            await message.reply(f"{channel_id} is not in the force-subscribe list.")
    except IndexError:
        await message.reply("Usage: /setjoinrequest : <channel_id_or_username> : true|false")
    except Exception as e:
        await message.reply(f"Error: {str(e)}")

@Bot.on_message(filters.private & filters.command('listforcesub') & filters.user(ADMINS))
async def list_force_sub(client: Client, message: Message):
    channels = await get_force_sub_channels()
    if channels:
        channel_list = "\n".join([f"{i+1}. {ch['name']} ({ch['id']}, Join Request: {ch['join_request']})" for i, ch in enumerate(channels)])
        await message.reply(f"Force-subscribe channels:\n{channel_list}")
    else:
        await message.reply("No force-subscribe channels are set.")
    
@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()

