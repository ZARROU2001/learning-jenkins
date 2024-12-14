# gold/services.py

import requests
from sqlalchemy.ext.asyncio import AsyncSession
from config import Config
from gold.repository import save_gold_price
from errors import APIError


async def fetch_gold_price() -> float:
    headers = {
        "x-access-token": Config.GOLD_API_KEY,
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(Config.GOLD_API_BASE_URL, headers=headers)
        response.raise_for_status()

        result = response.json()  # Change from response.text to response.json()
        return result["price"]
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))

async def update_gold_price(db: AsyncSession):
    price = await fetch_gold_price()
    return await save_gold_price(db, price)
