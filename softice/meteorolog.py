 # -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Погодный модуль для бота."""

import datetime as dtime
import asyncio
# pylint: disable=import-error
import aiohttp
# pylint: enable=import-error

from softice import basis

# pylint: disable=too-many-branches
# pylint: disable=too-many-nested-blocks
# pylint: disable=too-many-statements
# pylint: disable=too-many-locals


WEATHER_GROUP: int = 0
FORECAST_GROUP: int = 1
HINT_GROUP: int = 2
COMMANDS: tuple = (("погода", "пг", "weather", "wt"),
                   ("прогноз", "пр", "forecast", "fr"),
                   ("метео", "meteo"))
DESCRIPTIONS: tuple = ((f"{', '.join(COMMANDS[WEATHER_GROUP])} город - "
                         "получить сводку погоды по указанному городу на сегодня"),
                       (f"{', '.join(COMMANDS[FORECAST_GROUP])} город -"
                         " получить прогноз погоды по указанному городу на завтра"))

UNIT_ID: str = "meteorolog"
READ_TIMEOUT = 5 # 1

FIND_CITY_URL: str = 'http://api.openweathermap.org/data/2.5/find'
FORECAST_WEATHER_URL: str = 'http://api.openweathermap.org/data/2.5/forecast'
ICON_CONVERT: dict = {"01d": "Ясно. ☀️",
                      "02d": "Ясно. ☀️",
                      "01n": "Ясно. 🌜",
                      "02n": "Ясно. 🌜",
                      "03d": "Облачно. ☁",
                      "04d": "Облачно. ☁",
                      "03n": "Облачно. ☁",
                      "04n": "Облачно. ☁",
                      "09d": "Дождь. 🌧",
                      "10d": "Дождь. 🌧",
                      "09n": "Дождь. 🌧",
                      "10n": "Дождь. 🌧",
                      "11d": "Гроза. 🌩",
                      "11n": "Гроза. 🌩",
                      "13d": "Снег. ❄",
                      "13n": "Снег. ❄",
                      "50d": "Туман.🌫",
                      "50n": "Туман.🌫"}
RUSSIAN_DATE_FORMAT: str = "%d.%m.%Y"
STEP: int = 45
DIRECTIONS: list = ['сев. ', 'св', ' вост.', 'юв', 'юг ', 'юз', ' зап.', 'сз']
PRESSURE_COEFF: float = 1.02972973



def get_wind_direction(pdegree) -> str:
    """Возвращает направление ветра."""

    assert pdegree is not None, \
		"Assert: [meteorolog.get_wind_direction] " \
		"Пропущен параметр <pdegree> !"

    result: str = ""
    for i in range(0, 8):

        min_degree = i * STEP - STEP / 2.
        max_degree = i * STEP + STEP / 2.
        if i == 0 and pdegree > 360 - STEP / 2.:

            pdegree = pdegree - 360
        if min_degree <= pdegree <= max_degree:

            result = DIRECTIONS[i]
            break
    return result


def parse_weather(pdata, preq_date) -> str:
    """Парсит данные погоды и формирует строку погоды."""

    assert pdata is not None, \
		"Assert: [meteorolog.parse_weather] " \
		"Пропущен параметр <pdata> !"
    assert preq_date is not None, \
		"Assert: [meteorolog.parse_weather] " \
		"Пропущен параметр <preq_date> !"

    min_temperature: int = 100
    max_temperature: int = -100
    min_pressure: int = 10000
    max_pressure: int = 0
    min_humidity: int = 100
    max_humidity: int = 0
    min_wind_speed: int = 200
    max_wind_speed: int = 0
    min_wind_angle: int = 360
    max_wind_angle: int = 0
    weather: list = []

    for item in pdata['list']:

        # 1. Выбираем данные за заданную дату
        if dtime.datetime.fromtimestamp(item['dt']).date() == preq_date:

            # *** Температура
            min_temperature = min(item['main']["temp"], min_temperature)
            max_temperature = max(item['main']["temp"], max_temperature)
            # *** Давление
            min_pressure = min(item['main']["pressure"], min_pressure)
            max_pressure = max(item['main']["pressure"], max_pressure)
            # *** Влажность
            min_humidity = min(item['main']["humidity"], min_humidity)
            max_humidity = max(item['main']["humidity"], max_humidity)
            # *** Ветер
            wind_speed = item["wind"]["speed"]
            wind_angle = item["wind"]["deg"]

            if wind_speed < min_wind_speed:

                min_wind_speed = wind_speed
                min_wind_angle = wind_angle
            if wind_speed > max_wind_speed:

                max_wind_speed = wind_speed
                max_wind_angle = wind_angle
            # *** Иконка погоды
            icon = item["weather"][0]["icon"][0:2]
            # *** Если это не "ясно", то ночь не нужна
            icon = "01d" if icon in ["01", "02"] else icon + "d"
            if icon in ["04", "04d"]:

                # *** приводим всё к 3
                icon = "03d"
            # *** Если дождь
            elif icon == "10":

                # *** Приводим к 9
                icon = "09d"
            if icon not in weather:

                weather.append(icon)
    if min_temperature == max_temperature:

        answer = f"Темп.: {round(min_temperature)} °C, "
    else:
        answer = f"Темп.: {round(min_temperature)}  -  {round(max_temperature)} °C, "
    if min_pressure == max_pressure:

        answer = answer + f" давл.: {round((min_pressure * 0.75) / PRESSURE_COEFF)} мм.рт.ст., "
    else:

        answer = answer + (f" давл.: {round((min_pressure * 0.75) / PRESSURE_COEFF)} - "
                           f"{round((max_pressure * 0.75) / PRESSURE_COEFF)} мм.рт.ст., ")
    if min_humidity == max_humidity:

        answer = answer + f" влажн.: {round(min_humidity)} %, "
    else:

        answer = answer + f" влажн.: {round(min_humidity)} - {round(max_humidity)} %, "
    min_wind_dir: str = get_wind_direction(min_wind_angle)
    max_wind_dir: str = get_wind_direction(max_wind_angle)
    if round(min_wind_speed) == round(max_wind_speed):

        answer = answer + f" ветер: {round(min_wind_speed)} м/с {min_wind_dir} "
    else:

        answer = answer + f" ветер: {round(min_wind_speed)} м/с {min_wind_dir} - {round(max_wind_speed)} м/c {max_wind_dir} "
    """
    if min_wind_dir == max_wind_dir:

        answer = answer + f"{min_wind_dir}"
    else:

        answer = answer + f"{min_wind_dir}- {max_wind_dir} "
    """    
    for icon in weather:

        answer += ICON_CONVERT[icon] + " "
    return answer


class CMeteorolog(basis.CBasis):
    """Класс метеоролога."""

    def __init__(self, pconfig):
        super().__init__(pconfig)
        self.cities_id: dict = {}
        print("Метеоролог стартовал.")

    def can_process_command(self, pchat_title: str, pmessage: str,  punit_id: str = "",
                    pcommands: list = None) -> bool:
        """Процедура определяет, сможет ли данный модуль обработать данную команду."""

        assert pchat_title is not None, \
            "Assert: [meteorolog.can_process_command] " \
            "Пропущен параметр <pchat_title> !"
        assert pmessage is not None, \
            "Assert: [meteorolog.can_process_command] " \
            "Пропущен параметр <pmessage> !"
        return super().can_process_command(pchat_title, pmessage, UNIT_ID, COMMANDS)


    async def get_city_id(self, pcity_name: str, plang: str = "ru"):
        """Возвращает ID города"""

        assert pcity_name is not None, \
            "Assert: [meteorolog.get_city_id] " \
            "Пропущен параметр <pcity_name> !"

        city_id: int = 0
        # *** Если у нас есть уже ID этого города...
        if pcity_name in self.cities_id:

            # *** .. берём его из словаря
            city_id = self.cities_id[pcity_name]
        else:

            try:

                api_key: str = self.config.meteorolog["api_key"]
                # rint(f"+++ Mtrl +++ gci +++ {api_key=}")
                async with aiohttp.ClientSession() as session:

                    async with session.get(
                        FIND_CITY_URL,
                        params={
                            'q': pcity_name, 
                            'limit': 1, 
                            'lang': plang,
                            'APPID': api_key
                        },
                        timeout=READ_TIMEOUT
                    ) as res:

                        res.raise_for_status()
                        data = await res.json()
                # rint(f"+++ Mtrl +++ gci +++ {data=}")
                if data:

                    # rint(f"+++ Mtrl +++ gci +++ {data=}")
                    if "list" in data:

                        key_list: list = data["list"]
                        # rint(f"+++ Mtrl +++ gci +++ {key_list=}")
                        dictionary: dict = key_list[0]
                        if "id" in dictionary:

                            city_id = key_list[0]["id"]
                            # rint(f"+++ Mtrl +++ gci +++ {city_id=}")

                    # rint(f"+++ Mtrl +++ gci +++ {city_id=}")

            except asyncio.exceptions.TimeoutError as ex:

                print("Exception (find):", ex)
            assert isinstance(city_id, int)
        return city_id


    def get_commands(self, pchat_title: str, punit_id: str="", pdescriptions: tuple=None) -> str:
        """Пользователь запросил список команд."""

        assert pchat_title is not None, \
            "Assert: [meteorolog.get_commands] " \
            "Пропущен параметр <pchat_title> !"

        return super().get_commands(pchat_title, UNIT_ID, DESCRIPTIONS)


    def get_hint(self, pchat_title: str, punit_id: str = "", phints: str = "") -> str:
        """Возвращает список команд, поддерживаемых модулем.  """

        assert pchat_title is not None, \
            "Assert: [meteorolog.get_hint] " \
            "Пропущен параметр <pchat_title> !"

        return super().get_hint(pchat_title, UNIT_ID, COMMANDS[HINT_GROUP])


    async def meteorolog(self, pchat_title: str, pmessage_text: str) -> str:
        """Процедура разбора запроса пользователя."""

        assert pchat_title is not None, \
            "Assert: [meteorolog.meteorolog] " \
            "Пропущен параметр <pchat_title> !"
        assert pmessage_text is not None, \
            "Assert: [meteorolog.meteorolog] " \
            "Пропущен параметр <pmessage_text> !"


        answer: str = ""
        word_list: list = self.parse_input(pmessage_text)
        # *** Метеоролог может обработать эту команду?
        if self.can_process_command(pchat_title, pmessage_text):

            # rint(f"+++ Mtrl +++ mtrl +++ can proc")
            # *** Запросили помощь?
            if word_list[0] in COMMANDS[HINT_GROUP]:

                answer = self.get_commands(pchat_title)
                return answer
            # *** Запросили погоду? А город указали?
            if len(word_list) > 1:

                city_name = " ".join(word_list[1:])
            else:

                city_name = "Москва"
			# *** Получим ID города
            # rint(f"+++ Mtrl +++ mtrl +++ {city_name=}")
            city_id = await self.get_city_id(city_name)
            if city_id > 0:

                # rint(f"+++ Mtrl +++ mtrl +++ {city_id=}")
				# *** Указан существующий город, работаем.
                now: dtime.datetime = dtime.datetime.now()
                date_str: str = ""
                weather_str: str = ""
				# *** Прогноз на завтра?
				# if word_list[0] in ["прогноз", "пр", "forecast", "fr"]:
                if word_list[0] in COMMANDS[FORECAST_GROUP]:

					# *** Да, так и есть.
                    tomorrow: dtime.datetime = now + dtime.timedelta(days=1)
                    date_str = tomorrow.strftime(RUSSIAN_DATE_FORMAT)
                    weather_str = await self.request_weather(city_id, tomorrow)

				# elif word_list[0] in ["погода", "пг", "weather", "wt"]:
                elif word_list[0] in COMMANDS[WEATHER_GROUP]:

					# *** Нет, на сегодня. Еще не поздно?
                    if now.hour < 21:

						# *** Вполне еще можно
                        date_str = now.strftime(RUSSIAN_DATE_FORMAT)
                        weather_str = await self.request_weather(city_id, now)
				# *** Если еще не поздно, то выдадим погоду, иначе дадим знать юзеру
                if now.hour < 21:

                    answer = f"{city_name} : {date_str} : {weather_str}"
                else:

                    answer = "Уже слишком поздно, метеоролог уснул..."
            else:

                answer = f"Нет данных о погоде для города {' '.join(word_list[1:]).strip()}"
        return answer


    async def request_weather(self, pcity_id, prequest_date: dtime.datetime, plang: str = "ru"):
        """Запрос погоды на завтра."""

        assert pcity_id is not None, \
            "Assert: [meteorolog.request_weather] " \
            "Пропущен параметр <pcity_id> !"
        assert prequest_date is not None, \
            "Assert: [meteorolog.request_weather] " \
            "Пропущен параметр <prequest_date> !"

        answer: str = ""
        async with aiohttp.ClientSession() as session:

            async with session.get(
                FORECAST_WEATHER_URL,
                params={
                    'id': pcity_id,  # Используем ID вместо имени!
                    'appid': self.config.meteorolog["api_key"],
                    'units': 'metric',
                    'lang': plang
                },
                timeout=READ_TIMEOUT
            ) as res:

                res.raise_for_status()
                data = await res.json()
                # rint(f"+++ Mtrl +++ reqw +++ {data=}")
                answer = parse_weather(data, prequest_date.date())
                #temp = data["main"]["temp"]
                #description = data["weather"][0]["description"]

            #return f"Температура: {temp}°C, {description}"
        return answer
