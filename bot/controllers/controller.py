from typing import List
from bot.db.database import db
from bot.helpers.config import GET, POST, PUT, DELETE, COUNT, SINGLE, ALL


class Controller:
    def __init__(self, model):
        self.model = model

    async def process(self, method: str, query: dict, count: str = '', is_paginating: bool = False, data=None):
        result = ''

        if method == GET:
            result = self.model.query
        elif method == DELETE:
            result = self.model.delete
        elif method == PUT:
            result = self.model.update.values(data)
        if method == COUNT:
            result = db.select([db.func.count()]).select_from(self.model)

        if query:
            for key, value in query.items():
                column = getattr(self.model, key, None)
                if column is not None:
                    result = result.where(column == value)

                    if is_paginating:
                        result = result.limit(data['limit']).offset(data['offset'])

        if method in [DELETE, PUT]:
            result = await result.gino.status()
        if method == COUNT:
            result = await result.gino.scalar()
        if count:
            if count == SINGLE:
                result = await result.gino.first()
            elif count == ALL:
                result = await result.gino.all()

        return result

    async def get_all(self, query: dict) -> List:
        try:
            return await self.process(method=GET, query=query, count=ALL)
        except Exception as error:
            print(error)

    async def get_one(self, query: dict):
        try:
            return await self.process(method=GET, query=query, count=SINGLE)
        except Exception as error:
            print(error)

    async def get_pagination(self, query: dict, offset: int, limit: int) -> List:
        try:
            return await self.process(
                method=GET, query=query, count=ALL, is_paginating=True, data=dict(offset=offset, limit=limit)
            )
        except Exception as error:
            print(error)

    async def make(self, data: dict):
        try:
            return await self.model.create(**data)
        except Exception as error:
            print(error)

    async def update(self, query: dict, data: dict):
        try:
            return await self.process(method=PUT, query=query, data=data)
        except Exception as error:
            print(error)

    async def delete(self, query: dict):
        try:
            return await self.process(method=DELETE, query=query)
        except Exception as error:
            print(error)

    async def count(self, query: dict):
        try:
            return await self.process(method=COUNT, query=query)
        except Exception as error:
            print(error)