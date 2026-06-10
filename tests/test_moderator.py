from unittest import TestCase
from softice import moderator
from softice import config
import asyncio

class CTestModerator(TestCase):

    def setUp(self) -> None:

        self.config = config.Config("test_config.yaml")
        self.moderator: moderator.CModerator = moderator.CModerator(self.config, None)

    def test_replace_bad_words(self):

        self.assertEqual(moderator.replace_bad_words("чатлане","Жадный, как все чатлане"), 
                         f"Жадный, как все *beep*")


    def test_can_process_command(self):

        self.assertFalse(self.moderator.can_process_command("emptychat", "!bwrl"))
        self.assertTrue(self.moderator.can_process_command(self.config.test_chat, "!bwrl"))
        self.assertFalse(self.moderator.can_process_command(self.config.test_chat, "!кукабарра"))

    def test_check_bad_words_ex(self):

        asyncio.run(self.moderator.reload())
        self.assertNotIn("*", self.moderator.check_bad_words_ex("вразумляться"))
        self.assertNotIn("*", self.moderator.check_bad_words_ex("римляныня"))
        self.assertNotIn("*", self.moderator.check_bad_words_ex("земля"))
        self.assertNotIn("*", self.moderator.check_bad_words_ex("земляне"))
        self.assertNotIn("*", self.moderator.check_bad_words_ex("близко"))
        self.assertNotIn("*", self.moderator.check_bad_words_ex("яблоко"))
        self.assertNotIn("*", self.moderator.check_bad_words_ex("блокнот"))
        self.assertNotIn("*", self.moderator.check_bad_words_ex("благородство"))
        self.assertNotIn("*", self.moderator.check_bad_words_ex("пляж"))
        self.assertNotIn("*", self.moderator.check_bad_words_ex("блажь"))
        self.assertNotIn("*", self.moderator.check_bad_words_ex("блог"))
        self.assertNotEqual(self.moderator.check_bad_words_ex("похулить"), "*")
        self.assertNotEqual(self.moderator.check_bad_words_ex("застрахуй"), "*")
        self.assertNotEqual(self.moderator.check_bad_words_ex("похерить"), "*")
        self.assertNotEqual(self.moderator.check_bad_words_ex("парикмахерская"), "*")
        self.assertNotEqual(self.moderator.check_bad_words_ex("пистон"), "*")
        self.assertNotIn("*", self.moderator.check_bad_words_ex("ибо"))
        self.assertNotIn("*", self.moderator.check_bad_words_ex("enjoy"))
        self.assertNotIn("*", self.moderator.check_bad_words_ex("благодарю"))
        self.assertNotIn("*", self.moderator.check_bad_words_ex("плохо"))
    """    
    def test_control_talking(self):
        
        record: dict = {}
        record[cn.MCONTENT_TYPE] = "text"
        record[cn.MTEXT] = "мля"
        record[cn.MCAPTION] = "мля"
        record[cn.MCHAT_TITLE] = test_softice.TESTPLACE_CHAT_NAME
        record[cn.MCHAT_ID] = test_softice.TESTPLACE_CHAT_ID
        record[cn.MMESSAGE_ID] = 0
        record[cn.MUSER_TITLE] = self.config["master_name"]
        record[cn.MUSER_LASTNAME] = ""
        # def __init__(self, room_id: str, own_user_id: str, encrypted: bool = False) -> None:
        # def control_talking(self, proom: MatrixRoom, pevent: RoomMessageText, plocal_name: str) -> str:
        room = MatrixRoom('111', self.config.master)
        event = RoomMessageText()
        self.assertIn("*", self.moderator.control_talking(record))

        record[cn.MTEXT] = "абырвалг"
        self.assertEqual(self.moderator.control_talking(record), "")

        # *** Если сообщение пустое - не обрабатывается
        record[cn.MTEXT] = ""
        self.assertEqual(self.moderator.control_talking(record), "")

        # *** Проверка разрешенных чатов
        record[cn.MCHAT_TITLE] = "fakechat"
        record[cn.MTEXT] = "мля"
        self.assertEqual(self.moderator.control_talking(record), "")

        record[cn.MCHAT_TITLE] = "emptychat"
        self.assertEqual(self.moderator.control_talking(record), "")
    """    
        

    def test_moderator(self): 
       

        result = asyncio.run(self.moderator.moderator(self.config.test_chat, "абырвалг", "Хозяин", self.config.master))
        self.assertEqual(result, "")
   
        result = asyncio.run(self.moderator.moderator(self.config.test_chat, "!bwrl", "Хозяин", self.config.master))
        self.assertIn("Словарь", result)

        result = asyncio.run(self.moderator.moderator(self.config.test_chat, "!bwrl", "User", "user"))
        self.assertIn("Извини", result)
        result = asyncio.run(self.moderator.moderator("fakechat", "!bwrl", "Хозяин", self.config.master))
        self.assertEqual(result, "")
        result = asyncio.run(self.moderator.moderator("emptychat", "!bwrl", "Хозяин", self.config.master))
        self.assertEqual(result, "")

