# (©)CodeXBotz
import pymongo, os
from config import DB_URI, DB_NAME

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]
user_data = database['users']
config_data = database['config']
join_requests = database['join_requests']  # Collection for join request tracking

# Existing user management functions
async def present_user(user_id: int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return

# Config management functions
async def get_config():
    config = config_data.find_one({'_id': 'bot_config'})
    if config is None:
        default_config = {
            '_id': 'bot_config',
            'FORCE_SUB_CHANNELS': []  # List of {id, name, join_request}
        }
        config_data.insert_one(default_config)
        return default_config
    return config

async def update_config(key: str, value):
    config_data.update_one(
        {'_id': 'bot_config'},
        {'$set': {key: value}},
        upsert=True
    )

async def add_force_sub_channel(name: str, channel_id: str):
    config = await get_config()
    channels = config.get('FORCE_SUB_CHANNELS', [])
    if not any(ch['id'] == channel_id for ch in channels):
        channels.append({'id': channel_id, 'name': name, 'join_request': False})
        await update_config('FORCE_SUB_CHANNELS', channels)
        return True
    return False

async def remove_force_sub_channel(channel_id: str):
    config = await get_config()
    channels = config.get('FORCE_SUB_CHANNELS', [])
    if any(ch['id'] == channel_id for ch in channels):
        channels = [ch for ch in channels if ch['id'] != channel_id]
        await update_config('FORCE_SUB_CHANNELS', channels)
        return True
    return False

async def set_channel_join_request(channel_id: str, value: bool):
    config = await get_config()
    channels = config.get('FORCE_SUB_CHANNELS', [])
    for ch in channels:
        if ch['id'] == channel_id:
            ch['join_request'] = value
            await update_config('FORCE_SUB_CHANNELS', channels)
            return True
    return False

async def get_force_sub_channels():
    config = await get_config()
    return config.get('FORCE_SUB_CHANNELS', [])

# Join request tracking functions
async def add_join_request(user_id: int, channel_id: str):
    join_requests.update_one(
        {'user_id': user_id, 'channel_id': channel_id},
        {'$set': {'status': 'pending'}},
        upsert=True
    )

async def has_pending_join_request(user_id: int, channel_id: str):
    request = join_requests.find_one({'user_id': user_id, 'channel_id': channel_id, 'status': 'pending'})
    return bool(request)

async def clear_join_request(user_id: int, channel_id: str):
    join_requests.delete_one({'user_id': user_id, 'channel_id': channel_id})
