from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Секретная кнопка.")
        ]
    ],
    resize_keyboard=True
)
