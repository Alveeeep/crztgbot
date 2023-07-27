import asyncpg
from typing import List
from asyncpg import Record


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_data(self, user_id, user_name, user_defy):
        query = f"INSERT INTO datausers (user_id, user_name, user_defy) VALUES ({user_id}, '{user_name}', '{user_defy}') ON CONFLICT (user_id) DO UPDATE SET user_name='{user_name}';"
        await self.connector.execute(query)

    async def check_table(self, name_table):
        query = f"SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = '{name_table}');"
        return await self.connector.fetchval(query)

    async def create_table(self, name_table, choice):
        query = f"CREATE TABLE {name_table} (user_id bigint NOT NULL, statuse text, description text, PRIMARY KEY (user_id));"
        await self.connector.execute(query)
        if choice == 'zakazchik' or choice == 'postavchik':
            query = f"INSERT INTO {name_table} (user_id, statuse, description) SELECT user_id, 'waiting', null FROM datausers WHERE user_defy='{choice}' or user_defy='oba'"
        elif choice == 'oba':
            query = f"INSERT INTO {name_table} (user_id, statuse, description) SELECT user_id, 'waiting', null FROM datausers"
        await self.connector.execute(query)

    async def delete_table(self, name_table):
        query = f"DROP TABLE {name_table};"
        await self.connector.execute(query)

