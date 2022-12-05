from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ParseMode
)

FIRST, SECOND, THIRD, FOURTH = range(4)

MENU = ['hot_dishes', 'soup', 'pizza', 'drinks']

HOT_DISHES, SOUP, PIZZA, DRINKS = (
    'Горячие блюда',
    'Супы',
    'Пицца',
    'Напитки'
)

BACK, ADD_TO_SHOPPING_CART, REMOVE_FROM_SHOPPING_CART = (
    'Назад',
    'Добавить в корзину',
    'Удалить'
    )

INCREASE, DECREASE = (
    '▲',
    '▼'
)

KEYBOARD_NAVIGATION = [
    [InlineKeyboardButton("Показать еще", callback_data=str(PIZZA))],
    [InlineKeyboardButton("Моя корзина", callback_data=str(PIZZA))],
    [InlineKeyboardButton("Оформить заказ", callback_data=str(DRINKS))],
    [InlineKeyboardButton("Назад", callback_data=str(BACK))]
]

KEYBOARD_MENU = [
    [
        InlineKeyboardButton("Горячие блюда", callback_data=str(HOT_DISHES)),
        InlineKeyboardButton("Супы", callback_data=str(SOUP))
    ],
    [
        InlineKeyboardButton("Пицца", callback_data=str(PIZZA)),
        InlineKeyboardButton("Напитки", callback_data=str(DRINKS))
    ]
]

KEYBOARD_SHOPPING_CART = [
    [
        InlineKeyboardButton("Добавить в корзину", callback_data=str(ADD_TO_SHOPPING_CART)),
    ]
]

KEYBOARD_SET_PORTION = [
    [
        InlineKeyboardButton('▼', callback_data=str(DECREASE)),
        InlineKeyboardButton('1', callback_data=str('1')), #Надо вставить переменную для указания количества добавленных порций.
        InlineKeyboardButton('▲', callback_data=str(INCREASE))
    ],
    [
        InlineKeyboardButton('Удалить', callback_data=str(REMOVE_FROM_SHOPPING_CART))
    ]
]

def order_keyboard():
    return ReplyKeyboardMarkup([
        ['Заказать', 'Отменить']
    ])


def main_keyboard():
    return ReplyKeyboardMarkup([
        ["Меню", "Заказать"]
    ])


def save_message_id(context, message_id):
        context.user_data['message_ids'].append(message_id['message_id'])


def delete_message(context, chat_id):
    for message_id in context.user_data['message_ids']:
        context.bot.deleteMessage(
            chat_id=chat_id,
            message_id=message_id
        )
    context.user_data['message_ids'].clear()


def send_message(context, chat_id, menu, menu_type):
    for item in menu:
        message_id = context.bot.send_message(
            chat_id=chat_id,
            text=f"""
            Название: {item['name']}
Цена: {item['price']}
Описание: {item['description']}
<span class="tg-spoiler">ID: {menu_type}.{item['id']}</span>
            """,
            reply_markup=InlineKeyboardMarkup(KEYBOARD_SHOPPING_CART),
            parse_mode = ParseMode.HTML
        )
        save_message_id(context, message_id)
    message_id = context.bot.send_message(
        chat_id=chat_id,
        text="Для оформления заказа выбирите интересующее блюдо и перейдите в корзину.",
        reply_markup=InlineKeyboardMarkup(KEYBOARD_NAVIGATION)
    )
    save_message_id(context, message_id)


def create_menu_list(context, menu_type):
    if not context.user_data.get(menu_type):
        context.user_data[menu_type] = []