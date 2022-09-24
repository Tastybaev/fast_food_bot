from telegram import ReplyKeyboardMarkup


def order_keyboard():
    return ReplyKeyboardMarkup([
        ['Заказать', 'Отменить']
    ])


def main_keyboard():
    return ReplyKeyboardMarkup([
        ["Меню", "Заказать"]
    ])
