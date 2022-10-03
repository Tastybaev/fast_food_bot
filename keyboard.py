from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram_bot_pagination import InlineKeyboardPaginator
from telegram.ext import CallbackQueryHandler, ConversationHandler
from db import db, get_menu_hot_dishes

from settings import(
    FIRST,
    SECOND,
    HOT_DISHES,
    SOUP,
    PIZZA,
    DRINKS
)


def start(update, _):
    """Вызывается по команде `/start`."""
    # Получаем пользователя, который запустил команду `/start`
    user = update.message.from_user
    # logger.info("Пользователь %s начал разговор", user.first_name)
    # Создаем `InlineKeyboard`, где каждая кнопка имеет 
    # отображаемый текст и строку `callback_data`
    # Клавиатура - это список строк кнопок, где каждая строка, 
    # в свою очередь, является списком `[[...]]`
    keyboard = [
        [
            InlineKeyboardButton("Горячие блюда", callback_data=str(HOT_DISHES)),
            InlineKeyboardButton("Супы", callback_data=str(SOUP))
        ],
        [
            InlineKeyboardButton("Пицца", callback_data=str(PIZZA)),
            InlineKeyboardButton("Напитки", callback_data=str(DRINKS))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отправляем сообщение с текстом и добавленной клавиатурой `reply_markup`
    update.message.reply_text(
        text=f"Здравствуйте {user['first_name']}, что будете заказывать?", reply_markup=reply_markup
    )
    # Сообщаем `ConversationHandler`, что сейчас состояние `FIRST`
    return FIRST


def start_over(update, _):
    """Тот же текст и клавиатура, что и при `/start`, но не как новое сообщение"""
    # Получаем `CallbackQuery` из обновления `update`
    query = update.callback_query
    # На запросы обратного вызова необходимо ответить, 
    # даже если уведомление для пользователя не требуется.
    # В противном случае у некоторых клиентов могут возникнуть проблемы.
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("2", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
   # Отредактируем сообщение, вызвавшее обратный вызов.
   # Это создает ощущение интерактивного меню.
    query.edit_message_text(
        text="Выберите маршрут", reply_markup=reply_markup
    )
    # Сообщаем `ConversationHandler`, что сейчас находимся в состоянии `FIRST`
    return FIRST


def hot_dishes(update, _):
    """Показ нового выбора кнопок"""
    menu = get_menu_hot_dishes(db)
    paginator = InlineKeyboardPaginator(
        3,
        current_page=1,
        data_pattern='page#{page}'
    )
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Моя корзина", callback_data=str(PIZZA))],
        [InlineKeyboardButton("Оформить заказ", callback_data=str(DRINKS))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        f"{menu}",
        reply_markup=paginator.markup
    )
    query.edit_message_text(
        text="меню", reply_markup=reply_markup,
    )
    return FIRST


def soup(update, _):
    """Показ нового выбора кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("3", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Второй CallbackQueryHandler", reply_markup=reply_markup
    )
    return FIRST


def pizza(update, _):
    """Показ выбора кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Да, сделаем это снова!", callback_data=str(ONE)),
            InlineKeyboardButton("Нет, с меня хватит ...", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Третий CallbackQueryHandler. Начать сначала?", reply_markup=reply_markup
    )
    # Переход в состояние разговора `SECOND`
    return SECOND


def drinks(update, _):
    """Показ выбора кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("2", callback_data=str(TWO)),
            InlineKeyboardButton("4", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Четвертый CallbackQueryHandler, выберите маршрут", reply_markup=reply_markup
    )
    return FIRST


def end(update, _):
    """Возвращает `ConversationHandler.END`, который говорит 
    `ConversationHandler` что разговор окончен"""
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END
