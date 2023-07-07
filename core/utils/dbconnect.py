import asyncpg
from typing import List
from asyncpg import Record


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_trigger(self, name_trigger, value_trigger):
        query = f"INSERT INTO trigger_table (name_trigger, value_trigger) VALUES ('{name_trigger}', '{value_trigger}') " \
                f"ON CONFLICT (name_trigger) " \
                f"DO UPDATE SET value_trigger=trigger_table.value_trigger || '\r\n' || excluded.value_trigger"
        await self.connector.execute(query)

    async def get_triggers(self):
        query = f"SELECT name_trigger FROM trigger_table ORDER BY name_trigger"
        result_list: List[Record] = await self.connector.fetch(query)
        return '\r\n'.join([f"`#{result.get('name_trigger')}`" for result in result_list])

    async def get_values(self, name_trigger):
        query = f"SELECT value_trigger FROM trigger_table WHERE name_trigger='{name_trigger}'"
        return await self.connector.fetchval(query)
