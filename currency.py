import requests
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def get_exchange_rates(base_currency: str) -> dict:
    """
    Функция получения курса валют
    :param base_currency: базовая валюта
    :return: словарь с курсами валют
    """
    logger.info(f"Запрос для получения валюты")
    url: str = f'https://api.exchangerate-api.com/v4/latest/{base_currency}'

    response = requests.get(url)
    if response.status_code == 200:
        data: dict = response.json()
        return data['rates']
    else:
        logger.info(f"Ошибка при выполнении запроса: {response.status_code}")
        return None
