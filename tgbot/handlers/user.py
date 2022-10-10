from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.handlers.start import bot_start
from tgbot.keyboards.inline import user_block_menu, start_menu, task_menu
from tgbot.models.Account import Account
from tgbot.models.Task import Task
from tgbot.models.User import User


async def generate_block(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    offset = data['offset']

    try: old_rows = data['rows']
    except KeyError: old_rows = None

    items = Account.get_next_block(user_id=call.from_user.id, factor=offset, old_rows=old_rows)
    await state.update_data(offset=offset + 1)
    await state.update_data(rows=items)
    str_mess = ''
    for item in items:
        str_mess = str_mess + item[3] + "\n"

    await call.message.answer("Ваш блок:")
    await call.message.answer(str_mess, reply_markup=user_block_menu)


async def take_block(call: CallbackQuery, state: FSMContext):
    await call.answer()
    user = User(user_id=call.from_user.id)
    user.create_task()
    await state.finish()
    await call.message.answer("Задача сформирована и назначена Вам", reply_markup=task_menu)


async def task_view(call: CallbackQuery, state: FSMContext):
    await call.answer()
    user_id = call.from_user.id
    user = User(user_id=user_id)
    if user:
        items = user.get_task()
        if items:
            await call.message.answer(f"Ваша задача: №{items[0][0]} \n{items[0][1]} дата: {items[0][2]}")
            str_task = ''
            for item in items:
                str_task = str_task + f"{item[3]} \n"
            await call.message.answer(str_task, reply_markup=task_menu)
            await state.finish()


async def close_task(call: CallbackQuery, state: FSMContext):
    await call.answer()
    user_id = call.from_user.id
    user = User(user_id=user_id)
    if user:
        user.close_task()
        await state.set_state("Change_block")
        await state.update_data(offset=0)
        await call.message.answer("Спасибо! Ваша задача закрыта", reply_markup=start_menu)
    else:
        print("Пользователь не найден")


async def back_task(call: CallbackQuery, state: FSMContext):
    await call.answer()
    user = User(user_id=call.from_user.id)
    if user:
        user.back_task()
        await state.set_state("Change_block")
        await state.update_data(offset=0)
        await call.message.answer("Вы вернули свой блок. Можете получить новый:", reply_markup=start_menu)
    else:
        print("Пользователь не найден")


def register_user(dp: Dispatcher):
    dp.register_callback_query_handler(generate_block, text="GetBlock", state="Change_block")
    dp.register_callback_query_handler(take_block, text="TakeBlock", state="Change_block")
    dp.register_callback_query_handler(close_task, text="TaskClose")
    dp.register_callback_query_handler(task_view, text="TaskView")
    dp.register_callback_query_handler(back_task, text="TaskBack")
