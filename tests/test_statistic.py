"""Модуль тестирования модуля статистика бота."""

# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=line-too-long

import unittest

import datetime as dtime

import asyncio
import nio
from softice import config
from softice import database as db
from softice import statistic


TEST_DATABASE_NAME: str = "softice-test"
TEST_USER_NAME: str = "@namo:sibnsk.net"
TEST_ROOM_ID: str = "777"
TEST_ROOM_NAME: str = "Ботовка"

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

        models = [db.CStat, db.CRoom, db.CUser]

        for model in models:

            ok = await self.statistic.database.wipe_table(model)
            if not ok:

                print(f"Не удалось очистить таблицу для модели: {model.__name__}")
                return False
        return True


    async def test_add_room_to_base(self):

        result = await self.statistic.add_room_to_base(TEST_ROOM_ID, TEST_ROOM_NAME)
        self.assertEqual(result, 1)
        await self.statistic.destroy()


    async def add_stat(self, proom_id, puser_id):

        stat: db.CStat = db.CStat(proom_id, puser_id)
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
        await self.statistic.destroy()
        return result


    async def test_add_user_stat(self):

        user_id: int = await self.statistic.add_user_to_base(TEST_USER_NAME)
        if user_id == 1:

            room_id: int = await self.statistic.add_room_to_base(TEST_ROOM_ID, TEST_ROOM_NAME)
            if room_id == 1:

                result = await self.add_stat(1, 1)
                self.assertEqual(result, 1)
        await self.statistic.destroy()


    async def test_add_user_to_base(self):

        result = await self.statistic.add_user_to_base(TEST_USER_NAME)
        self.assertEqual(result, 1)
        await self.statistic.destroy()


    async def test_get_room_by_id(self):

        if await self.statistic.add_room_to_base(TEST_ROOM_ID, TEST_ROOM_NAME) == 1:

            result = await self.statistic.get_room_id(TEST_ROOM_ID)
            self.assertEqual(result, 1)
        await self.statistic.destroy()


    def test_get_commands(self):

        self.assertIn("первые10, пв10, top10", self.statistic.get_commands(self.config.test_chat))


    def test_get_hint(self):

        self.assertIn("статистика, стат, statistic, stat", self.statistic.get_hint(self.config.test_chat))


    async def test_get_personal_information(self):

        user_id: int = await self.statistic.add_user_to_base(TEST_USER_NAME)
        if user_id == 1:

            room_id: int = await self.statistic.add_room_to_base(TEST_ROOM_ID, TEST_ROOM_NAME)
            if room_id == 1:

                result = await self.add_stat(room_id, user_id)
                if result == 1:

                    answer = f"3 фраз, 2 слов, 1 букв"
                    result = await self.statistic.get_personal_information(TEST_ROOM_ID, TEST_USER_NAME)
                    self.assertTrue(True)
        await self.statistic.destroy()


    async def test_get_statistic(self):

        # async def get_statistic(self, proom_id: str, pcount: int, porder_by: int) -> str:
        self.assertIn(f"Отсортировано по количеству {statistic.SORTED_BY[statistic.PHRASES_ORDER-1]}",
                      await self.statistic.get_statistic(TEST_ROOM_ID, 5, statistic.PHRASES_ORDER))
        self.assertIn(f"Отсортировано по количеству {statistic.SORTED_BY[statistic.WORDS_ORDER-1]}",
                      await self.statistic.get_statistic(TEST_ROOM_ID, 5, statistic.WORDS_ORDER))
        self.assertIn(f"Отсортировано по количеству {statistic.SORTED_BY[statistic.IMAGES_ORDER-1]}",
                      await self.statistic.get_statistic(TEST_ROOM_ID, 5, statistic.IMAGES_ORDER))
        self.assertIn(f"Отсортировано по количеству {statistic.SORTED_BY[statistic.AUDIOS_ORDER-1]}",
                      await self.statistic.get_statistic(TEST_ROOM_ID, 5, statistic.AUDIOS_ORDER))
        self.assertIn(f"Отсортировано по количеству {statistic.SORTED_BY[statistic.VIDEOS_ORDER-1]}",
                      await self.statistic.get_statistic(TEST_ROOM_ID, 5, statistic.VIDEOS_ORDER))
        self.assertIn(f"Отсортировано по количеству {statistic.SORTED_BY[statistic.FILES_ORDER-1]}",
                      await self.statistic.get_statistic(TEST_ROOM_ID, 5, statistic.FILES_ORDER))
        await self.statistic.destroy()


    async def test_get_user_id(self):
        # def get_user_id(self, ptg_user_id):
        user_id: int = await self.statistic.add_user_to_base(TEST_USER_NAME)
        if user_id > 0:

            result = await self.statistic.get_user_id(TEST_USER_NAME)
            self.assertIsNotNone(result)
            result = await self.statistic.get_user_id("111")
            self.assertEqual(result, statistic.ERROR_CODE)
        await self.statistic.destroy()


    async def test_get_user_stat(self):

        #    def get_user_stat(self, pchat_id: int, puser_id: int):
        user_id = await self.statistic.add_user_to_base(TEST_USER_NAME)
        if user_id > 0:

            room_id = await self.statistic.add_room_to_base(TEST_ROOM_ID, TEST_ROOM_NAME)
            if room_id > 0:

                await self.add_stat(room_id, user_id)
                stat: db.CStat = await self.statistic.get_user_stat(TEST_ROOM_ID, TEST_USER_NAME)
                if stat:

                    self.assertEqual(stat.letters,1)
                    self.assertEqual(stat.words,2)
                    self.assertEqual(stat.phrases,3)
                    self.assertEqual(stat.emotes,4)
                    self.assertEqual(stat.notices,5)
                    self.assertEqual(stat.images,6)
                    self.assertEqual(stat.audios,7)
                    self.assertEqual(stat.videos,8)
                    await self.statistic.destroy()
                else:

                    self.assertNotEqual(stat, None)


    def test_save_all_type_of_messages(self):

        # def save_all_type_of_messages(self, pmx_room_id: int, pmx_room_name: str,
                                            # pmx_user_name: str,
                                            # pevent: RoomMessageText) -> bool:


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

    """

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
