from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Задание", callback_data="Task"),
            InlineKeyboardButton(text="Описание", callback_data="Notes"),
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