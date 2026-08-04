# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль звездочёта."""

import datetime as dtime
from datetime import datetime as dt
import locale
from softice import basis

# pylint: disable=too-many-branches

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

NEW_STYLE_OFFSET: int = 13
EASTER_GROUP: int = 0
DATE_GROUP: int = 1
DAY_GROUP: int = 2
NEW_YEAR_GROUP: int = 3
YEARS_GROUP: int = 4
DAYS_GROUP: int = 5
HOURS_GROUP: int = 6
MINUTES_GROUP: int = 7
SECONDS_GROUP: int = 8
HINT_GROUP: int = 9

COMMANDS: tuple = (("пасха", "easter"),
                   ("дата", "date"),
                   ("день", "day"),
                   ("новыйгод", "newyear", "нг", "ny"),
                   ("лет", "years", "лт", "yr"),
                   ("дней", "days", "дн", "dy"),
                   ("часов", "hours", "чс", "hr"),
                   ("минут", "minutes", "мин", "min"),
                   ("секунд", "seconds", "сек", "sec"),
                   ("календарь", "calendar", "кл", "cl")
                  )

DESCRIPTIONS: tuple = ((f"{', '.join(COMMANDS[EASTER_GROUP])} [год] - "
                         "получить дату Пасхи в указанном году"),
                       (f"{', '.join(COMMANDS[DATE_GROUP])} -"
                         " получить гражданские праздники на текущую дату"),
                       (f"{', '.join(COMMANDS[DAY_GROUP])} -"
                         " получить церковные праздники на текущую дату"),
                       (f"{', '.join(COMMANDS[NEW_YEAR_GROUP])} -"
                         " получить количество оставшихся дней до Нового года"),
                       (f"{', '.join(COMMANDS[YEARS_GROUP])} -"
                         " получить разницу между указанной датой и текущей в годах, "
                         "форматзадания даты ДД.ММ.ГГГГ"),
                       (f"{', '.join(COMMANDS[DAYS_GROUP])} -"
                         " получить разницу между указанной датой и текущей в днях"),
                       (f"{', '.join(COMMANDS[HOURS_GROUP])} -"
                         " получить разницу между указанной датой и текущей в часах"),
                       (f"{', '.join(COMMANDS[MINUTES_GROUP])} -"
                         " получить разницу между указанной датой и текущей в минутах"),
                       (f"{', '.join(COMMANDS[SECONDS_GROUP])} -"
                         " получить разницу между указанной датой и текущей в секундах")
                      )

# HINTS: tuple = ("календарь", "кл", "calendar", "cl")
UNIT_ID = "stargazer"
RUSSIAN_DATE_FORMAT = "%d.%m.%Y"
STARGAZER_FOLDER: str = "stargazer/"
LOW_MARGIN: int = 1899
HIGH_MARGIN: int = 2100
CHURCH_CALENDAR: str = "calendar.txt"
CIVILIAN_CALENDAR: str = "dates.txt"
JUL_GREG_CALENDAR_DIFF: int = 13
YEAR_DAYS: int = 365
LEAP_YEAR_DAYS: int = 366
BOLD: str = "*"
ITALIC: str = "_"

SECONDS_IN_MINUTE: int = 60
SECONDS_IN_HOUR: int = SECONDS_IN_MINUTE * 60
SECONDS_IN_DAY: int = SECONDS_IN_HOUR*24


def calculate_easter(pyear):
    """Вычисляет дату пасхи на заданный год."""

    assert pyear is not None, \
        "Assert: [stargazer:calculate_easter] " \
        "Пропущен параметр <pyear> !"

    first_value: int = (19 * (pyear % 19) + 15) % 30
    second_value: int = (2 * (pyear % 4) + 4 * (pyear % 7) + 6 * first_value + 6) % 7
    month: int
    day: int
    if (first_value + second_value) > 9:

        # *** Апрель
        month = 4
        day = (first_value + second_value) - 9 + NEW_STYLE_OFFSET
        if day > 30:

            month += 1
            day = day - 30
    else:

        # *** Март
        month = 3
        day = first_value + second_value + 22 + NEW_STYLE_OFFSET
        if day > 31:

            month += 1
            day = day - 31
    return dtime.datetime(pyear, month, day)


class CStarGazer(basis.CBasis):
    """Класс модуля звездочёта."""


    def __init__(self, pconfig):

        super().__init__(pconfig)
        self.data_path: str = self.config.data_folder + STARGAZER_FOLDER
        print("Звездочёт стартовал.")


    def additional_info(self, pnow_date):
        """Возвращает дополнительные сведения об указанном дне."""

        assert pnow_date is not None, \
            "Assert: [stargazer.additional_info] " \
            "Пропущен параметр <pnow_date> !"

        # pnow_date = date(pnow_date.year, 6, 9)  # закоментить!!!
        easter_date: dtime.date = calculate_easter(pnow_date.year).date()
        # rint(f"+++ Strg +++ ai +++ {key_list=}")
        peter_paul_date: dtime.date = dtime.date(pnow_date.year, 7, 12)
        answer: str = ""
        if easter_date > pnow_date:

            if pnow_date < dtime.datetime(pnow_date.year, 1, 7).date():

                answer = "Рождественский пост."
            elif pnow_date == dtime.datetime(pnow_date.year, 1, 7).date():

                answer = "Рождество."
            elif dtime.datetime(pnow_date.year, 1, 7).date() < pnow_date < \
                 dtime.datetime(pnow_date.year, 1, 18).date():

                answer = "Святки."
            elif dtime.timedelta(days=56) <= (easter_date - pnow_date) <= dtime.timedelta(days=62):

                answer = "Сырная седмица."
            elif dtime.timedelta(days=7) <= (easter_date - pnow_date) <= dtime.timedelta(days=55):

                answer = "Великий пост."
            elif dtime.timedelta(days=1) <= (easter_date - pnow_date) <= dtime.timedelta(days=7):

                answer = "Страстная седмица."
        elif pnow_date == easter_date:

            answer = "Пасха."
        elif (pnow_date - easter_date)  < dtime.timedelta(days=7):

            answer = "Светлая седмица."
        elif (pnow_date - easter_date) > dtime.timedelta(days=49) and \
             (pnow_date - easter_date) < dtime.timedelta(days=57):

            answer = "Сплошная седмица"
        elif pnow_date < peter_paul_date and (pnow_date - easter_date) > dtime.timedelta(days=56):

            answer = "Петров пост."
        elif dtime.datetime(pnow_date.year, 8, 14).date() < pnow_date < \
             dtime.datetime(pnow_date.year, 8, 28).date():

            answer = "Успенский пост."
        return answer


    def get_diff_in_years(self, pdifference: dtime.timedelta) -> int:
        """Возвращает разницу в годах между двумя датами."""

        assert pdifference is not None, \
            "Assert: [stargazer.get_diff_in_years] " \
            "Пропущен параметр <pdifference> !"

        return int((pdifference.days + pdifference.seconds/86400)/365.2425)


    def calc_difference(self, pcommands: list) -> str:
        """Возвращает разницу между указанной датой и текущей в заданных единицах."""

        assert pcommands is not None, \
            "Assert: [stargazer.calc_difference] " \
            "Пропущен параметр <pcommands> !"

        answer_part: str
        answer: str = ""
        difference: dtime.timedelta
        # rint(f"+++ Strg +++ ai +++ {pcommands[1]=}")

        if len(pcommands) > 1:

            target_date: dtime.date = dt.strptime(pcommands[1], RUSSIAN_DATE_FORMAT).date()
            now_date: dtime.date = dt.now().date()
            if target_date>now_date:

                difference = target_date - now_date
                answer_part = "До указанной даты осталось"
                # rint(f"+++ Strg +++ ai1 +++ {difference=}")
            else:

                difference = now_date - target_date
                answer_part = "C указанной даты прошло"
                # rint(f"+++ Strg +++ ai2 +++ {difference=}")

            if pcommands[0] in COMMANDS[YEARS_GROUP]:

                answer = f"{answer_part} {self.get_diff_in_years(difference): } лет"
            if pcommands[0] in COMMANDS[DAYS_GROUP]:

                answer = f"{answer_part} {difference.total_seconds() * SECONDS_IN_DAY: } дней"
            if pcommands[0] in COMMANDS[HOURS_GROUP]:

                answer = f"{answer_part} {difference.total_seconds() * SECONDS_IN_HOUR: } часов"
            if pcommands[0] in COMMANDS[MINUTES_GROUP]:

                answer = f"{answer_part} {difference.total_seconds() * SECONDS_IN_MINUTE: } минут"
            if pcommands[0] in COMMANDS[SECONDS_GROUP]:

                answer = f"{answer_part} {difference.total_seconds(): } секунд"
        else:

            answer = "А дата где?"
        return answer


    def can_process_command(self, pchat_title: str, pmessage: str,  punit_id: str = "",
                    pcommands: list = None) -> bool:
        """Процедура определяет, сможет ли данный модуль обработать данную команду."""

        assert pchat_title is not None, \
            "Assert: [stargazer.can_process_command] " \
            "Пропущен параметр <pchat_title> !"
        assert pmessage is not None, \
            "Assert: [stargazer.can_process_command] " \
            "Пропущен параметр <pmessage> !"
        return super().can_process_command(pchat_title, pmessage, UNIT_ID, COMMANDS)


    def get_commands(self, pchat_title: str, punit_id: str="", pdescriptions: list=None) -> str:
        """Пользователь запросил список команд."""

        assert pchat_title is not None, \
            "Assert: [stargazer.get_commands] " \
            "Пропущен параметр <pchat_title> !"

        return super().get_commands(pchat_title, UNIT_ID, DESCRIPTIONS)


    def get_hint(self, pchat_title: str, punit_id: str = "", phints: str = "") -> str:
        """Возвращает список команд, поддерживаемых модулем.  """

        assert pchat_title is not None, \
            "Assert: [stargazer.get_hint] " \
            "Пропущен параметр <pchat_title> !"

        return super().get_hint(pchat_title, UNIT_ID, COMMANDS[HINT_GROUP])

    # pylint: disable=pointless-string-statement
    """
    def print_month(self):
        ""Выводит календарь на текущий месяц, используя команду cal линукса.""

        now_date: date = date.today()
        this_day: str = str(now_date.day)
        result = sub.run(["cal","-mv"], stdout=sub.PIPE)
        answer = result.stdout.decode("utf-8") # .strip()
        lines: list = answer.split("\n")
        days: list
        today_found: bool = False
        for lindex, line in enumerate(lines[1:]):

            if not today_found:

                days = line.split(" ")
                for dindex, day in enumerate(days):

                    if day.strip() == this_day:

                        days[dindex] = f"{BOLD}{day}{BOLD}"
                        today_found = True
                        lines[lindex+1] = " ".join(days)
            if "Сб" in line or "Вс" in line:

                if lindex >1:

                    days = line.strip().split(" ")
                    for index, day in enumerate(days):

                        days[index] = f"{ITALIC}{day}{ITALIC}"

                    lines[lindex+1] = " ".join(days)
        return "\n".join(lines)
    """



    async def stargazer(self, pchat_title: str, pmessage_text: str) -> str:
        """Обработчик команд звездочёта."""

        assert pchat_title is not None, \
            "Assert: [stargazer.stargazer] No <pchat_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [stargazer.stargazer] No <pmessage_text> parameter specified!"

        answer: str = ""
        word_list: list = self.parse_input(pmessage_text)
        year: int
        now_date: dtime.date = dtime.date.today()
        today: str
        if self.can_process_command(pchat_title, pmessage_text):

            # *** Возможно, запросили меню.
            if word_list[0] in COMMANDS[HINT_GROUP]:

                answer = self.get_commands(pchat_title)
            # *** Запросили Пасху?
            elif word_list[0] in COMMANDS[EASTER_GROUP]:

                if len(word_list) > 1:

                    if word_list[1].isdigit():

                        year = int(word_list[1])
                    else:

                        year = 0
                else:

                    year = dtime.date.today().year
                if HIGH_MARGIN > year > LOW_MARGIN:

                    answer = calculate_easter(year).strftime(RUSSIAN_DATE_FORMAT)
                else:

                    answer = "Невозможно рассчитать Пасху на заданную дату."
            # *** Запросили гражданские праздники
            elif word_list[0] in COMMANDS[DATE_GROUP]:

                today = f"{now_date.day:02}/{now_date.month:02}"
                answer = await self.search_in_calendar(CIVILIAN_CALENDAR, today)
            # *** Запросили церковные праздники
            elif word_list[0] in COMMANDS[DAY_GROUP]:

                today = f"{now_date.day:02}/{now_date.month:02}"
                jul_greg_delta = dtime.timedelta(days=JUL_GREG_CALENDAR_DIFF)
                jul_now_date: dtime.date = now_date - jul_greg_delta
                answer = "Сегодня " + now_date.strftime("%d %B %Y") + \
                         " г., по старому стилю " + jul_now_date.strftime("%d %B %Y") + " г. "
                answer += await self.search_in_calendar(CHURCH_CALENDAR, today)
                answer += " " + self.additional_info(now_date)
            elif word_list[0] in COMMANDS[NEW_YEAR_GROUP]:

                today: dtime.date = dtime.date.today()
                newyear: dtime.date = dtime.date(today.year, 12, 31)
                delta: dtime.timedelta = newyear - today
                print(delta.days + 1)
                answer = f"До Нового года осталось {delta.days+1} дней."
            else:

                answer = self.calc_difference(word_list)
                print("***********************", answer)
        if answer:

            print(f"Stargazer answers: {answer[:basis.OUT_MSG_LOG_LEN]}")
        return answer.strip()


    async def search_in_calendar(self, pcalendar: str, ptoday: str):
        """Ищет заданную дату в заданном календаре."""
        calendar: list = await self.load_from_file_async(self.data_path + pcalendar)
        # now_date: date = date.today()
        answer: str = ""
        for item in calendar:

            if item[:5] == ptoday:

                answer += item[6:] + "\n"
        if not answer:

            answer = "В этот день ничего не произошло."
        return answer # [:-1:]
