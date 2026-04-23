from unittest import TestCase
import json
from softice import librarian
from softice import config

from pathlib import Path
from sys import platform


class CTestLibrarian(TestCase):

    def setUp(self) -> None:

        self.config = config.Config("test_config.yaml")
        self.librarian: librarian.CLibrarian = librarian.CLibrarian(self.config, self.config.data_folder)


    async def test_find_in_book(self):
        
        book: list = ["Не экономь на душе. Не наготовить запасов там, где должно трудиться сердце. Отдать - значит перебросить мост через бездну своего одиночества. Антуан де Сент-Экзюпери", "Мы думаем, что Бог видит нас сверху - но Он видит нас изнутри..."]
        word_list: list = "Мы думаем".split(" ")
        await self.librarian.reload()
        self.assertEqual(librarian.find_in_book(book, word_list), "[2]"+book[1])
        
        
    def test_get_command(self):
        
        self.assertEqual(librarian.get_command("qt"), librarian.ASK_QUOTE_CMD)
        self.assertEqual(librarian.get_command("qt?"), librarian.FIND_QUOTE_CMD)
        self.assertEqual(librarian.get_command("qt+"), librarian.ADD_QUOTE_CMD)
        self.assertEqual(librarian.get_command("qt-"), librarian.DEL_QUOTE_CMD)


    async def test_quote(self):
        
        await self.librarian.reload()
        self.assertEqual(librarian.quote(["No fate.",], [""],), "[1] No fate.")
        self.assertEqual(librarian.quote(["No fate.",], ["qt", "0"],), "Номер должен быть больше нуля")
        self.assertEqual(librarian.quote(["No fate.",], ["qt", "5"],), "Номер должен быть от 1 до 1")
        self.assertEqual(librarian.quote(["No fate.",], ["fate"],), "[1] No fate.")
        self.assertEqual(librarian.quote(["No fate.",], ["1"],), "[1] No fate.")
        
    
    def test_can_process(self):
        
        self.assertTrue(self.librarian.can_process(test_softice.TESTPLACE_CHAT_NAME, '!цт'))
        self.assertFalse(self.librarian.can_process('fakechat', '!цт'))
        self.assertFalse(self.librarian.can_process('empttychat', '!хквс'))


    async def test_execute_quotes_commands(self):

        await self.librarian.reload()
        result = "Мы думаем, что Бог видит нас сверху - но Он видит нас изнутри..."
        self.assertIn(result, self.librarian.execute_quotes_commands(self.config["master"], self.config["master_name"],
                                                                     [""], librarian.ASK_QUOTE_CMD))

        quote = "Нет у тебя, человек, ничего, кроме души. Пифагор"
        self.assertIn("Спасибо, Петрович, цитата добавлена под номером 2",
                      self.librarian.execute_quotes_commands(self.config["master"], self.config["master_name"],
                                                     ["qt+", quote], librarian.ADD_QUOTE_CMD))
        self.assertIn("Цитата 2 удалена", 
                      self.librarian.execute_quotes_commands(self.config["master"], self.config["master_name"],
                      ["hk-", "2"], librarian.DEL_QUOTE_CMD))
        # Запрос на удаление от нелегитимного лица
        result = "Извини, User, только Петрович может удалять цитаты"
        self.assertIn(result, self.librarian.execute_quotes_commands("user", "User", ["hk-", "1"], librarian.DEL_QUOTE_CMD))


    def test_get_help(self):
        
        self.assertNotEqual(self.librarian.get_help(self.config.test_chat), "")
        self.assertEqual(self.librarian.get_help("fakechat"), "")
        self.assertEqual(self.librarian.get_help("emptychat"), "")


    def test_get_hint(self):
        
        self.assertNotEqual(self.librarian.get_hint(self.config.test_chat), "")
        self.assertEqual(self.librarian.get_hint("fakechat"), "")
        self.assertEqual(self.librarian.get_hint("emptychat"), "")

    """
    def test_is_enabled(self):
        
        self.assertTrue(self.librarian.is_enabled(self.config.test_chat))
        self.assertFalse(self.librarian.is_enabled("fakechat"))
        self.assertFalse(self.librarian.is_enabled("emptychat"))


    def test_is_master(self):
        
        self.assertTrue(self.librarian.is_master(self.config.master, self.config["master_name"]))
        self.assertEqual(self.librarian.is_master('User', 'Юзер'), (False, 'У вас нет на это прав, Юзер.'))
       
    """
    def test_librarian(self):

        self.assertEqual(self.librarian.librarian('fakechat', 'User', '!lbreload'), "")
        self.assertEqual(self.librarian.librarian('emptychat', 'User', '!lbreload'), "")
        self.assertEqual(self.librarian.librarian(self.config.test_chat, 
                                                  self.config.master, '!lbreload'), "Книга обновлена") 
        self.assertEqual(self.librarian.librarian(self.config.test_chat, 'User', 
                                                  '!lbreload'), f"Извини, Юзер, только Петрович может перегружать цитаты!")
        self.assertEqual(self.librarian.librarian('fakechat', 'User', '!lbsave'), "")
        self.assertEqual(self.librarian.librarian('emptychat', 'User', '!lbsave'), "")
        self.assertEqual(self.librarian.librarian(self.config.test_chat, 
                                                  self.config.master, "!lbsave"),
                                                  "Книга сохранена") 
        self.assertEqual(self.librarian.librarian(self.config.test_chat, "User",
                                                  '!lbsave'), "Извини, Юзер, только Петрович может сохранять цитаты!")
        self.assertIn("quoteadd", self.librarian.librarian(self.config.test_chat, 'user', 'Юзер', '!библиотека'))
        self.assertEqual(self.librarian.librarian("fakechat", 'user', '!библиотека'), "")
        self.assertEqual(self.librarian.librarian("emptychat", 'user', '!библиотека'), "")
        self.assertIn("Спасибо, Петрович, цитата добавлена под номером 2",
                      self.librarian.librarian(self.config.test_chat, 
                                               self.config.master, "!qt+ No fate"))
        self.assertIn("Цитата 2 удалена", 
                      self.librarian.librarian(self.config.test_chat,
                                               self.config.master, "!qt- 2"))

        self.assertEqual(self.librarian.librarian(self.config.test_chat, "user", "!qt- 2"),
                                                  "Извини, Юзер, только Петрович может удалять цитаты")     
        self.assertEqual(self.librarian.librarian(self.config.test_chat, "user", "!qt"), 
                                             "[1] Мы думаем, что Бог видит нас сверху - но Он видит нас изнутри...")

    def tearDown(self):

        for file in Path(self.librarian.data_path).glob("quotes.txt_*"):
  
            file.unlink()
