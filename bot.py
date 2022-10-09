import asyncio
import logging


from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import BotCommand

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.echo import register_echo
from tgbot.handlers.secret import register_menu
from tgbot.handlers.start import register_start
from tgbot.handlers.user import register_user
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.middlewares.throttling import ThrottlingMiddleware
from tgbot.models.User import User


logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    # dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(ThrottlingMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_start(dp)
    #register_menu(dp)
    # register_user(dp)
    # register_echo(dp)


async def register_my_commands(bot):
    return await bot.set_my_commands(commands=[
        BotCommand('start', 'Запуск бота'),
        BotCommand('menu', 'Главное меню'),
        BotCommand('invite', 'Отправить запрос на доступ'),
        BotCommand('admin', 'Функции администратора'),
    ])


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    await register_my_commands(bot)

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    User.select_all()
    inst = Instargam(config.instagram['username'], config.instagram['password'])
    inst.test()

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
