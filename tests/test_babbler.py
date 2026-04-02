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
# import test_softice
UNIT_CONFIG: str = "unittest_config.json"

class CTestBabbler(TestCase):

    def setUp(self) -> None:

        self.config = Config("/home/app/Projects/softice-mx/test_config.yaml")
        self.babbler = babbler.CBabbler(self.config)


    def test_babbler(self):

        event: dict = {}
        event[cn.MTEXT] = "!blreload"
        event[cn.MCHAT_TITLE] = test_softice.TESTPLACE_CHAT_NAME
        event[cn.MUSER_NAME] = self.config["master"]
        event[cn.MUSER_TITLE] = self.config["master_name"]
        self.assertEqual(self.babbler.babbler(event), "База болтуна обновлена")
        event[cn.MCHAT_TITLE] = "superchat"
        event[cn.MUSER_NAME] = "username"
        event[cn.MUSER_TITLE] = "usertitle"
        self.assertNotEqual(self.babbler.babbler(event), "База болтуна обновлена")


    def test_reload(self):

        self.assertTrue(self.babbler.reload())


    def test_talk(self):

        sleep(int(self.babbler.config[babbler.BABBLER_PERIOD_KEY]))
        event: dict = {}
        event[cn.MCHAT_TITLE] = test_softice.TESTPLACE_CHAT_NAME
        event[cn.MTEXT] = 'Привет'
        self.assertEqual(self.babbler.talk(event), ("Здорово!", ""))
        event[cn.MTEXT] = 'Хай'
        self.assertEqual(self.babbler.talk(event), ("", ""))


    def test_think(self):

        event: dict = {}
        event[cn.MCHAT_TITLE] = test_softice.TESTPLACE_CHAT_NAME
        event[cn.MTEXT] = "Спасибо, бот"
        self.assertEqual(self.babbler.think(event), ("Пожалуйста.", ""))
        event[cn.MTEXT] = "Спасибо"
        self.assertEqual(self.babbler.think(event), ("", ""))
        event[cn.MTEXT] = "чаю"
        self.assertEqual(self.babbler.think(event), ("Обязательно!", "test_data/babbler/reactions/images/tea.jpg"))
        event[cn.MTEXT] = 'Привет'
        self.assertEqual(self.babbler.talk(event), ("Здорово!", ""))

