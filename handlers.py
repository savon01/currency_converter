import logging

from typing import List

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from currency import get_exchange_rates
from config import TOKEN


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


dp: Dispatcher = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Обработчик команды `/start`
    """
    logger.info(f"Введена команда /start пользователем: {message.from_user.username}")
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!"
                         f" Я бот для конвертации валют. Введите команду /help, чтобы узнать доступные команды!")


@dp.message(Command("help"))
async def cmd_answer(message: types.Message):
    """
    Обработчик команды `help`
    :param message: сообщение
    :return: None
    """
    logger.info(f"Введена команда /help пользователем: {message.from_user.username}")
    help_text: str = "Доступные команды:\n" \
                     "/start - Начать общение с ботом\n" \
                     "/help - Получить справку о доступных командах\n" \
                     "/convert <b>сумма</b> из <b>валюты</b> to <b>в валюту</b>" \
                     "- Конвертировать сумму из одной валюты в другую\n" \
                     "Например: /convert 100 USD to EUR"
    await message.answer(help_text)


@dp.message(Command('convert'))
async def convert_command(message: types.Message):
    """
    Обработчик команды `/convert`
    :param message: сообщение
    :return: None
    """
    try:
        # Разбиваем сообщение на аргументы
        logger.info(f"Введена команда /convert пользователем: {message.from_user.username}")
        args: List[str] = message.text.split(' ')
        amount: float = float(args[1])
        from_currency: str = args[2].rstrip().upper()
        to_currency: str = args[4].upper()

        exchange_rates: dict = await get_exchange_rates(from_currency)
        if exchange_rates is None:
            await message.reply("Не удалось получить курсы обмена валют. Пожалуйста, попробуйте позже.")
            return

        if to_currency not in exchange_rates:
            await message.reply("Неверно указана валюта для конвертации.")
            return
        logger.info(f"Получен словарь с волютой пользователем: {message.from_user.username}")
        converted_amount: float = round(amount * exchange_rates[to_currency], 4)
        result_text: str = f"{amount} {from_currency} = {converted_amount} {to_currency}"
        await message.reply(result_text)
    except IndexError:
        await message.reply("Неверный формат команды. Пожалуйста, используйте команду в формате "
                            "/convert <b>сумма</b> из <b>валюты</b> to <b>в валюту</b>")
    except ValueError:
        await message.reply("Неверно указана сумма для конвертации.")


@dp.message()
async def handle_text(message: types.Message):
    """
    Обработчик других сообщений
    :param message: сообщение
    :return: None
    """
    text: str = message.text.lower()
    logger.info(f"Пользователем: {message.from_user.username}, введен текст: {text}")
    if 'привет' in text:
        await message.answer(f"Привет, {hbold(message.from_user.full_name)}!")
    elif 'пока' in text:
        await message.answer(f"Пока, {hbold(message.from_user.full_name)}!")
    else:
        await message.answer("Неизвестная команда. Введите /help, чтобы узнать доступные команды.")


async def main() -> None:
    """Запуск бота"""
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

