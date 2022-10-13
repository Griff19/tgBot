from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.handler import current_handler
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline import start_menu, task_menu
from tgbot.misc.throttling import rate_limit
from tgbot.models.User import User


@rate_limit(5, key="start")
async def bot_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = User(user_id=user_id)

    if user.id:
        if user.is_member():
            items = user.get_task()
            if items:
                await message.answer(f"Ваша задача: №{items[0][0]} \n{items[0][1]} дата: {items[0][2]}")
                str_task = ''
                for item in items:
                    str_task = str_task + f"{item[3]} \n"
                await message.answer(str_task, reply_markup=task_menu)
                await state.finish()
                return

            await state.set_state("Change_block")
            await state.update_data(offset=0)
            await message.answer("Вы можете сгенерировать свой блок:", reply_markup=start_menu)
        else:
            await message.answer("Вы отправили запрос, но администратор еще не принял его.")
    else:
        await message.answer("Здравствуйте! Это демонстрационный бот. Чтобы отправить запрос на добавление нажмите "
                             "или напишите /invite")


# async def button_task(call: CallbackQuery):
#     await call.message.answer("Нажата кнопка Задание")
#
#
# async def button_notes(call: CallbackQuery):
#     await call.message.answer("Нажата кнопка Описание")


# async def open_menu(message: Message):
#     await message.answer("Главное меню:", reply_markup=start_menu)


# async def be_happy(call: CallbackQuery):
#     await call.message.answer("<b>Все будет хорошо!</>\n \U0001f60a \U0001f970 \U0001f618 \U00002764")


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
    dp.register_message_handler(bot_start, Command(["start", "menu"]), state="*")
    # dp.register_callback_query_handler(button_task, text="Task")
    # dp.register_callback_query_handler(button_notes, text="Notes")
    # dp.register_callback_query_handler(be_happy, text="Gift")
    dp.register_message_handler(invite_request, commands=["invite"])
