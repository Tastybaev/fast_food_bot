from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ParseMode
)

from db import get_menu, get_dish

from glob import glob

FIRST, SECOND, THIRD, FOURTH = range(4)

MENU = ['hot_dishes', 'soup', 'pizza', 'drinks']

HOT_DISHES, SOUP, PIZZA, DRINKS = (
    'Горячие блюда',
    'Супы',
    'Пицца',
    'Напитки'
)

BACK, ADD_TO_SHOPPING_CART, REMOVE_FROM_SHOPPING_CART, MY_SHOPPING_CART, MAKE_ORDER = (
    'Назад',
    'Добавить в корзину',
    'Удалить',
    'Моя корзина',
    'Оформить заказ'
    )

INCREASE, DECREASE = (
    '▲',
    '▼'
)

KEYBOARD_NAVIGATION = [
    # [InlineKeyboardButton("Показать еще", callback_data=str(PIZZA))],
    [InlineKeyboardButton("Моя корзина", callback_data=str(MY_SHOPPING_CART))],
    # [InlineKeyboardButton("Оформить заказ", callback_data=str(DRINKS))],
    [InlineKeyboardButton("Назад", callback_data=str(BACK))]
]

KEYBOARD_MY_SHOPPING_CART = [
    [
        InlineKeyboardButton("Оформить заказ", callback_data=str(MAKE_ORDER)),
        InlineKeyboardButton("Назад", callback_data=str(BACK)),
    ]
]

KEYBOARD_MENU = [
    [
        InlineKeyboardButton("Горячие блюда", callback_data=str(HOT_DISHES)),
        InlineKeyboardButton("Супы", callback_data=str(SOUP))
    ],
    [
        InlineKeyboardButton("Пицца", callback_data=str(PIZZA)),
        InlineKeyboardButton("Напитки", callback_data=str(DRINKS))
    ],
    [InlineKeyboardButton("Моя корзина", callback_data=str(MY_SHOPPING_CART))]
]

KEYBOARD_SHOPPING_CART = [
    [
        InlineKeyboardButton("Добавить в корзину", callback_data=str(ADD_TO_SHOPPING_CART)),
    ]
]

KEYBOARD_SET_PORTION = [
    [
        InlineKeyboardButton('▼', callback_data=str(DECREASE)),
        InlineKeyboardButton(str(1), callback_data=str(1)), #Надо вставить переменную для указания количества добавленных порций.
        InlineKeyboardButton('▲', callback_data=str(INCREASE))
    ],
    [
        InlineKeyboardButton('Удалить', callback_data=str(REMOVE_FROM_SHOPPING_CART))
    ]
]

KEYBOARD_REMOVE_FROM_SHOPPING_CART = [
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


def delete_message_one(context, chat_id, message_id):
    context.bot.deleteMessage(
            chat_id=chat_id,
            message_id=message_id
        )
    context.user_data['message_ids'].remove(message_id)

def delete_message_all(context, chat_id):
    for message_id in context.user_data['message_ids']:
        context.bot.deleteMessage(
            chat_id=chat_id,
            message_id=message_id
        )
    context.user_data['message_ids'].clear()


def send_message(context, chat_id, menu, menu_type):
    for item in menu:
        message_id = context.bot.send_photo(
            chat_id=chat_id,
            photo=open(f"menu_imgs/{menu_type}/{item['id']}.png", 'rb'),
            caption=f"""
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


def edit_message_reply_markup(context, dish_count, message_id, chat_id):
    context.bot.edit_message_reply_markup(
        message_id=message_id,
        chat_id=chat_id,
        reply_markup = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton('▼', callback_data=str(DECREASE)),
                InlineKeyboardButton(str(dish_count), callback_data=str(dish_count)), #Надо вставить переменную для указания количества добавленных порций.
                InlineKeyboardButton('▲', callback_data=str(INCREASE))
            ],
            [
                InlineKeyboardButton('Удалить', callback_data=str(REMOVE_FROM_SHOPPING_CART))
            ]]
        )
    )


def show_my_shopping_cart(context, chat_id):
    total_price = 0
    for key, value in context.user_data.items():
        if key in MENU:
            for dish_dict in value:
                dish = get_dish(key, next(iter(dish_dict.keys())))
                dish_position_price = dish['price']*int(next(iter(dish_dict.values())))
                total_price += dish_position_price
                message_id = context.bot.send_photo(
                    chat_id=chat_id,
                    photo=open(f"menu_imgs/{key}/{dish['id']}.png", 'rb'),
                    caption=f"Блюдо: {dish['name']}\nЦена: {dish['price']}\nКоличество порций: {next(iter(dish_dict.values()))}\nСтоимость: {dish_position_price}\n<span class='tg-spoiler'>ID: {key}.{dish['id']}</span>",
                    reply_markup=InlineKeyboardMarkup(KEYBOARD_REMOVE_FROM_SHOPPING_CART),
                    parse_mode = ParseMode.HTML
                )
                save_message_id(context, message_id)
    message_id = context.bot.send_message(
        chat_id=chat_id,
        text=f"К оплате: {total_price}",
        reply_markup=InlineKeyboardMarkup(KEYBOARD_MY_SHOPPING_CART)
    )
    save_message_id(context, message_id)
    context.user_data['total_price'] = total_price


def refresh_total_price(context, chat_id, message):
    message_id = context.user_data['message_ids'][-1]
    dish_price = message['caption'].split('\n')[3].split()[-1]
    total_price = context.user_data['total_price']
    refreshed_price = total_price - int(dish_price)
    context.user_data['total_price'] = refreshed_price
    context.bot.edit_message_text(
        message_id=message_id,
        chat_id=chat_id,
        text=f'К оплате: {refreshed_price}',
        reply_markup=InlineKeyboardMarkup(KEYBOARD_MY_SHOPPING_CART)
    )

def delete_dish(context, chat_id, message_id, message=0, flag=0):
    if flag == 'menu':
        message = context.bot.edit_message_reply_markup(
            message_id=message_id,
            chat_id=chat_id,
            reply_markup=InlineKeyboardMarkup(KEYBOARD_SHOPPING_CART)
        )
    else:
        delete_message_one(context, chat_id,  message_id)
        refresh_total_price(context, chat_id, message)
    print(message['caption'])
    dish_type = message['caption'].split()[-1].split('.')[0]
    dish_id = message['caption'].split()[-1].split('.')[-1]
    for dish in context.user_data[dish_type]:
        if dish.get(dish_id, False):
            context.user_data[dish_type].remove(dish)
            break
    print(context.user_data)
