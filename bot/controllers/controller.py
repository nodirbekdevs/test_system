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
            print(self.model)
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