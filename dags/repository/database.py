import asyncpg

class AsyncDatabase:
    def __init__(self, dsn):
        self.dsn = dsn
        self.pool = None

    async def connect(self):
        # Создаем пул соединений
        self.pool = await asyncpg.create_pool(dsn=self.dsn)

    async def get_connection(self):
        # Возвращает соединение из пула
        if self.pool is None:
            await self.connect()
        return self.pool.acquire()

    async def close(self):
        # Закрываем пул соединений
        if self.pool:
            await self.pool.close()

    async def insert_data(self, pair_id, price):
        # Вставляем данные в базу
        async with self.pool.acquire() as connection:
            await connection.execute(
                "INSERT INTO crypto.history_price (pair_id, price) VALUES ($1, $2)",
                pair_id, price
            )