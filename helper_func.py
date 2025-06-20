#(©)Codexbotz

import base64
import re
import asyncio
import logging 
from pyrogram.enums import ChatMemberStatus
from config import FORCE_SUB_CHANNEL, ADMINS, AUTO_DELETE_TIME, AUTO_DEL_SUCCESS_MSG
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait
from pyrogram import Client, filters
from database.database import add_force_sub_channel, remove_force_sub_channel, set_channel_join_request, get_force_sub_channels

# is_subscribed (unchanged)
async def is_subscribed(filter, client: Client, update):
    FORCE_SUB_CHANNELS = await get_force_sub_channels()
    
    if not FORCE_SUB_CHANNELS:
        return True
    
    user_id = update.from_user.id
    if user_id in ADMINS:
        return True
    
    for channel in FORCE_SUB_CHANNELS:
        try:
            member = await client.get_chat_member(chat_id=channel['id'], user_id=user_id)
            if member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
                return False
        except UserNotParticipant:
            return False
        except Exception as e:
            print(f"Error checking membership for {channel['id']}: {str(e)}")
            return False
    
    return True

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
async def encode(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    base64_string = (base64_bytes.decode("ascii")).strip("=")
    return base64_string

async def decode(base64_string):
    base64_string = base64_string.strip("=") # links generated before this commit will be having = sign, hence striping them to handle padding errors.
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    string_bytes = base64.urlsafe_b64decode(base64_bytes) 
    string = string_bytes.decode("ascii")
    return string

async def get_messages(client, message_ids):
    messages = []
    total_messages = 0
    while total_messages != len(message_ids):
        temb_ids = message_ids[total_messages:total_messages+200]
        try:
            msgs = await client.get_messages(
                chat_id=client.db_channel.id,
                message_ids=temb_ids
            )
        except FloodWait as e:
            await asyncio.sleep(e.x)
            msgs = await client.get_messages(
                chat_id=client.db_channel.id,
                message_ids=temb_ids
            )
        except:
            pass
        total_messages += len(temb_ids)
        messages.extend(msgs)
    return messages

async def get_message_id(client, message):
    if message.forward_from_chat:
        if message.forward_from_chat.id == client.db_channel.id:
            return message.forward_from_message_id
        else:
            return 0
    elif message.forward_sender_name:
        return 0
    elif message.text:
        pattern = "https://t.me/(?:c/)?(.*)/(\d+)"
        matches = re.match(pattern,message.text)
        if not matches:
            return 0
        channel_id = matches.group(1)
        msg_id = int(matches.group(2))
        if channel_id.isdigit():
            if f"-100{channel_id}" == str(client.db_channel.id):
                return msg_id
        else:
            if channel_id == client.db_channel.username:
                return msg_id
    else:
        return 0

def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += f"{time_list.pop()}, "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time

async def delete_file(messages, client, process):
    await asyncio.sleep(AUTO_DELETE_TIME)
    for msg in messages:
        try:
            await client.delete_messages(chat_id=msg.chat.id, message_ids=[msg.id])
        except Exception as e:
            await asyncio.sleep(e.x)
            print(f"The attempt to delete the media {msg.id} was unsuccessful: {e}")

    await process.edit_text(AUTO_DEL_SUCCESS_MSG)


subscribed = filters.create(is_subscribed)
