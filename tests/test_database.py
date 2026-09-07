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
        self.assertEqual(result, True)


    def test_create(self):


        result = asyncio.run(self.database.connect())
        if result:

            result = asyncio.run(self.database.create())
            self.assertEqual(result, True)


    def test_commit_changes(self):


        result = asyncio.run(self.database.connect())
        if result:

            room: database.CRoom = database.CRoom("777", "super_room")
            result = asyncio.run(self.database.commit_changes(room))

            self.assertTrue(result)


    def test_query_data(self):

        query = asyncio.run(self.database.query_data(database.CRoom))
        query.where(database.CRoom.id == '777')
        room: database.CRoom = query.scalars.first()
        self.assertEqual(room.name, "super_room")
