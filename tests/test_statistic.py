"""Модуль тестирования модуля статистика бота."""

# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=line-too-long

import unittest

import datetime as dtime

import asyncio

from softice import config
from softice import database as db
from softice import statistic


TEST_DATABASE_NAME: str = "softice-test"
TEST_USER_ID: str = "777"
TEST_ROOM_ID: str = "777"

first_run: bool = True

class CTestStatistic(unittest.IsolatedAsyncioTestCase):


    def setUp(self) -> None:

        self.config = config.Config("test_config.yaml")
        self.statistic: statistic.CStatistic = \
            statistic.CStatistic(self.config, TEST_DATABASE_NAME)


    async def asyncSetUp(self) -> None:
        # Асинхронный setup: один event loop на весь тест

        if await self.statistic.init():

            await self._clean_tables()


    async def _clean_tables(self) -> bool:

        models = [db.CRoom, db.CUser, db.CStat]

        for model in models:

            ok = await self.statistic.database.wipe_table(model)
            if not ok:

                print(f"Не удалось очистить таблицу для модели: {model.__name__}")
                return False
        return True


    async def test_add_room_to_base(self):

        result = await self.statistic.add_room_to_base(TEST_ROOM_ID, "Ботовка")
        self.assertEqual(result, 1)


    async def test_add_user_to_base(self):

        result = await self.statistic.add_user_to_base(TEST_USER_ID, "Master")
        self.assertEqual(result, 1)


    async def test_add_user_stat(self):

        stat: db.CStat = db.CStat(1, 1)
        stat.letters = 1
        stat.words = 2
        stat.phrases = 3
        stat.emotes = 4
        stat.notices = 5
        stat.images = 6
        stat.audios = 7
        stat.videos = 8
        stat.files = 9
        stat.silence = False
        result = await self.statistic.add_user_stat(stat)
        self.assertEqual(result, 1)


    async def test_get_room_by_id(self):

        result = await self.statistic.get_room_by_id(TEST_ROOM_ID)
        self.assertEqual(result, 1)

"""


    def test_get_chat_id(self):

        self.assertEqual(self.statistic.get_chat_id(777), 1)
        self.assertEqual(self.statistic.get_chat_id(0), -1)


    def test_get_help(self):

        self.assertIn("перв10, перв25, перв50, личные", self.statistic.get_help(test_softice.TESTPLACE_CHAT_NAME))


    def test_get_hint(self):

        self.assertIn("стат, stat", self.statistic.get_hint(test_softice.TESTPLACE_CHAT_NAME))


    def test_get_personal_information(self):

        # def get_personal_information(self, ptg_chat_id: int, puser_title: str):
        self.assertIn("наболтал", self.statistic.get_personal_information(777, "Master"))
        self.assertEqual(self.statistic.get_personal_information(777, "Somebody"), "")
        self.assertEqual(self.statistic.get_personal_information(1, "Master"), "")


    def test_get_statistic(self):

        #  def get_statistic(self, ptg_chat_id: int, pcount: int, porder_by: int):
        self.assertIn(f"Отсортировано по количеству {statistic.SORTED_BY[0]}",
                      self.statistic.get_statistic(777, 5, 1))
        self.assertIn(f"Отсортировано по количеству {statistic.SORTED_BY[1]}",
                      self.statistic.get_statistic(777, 5, 2))
        self.assertIn(f"Отсортировано по количеству {statistic.SORTED_BY[2]}",
                      self.statistic.get_statistic(777, 5, 3))
        self.assertIn(f"Отсортировано по количеству {statistic.SORTED_BY[3]}",
                      self.statistic.get_statistic(777, 5, 4))
        self.assertIn(f"Отсортировано по количеству {statistic.SORTED_BY[4]}",
                      self.statistic.get_statistic(777, 5, 5))
        self.assertIn(f"Отсортировано по количеству {statistic.SORTED_BY[5]}",
                      self.statistic.get_statistic(777, 5, 6))


    def test_get_user_id(self):
        # def get_user_id(self, ptg_user_id):
        self.assertIsNotNone(self.statistic.get_user_id(777))
        self.assertIsNone(self.statistic.get_user_id(111))


    def test_get_user_stat(self):

        #    def get_user_stat(self, pchat_id: int, puser_id: int):
        stat: db.CStat = self.statistic.get_user_stat(1, 1)
        self.assertEqual(stat.fletters,2)
        self.assertEqual(stat.fwords,3)
        self.assertEqual(stat.fphrases,4)
        self.assertEqual(stat.fpictures,5)
        self.assertEqual(stat.fstickers,6)
        self.assertEqual(stat.faudios,7)
        self.assertEqual(stat.fvideos,8)


    def test_is_enabled(self):

        self.assertTrue(self.statistic.is_enabled(test_softice.TESTPLACE_CHAT_NAME))
        self.assertFalse(self.statistic.is_enabled("fakechat"))
        self.assertFalse(self.statistic.is_enabled("emptychat"))


    def test_save_all_type_of_messages(self):

        #    def save_all_type_of_messages(self, pevent: dict):
        event: dict = {}
        event[cn.MTEXT] = "Hello, world!"
        event[cn.MCHAT_ID] = 777
        event[cn.MCHAT_TITLE] = "TestPlace"
        event[cn.MUSER_ID] = 777
        event[cn.MUSER_NAME] = "Master"
        event[cn.MCONTENT_TYPE] = "text"
        self.assertTrue(self.statistic.save_all_type_of_messages(event))
        event[cn.MCAPTION] = "Some picture"
        self.assertTrue(self.statistic.save_all_type_of_messages(event))
        event[cn.MUSER_NAME] = "User"
        self.assertTrue(self.statistic.save_all_type_of_messages(event))
        event[cn.MUSER_NAME] = "Mafioso"
        self.assertFalse(self.statistic.save_all_type_of_messages(event))
        event[cn.MCHAT_TITLE] = "fakechat"
        self.assertFalse(self.statistic.save_all_type_of_messages(event))
        event[cn.MCHAT_TITLE] = "emptychat"
        self.assertFalse(self.statistic.save_all_type_of_messages(event))


    def test_statistic(self):

        # def statistic(self, pchat_id: int, pchat_title: str, puser_title, pmessage_text: str):
        self.assertTrue(self.statistic.statistic(1, test_softice.TESTPLACE_CHAT_NAME, "Master", "!top10"))
        self.assertIn("перв10", self.statistic.statistic(1, test_softice.TESTPLACE_CHAT_NAME, "Master", "!стат"))
        self.assertIn("Самые говорливые", self.statistic.statistic(777, test_softice.TESTPLACE_CHAT_NAME, "Master", "!top10 1"))
        self.assertIn("Самые говорливые", self.statistic.statistic(777, test_softice.TESTPLACE_CHAT_NAME, "Master", "!top25 2"))
        self.assertIn("Самые говорливые", self.statistic.statistic(777, test_softice.TESTPLACE_CHAT_NAME, "Master", "!top50 3"))
        self.assertIn("Самые говорливые", self.statistic.statistic(777, test_softice.TESTPLACE_CHAT_NAME, "Master", "!top10 4"))
        self.assertIn("Самые говорливые", self.statistic.statistic(777, test_softice.TESTPLACE_CHAT_NAME, "Master", "!top25 5"))
        self.assertIn("Самые говорливые", self.statistic.statistic(777, test_softice.TESTPLACE_CHAT_NAME, "Master", "!top50 6"))
        self.assertIn("Master наболтал", self.statistic.statistic(777, test_softice.TESTPLACE_CHAT_NAME, "Master", "!pers"))


    def tearDown(self):

        self.database.disconnect()
        # pass
"""
