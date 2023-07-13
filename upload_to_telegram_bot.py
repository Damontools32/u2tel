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

@client.on(events.NewMessage(pattern='/send'))
async def upload_files(event):
    logger.debug('Received /send command')
    for file_name in os.listdir(downloads_folder):
        if file_name == ".torrent.bolt.db":
            continue

        file_path = os.path.join(downloads_folder, file_name)

        if not os.path.isfile(file_path):
            await event.reply(f'Error: {file_name} is not a file.')
            continue

        try:
            with open(file_path, 'rb') as f:
                await client.send_file(event.chat_id, f, caption=file_name)
        except IsADirectoryError as e:
            await event.reply(f'Error uploading {file_name}: {e}')
        except Exception as e:
            await event.reply(f'Error uploading {file_name}: {e}')

client.run_until_disconnected()
