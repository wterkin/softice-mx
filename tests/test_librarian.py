from unittest import TestCase
import json
from softice import librarian
from softice import config

from pathlib import Path
from sys import platform
import asyncio

class CTestLibrarian(TestCase):

    def setUp(self) -> None:

        self.config = config.Config("test_config.yaml")
        self.librarian: librarian.CLibrarian = librarian.CLibrarian(self.config)


    def test_find_in_book(self):

        book: list = ["Не экономь на душе. Не наготовить запасов там, где должно трудиться сердце. Отдать - значит перебросить мост через бездну своего одиночества. Антуан де Сент-Экзюпери", "Мы думаем, что Бог видит нас сверху - но Он видит нас изнутри..."]
        word_list: list = "Мы думаем".split(" ")
        asyncio.run(self.librarian.reload())
        self.assertEqual(librarian.find_in_book(book, word_list), "[2]"+book[1])


    def test_get_command(self):

        self.assertEqual(librarian.get_command("qt"), librarian.ASK_QUOTE_CMD)
        self.assertEqual(librarian.get_command("qt?"), librarian.FIND_QUOTE_CMD)
        self.assertEqual(librarian.get_command("qt+"), librarian.ADD_QUOTE_CMD)
        self.assertEqual(librarian.get_command("qt-"), librarian.DEL_QUOTE_CMD)


    def test_quote(self):

        asyncio.run(self.librarian.reload())
        self.assertEqual(librarian.quote(["No fate.",], [""],), "[1] No fate.")
        self.assertEqual(librarian.quote(["No fate.",], ["qt", "0"],), "Номер должен быть больше нуля")
        self.assertEqual(librarian.quote(["No fate.",], ["qt", "5"],), "Номер должен быть от 1 до 1")
        self.assertEqual(librarian.quote(["No fate.",], ["fate"],), "[1] No fate.")
        self.assertEqual(librarian.quote(["No fate.",], ["1"],), "[1] No fate.")


    def test_can_class_process(self):

        self.assertTrue(self.librarian.can_class_process(self.config.test_chat, '!цт'))
        self.assertFalse(self.librarian.can_class_process('fakechat', '!цт'))
        self.assertFalse(self.librarian.can_class_process('empttychat', '!хквс'))


    def test_execute_quotes_commands(self):

        asyncio.run(self.librarian.reload())
        result = "Мы думаем, что Бог видит нас сверху - но Он видит нас изнутри..."
        self.assertIn(result, self.librarian.execute_quotes_commands(self.config.master, [""], librarian.ASK_QUOTE_CMD))

        quote = "Нет у тебя, человек, ничего, кроме души. Пифагор"
        self.assertIn(f"Спасибо, {self.config.master}, цитата добавлена под номером 2",
                      self.librarian.execute_quotes_commands(self.config.master,
                                                     ["qt+", quote], librarian.ADD_QUOTE_CMD))
        self.assertIn("Цитата 2 удалена",
                      self.librarian.execute_quotes_commands(self.config.master,
                      ["hk-", "2"], librarian.DEL_QUOTE_CMD))
        # Запрос на удаление от нелегитимного лица
        result = f"Извини, User, только {self.config.master} может удалять цитаты"
        self.assertIn(result, self.librarian.execute_quotes_commands("User", ["hk-", "1"], librarian.DEL_QUOTE_CMD))


    def test_get_help(self):

        self.assertNotEqual(self.librarian.get_help(self.config.test_chat), "")
        self.assertEqual(self.librarian.get_help("fakechat"), "")
        self.assertEqual(self.librarian.get_help("emptychat"), "")


    def test_get_hint(self):

        self.assertNotEqual(self.librarian.get_hint(self.config.test_chat), "")
        self.assertEqual(self.librarian.get_hint("fakechat"), "")
        self.assertEqual(self.librarian.get_hint("emptychat"), "")


    def test_librarian(self):

        result = asyncio.run(self.librarian.librarian('fakechat', 'User', '!lbreload'))
        self.assertEqual(result, "")
        result = asyncio.run(self.librarian.librarian('emptychat', 'User', '!lbreload'))
        self.assertEqual(result, "")
        result = asyncio.run(self.librarian.librarian(self.config.test_chat,
                                                      self.config.master, '!lbreload'))
        self.assertEqual(result, "Книга обновлена")
        result = asyncio.run(self.librarian.librarian(self.config.test_chat, 'User', '!lbreload'))
        self.assertEqual(result, f"Извини, User, только {self.config.master} может перегружать цитаты!")
        result = asyncio.run(self.librarian.librarian('fakechat', 'User', '!lbsave'))
        self.assertEqual(result, "")
        result = asyncio.run(self.librarian.librarian('emptychat', 'User', '!lbsave'))
        self.assertEqual(result , "")
        result = asyncio.run(self.librarian.librarian(self.config.test_chat,
                                                      self.config.master, "!lbsave"))
        self.assertEqual(result, "Книга сохранена")
        result = asyncio.run(self.librarian.librarian(self.config.test_chat, "User", '!lbsave'))
        self.assertEqual(result, f"Извини, User, только {self.config.master} может сохранять цитаты!")
        result = asyncio.run(self.librarian.librarian(self.config.test_chat, 'user', '!библиотека'))
        self.assertIn("quoteadd", result)
        result = asyncio.run(self.librarian.librarian("fakechat", 'user', '!библиотека'))
        self.assertEqual(result, "")
        result = asyncio.run(self.librarian.librarian("emptychat", 'user', '!библиотека'))
        self.assertEqual(result, "")
        result = asyncio.run(self.librarian.librarian(self.config.test_chat,
                                                      self.config.master, "!qt+ No fate"))
        self.assertIn(f"Спасибо, {self.config.master}, цитата добавлена под номером 2", result)
        result = asyncio.run(self.librarian.librarian(self.config.test_chat,
                                                      self.config.master, "!qt- 2"))
        self.assertIn("Цитата 2 удалена", result)
        result = asyncio.run(self.librarian.librarian(self.config.test_chat, "User", "!qt- 2"))
        self.assertEqual(result, f"Извини, User, только {self.config.master} может удалять цитаты")
        result = asyncio.run(self.librarian.librarian(self.config.test_chat, "User", "!qt"))
        self.assertEqual(result, "[1] Мы думаем, что Бог видит нас сверху - но Он видит нас изнутри...")

    def tearDown(self):

        for file in Path(self.librarian.data_path).glob("quotes.txt_*"):

            file.unlink()
