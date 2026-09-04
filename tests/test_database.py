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

    """
    def test_commit_changes(self):

        
        self.assertEqual(self.database.t("fakechat"), "")
        #self.assertEqual(self.gambler.get_hint("emptychat"), "")
        #self.assertIn("игры, games", self.gambler.get_hint(self.config.test_chat))


    def test_is_enabled(self):


        self.assertFalse(self.gambler.is_enabled("fakechat", gambler.UNIT_ID))
        self.assertFalse(self.gambler.is_enabled("emptychat", gambler.UNIT_ID))
        self.assertTrue(self.gambler.is_enabled(self.config.test_chat, gambler.UNIT_ID))
    """
