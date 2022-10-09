from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_menu_old = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Задание", callback_data="Task"),
            InlineKeyboardButton(text="Описание", callback_data="Notes"),
        ],
    ]
)

start_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Сгенерировать блок!", callback_data="GetBlock"),
        ],
    ]
)

admin_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Новые пользователи", callback_data="show_new_users"),
        ],
    ]
)