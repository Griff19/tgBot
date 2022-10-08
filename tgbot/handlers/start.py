from aiogram import Dispatcher
from aiogram.dispatcher.handler import current_handler
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline import start_menu
from tgbot.misc.throttling import rate_limit
from tgbot.models.User import User


@rate_limit(10, key="start")
async def bot_start(message: Message):
    await message.answer("Здравствуйте! Это демонстрационный бот. Чтобы отправить запрос на добавление нажмите "
                         "или напишите /invite")


async def button_task(call: CallbackQuery):
    await call.message.answer("Нажата кнопка Задание")


async def button_notes(call: CallbackQuery):
    await call.message.answer("Нажата кнопка Описание")


async def open_menu(message: Message):
    await message.answer("Главное меню:", reply_markup=start_menu)


async def be_happy(call: CallbackQuery):
    await call.message.answer("<b>Все будет хорошо!</>\n \U0001f60a \U0001f970 \U0001f618 \U00002764")


async def invite_request(message: Message):
    id_user = message.from_user.id
    user = User.find_user_by_id(id_user)
    if user:
        await message.answer("Вы уже отправляли этот запрос")
        return
    alias = message.from_user.username
    name = message.from_user.first_name
    surname = message.from_user.last_name
    User.insert(id_user, alias, name, surname, User.STATUS_NEW, '')
    await message.answer("Ваш запрос добавлен!")


def register_start(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands=["start"])
    dp.register_message_handler(open_menu, commands=["menu"])
    dp.register_callback_query_handler(button_task, text="Task")
    dp.register_callback_query_handler(button_notes, text="Notes")
    dp.register_callback_query_handler(be_happy, text="Gift")
    dp.register_message_handler(invite_request, commands=["invite"])
