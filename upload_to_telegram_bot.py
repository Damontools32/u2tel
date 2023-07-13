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

def get_all_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file != ".torrent.bolt.db":
                yield os.path.join(root, file)

@client.on(events.NewMessage(pattern='/send'))
async def upload_files(event):
    logger.debug('Received /send command')
    for file_path in get_all_files(downloads_folder):
        file_name = os.path.basename(file_path)

        try:
            with open(file_path, 'rb') as f:
                await client.send_file(event.chat_id, f, caption=file_name)
        except IsADirectoryError as e:
            await event.reply(f'Error uploading {file_name}: {e}')
        except Exception as e:
            await event.reply(f'Error uploading {file_name}: {e}')

client.run_until_disconnected()
