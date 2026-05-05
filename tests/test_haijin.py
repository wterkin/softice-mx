from unittest import TestCase
import json
from sys import platform
from pathlib import Path
import os
import logging
import asyncio

from softice import haijin
from softice import config

class CTestHaijin(TestCase):

    def setUp(self) -> None:

        self.config = config.Config("test_config.yaml")
        self.haijin: haijin.CHaijin = haijin.CHaijin(self.config)


    def test_can_class_process(self):

        self.assertFalse(self.haijin.can_class_process("fakechat", "!hk"))
        self.assertFalse(self.haijin.can_class_process("emptychat", "!хк+"))
        self.assertTrue(self.haijin.can_class_process(self.config.test_chat, "!хк"))
        self.assertTrue(self.haijin.can_class_process(self.config.test_chat, "!хк+"))
        self.assertTrue(self.haijin.can_class_process(self.config.test_chat, "!хк-"))
        self.assertTrue(self.haijin.can_class_process(self.config.test_chat, "!hksv"))
        self.assertTrue(self.haijin.can_class_process(self.config.test_chat, "!hkrl"))
        self.assertTrue(self.haijin.can_class_process(self.config.test_chat, "!hokku"))
        self.assertFalse(self.haijin.can_class_process(self.config.test_chat, "!кукабарра"))

       
    def test_format_hokku(self):

        asyncio.run(self.haijin.reload())
        text: str = "[1] Печальный мир. \n Даже когда расцветают вишни..  Даже тогда...  (Исса) "
        result_text: str = (f"<i> Печальный мир. \n Даже когда расцветают вишни..  Даже тогда...   </i> \n"
                            f"{haijin.AUTHOR_INDENT} <b>Исса</b> {haijin.DELIMITER} 1 {haijin.DELIMITER} 1")
        formatted_text: str = self.haijin.format_hokku(text)
        self.assertEqual(formatted_text, result_text)
  
        
    def test_get_help(self):

        self.assertIn("хк, hk : получить случайное хокку, \n", self.haijin.get_help(self.config.test_chat))


    def test_get_hint(self):

        self.assertIn("хокку, hokku", self.haijin.get_hint(self.config.test_chat))


    def test_get_command(self):

        self.assertEqual(self.haijin.identify_command("hk", haijin.HAIJIN_COMMANDS), haijin.ASK_HOKKU_CMD)
        self.assertEqual(self.haijin.identify_command("hk+", haijin.HAIJIN_COMMANDS), haijin.ADD_HOKKU_CMD)
        self.assertEqual(self.haijin.identify_command("hk-", haijin.HAIJIN_COMMANDS), haijin.DEL_HOKKU_CMD)
      

    def test_haijin(self):
    
        result = asyncio.run(self.haijin.haijin(self.config.test_chat, self.config.master, "!hkrl"))
        self.assertEqual(result, "Книга загружена")
        result = asyncio.run(self.haijin.haijin(self.config.test_chat, self.config.master,"!hksv"))
        self.assertEqual(result, "Книга сохранена")
        for file in Path(self.haijin.data_path).glob("hokku.txt_*"):

            file.unlink()

        self.assertIn("хк, hk : получить случайное хокку, \n",             self.haijin.get_help(self.config.test_chat))

    def test_is_enabled(self):

        self.assertFalse(self.haijin.is_enabled("fakechat", haijin.UNIT_ID))
        self.assertFalse(self.haijin.is_enabled("emptychat", haijin.UNIT_ID))
        self.assertTrue(self.haijin.is_enabled(self.config.test_chat, haijin.UNIT_ID))


    def test_is_master(self):

        self.assertEqual(self.haijin.is_master("user"), False)
        self.assertTrue(self.haijin.is_master(self.config.master)) #, self.config["master_name"]))


    def test_process_command(self):

        asyncio.run(self.haijin.reload())
        
        answer = "[1] Печальный мир. / Даже когда расцветают вишни.. / Даже тогда... (Исса)"
        result = asyncio.run(self.haijin.process_command(["hk"], self.config.master))
        self.assertIn(answer, result)
        
        hokku = "Утром / Тихонько упал на землю / С дерева лист. (Кобаяси Исса)"
        result = asyncio.run(self.haijin.process_command(["hk+", hokku],                                                     self.config.master))
        self.assertIn("Спасибо, Namo, хокку добавлено под номером 2", result)
        
        result = asyncio.run(self.haijin.process_command(["hk-", "2"],self.config.master))
        self.assertIn("Хокку 2 удалена.", result)
        
        # Запрос на удаление от нелегитимного лица
        answer = "Извини, User, только @namo:sibnsk.net может удалять хокку"
        result = result = asyncio.run(self.haijin.process_command(["hk-", "1"], "user"))
        self.assertIn(answer, result)
        
