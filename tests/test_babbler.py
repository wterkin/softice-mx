import sys
from time import sleep
from unittest import TestCase
import json
import uuid
from sys import platform

# import constants as cn
sys.path.insert(0, "tests/")
import softice
from softice.config import Config
from softice import babbler
import asyncio

UNIT_CONFIG: str = "unittest_config.json"

class CTestBabbler(TestCase):

    def setUp(self) -> None:

        self.config = Config("test_config.yaml")
        self.babbler = babbler.CBabbler(self.config)


    def test_babbler(self):

        result = asyncio.run(self.babbler.babbler(self.config.test_chat, self.config.master, "!blreload"))
        self.assertEqual(result, "База болтуна обновлена")
        result = asyncio.run(self.babbler.babbler("superchat", "username", "!blreload"))
        self.assertNotEqual(result, "База болтуна обновлена")


    def test_reload(self):

        result = asyncio.run(self.babbler.reload())
        self.assertTrue(result)


    def test_talk(self):

        result = asyncio.run(self.babbler.reload())
        sleep(int(self.config.babbler["period"]))
        result = asyncio.run(self.babbler.talk(self.config.test_chat, "Привет"))
        self.assertEqual(result, ("Здорово!", ""))
        result = asyncio.run(self.babbler.talk(self.config.test_chat, "Хай"))
        self.assertEqual(result, ("", ""))


    def test_think(self):

        result = asyncio.run(self.babbler.reload())
        result = asyncio.run(self.babbler.think("Спасибо, бот")) 
        self.assertEqual(result, ("Пожалуйста.", ""))
        result = asyncio.run(self.babbler.think("Спасибо")) 
        self.assertEqual(result, ("", ""))
        result = asyncio.run(self.babbler.think("чаю")) 
        self.assertEqual(result[0], "Обязательно!")
        self.assertIn("test_data/babbler/reactions/images/tea.jpg", result[1])        
                             
