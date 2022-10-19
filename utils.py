from telegram import ReplyKeyboardMarkup, InlineKeyboardButton

from settings import(
    ADD_TO_SHOPPING_CART,
    BACK,
    FIRST,
    NAVIGATION_MENU,
    SECOND,
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
    ],
    [
        InlineKeyboardButton("Навигация", callback_data=str(NAVIGATION_MENU))
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

