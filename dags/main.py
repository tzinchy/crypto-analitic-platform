import asyncio
import aiohttp
from core.config import BINANCE_API_URL_CURRENT_COIN_PRICE, BINANCE_PAIRS, Settings
from repository.database import AsyncDatabase

# Асинхронная функция для получения данных
async def fetch_ticker_data(session, symbol):
    await asyncio.sleep(1)  
    url = BINANCE_API_URL_CURRENT_COIN_PRICE + symbol
    async with session.get(url) as response:
        data = await response.json()
        return data

# Асинхронная функция для обработки одного символа
async def process_symbol(session, db, symbol, pair_id):
    while True:  # Бесконечный цикл для периодического запроса данных
        try:
            # Получаем данные
            data = await fetch_ticker_data(session, symbol)
            print(f"Received data for {symbol}: {data}")

            # Проверяем, что данные содержат нужные ключи
            if "symbol" not in data or "price" not in data:
                raise ValueError(f"Invalid data format for {symbol}: {data}")

            # Преобразуем цену в float
            price = float(data["price"])
            print(f"Processed data for {symbol}: price={price}")

            # Вставляем данные в базу
            await db.insert_data(pair_id, price)
            print(f"Inserted {symbol} with price {price} into database.")

        except ValueError as e:
            print(f"Value error for {symbol}: {e}")
        except Exception as e:
            print(f"Error processing {symbol}: {e}")

        # Задержка между запросами
        await asyncio.sleep(1)

async def main():
    # Создаем экземпляр настроек
    settings = Settings()

    # Получаем строку подключения к базе данных
    dsn = settings.DATABASE_URL

    # Словарь symbol: pair_id
    symbols = BINANCE_PAIRS

    # Создаем экземпляр базы данных
    db = AsyncDatabase(dsn)

    # Подключаемся к базе данных
    await db.connect()

    try:
        # Используем одно соединение для всех задач
        async with await db.get_connection() as connection:  # Добавлен await
            async with aiohttp.ClientSession() as session:
                # Создаем задачи для каждого символа
                tasks = [
                    process_symbol(session, db, symbol, pair_id)
                    for symbol, pair_id in symbols.items()
                ]

                # Запускаем все задачи одновременно
                await asyncio.gather(*tasks)
    finally:
        # Закрываем соединение с базой данных
        await db.close()

# Запуск асинхронного кода
asyncio.run(main())