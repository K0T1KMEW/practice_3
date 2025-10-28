from telethon import TelegramClient, events
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import logging
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")

client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

def check_login_success(driver):
    try:
        current_url = driver.current_url
        if "clientarea" in current_url and "dashboard" in current_url:
            return True
        
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "ddCredit"))
        )
        return True
    except:
        return False

def perform_login(email, password):
    driver = None
    try:
        logging.info("Запуск браузера...")
        firefox_options = Options()
        firefox_options.page_load_strategy = 'eager'

        driver = webdriver.Firefox(options=firefox_options)
        url = "https://secure.veesp.com/clientarea"
        driver.get(url)

        wait = WebDriverWait(driver, 10)

        email_form = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        email_form.send_keys(email)
        logging.info("Введена почта")

        passwd_form = driver.find_element(By.NAME, "password")
        passwd_form.send_keys(password)
        logging.info("Введен пароль")

        enter_button = driver.find_element(By.XPATH, '//button[text()="Вход"]')
        enter_button.click()
        logging.info("Кнопка входа нажата")

        success = check_login_success(driver)
        logging.info(f"Результат входа: {'Успешно' if success else 'Неудачно'}")

        return success
    except Exception as e:
        logging.error(f"Ошибка при выполнении входа: {e}")
        return False
    finally:
        if driver:
            driver.quit()
            logging.info("Браузер закрыт")

@client.on(events.NewMessage)
async def message_handler(event):
    if event.out:
        return
        
    text = event.text.strip()
    
    if text.startswith('/login'):
        parts = text.split()
        if len(parts) < 3:
            await event.respond("Использование: /login email password")
            return
            
        email = parts[1]
        password = parts[2]
        
        await event.respond("Выполнение входа...")
        
        result = await asyncio.get_event_loop().run_in_executor(
            None, 
            perform_login, 
            email, 
            password
        )

        if result:
            await event.respond("Вход выполнен успешно")
        else:
            await event.respond("Вход не удался")

if __name__ == '__main__':
    logging.info("Бот запущен")
    client.run_until_disconnected()