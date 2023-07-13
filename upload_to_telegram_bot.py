import os
import logging
from telethon import TelegramClient, events

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_BOT_TOKEN'

downloads_folder = '/root/downloads'

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, _, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def get_target_folders(root_folder):
    target_folders = []
    for item in os.listdir(root_folder):
        item_path = os.path.join(root_folder, item)
        if os.path.isdir(item_path):
            target_folders.append(item_path)
    return target_folders

@client.on(events.NewMessage(pattern='/send'))
async def upload_files(event):
    logger.debug('Received /send command')

    target_folders = get_target_folders(downloads_folder)

    if target_folders:
        for target_folder in target_folders:
            folder_name = os.path.basename(target_folder)

            if get_folder_size(target_folder) > 2 * (1024 ** 3):  # Check if folder size is more than 2 GiB
                for root, _, files in os.walk(target_folder):
                    for file in files:
                        if file.lower().endswith('.rar'):
                            file_path = os.path.join(root, file)
                            try:
                                with open(file_path, 'rb') as f:
                                    await client.send_file(event.chat_id, f, caption=f'{folder_name}/{file}')
                            except Exception as e:
                                await event.reply(f'Error uploading {file}: {e}')
            else:
                await event.reply(f'Folder size of {folder_name} is less than 2 GiB.')

    else:
        await event.reply('No folder found in the downloads directory.')

client.run_until_disconnected()
