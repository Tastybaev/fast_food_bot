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
    delete_from_shopping_list,
    delete_from_shopping_cart,
    increase_dish,
    decrease_dish,
    my_shopping_cart,
    end
)

from settings import TELEGRAM_TOKEN

from utils import(
    ADD_TO_SHOPPING_CART,
    REMOVE_FROM_SHOPPING_CART,
    MY_SHOPPING_CART,
    MAKE_ORDER,
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
                CallbackQueryHandler(drinks, pattern='^' + str(DRINKS) + '$'),
                CallbackQueryHandler(my_shopping_cart, pattern='^' + str(MY_SHOPPING_CART) + '$'),
            ],
            SECOND: [
                CallbackQueryHandler(add_to_shopping_cart, pattern='^' + str(ADD_TO_SHOPPING_CART) + '$'),
                CallbackQueryHandler(delete_from_shopping_list, pattern='^' + str(REMOVE_FROM_SHOPPING_CART) + '$'),
                CallbackQueryHandler(start_over, pattern='^' + str(BACK) + '$'),
                CallbackQueryHandler(increase_dish, pattern='^' + str(INCREASE) + '$'),
                CallbackQueryHandler(decrease_dish, pattern='^' + str(DECREASE) + '$'),
                CallbackQueryHandler(my_shopping_cart, pattern='^' + str(MY_SHOPPING_CART) + '$'),
            ],
            THIRD: [
                CallbackQueryHandler(start_over, pattern='^' + str(BACK) + '$'),
                CallbackQueryHandler(delete_from_shopping_cart, pattern='^' + str(REMOVE_FROM_SHOPPING_CART) + '$'),
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
