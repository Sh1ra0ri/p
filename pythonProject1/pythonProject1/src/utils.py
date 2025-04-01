import json
from pathlib import Path
from typing import List, Dict, Any
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def read_transactions(file_path: Path) -> List[Dict[str, Any]]:
    """функция, которая принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                return []
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        return []


def transaction_sum(transaction: dict, file_type: str = "json") -> float:
    """ функция, которая принимает на вход транзакцию и возвращает сумму транзакции в рублях,"""
    response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js", timeout=5)
    data = response.json()

    if file_type == "json":
        currency_code = transaction["operationAmount"]["currency"]["code"]
        amount = float(transaction["operationAmount"]["amount"])

        if currency_code == "RUB":
            return amount
        else:
            currency_rate = data["Valute"].get(currency_code, {}).get("Value", 1.0)
            return amount * currency_rate
    else:
        currency_code = transaction["currency_code"]
        amount = float(transaction["amount"])
        if currency_code == "RUB":
            return amount
        else:
            currency_rate = data["Valute"].get(currency_code, {}).get("Value", 1.0)
            return amount * currency_rate