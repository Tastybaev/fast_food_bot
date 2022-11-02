import logging
from telegram.ext import (
    CommandHandler,
    Updater,
    ConversationHandler,
    CallbackQueryHandler
)

from keyboard import Main

from settings import ADD_TO_SHOPPING_CART, BACK, TELEGRAM_TOKEN, THIRD
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
    roots = Main()
    fast_food_bot = Updater(token=TELEGRAM_TOKEN)
    dp = fast_food_bot.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', roots.start)],
        states={ # словарь состояний разговора, возвращаемых callback функциями
            FIRST: [
                CallbackQueryHandler(roots.hot_dishes, pattern='^' + str(HOT_DISHES) + '$'),
                CallbackQueryHandler(roots.soup, pattern='^' + str(SOUP) + '$'),
                CallbackQueryHandler(roots.pizza, pattern='^' + str(PIZZA) + '$'),
                CallbackQueryHandler(roots.drinks, pattern='^' + str(DRINKS) + '$')
            ],
            SECOND: [
                CallbackQueryHandler(roots.add_to_shopping_cart, pattern='^' + str(ADD_TO_SHOPPING_CART) + '$'),
                CallbackQueryHandler(roots.start_over, pattern='^' + str(BACK) + '$'),
            ],
            THIRD: [
                CallbackQueryHandler(roots.start_over, pattern='^' + str(BACK) + '$'),
                CallbackQueryHandler(roots.end, pattern='^' + str(SOUP) + '$'),
            ],
        },
        fallbacks=[CommandHandler('start', roots.start)],
    )


    dp.add_handler(conv_handler)

    logging.info('BOT IS STARTED!')
    fast_food_bot.start_polling(poll_interval=1.0)
    fast_food_bot.idle()


if __name__ == "__main__":
    main()
