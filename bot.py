import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.user import register_user
from tgbot.keyboards.inline import register_inline
from tgbot.middlewares.environment import EnvironmentMiddleware

logger = logging.getLogger(__name__)


async def on_startup_notify(dp):
    message = "Бот успішно стартував"
    admin_ids = dp.bot.get('config').tg_bot.admin_ids
    for admin_id in admin_ids:
        await dp.bot.send_message(admin_id, message)


async def on_shutdown_notify(dp):
    message = "Бот завершив свою роботу"
    admin_ids = dp.bot.get('config').tg_bot.admin_ids
    for admin_id in admin_ids:
        await dp.bot.send_message(admin_id, message)


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)
    # register_echo(dp)


def register_all_keyboards(dp):
    register_inline(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    PROXY_URL = "http://proxy.server:3128"
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML', proxy=PROXY_URL)
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)
    register_all_keyboards(dp)

    # start
    try:
        await on_startup_notify(dp)
        await dp.start_polling()
    finally:
        await on_shutdown_notify(dp)
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
