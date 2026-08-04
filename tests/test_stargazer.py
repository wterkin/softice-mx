from unittest import TestCase
import json
import asyncio
from softice import config
from softice import stargazer
import datetime as dtime
from datetime import datetime as dt

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


    def test_calc_difference(self):

        sample_date_str: str = "19.07.1980"
        sample_date = dt.strptime(sample_date_str, stargazer.RUSSIAN_DATE_FORMAT).date()
        difference: dt.timedelta = dt.now().date() - sample_date
        self.assertEqual(self.stargazer.calc_difference(["yr",sample_date_str]),
                         f"C указанной даты прошло {self.stargazer.get_diff_in_years(difference): } лет")
        self.assertEqual(self.stargazer.calc_difference(["dy",sample_date_str]),
                         f"C указанной даты прошло {difference.total_seconds()*stargazer.SECONDS_IN_DAY: } дней")
        self.assertEqual(self.stargazer.calc_difference(["hr",sample_date_str]),
                         f"C указанной даты прошло {difference.total_seconds()*stargazer.SECONDS_IN_HOUR: } часов")
        self.assertEqual(self.stargazer.calc_difference(["min",sample_date_str]),
                         f"C указанной даты прошло {difference.total_seconds()*stargazer.SECONDS_IN_MINUTE: } минут")
        self.assertEqual(self.stargazer.calc_difference(["sec",sample_date_str]),
                         f"C указанной даты прошло {difference.total_seconds()  : } секунд")
        self.assertEqual(self.stargazer.calc_difference(["yr"]), "А дата где?")


    def test_can_process_command(self):

        self.assertTrue(self.stargazer.can_process_command(self.config.test_chat, '!пасха'))
        self.assertTrue(self.stargazer.can_process_command(self.config.test_chat, '!нг'))
        self.assertFalse(self.stargazer.can_process_command('fakechat', '!день'))
        self.assertFalse(self.stargazer.can_process_command('empttychat', '!дата'))
        self.assertFalse(self.stargazer.can_process_command(self.config.test_chat, '!кукабарра'))


    def test_get_commands(self):

        self.assertIn("пасха, easter", self.stargazer.get_commands(self.config.test_chat))


    def test_get_hint(self):

        self.assertIn("календарь, calendar, кл, cl", self.stargazer.get_hint(self.config.test_chat))


    def test_stargazer(self):

        result = asyncio.run(self.stargazer.stargazer(self.config.test_chat, "!кукабарра"))
        self.assertEqual(result, "")
        result = asyncio.run(self.stargazer.stargazer(self.config.test_chat, "!календарь"))
        self.assertIn("пасха, easter", result)
        result = asyncio.run(self.stargazer.stargazer(self.config.test_chat, "!пасха 2025"))
        self.assertIn("20.04.2025", result)
        result = asyncio.run(self.stargazer.stargazer(self.config.test_chat, "!пасха в этом году"))
        self.assertIn("Невозможно рассчитать", result)
        now_date: dtime.date = dtime.date.today()
        if now_date.day == 1 and now_date.month == 1:

            result = asyncio.run(self.stargazer.stargazer(self.config.test_chat, "!дата"))
            self.assertIn(f"Новый год", result)
        else:

            result = asyncio.run(self.stargazer.stargazer(self.config.test_chat, "!дата"))
            self.assertIn(f"В этот день", result)
        sample_date_str: str = "19.07.1980"
        sample_date = dt.strptime(sample_date_str, stargazer.RUSSIAN_DATE_FORMAT).date()
        difference: dt.timedelta = dt.now().date() - sample_date
        self.assertEqual(self.stargazer.calc_difference(["yr",sample_date_str]),
                         f"C указанной даты прошло {self.stargazer.get_diff_in_years(difference): } лет")
        self.assertEqual(self.stargazer.calc_difference(["yr"]), "А дата где?")

