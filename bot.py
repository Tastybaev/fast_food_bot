import logging
from telegram.ext import (
    CommandHandler,
    Updater,
    ConversationHandler,
    CallbackQueryHandler
)

from keyboard import (
    start,
    start_over,
    hot_dishes,
    soup,
    pizza,
    drinks,
    add_to_shopping_cart,
    increase_dish,
    decrease_dish,
    end
)

from settings import TELEGRAM_TOKEN

from utils import(
    ADD_TO_SHOPPING_CART,
    FIRST,
    SECOND,
    THIRD,
    HOT_DISHES,
    SOUP,
    PIZZA,
    DRINKS,
    BACK,
    DECREASE,
    INCREASE
)

logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    fast_food_bot = Updater(TELEGRAM_TOKEN)
    dp = fast_food_bot.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={ # словарь состояний разговора, возвращаемых callback функциями
            FIRST: [
                CallbackQueryHandler(hot_dishes, pattern='^' + str(HOT_DISHES) + '$'),
                CallbackQueryHandler(soup, pattern='^' + str(SOUP) + '$'),
                CallbackQueryHandler(pizza, pattern='^' + str(PIZZA) + '$'),
                CallbackQueryHandler(drinks, pattern='^' + str(DRINKS) + '$')
            ],
            SECOND: [
                CallbackQueryHandler(add_to_shopping_cart, pattern='^' + str(ADD_TO_SHOPPING_CART) + '$'),
                CallbackQueryHandler(start_over, pattern='^' + str(BACK) + '$'),
                CallbackQueryHandler(increase_dish, pattern='^' + str(INCREASE) + '$'),
                CallbackQueryHandler(decrease_dish, pattern='^' + str(DECREASE) + '$'),
            ],
            THIRD: [
                CallbackQueryHandler(start_over, pattern='^' + str(BACK) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(SOUP) + '$'),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    dp.add_handler(conv_handler)

    logging.info('BOT IS STARTED!')
    fast_food_bot.start_polling(poll_interval=1.0)
    fast_food_bot.idle()


if __name__ == "__main__":
    main()
