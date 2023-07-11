import asyncpg
from typing import List
from asyncpg import Record


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_data(self, user_id, user_name):
        query = f"INSERT INTO datausers (user_id, user_name) VALUES ({user_id}, '{user_name}') ON CONFLICT (user_id) DO UPDATE SET user_name='{user_name}';"
        await self.connector.execute(query)

    async def check_table(self, name_table):
        query = f"SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = '{name_table}';"
        return await self.connector.fetchval(query)

    async def create_table(self, name_table):
        query = f"CREATE TABLE {name_table} (user_id bigint NOT NULL, statuse text, description text, PRIMARY KEY (user_id));"
        await self.connector.execute(query)
        query = f"INSERT INTO {name_table} (user_id, statuse, description) SELECT user_id, 'waiting', null FROM users;"
        await self.connector.execute(query)

    async def delete_table(self, name_table):
        query = f"DROP TABLE {name_table}"
        await self.connector.execute(query)

    # async def add_trigger(self, name_trigger, value_trigger):
    #    query = f"INSERT INTO trigger_table (name_trigger, value_trigger) VALUES ('{name_trigger}', '{value_trigger}') " \
    #            f"ON CONFLICT (name_trigger) " \
    #            f"DO UPDATE SET value_trigger=trigger_table.value_trigger || '\r\n' || excluded.value_trigger"
    #    await self.connector.execute(query)
#
# async def get_triggers(self):
#    query = f"SELECT name_trigger FROM trigger_table ORDER BY name_trigger"
#    result_list: List[Record] = await self.connector.fetch(query)
#    return '\r\n'.join([f"`#{result.get('name_trigger')}`" for result in result_list])
#
# async def get_values(self, name_trigger):
#    query = f"SELECT value_trigger FROM trigger_table WHERE name_trigger='{name_trigger}'"
#    return await self.connector.fetchval(query)
