from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.markdown import hlink, link

from tgbot.keyboards.inline import admin_menu
from tgbot.models.User import User
from tgbot.services.callbackdata import user_data


def get_list_new_user():
    users = User.select_new()
    str_users = InlineKeyboardMarkup()
    if not users:
        return False

    print(users)
    for user in users:
        alias = user[1] if user[1] else user[2]
        str_users.add(
            InlineKeyboardButton(text=alias, url="tg://user?id="+str(user[0])),
            InlineKeyboardButton(text="\U00002705", callback_data=f"action:{user[0]}:accept"),
            InlineKeyboardButton(text="\U0000274C", callback_data=f"action:{user[0]}:delete"),
        )

    return str_users


async def admin_start(message: Message):
    await message.reply("Hello, admin!")


async def show_admin_menu(message: Message):
    await message.answer("Меню администратора:", reply_markup=admin_menu)


# выводим список новых пользователей
async def get_new_user(call: CallbackQuery, state: FSMContext):
    await call.answer()
    if not get_list_new_user():
        await call.message.answer("Нет новых заявок")
        return
    await state.set_state("invite_user")
    await call.message.answer("Новые пользователи:", reply_markup=get_list_new_user())


# обрабатываем возврат от кнопки действия с пользователем
async def user_action(call: CallbackQuery):
    await call.answer()
    print(call.data)
    data = call.data.split(':')
    user_id = data[1]
    action = data[2]

    if action == 'delete':
        User.update(user_id, User.STATUS_BLOCkED)
        if not get_list_new_user():
            await call.message.answer("Нет новых заявок")
            return
        await call.message.answer(f"Пользователь удален...", reply_markup=get_list_new_user())
        return
    if action == 'accept':
        User.update(user_id, User.STATUS_MEMBER)
        if not get_list_new_user():
            await call.message.answer("Нет новых заявок")
            return
        await call.message.answer("Пользователь добвален", reply_markup=get_list_new_user())
        return


# допускаем пользователя к работе с ботом
async def invite_user(call: CallbackQuery):

    print(call)
    await call.message.answer("Статус пользователя изменен")
    await call.message.answer("Новые пользователи:", reply_markup=get_list_new_user())


def register_admin(dp: Dispatcher):
    dp.register_message_handler(show_admin_menu, commands=["admin"], is_admin=True)
    dp.register_callback_query_handler(get_new_user, text='show_new_users', is_admin=True)
    dp.register_callback_query_handler(user_action, text_contains="action", state="invite_user", is_admin=True)
    dp.register_message_handler(invite_user, commands=['invite'], state="invite_user", is_admin=True)
