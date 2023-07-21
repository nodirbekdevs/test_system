from typing import List


class Controller:
    def __init__(self, model):
        self.model = model

    async def get_all(self, query: dict) -> List:
        try:
            return await self.model.query.where(**query).gino.all()
        except Exception as error:
            print(error)

    async def get_one(self, query):
        try:
            return await self.model.query.where(query).gino.first()
        except Exception as error:
            print(error)

    async def get_pagination(self, query: dict, offset: int, limit: int) -> List:
        try:
            return await self.model.query.where(query).offset(offset).limit(limit).gino.all()
        except Exception as error:
            print(error)

    async def make(self, data: dict):
        try:
            return await self.model.create(**data)
        except Exception as error:
            print(error)

    async def update(self, query: dict, data: dict):
        try:
            await self.model.update.values(data).where(query).gino.status()
        except Exception as error:
            print(error)

    async def increment(self, query: dict, data: dict):
        try:
            await self.model.update.values(data).where(query).gino.status()
        except Exception as error:
            print(error)

    async def delete(self, query: dict):
        try:
            await self.model.delete.where(query).gino.status()
        except Exception as error:
            print(error)

    async def count(self, query: dict):
        try:
            return await self.model.query.where(query).gino.scalar()
        except Exception as error:
            print(error)


# import asyncpg
#
#
# class Controller:
#     dsn = DB_URL
#
#     def __init__(self, model_type):
#         self.connection = None
#         self.type = model_type
#
#     async def connect(self):
#         self.connection = await asyncpg.connect(
#             dsn=self.dsn,
#         )
#
#     async def disconnect(self):
#         if self.connection:
#             await self.connection.close()
#
#     async def execute_query(self, query, data=None):
#         if not self.connection:
#             raise Exception('Not connected to the database.')
#
#         result = dict()
#
#         if data:
#             result = await self.connection.fetch(query, data)
#         elif not data:
#             result = await self.connection.fetch(query)
#
#         return result
#
#     async def get_users(self, condition, *datas):
#         await self.connect()
#
#         query = 'SELECT * FROM users'
#         if condition:
#             query += f' WHERE {condition}'
#
#         response = await self.execute_query(query, *datas)
#
#         if len(response) != 0:
#             return None
#
#         return response
#
#     async def create_user(self, data: dict):
#         await self.connect()
#         columns = ', '.join(data.keys())
#         # values = ', '.join(f'${i + 1}' for i in range(len(data)))
#         query = f'INSERT INTO {self.type} ({columns}) VALUES ({data.values()})'
#
#         response = await self.execute_query(query)
#
#         await self.disconnect()
#
#         if not response:
#             return None
#
#         return response
#
#     async def get_one(self, key, value):
#         await self.connect()
#
#         query = f'SELECT * FROM {self.type} WHERE {key} = {value}'
#
#         response = await self.execute_query(query)
#
#         await self.disconnect()
#
#         if not response:
#             return None
#
#         return dict(response[0])
#
#
#
#     async def update_user(self, user_id: int, data: dict):
#         try:
#             async with self.connection_pool.acquire() as connection:
#                 set_clause = ', '.join(f'{key} = ${i+1}' for i, key in enumerate(data.keys()))
#                 query = f'UPDATE users SET {set_clause} WHERE id = $1'
#                 return await connection.execute(query, user_id, *data.values())
#         except Exception as error:
#             print(error)
#
#     async def delete_user(self, user_id: int):
#         try:
#             async with self.connection_pool.acquire() as connection:
#                 query = 'DELETE FROM users WHERE id = $1'
#                 return await connection.execute(query, user_id)
#         except Exception as error:
#             print(error)