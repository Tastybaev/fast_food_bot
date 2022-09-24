from telegram.ext import (
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
    ConversationHandler
)
from handlers import menu_message, start_message
from order import (
    order_adress,
    order_complete,
    order_name,
    order_payment,
    order_portion,
    order_start,
    order_stop,
)

from settings import TELEGRAM_TOKEN


def main():
    fast_food_bot = Updater(token=TELEGRAM_TOKEN)
    dp = fast_food_bot.dispatcher

    order = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("^(Заказать)$"), order_start)],
        states={
            'name': [MessageHandler(Filters.text, order_name)],
            'count_of_portions': [MessageHandler(Filters.text, order_portion)],
            'adress': [MessageHandler(Filters.text, order_adress)],
            'payment': [MessageHandler(Filters.text, order_payment)],
            'complete': [MessageHandler(Filters.text, order_complete)]
        },
        fallbacks=[
            MessageHandler(Filters.text, order_stop)
        ]
    )

    dp.add_handler(order)
    dp.add_handler(CommandHandler('start', start_message))
    dp.add_handler(MessageHandler(Filters.regex("^(Меню)$"), menu_message))
    fast_food_bot.start_polling(poll_interval=1.0)
    fast_food_bot.idle()


if __name__ == "__main__":
    main()
