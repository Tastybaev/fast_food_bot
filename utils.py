from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from settings import(
    ADD_TO_SHOPPING_CART,
    BACK,
    HOT_DISHES,
    SOUP,
    PIZZA,
    DRINKS
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
        InlineKeyboardButton("Добавить в корзину", callback_data=str(ADD_TO_SHOPPING_CART))
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


def save_message_id(message_id, context):
        context.user_data['message_ids'].append(message_id['message_id'])


def delete_message(chat_id, context):
    for message_id in context.user_data['message_ids']:
        context.bot.deleteMessage(
            chat_id=chat_id,
            message_id=message_id
        )
    context.user_data['message_ids'].clear()


def send_message(menu, chat_id, context):
    for item in menu:
        message_id = context.bot.send_message(
            chat_id=chat_id,
            text=f"Название: {item['name']}\nЦена: {item['price']}\nОписание: {item['description']}",
            reply_markup=InlineKeyboardMarkup(KEYBOARD_SHOPPING_CART),
        )
        save_message_id(message_id, context)
    message_id = context.bot.send_message(
        chat_id=chat_id,
        text="Для оформления заказа выбирите интересующее блюдо и перейдите в корзину.",
        reply_markup=InlineKeyboardMarkup(KEYBOARD_NAVIGATION)
    )
    save_message_id(message_id, context)
