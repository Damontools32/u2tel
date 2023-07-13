import os
import zipfile
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

def zip_directory(directory, zip_file):
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(directory):
            for file in files:
                if file != ".torrent.bolt.db":
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, directory))

@client.on(events.NewMessage(pattern='/send'))
async def upload_files(event):
    logger.debug('Received /send command')

    zip_file = 'downloads.zip'
    zip_directory(downloads_folder, zip_file)

    try:
        with open(zip_file, 'rb') as f:
            await client.send_file(event.chat_id, f, caption=zip_file)
    except Exception as e:
        await event.reply(f'Error uploading {zip_file}: {e}')
    finally:
        os.remove(zip_file)

client.run_until_disconnected()
