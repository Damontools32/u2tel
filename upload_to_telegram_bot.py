import os
import glob
from telethon import TelegramClient, events

TELEGRAM_API_ID = 'YOUR_TELEGRAM_API_ID'
TELEGRAM_API_HASH = 'YOUR_TELEGRAM_API_HASH'
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
DOWNLOADS_DIR = '/root/downloads/'

client = TelegramClient('bot', api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH).start(bot_token=TELEGRAM_BOT_TOKEN)

@client.on(events.NewMessage(pattern='/upload'))
async def upload_files(event):
    sender_id = event.sender_id
    files = glob.glob(os.path.join(DOWNLOADS_DIR, '*'))
    for file_path in files:
        try:
            with open(file_path, 'rb') as f:
                file_name = os.path.basename(file_path)
                await event.reply(f'Uploading {file_name}...')
                await client.send_file(sender_id, f, caption=file_name)
                await event.reply(f'{file_name} uploaded successfully.')
        except Exception as e:
            await event.reply(f'Error uploading {file_name}: {e}')

client.run_until_disconnected()￼Enter
