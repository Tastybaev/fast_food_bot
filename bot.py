import logging
from telegram.ext import (
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
    ConversationHandler,
    CallbackQueryHandler
)
from old_handlers import menu_message
from keyboard import(
    start,
    start_over,
    hot_dishes,
    soup,
    pizza,
    drinks,
    end
)

from settings import TELEGRAM_TOKEN
from settings import(
    FIRST,
    SECOND,
    HOT_DISHES,
    SOUP,
    PIZZA,
    DRINKS
)

logging.basicConfig(filename='bot.log', level=logging.INFO)
def main():
    fast_food_bot = Updater(token=TELEGRAM_TOKEN)
    dp = fast_food_bot.dispatcher

    # order = ConversationHandler(
    #     entry_points=[MessageHandler(Filters.regex("^(Заказать)$"), order_start)],
    #     states={
    #         'name': [MessageHandler(Filters.text, order_name)],
    #         'count_of_portions': [MessageHandler(Filters.text, order_portion)],
    #         'adress': [MessageHandler(Filters.text, order_adress)],
    #         'payment': [MessageHandler(Filters.text, order_payment)],
    #         'complete': [MessageHandler(Filters.text, order_complete)]
    #     },
    #     fallbacks=[
    #         MessageHandler(Filters.text, order_stop)
    #     ]
    # )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={ # словарь состояний разговора, возвращаемых callback функциями
            FIRST: [
                CallbackQueryHandler(hot_dishes, pattern='^' + str(HOT_DISHES) + '$'),
                CallbackQueryHandler(soup, pattern='^' + str(SOUP) + '$'),
                CallbackQueryHandler(pizza, pattern='^' + str(PIZZA) + '$'),
                CallbackQueryHandler(drinks, pattern='^' + str(DRINKS) + '$'),
            ],
            SECOND: [
                CallbackQueryHandler(start_over, pattern='^' + str(HOT_DISHES) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(SOUP) + '$'),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )


    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.regex("^(Меню)$"), menu_message))

    logging.info('BOT IS STARTED!')
    fast_food_bot.start_polling(poll_interval=1.0)
    fast_food_bot.idle()


if __name__ == "__main__":
    main()
