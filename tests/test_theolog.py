from unittest import TestCase
import json
from pathlib import Path
import asyncio

from softice import config
from softice import theolog

class CTestTheolog(TestCase):

    def setUp(self) -> None:

        self.config = config.Config("test_config.yaml")
        self.theolog: theolog.CTheolog = theolog.CTheolog(self.config)


    def test_find_by_quote(self):  # ok

        # * Без доп параметров - возвращает случайную строчку из выборки
        result = asyncio.run(theolog.find_by_quote(self.theolog.data_path+"1.txt", "Книга Бытия",
                             "И совершил Бог".lower()))
        self.assertIn("И совершил Бог", result)
        # * Поиск несуществующей строки
        result = asyncio.run(theolog.find_by_quote(self.theolog.data_path+"1.txt", "Книга Бытия",
                             "Хорошо живёт на свете Винни-Пух!".lower()))
        self.assertEqual(result, "")
        # * Полная выборка
        result = asyncio.run(theolog.find_by_quote(self.theolog.data_path+"1.txt", "Книга Бытия",
                             "Бог".lower(), theolog.FULL_SELECTION))
        self.assertIn("И назвал Бог твердь небом",result)
        # * Заданное количество строк
        result = asyncio.run(theolog.find_by_quote(self.theolog.data_path+"1.txt", "Книга Бытия",
                             "совершил".lower(), theolog.NUMBER_OF_LINES+" 3"))
        self.assertEqual(result.count("\n"), 3)
        # * Заданную строчку из выборки
        result = asyncio.run(theolog.find_by_quote(self.theolog.data_path+"1.txt", "Книга Бытия",
                             "Бог".lower(), theolog.SPECIFIED_LINE+" 2"))
        self.assertIn("да будет свет.",result)

    def test_can_process_command(self):

        self.assertTrue(self.theolog.can_process_command(self.config.test_chat, "!вз В начале сотворил"))
        self.assertTrue(self.theolog.can_process_command(self.config.test_chat, "!найтинз Блажен читающий"))
        self.assertTrue(self.theolog.can_process_command(self.config.test_chat, "!bible"))
        self.assertTrue(self.theolog.can_process_command(self.config.test_chat, "!books"))
        self.assertFalse(self.theolog.can_process_command("fakechat", "!bible"))
        self.assertFalse(self.theolog.can_process_command("emptychat", "!книги"))


    def test_can_process_book(self):

        self.assertTrue(self.theolog.can_process_book("быт"))
        self.assertTrue(self.theolog.can_process_book("откр"))
        self.assertFalse(self.theolog.can_process_book("трали"))
        self.assertFalse(self.theolog.can_process_book("вали"))


    def test_find_by_verse_number(self):
        
        result = asyncio.run(self.theolog.find_by_verse_number(0, "Бытие", "1", "1", 1))
        self.assertIn("небо и землю", result)
        result = asyncio.run(self.theolog.find_by_verse_number(0, "Бытие", "1", "2", 1))
        self.assertIn("и тьма над бездною", result)
        result = asyncio.run(self.theolog.find_by_verse_number(0, "Бытие", "1", "211", 1))
        self.assertEqual(result, "")
        result = asyncio.run(self.theolog.find_by_verse_number(0, "Бытие", "111", "1", 1))
        self.assertEqual(result, "")
        result = asyncio.run(self.theolog.find_by_verse_number(0, "Бытие", "1", "12", 3))
        self.assertIn("И был вечер, и было утро", result)


    def test_get_commands(self):

        self.assertIn("найтинз, нз, findnew, fn",
                      self.theolog.get_commands(self.config.test_chat))
        self.assertEqual(self.theolog.get_commands("fakechat"), "")
        self.assertEqual(self.theolog.get_commands("emptychat"), "")        

    def test_get_books(self):
        
        # def get_books(self, pchat_title: str) -> str:
        self.assertIn("Бытие", self.theolog.get_books(self.config.test_chat))
        self.assertIn("", self.theolog.get_books("fakechat"))
        self.assertIn("", self.theolog.get_books("emptychat"))        

    def test_get_hint(self):
        
        self.assertIn("библия, бб, bible, bb", self.theolog.get_hint(self.config.test_chat))
        self.assertIn("", self.theolog.get_hint("fakechat"))
        self.assertIn("", self.theolog.get_hint("emptychat"))        


    def test_find_in_testament(self):
        
        # async def find_in_testament(self, ptestament: str, pphrase: str,
        #                             pfull_selection: bool = False,
        #                             pnumber_of_lines: int = DEFAULT_NUMBER_OF_LINES,
        #                             pspecified_line: int = DEFAULT_SPECIFIED_LINE):
        #result = asyncio.run(self.find.theolog_in_testament(0, "Бытие", "1", "1", 1))
        #self.assertIn("глава 22 стих 1 : И показал мне чистую реку воды жизни", \
        #              self.theolog.global_search("найтинз", "чистую реку воды жизни"))
        #self.assertEqual(self.theolog.global_search("найтинз", "трали-вали"), "")
        # ищем несуществующую фразу
        result = asyncio.run(self.theolog.find_in_testament("вз", "Хорошо живёт на свете Винни-Пух!".lower(), False, 1, 0))
        self.assertEqual(result, "")
        # full selection
        result = asyncio.run(self.theolog.find_in_testament("вз", "и назвал", True, 1, 0))     
        self.assertIn("сушу землею", result)
        # number_of_line
        # specified_line
        # random
