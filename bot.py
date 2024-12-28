# bot.py

import time
import handlers
from config import BOT_TOKEN
from telebot import TeleBot, apihelper

if __name__ == '__main__':
    bot = TeleBot(BOT_TOKEN)

    while True:
        try:
            handlers.bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Ошибка во время работы бота: {e}")

