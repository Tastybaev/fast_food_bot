from unicodedata import name
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from handlers import start_message

from settings import TELEGRAM_TOKEN

import telegram


def main():
    fast_food_bot = Updater(token=TELEGRAM_TOKEN)
    dp = fast_food_bot.dispatcher

    dp.add_handler(CommandHandler('start', start_message))

    fast_food_bot.start_polling(poll_interval=1.0)
    fast_food_bot.idle() 


if __name__ == "__main__":
    main()
