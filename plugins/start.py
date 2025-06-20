#(©)CodeXBotz

import os
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant
from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, START_PIC, AUTO_DELETE_TIME, AUTO_DELETE_MSG, JOIN_REQUEST_ENABLE,FORCE_SUB_CHANNEL
from helper_func import subscribed,decode, get_messages, delete_file
from database.database import add_user, del_user, full_userbase, present_user, get_force_sub_channels, add_force_sub_channel, remove_force_sub_channel, set_channel_join_request


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
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()

        track_msgs = []

        for msg in messages:

            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption = "" if not msg.caption else msg.caption.html, filename = msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            if AUTO_DELETE_TIME and AUTO_DELETE_TIME > 0:

                try:
                    copied_msg_for_deletion = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    if copied_msg_for_deletion:
                        track_msgs.append(copied_msg_for_deletion)
                    else:
                        print("Failed to copy message, skipping.")

                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    copied_msg_for_deletion = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    if copied_msg_for_deletion:
                        track_msgs.append(copied_msg_for_deletion)
                    else:
                        print("Failed to copy message after retry, skipping.")

                except Exception as e:
                    print(f"Error copying message: {e}")
                    pass

            else:
                try:
                    await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    await asyncio.sleep(0.5)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                except:
                    pass

        if track_msgs:
            delete_data = await client.send_message(
                chat_id=message.from_user.id,
                text=AUTO_DELETE_MSG.format(time=AUTO_DELETE_TIME)
            )
            # Schedule the file deletion task after all messages have been copied
            asyncio.create_task(delete_file(track_msgs, client, delete_data))
        else:
            print("No messages to track for deletion.")

        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("😊 About Me", callback_data = "about"),
                    InlineKeyboardButton("🔒 Close", callback_data = "close")
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
    FORCE_SUB_CHANNELS = await get_force_sub_channels()

    if not FORCE_SUB_CHANNELS:
        await message.reply("No force-subscribe channels are set!")
        return

    buttons = []
    not_joined_channels = []

    # Check membership for each channel
    for channel in FORCE_SUB_CHANNELS:
        try:
            member = await client.get_chat_member(chat_id=channel['id'], user_id=message.from_user.id)
            if member.status not in ["owner", "administrator", "member"]:
                not_joined_channels.append(channel)
        except Exception:
            not_joined_channels.append(channel)  # Assume not joined if error occurs

    # Generate invite links for unjoined channels
    if not_joined_channels:
        for channel in not_joined_channels:
            try:
                if channel['join_request']:
                    invite = await client.create_chat_invite_link(
                        chat_id=channel['id'],
                        creates_join_request=True
                    )
                    ButtonUrl = invite.invite_link
                else:
                    try:
                        # Try to get chat to check if it's a username
                        chat = await client.get_chat(channel['id'])
                        ButtonUrl = chat.invite_link
                        if not ButtonUrl:
                            # Fallback for channels without invite links
                            ButtonUrl = f"https://t.me/c/{str(channel['id']).replace('-100', '')}/1"
                    except UsernameInvalid:
                        # Handle numeric IDs directly
                        ButtonUrl = f"https://t.me/c/{str(channel['id']).replace('-100', '')}/1"
                    except ChatAdminRequired:
                        await message.reply(f"Cannot generate invite link for {channel['name']} ({channel['id']}): Bot lacks admin permissions.")
                        continue
                buttons.append(
                    InlineKeyboardButton(
                        text=f"Join {channel['name']}",
                        url=ButtonUrl
                    )
                )
            except Exception as e:
                await message.reply(f"Error generating invite link for {channel['name']} ({channel['id']}): {str(e)}")
                continue

        if not buttons:
            await message.reply("Unable to generate invite links for any channels. Please contact the admin.")
            return

        # Organize buttons in rows of two
        button_rows = [buttons[i:i+2] for i in range(0, len(buttons), 2)]

        try:
            button_rows.append(
                [
                    InlineKeyboardButton(
                        text="Try Again",
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
            reply_markup=InlineKeyboardMarkup(button_rows),
            quote=True,
            disable_web_page_preview=True
        )

# Management commands
@Bot.on_message(filters.command('addforcesub') & filters.user("YOUR_ADMIN_ID"))
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

@Bot.on_message(filters.command('removeforcesub') & filters.user("YOUR_ADMIN_ID"))
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

@Bot.on_message(filters.command('setjoinrequest') & filters.user("YOUR_ADMIN_ID"))
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

@Bot.on_message(filters.command('listforcesub') & filters.user("YOUR_ADMIN_ID"))
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

