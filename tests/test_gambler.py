from unittest import TestCase
import json
from sys import platform

import softice
from softice import gambler
from softice import config

class CTestGambler(TestCase):


    def setUp(self) -> None:

        self.config = config.Config("test_config.yaml")
        self.gambler: gambler.CGambler = gambler.CGambler(self.config)


    def test_can_class_process(self):

        self.assertFalse(self.gambler.can_class_process("fakechat", "!спок"))
        self.assertFalse(self.gambler.can_class_process("emptychat", "!coin"))
        self.assertTrue(self.gambler.can_class_process(self.config.test_chat, "!камень"))
        self.assertFalse(self.gambler.can_class_process(self.config.test_chat, "!кукабарра"))
        self.assertTrue(self.gambler.can_class_process(self.config.test_chat, "!монета"))


    def test_get_help(self):

        self.assertEqual(self.gambler.get_help("fakechat"), "")
        self.assertEqual(self.gambler.get_help("emptychat"), "")
        self.assertIn("камень", self.gambler.get_help(self.config.test_chat ))
        self.assertIn("спок", self.gambler.get_help(self.config.test_chat))
        self.assertIn("монета", self.gambler.get_help(self.config.test_chat ))
        

    def test_get_hint(self):

        self.assertEqual(self.gambler.get_hint("fakechat"), "")
        self.assertEqual(self.gambler.get_hint("emptychat"), "")
        self.assertIn("игра, game", self.gambler.get_hint(self.config.test_chat))


    def test_is_enabled(self):


        self.assertFalse(self.gambler.is_enabled("fakechat", gambler.UNIT_ID))
        self.assertFalse(self.gambler.is_enabled("emptychat", gambler.UNIT_ID))
        self.assertTrue(self.gambler.is_enabled(self.config.test_chat, gambler.UNIT_ID))
