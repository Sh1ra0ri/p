import json
import os
import requests
import logging
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger("utils")

load_dotenv()
API_KEY = os.getenv("API_KEY")


def read_transactions(file_path: Path) -> list:
    """Читает файл и возвращает данные как список."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                logger.info("Файл прочитан.")
                return data
            else:
                logger.warning(f"Файл {file_path} не содержит корректных данных.")
                return []
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {file_path}: {e}")
        return []


def transaction_sum(transaction: dict, file_type: str = "json") -> float:
    """Возвращает сумму транзакции в рублях."""
    try:
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js", timeout=5)
        data = response.json()

        if file_type == "json":
            if transaction["operationAmount"]["currency"]["code"] == "RUB":
                amount = float(transaction["operationAmount"]["amount"])
                currency = 1.0
            else:
                valute = transaction["operationAmount"]["currency"]["code"]
                currency = data["Valute"][valute]["Value"]
                amount = float(transaction["operationAmount"]["amount"])
        else:
            if transaction["currency_code"] == "RUB":
                amount = float(transaction["amount"])
                currency = 1.0
            else:
                valute = transaction["currency_code"]
                if valute in data["Valute"]:
                    currency = data["Valute"][valute]["Value"]
                else:
                    currency = 1.0
                amount = float(transaction["amount"])

        logger.info(f"Функция выполнена")
        return float(amount * currency)

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к API: {e}")
        return 0.0