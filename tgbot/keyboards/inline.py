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

user_block_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Взять блок", callback_data="TakeBlock"),
            InlineKeyboardButton(text="Следующий блок", callback_data="GetBlock"),
        ],
    ]
)

task_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Закрыть", callback_data="TaskClose"),
            InlineKeyboardButton(text="Вернуть", callback_data="TaskBack"),
            InlineKeyboardButton(text="Просмотр", callback_data="TaskView"),
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