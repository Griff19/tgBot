from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from tgbot.keyboards.reply import menu1


async def show_menu(message, state: FSMContext):
    await message.answer("Нажмите на кнопку", reply_markup=menu1)
    await state.set_state("secret")


async def check_menu(message, state: FSMContext):
    await message.answer("Ай ай ай! Это был секрет! \U0001f970", reply_markup=ReplyKeyboardRemove())
    await state.reset_state()


def register_menu(dp: Dispatcher):
    dp.register_message_handler(show_menu, commands=["secret"])
    dp.register_message_handler(check_menu, Text(startswith="Секрет"), state="secret")
