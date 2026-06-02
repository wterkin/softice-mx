from unittest import TestCase
import datetime as dtime
import json
# import constants as cn
import asyncio
from softice import config
from softice import meteorolog

class CTestMeterolog(TestCase):

    def setUp(self) -> None:

        self.config = config.Config("test_config.yaml")
        self.meteorolog: meteorolog.CMeteorolog = meteorolog.CMeteorolog(self.config)


    def test_get_wind_direction(self):
        
        self.assertEqual(meteorolog.get_wind_direction(180), meteorolog.DIRECTIONS[4]) # Юг
        self.assertEqual(meteorolog.get_wind_direction(270), meteorolog.DIRECTIONS[6]) # Запад

    
    def test_parse_weather(self):
        
        data: dict = {}
        temp_list: list = [15, 20, 25, 30]
        press_list: list = [710, 720, 730, 740]
        hum_list: list = [70, 80, 90, 100]
        wind_speed_list: list = [10, 20, 30, 40]
        wind_deg_list: list = [0, 45, 90, 180]
        icon_list: list = ["01  ", "02   ", "04d  ", "03d  "]
        data["list"] = []
        now: dtime.datetime = dtime.datetime.now()
        for idx in range(0, len(temp_list)):
            
            item: dict = {}
            item["dt"] = now.timestamp()
            item['main']: dict = {}
            item['main']["temp"] = temp_list[idx]
            item['main']["pressure"] = press_list[idx]/0.75
            item['main']["humidity"] = hum_list[idx]
            item['wind']: dict = {}
            item["wind"]["speed"] = wind_speed_list[idx]
            item["wind"]["deg"] = wind_deg_list[idx]
            data["list"].append(item)
            weather: dict = {'icon':icon_list[idx]} 
            item["weather"]: list = []
            item["weather"].append(weather)
            
        result: str = "Темп.: 15  -  30 °C,  давл.: 710 - 740 мм.рт.ст.,  влажн.: 70 - 100 %,  ветер: 10 м/с - 40 м/c сев. - юг Ясно. \u2600\ufe0f Облачно. \u2601 "
        self.assertEqual(meteorolog.parse_weather(data, now.date()), result)


    def test_can_process_command(self):
        
        self.assertTrue(self.meteorolog.can_process_command(self.config.test_chat, '!пг Смоленск'))
        self.assertTrue(self.meteorolog.can_process_command(self.config.test_chat, '!пр Смоленск'))
        self.assertFalse(self.meteorolog.can_process_command('fakechat', '!пр'))
        self.assertFalse(self.meteorolog.can_process_command('empttychat', '!пг'))
        self.assertFalse(self.meteorolog.can_process_command(self.config.test_chat, '!кукабарра'))

    def test_get_city_id(self):

        result = asyncio.run(self.meteorolog.get_city_id("Смоленск"))
        self.assertEqual(result, 491687)


    def test_get_commands(self):

        self.assertIn("погода, пг, weather, wt город", self.meteorolog.get_commands(self.config.test_chat))


    def test_get_hint(self):

        self.assertIn("метео, meteo", self.meteorolog.get_hint(self.config.test_chat))
    

    def test_is_enabled(self):

        self.assertFalse(self.meteorolog.is_enabled("fakechat", meteorolog.UNIT_ID))
        self.assertFalse(self.meteorolog.is_enabled("emptychat", meteorolog.UNIT_ID))
        self.assertTrue(self.meteorolog.is_enabled(self.config.test_chat, meteorolog.UNIT_ID))

    """


        def test_meteorolog(self):

            #Смоленск : 02.10.2025
            self.assertEqual(self.meteorolog.meteorolog("fakechat", "!пг Смоленск"), "")
            self.assertEqual(self.meteorolog.meteorolog("emptychat", "!пг Смоленск"), "")
            # self.assertIn("А в каком городе погода нужна?", self.meteorolog.meteorolog(self.config.test_chat, "!пг"))
            self.assertIn("Нет данных о погоде для города Диптаун", self.meteorolog.meteorolog(self.config.test_chat, "!пг Диптаун"))
            now_date = dtime.datetime.now()
            self.assertIn(now_date.strftime("Смоленск : %d.%m.%Y"), self.meteorolog.meteorolog(self.config.test_chat, "!пг Смоленск"))
            tomorrow_date = now_date + dtime.timedelta(days=1) 
            self.assertIn(tomorrow_date.strftime("Смоленск : %d.%m.%Y"), self.meteorolog.meteorolog(self.config.test_chat, "!пр Смоленск"))
    """


    def test_request_weather(self):

        now_date = dtime.datetime.now()
        result = asyncio.run(self.meteorolog.request_weather(491687, now_date))
        self.assertIn("Темп.:", result)
        
#Темп.: 15  -  30 °C,  давл.: 710 - 740 мм.рт.ст.,  влажн.: 70 - 100 %,  ветер: 10 м/с - 40 м/c сев. - юг Ясно. ☀️ Облачно. ☁ 
#Темп.: 15  -  30 °C,  давл.: 710 - 740 мм.ст.рт.,  влажн.: 70 - 100 %,  ветер: 10 м/с - 40 м/c сев. - юг Ясно. ☀️ Облачно. ☁ 


