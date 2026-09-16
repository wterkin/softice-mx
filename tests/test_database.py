from unittest import TestCase
import json
import asyncio

from softice import database
from softice import config

class CTestDataBase(TestCase):


    def setUp(self) -> None:

        self.config = config.Config("test_config.yaml")
        self.database: database.CDataBase = database.CDataBase(self.config, "softice-test")


    def test_connect(self):

        result = asyncio.run(self.database.connect())
        self.assertTrue(result)


    def test_commit_changes(self):

        async def run_test():

            result = await self.database.connect()

            if result:

                if await self.database.wipe_table(database.CRoom):

                    room = database.CRoom("777", "super_room")
                    result = await self.database.commit_changes(room)
                    self.assertTrue(result)

        asyncio.run(run_test())



    def test_query_data(self):

        async def run_test():

            # result = await self.database.connect()
            if await self.database.connect():

                session = await self.database.get_session()
                query = await self.database.query_data(database.CRoom)
                query.where(database.CRoom.id == '777')
                data = await session().execute(query)
                room = data.scalars().first()
            self.assertEqual(room.froomname, "super_room")
        asyncio.run(run_test())
