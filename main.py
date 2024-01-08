import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, BufferedInputFile

from channels_profile import world_news_en_profile
from monitor.tg_monitor import Monitor
from email_validator import validate_email, EmailNotValidError

# Bot token can be obtained via https://t.me/BotFather
bot_token = getenv("bot_token")

api_id = int(getenv("listener_api_id"))
api_hash = getenv("listener_api_hash")
tg_client_owner = getenv("tg_client_owner")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
monitor = Monitor(api_id, api_hash, tg_client_owner)
bot = Bot(bot_token, parse_mode=ParseMode.HTML)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Welcome!")


@dp.message()
async def echo_handler(message: types.Message) -> None:
    # Send a copy of the received message
    text_file = BufferedInputFile(bytes(f"Stats:\n {monitor.archive.statistics}", 'UTF-8'),
                                  filename="stats.txt")
    await message.answer_document(text_file)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    await asyncio.gather(monitor.start_tg_client(world_news_en_profile.instance), dp.start_polling(bot))
    # await monitor.start_tg_client(politic_profile.instance)
    # await monitor.start_tg_client(recruitment_profile.instance)

    # And the run events dispatching
    # await dp.start_polling(bot)


def check(email):
    try:
        # validate and get info
        result = validate_email(email)
        # replace with normalized form
        return result["email"]
    except EmailNotValidError:
        return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())
