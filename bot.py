from telethon import TelegramClient, events
import logging
import asyncio
import os
from dotenv import load_dotenv
from auth import perform_login

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")

client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

waiting_for_password = False
current_email = ""

@client.on(events.NewMessage(pattern='/login'))
async def login_handler(event):
    global waiting_for_password, current_email
    
    waiting_for_password = False
    current_email = ""
    await event.respond("Введите email:")

@client.on(events.NewMessage)
async def message_handler(event):
    global waiting_for_password, current_email
    
    if event.text.startswith('/'):
        return
    
    if waiting_for_password:
        password = event.text.strip()
        await event.respond("Выполняю вход...")
        
        result = await asyncio.get_event_loop().run_in_executor(
            None, 
            perform_login, 
            current_email, 
            password
        )

        if result:
            await event.respond("Вход выполнен успешно")
        else:
            await event.respond("Вход не удался")
        
        waiting_for_password = False
        current_email = ""
    
    elif '@' in event.text and '.' in event.text:
        current_email = event.text.strip()
        waiting_for_password = True
        await event.respond("Теперь введите пароль:")