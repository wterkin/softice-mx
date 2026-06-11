from unittest import TestCase
import json
import asyncio
from datetime import date
from softice import config
from softice import stargazer
import datetime as dtime

class CTestStarGazer(TestCase):

    def setUp(self) -> None:

        self.config = config.Config("test_config.yaml")
        self.stargazer: stargazer.CStarGazer = stargazer.CStarGazer(self.config)


    def test_calculate_easter(self):

        self.assertEqual(stargazer.calculate_easter(2025), dtime.datetime(2025, 4, 20))


    def test_additional_inf(self):

        self.assertIn("Рождественский пост.", self.stargazer.additional_info(dtime.date(2025, 1, 6)))
        self.assertIn("Рождество.", self.stargazer.additional_info(dtime.date(2025, 1, 7)))
        self.assertIn("Святки.", self.stargazer.additional_info(dtime.date(2025, 1, 8)))
        self.assertIn("Сырная седмица.", self.stargazer.additional_info(dtime.date(2025, 2, 20)))
        self.assertIn("Страстная седмица.", self.stargazer.additional_info(dtime.date(2025, 4, 18)))
        self.assertIn("Пасха.", self.stargazer.additional_info(dtime.date(2025, 4, 20)))
        self.assertIn("Светлая седмица.", self.stargazer.additional_info(dtime.date(2025, 4, 21)))
        self.assertIn("Сплошная седмица", self.stargazer.additional_info(dtime.date(2025, 6, 12)))
        self.assertIn("Петров пост.", self.stargazer.additional_info(dtime.date(2025, 6, 20)))
        self.assertIn("Успенский пост.", self.stargazer.additional_info(dtime.date(2025, 8, 27)))


    def test_can_process_command(self):

        self.assertTrue(self.stargazer.can_process_command(self.config.test_chat, '!пасха'))
        self.assertTrue(self.stargazer.can_process_command(self.config.test_chat, '!нг'))
        self.assertFalse(self.stargazer.can_process_command('fakechat', '!день'))
        self.assertFalse(self.stargazer.can_process_command('empttychat', '!дата'))
        self.assertFalse(self.stargazer.can_process_command(self.config.test_chat, '!кукабарра'))


    def test_get_commands(self):

        self.assertIn("пасха, easter", self.stargazer.get_commands(self.config.test_chat))


    def test_get_hint(self):

        self.assertIn("календарь, кл", self.stargazer.get_hint(self.config.test_chat))


    def test_stargazer(self):

        result = asyncio.run(self.stargazer.stargazer(self.config.test_chat, "!кукабарра"))
        self.assertEqual(result, "")
        result = asyncio.run(self.stargazer.stargazer(self.config.test_chat, "!календарь"))
        self.assertIn("пасха, easter", result)
        result = asyncio.run(self.stargazer.stargazer(self.config.test_chat, "!пасха 2025"))
        self.assertIn("20.04.2025", result)
        result = asyncio.run(self.stargazer.stargazer(self.config.test_chat, "!пасха в этом году"))
        self.assertIn("Невозможно рассчитать", result)
        now_date: date = date.today()
        if now_date.day == 1 and now_date.month == 1:

            result = asyncio.run(self.stargazer.stargazer(self.config.test_chat, "!дата"))
            self.assertIn(f"Новый год", result)
        else:

            result = asyncio.run(self.stargazer.stargazer(self.config.test_chat, "!дата"))
            self.assertIn(f"В этот день", result)

