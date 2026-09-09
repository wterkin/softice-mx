from unittest import TestCase
import json
import asyncio

from softice import database
from softice import config

class CTestDataBase(TestCase):


    @classmethod
    def setUpClass(cls):

        # Один раз перед всеми тестами
        cls.database = database.CDataBase(self.config, "softice-test")
        async def do_connect():

            return await cls.database.connect()
        ok = asyncio.run(do_connect())
        assert ok, "Не удалось подключиться в setUpClass"


    def setUp(self) -> None:

        self.config = config.Config("test_config.yaml")
        self.database: database.CDataBase = database.CDataBase(self.config, "softice-test")


    def test_connect(self):

        self.assertTrue(self.database.connected)
    """
    def test_create(self):

        async def run_test():

            result = await self.database.connect()

            if result:

                result = await self.database.create()
                self.assertEqual(result, True)
        asyncio.run(run_test())

    """


    def test_commit_changes(self):

        room = database.CRoom("777", "super_room")
        result = asyncio.run(self.database.commit_changes(room))
        self.assertTrue(result)



    """
    def test_query_data(self):

        result = asyncio.run(self.database.connect())
        if result:

            session = asyncio.run(self.database.get_session())
            query = asyncio.run(self.database.query_data(database.CRoom))
            query.where(database.CRoom.id == '777')
            result = asyncio.run(session().execute(query))
            rows = result.scalars()
            room: database.CRoom = rows.first()
            self.assertEqual(room.froomname, "super_room")
    """
    @classmethod
    def tearDownClass(cls):
        # Один раз после всех тестов

        async def do_close():

            await cls.database.close()  # важно: закрыть движок и пул
        asyncio.run(do_close())
