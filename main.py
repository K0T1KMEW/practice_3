import logging
from bot import client

if __name__ == '__main__':
    logging.info("Бот запущен")
    client.run_until_disconnected()