from unittest import TestCase
from sys import platform

from softice import config  
from softice import barman
#import test_softice
import asyncio

class CTestBarman(TestCase):

    def setUp(self) -> None:

        self.config = config.Config("test_config.yaml")
        self.barman: barman.CBarman = barman.CBarman(self.config)


    def test_barman(self):

        asyncio.run(self.barman.reload())
        result = asyncio.run(self.barman.barman(self.config.test_chat, self.config.master, "!пиво"))
        self.assertNotEqual(result, "")
        result = asyncio.run(self.barman.barman(self.config.test_chat, self.config.master,"!пиво User"))
        self.assertIn("User", result)
        result = asyncio.run(self.barman.barman(self.config.test_chat, self.config.master, "!виски"))
        self.assertEqual(result, "")
        result = asyncio.run(self.barman.barman(self.config.test_chat, self.config.master, "!bar"))
        self.assertIn("Сегодня в баре", result)
        result = asyncio.run(self.barman.barman(self.config.test_chat, self.config.master, "!brreload"))
        self.assertEqual(result, "Ассортимент бара обновлён.")
        result = asyncio.run(self.barman.barman(self.config.test_chat, "user", "!brreload"))
        self.assertIn("У вас нет на это прав", result) 


    def test_can_class_process(self):

        self.assertFalse(self.barman.can_class_process("fakechat", "!пиво"))
        self.assertFalse(self.barman.can_class_process("emptychat", "!beer"))
        self.assertTrue(self.barman.can_class_process(self.config.test_chat, "!beer"))
        self.assertFalse(self.barman.can_class_process(self.config.test_chat, "!кукабарра"))
        self.assertTrue(self.barman.can_class_process(self.config.test_chat,  "!bar"))
        self.assertTrue(self.barman.can_class_process(self.config.test_chat,  "!brreload"))


    def test_get_help(self):

        self.assertEqual(self.barman.get_help("fakechat"), "")
        self.assertEqual(self.barman.get_help("emptychat"), "")
        self.assertIn("чай, tea, чй, te", self.barman.get_help(self.config.test_chat))

    def test_get_hint(self):

        self.assertEqual(self.barman.get_hint("fakechat"), "")
        self.assertEqual(self.barman.get_hint("emptychat"), "")
        self.assertIn("бар, bar", self.barman.get_hint(self.config.test_chat))


    def test_is_enabled(self):


        self.assertFalse(self.barman.is_enabled("fakechat", barman.UNIT_ID))
        self.assertFalse(self.barman.is_enabled("emptychat", barman.UNIT_ID))
        self.assertTrue(self.barman.is_enabled(self.config.test_chat, barman.UNIT_ID))


    def test_is_master(self):

        self.assertFalse(self.barman.is_master("user"))
        self.assertTrue(self.barman.is_master(self.config.master))


    def test_serve_client(self):
        
        asyncio.run(self.barman.reload())
        self.assertIn("Балтика", self.barman.serve_client(self.config.master, "пиво"))
        self.assertIn("Балтика", self.barman.serve_client("Юзер", "beer"))
        self.assertEqual(self.barman.serve_client("Юзер", "кузинатра"), "")
