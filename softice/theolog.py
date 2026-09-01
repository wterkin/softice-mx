    # -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль цитатника Библии."""

import re
import random
from pathlib import Path
import aiofiles

from softice import basis

# FixMe: findbyversenumber возвращает короткое имя книги, а должно возвращаться длинное
# FixMe: найтивз не отрабатывает

# *** Путь к файлам Библии
THEOLOG_FOLDER: str = "theolog/"
# *** Константы частей сообщения
COMMAND_ARG: int = 0
LINE_ARG: int = 1

# *** Ключ для списка доступных каналов в словаре конфига
UNIT_ID = "theolog"

# *** Команды поиска текста по книгам Библии
OLD_TESTAMENT_BOOKS = range(1, 40)
NEW_TESTAMENT_BOOKS = range(40, 67)

BOOKS_LIST: tuple = (("бытие", "быт", "Книга Бытия"),
                     ("исход", "исх", "Книга Исход"),
                     ("левит", "лев", "Книга Левит"),
                     ("числа", "числ", "Книга Числа"),
                     ("второзаконие", "втор", "Книга Второзаконие"),
                     ("инавин", "нав", "Книга Иисуса Навина"),
                     ("судей", "суд", " Книга Судей"),
                     ("руфь", "руфь", "Книга Руфи"),
                     ("1царств", "1цар", "1-я книга Царств"),
                     ("2царств", "2цар", "2-я книга Царств"),
                     ("3царств", "3цар", "3-я книга Царств"),
                     ("4царств", "4цар", "4-я книга Царств"),
                     ("1паралипоменон", "1пар", "1-я книга Паралипоменон"),
                     ("2паралипоменон", "2пар", "2-я книга Паралипоменон"),
                     ("ездра", "езд", "Книга Ездры"),
                     ("неемия", "неем", "Книга Неемии"),
                     ("есфирь", "есф", "Книга Есфири"),
                     ("иов", "иов", "Книга Иова"),
                     ("псалтирь", "пс", "Псалтирь"),
                     ("притчи", "притч", "Книга Притчей"),
                     ("екклесиаст", "еккл", "Книга Екклесиаста"),
                     ("песни", "песн", "Песнь Песней"),
                     ("исаии", "ис", "Книга пророка Исайи"),
                     ("иеремии", "иер", "Книга пророка Иеремии"),
                     ("плачиеремии", "плач", "Плач Иеремии"),
                     ("иезекииль", "иез", "Книга пророка Иезекииля"),
                     ("даниил", "дан", "Книга пророка Даниила"),
                     ("осия", "ос", "Книга пророка Осии"),
                     ("иоиль", "иоиль", "Книга пророка Иоиля"),
                     ("амос", "ам", "Книга пророка Амоса"),
                     ("авдий", "ав", "Книга пророка Авдия"),
                     ("иона", "иона", "Книга пророка Ионы"),
                     ("михей", "мих", "Книга пророка Михея"),
                     ("наум", "наум", "Книга пророка Наума"),
                     ("аввакум", "авв", "Книга пророка Аввакума"),
                     ("софония", "соф", "Книга пророка Софонии"),
                     ("аггей", "агг", "Книга пророка Аггея"),
                     ("захария", "зах", "Книга пророка Захарии"),
                     ("малахия", "мал", "Книга пророка Малахии"),
                     ("матфей", "мф", "Евангелие от Матфея"),
                     ("марка", "мк", "Евангелие от Марка"),
                     ("луки", "лк", "Евангелие от Луки"),
                     ("иоанна", "ин", "Евангелие от Иоанна"),
                     ("деяния", "деян", "Деяния апостолов"),
                     ("иакова", "иак", "Послание Иакова"),
                     ("1петра", "1пет", "1-е послание Петра"),
                     ("2петра", "2пет", "2-е послание Петра"),
                     ("1иоанна", "1ин", "1-е послание Иоанна"),
                     ("2иоанна", "2ин", "2-е послание Иоанна"),
                     ("3иоанна", "3ин", "3-е послание Иоанна"),
                     ("иуды", "иуд", "1-е послание Иуды"),
                     ("римлянам", "рим", "Послание римлянам"),
                     ("1коринфянам", "1кор", "1-е послание коринфянам"),
                     ("2коринфянам", "2кор", "2-е послание коринфянам"),
                     ("галатам", "гал", "Послание галатам"),
                     ("ефесянам", "еф", "Послание ефесянам"),
                     ("филиппийцам", "флп", "Послание филиппийцам"),
                     ("колоссянам", "кол", "Послание колоссянам"),
                     ("1фессалоникийцам", "1фес", "1-е послание фессалоникийцам"),
                     ("2фессалоникийцам", "2фес", "2-е послание фессалоникийцам"),
                     ("1тимофею", "1тим", "1-е послание Тимофею"),
                     ("2тимофею", "2тим", "2-е послание Тимофею"),
                     ("титу", "тит", "Послание Титу"),
                     ("филимону", "флм", "Послание Филимону"),
                     ("евреям", "евр", "Послание евреям"),
                     ("откровение", "откр", "Откровение Иоанна Богослова"))

FIND_IN_NEW_GROUP: int = 0
FIND_IN_OLD_GROUP: int = 1
FIND_BY_VERSE_NUMBER_GROUP: int = 2
# FIND_BY_QUOTE_GROUP: int = 3
BOOKS_GROUP: int = 3
HINT_GROUP: int = 4

COMMANDS: tuple = (("найтинз", "нз", "findnew", "fn"),
                   ("найтивз", "вз", "findold", "fo"),
                   ("<имя книги>"),
                   # ("найpbook_nameти", "нт", "find", "fn"),
                   ("книги", "кн", "books", "bk"),
                   ("библия", "бб", "bible", "bb"))

MAX_SEARCH_RESULT: int = 8
FULL_SELECTION: str = "-f"
NUMBER_OF_LINES: str = "-n"
SPECIFIED_LINE: str = "-l"

DESCRIPTIONS: tuple = ((f"{', '.join(COMMANDS[FIND_IN_NEW_GROUP])} фраза - "
                         " найти указанную фразу в Новом Завете, "
                         "-f - выдать все вхождения, -n число - выдать указанное количество строк"),
                       (f"{', '.join(COMMANDS[FIND_IN_OLD_GROUP])} фраза -  "
                         "найти указанную фразу в Ветхом Завете"
                         "-f - выдать все вхождения, -n число - выдать указанное количество строк"),
                       #DESC_FIND_IN_OLD,
                       (f"{', '.join(COMMANDS[FIND_BY_VERSE_NUMBER_GROUP])} глава "
                         "стих [количество] -"
                         " получить указанные стих/стихи из выбранной книги и главы Библии."
                         " Название книги указывается в любом формате из приведенных"
                         "[ {NUMBER_OF_LINES} ] число - выдать указанное кол-во найденных строк "
                         "(макс. {MAX_SEARCH_RESULT}"
                         ),
                       #(f"{', '.join(COMMANDS[FIND_BY_QUOTE_GROUP])} 'имя книги' 'строка'"
                       #  " - Найти в указанной книге указанную цитату"
                       # "[ {FULL_SELECTION} ] - выдать все найденные строки "
                       # "(макс. {MAX_SEARCH_RESULT})"
                       #  "[ {NUMBER_OF_LINES} ] число - выдать указанное кол-во найденных строк"
                       #  " (макс. {MAX_SEARCH_RESULT}"
                       #  "[ {SPECIFIED_LINE} номер - выдать заданную строку из списка найденных ]"
                       #  ),
                       (f"{', '.join(COMMANDS[BOOKS_GROUP])} -"
                         " получить полный список книг Библии")
                         )



DEFAULT_NUMBER_OF_LINES: int = 1
DEFAULT_SPECIFIED_LINE: int = 0
MAXIMUM_ANSWER_LENGTH: int = 1024

"""
async def find_by_quote(pbook_file: str, pbook_title: str, pphrase: str,
                        pfull_selection: bool = False,
                        pnumber_of_lines: int = DEFAULT_NUMBER_OF_LINES,
                        pspecified_line: int = DEFAULT_SPECIFIED_LINE):
    ""Ищет заданную строку в заданном файле.""

    assert pbook_file is not None, \
        "Assert: [theolog:find_by_quote] " \
        "Пропущен параметр <pbook_file> !"
    assert pbook_title is not None, \
        "Assert: [theolog:find_by_quote] " \
        "Пропущен параметр <pbook_title> !"
    assert pphrase is not None, \
        "Assert: [theolog:find_by_quote] " \
        "Пропущен параметр <pphrase> !"

    result_list: list = []
    async with aiofiles.open(pbook_file, "r", encoding="utf-8") as book_file:

        async for line in book_file:

            parsed_line = re.split(r':', line, maxsplit=2)
            joined_line: str = " ".join(parsed_line[2:]).lower()
            # rint(f"+++ Th +++ fbq +++ prsl1 * {joined_line=}")
            if pphrase in joined_line:

                # rint(f"+++ Th +++ fbq +++ prsl2 * {parsed_line=}")
                result_line: str = " ".join(parsed_line[2:])
                result_list.append(f"{pbook_title} глава {parsed_line[0]} стих "
                                   f"{parsed_line[1]}: {result_line}")
            if len(result_list) >= MAX_SEARCH_RESULT:

                break

    if pfull_selection:

        return "\n".join(result_list[:MAX_SEARCH_RESULT])
    if pnumber_of_lines > DEFAULT_NUMBER_OF_LINES:

        return "\n".join(result_list[:pnumber_of_lines])
    if pspecified_line > DEFAULT_SPECIFIED_LINE:

        return result_list[pspecified_line - 1]
    if not result_list:

        return ""
    return random.choice(result_list)
"""

class CTheolog(basis.CBasis):
    """Класс теолога."""

    def __init__(self, pconfig: dict):
        """Конструктор."""

        super().__init__(pconfig)
        self.data_path: str = self.config.data_folder + THEOLOG_FOLDER


    def can_process_command(self, pchat_title: str, pmessage: str,
                            punit_id: str = "", pcommands: list = None) -> bool:  # ok
        """Процедура определяет, сможет ли данный модуль обработать данную команду."""

        assert pchat_title is not None, \
            "Assert: [theolog.can_process_command] " \
            "Пропущен параметр <pchat_title> !"
        assert pmessage is not None, \
            "Assert: [theolog.can_process_command] " \
            "Пропущен параметр <pmessage> !"

        return super().can_process_command(pchat_title, pmessage, UNIT_ID, COMMANDS)


    def can_process_book(self, pword: str) -> bool:  # ok
        """Процедура определяет, существует ли требуемая книга."""

        assert pword is not None, \
            "Assert: [theolog.can_process_book] " \
            "Пропущен параметр <pword_list> !"

        # rint(f"+++ Th +++ cpb +++ * 111 ")
        for book in BOOKS_LIST:

            if pword.lower() in book:

                # rint(f"+++ Th +++ cpb +++ * 222 ")
                return True
        return False


    async def find_by_verse_number(self, pbook_idx: int, pbook_name: str, pchapter: str,
                                   pverse: str,
                                   pnumber_of_lines: int = DEFAULT_NUMBER_OF_LINES) -> str:
        """Ищет заданную строку в файле."""

        assert pbook_idx is not None, \
            "Assert: [theolog.find_by_verse_number] No <pbook_idx> parameter specified!"
        assert pbook_name is not None, \
            "Assert: [theolog.find_by_verse_number] No <pbook> parameter specified!"
        assert pchapter is not None, \
            "Assert: [theolog.find_by_verse_number] No <pchapter> parameter specified!"
        assert pverse is not None, \
            "Assert: [theolog.find_by_verse_number] No <pverse> parameter specified!"

        answer: str = ""
        # *** Путь к файлу
        book_file_name: str = f"{self.data_path}{pbook_idx + 1}.txt"
        line_id: str = f"{pchapter}:{pverse}:"
        # *** Открываем нужную книгу и перебираем её
        async with aiofiles.open(book_file_name, "r", encoding="utf-8") as book_file:

            # *** Читаем файл построчно
            async for line in book_file:

                # *** Ищем в файле заданный идентификатор строки
                if re.search(f"^{line_id}", line) is not None:

                    # rint(f"+++ Th +++ fbvn +++ * 1")
                    # *** находим начало текста после двух двоеточий
                    text_pos: int = line.find(':', line.find(':') + 1)
                    # rint(f"+++ Th +++ fbvn +++ * {text_pos=}")

                    # *** Добавляем к тексту номер главы и стиха
                    result: str = line[:text_pos] + " " + line[text_pos+1:]
                    # rint(f"+++ Th +++ fbvn +++ * {result=}")
                    answer = f"{pbook_name} {result}"
                    # rint(f"+++ Th +++ fbvn +++ * {answer=}")
                    if pnumber_of_lines == DEFAULT_NUMBER_OF_LINES:

                        break
                # *** Если что-то нашлось в предыдущей итерации..
                elif answer:

                    # *** и нужно выдать больше одной строки...
                    if pnumber_of_lines > DEFAULT_NUMBER_OF_LINES:

                        # *** Добавляем их в ответ
                        parsed_line: list = line.split(":")
                        answer += "\n" + " ".join(parsed_line[2:])
                        pnumber_of_lines -= 1
                    else:

                        break
        return answer




    def get_commands(self, pchat_title: str, punit_id: str="", pdescriptions: list=None) -> str:
        """Пользователь запросил список команд."""

        assert pchat_title is not None, \
            "Assert: [theolog.get_commands] " \
            "Пропущен параметр <pchat_title> !"

        return super().get_commands(pchat_title, UNIT_ID, DESCRIPTIONS)


    def get_books(self, pchat_title: str) -> str:
        """Возвращает список книг Библии."""

        assert pchat_title is not None, \
            "Assert: [theolog.get_books] " \
            "Пропущен параметр <pchat_title> !"

        books: str = ""
        for book in BOOKS_LIST:

            if not book[0][0].isdigit():

                books += f"{book[0].capitalize()}({book[1]}), "
            else:

                books += f"{book[0]}({book[1]}), "
        return books


    def get_hint(self, pchat_title: str, punit_id: str = "", phints: str = "") -> str:
        """Возвращает список команд, поддерживаемых модулем.  """

        assert pchat_title is not None, \
            "Assert: [haijin.get_hint] " \
            "Пропущен параметр <pchat_title> !"

        return super().get_hint(pchat_title, UNIT_ID, COMMANDS[HINT_GROUP])


    async def find_in_testament(self, ptestament: str, pphrase: str,
                                pfull_selection: bool = False,
                                pnumber_of_lines: int = DEFAULT_NUMBER_OF_LINES,
                                pspecified_line: int = DEFAULT_SPECIFIED_LINE):
        """Ищет заданную строку по всем книгам заданного завета"""

        assert ptestament is not None, \
            "Assert: [theolog.find_in_testament] No <ptestament> parameter specified!"
        assert pphrase is not None, \
            "Assert: [theolog.find_in_testament] No <pphrase> parameter specified!"

        result_list: list = []
        parsed_line: list
        answer: str = ""
        # rint(f"+++ Th +++ fbvn +++ 0* {answer=}")

        # *** По умолчанию берем Ветхий Завет
        search_range = OLD_TESTAMENT_BOOKS
        # *** Если нужен Новый - выбираем его
        if ptestament in COMMANDS[FIND_IN_NEW_GROUP]:

            search_range = NEW_TESTAMENT_BOOKS
        # *** Перебираем книги в заданном диапазоне
        for book in search_range:

            # *** Берем полное наименование книги
            book_title: str = BOOKS_LIST[book-1][2]
            # *** И название файла книги
            book_name = f"{self.data_path}{book}.txt"
            # rint(f"+++ Th +++ fit +++ 0* {self.data_path + book_name}")

            if Path(book_name).exists():

                # *** Открываем файл и экшен!
                async with aiofiles.open(book_name, "r", encoding="utf-8") as book_file:

                    async for line in book_file:

                        lower_line = line.lower()
                        # *** Если искомая фраза содержится в строке...
                        # rint(f"+++ Th +++ fit +++ 0* {lower_line=}")
                        # rint(f"+++ Th +++ fit +++ 0* {pprase=}")
                        if pphrase in lower_line:

                            # *** Парсим строчку на три части
                            parsed_line = re.split(r'\:', line, maxsplit=2)
                            # *** Формируем ответ

                            result_list.append(f"{book_title} глава {parsed_line[0]}"
                                               f" стих {parsed_line[1]} : {parsed_line[2]}")
                            #    rint(f"+++ Th +++ fit +++ 0* {result_list=}")
                            if len(result_list) == MAX_SEARCH_RESULT:

                                break

        # *** Если что-то нашли и ответ готов...
        if len(result_list) > 0:

            # *** Если нужна полная выдача (??)
            if pfull_selection:

                answer = "\n".join(result_list)
            # *** Или задано количество строк в выдаче...
            elif pnumber_of_lines > DEFAULT_NUMBER_OF_LINES:

                pnumber_of_lines = min(pnumber_of_lines, len(result_list))
                answer = "\n".join(result_list[:pnumber_of_lines])
            elif pspecified_line > DEFAULT_SPECIFIED_LINE:

                answer = result_list[pspecified_line - 1]
            else:

                # *** Иначе берем случайную строчку
                answer = random.choice(result_list)
        return answer


    def find_book_by_name(self, pbook: str) -> int:
        """Ищет указанную книгу в списке книг."""

        book_name: str = pbook.lower()
        book_index: int = -1
        for index, book in enumerate(BOOKS_LIST):

            if book_name in book:

                book_index = index
                break
        return book_index


    async def reload(self):
        pass


    async def theolog(self, pchat_title: str, pmessage_text: str) -> str:
        """Обрабатывает запросы теолога."""

        assert pchat_title is not None, \
            "Assert: [theolog.theolog] No <pchat_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [theolog.theolog] No <pmessage_text> parameter specified!"

        answer: str = ""
        word_list: list = self.parse_input(pmessage_text.replace(":", " "))
        verse: str = ""
        param_count = len(word_list)
        #book_name: str
        chapter: str = ""
        full_selection: bool = False
        number_of_lines: int = DEFAULT_NUMBER_OF_LINES
        specified_line: int = DEFAULT_SPECIFIED_LINE
        # rint(f"+++ Th +++ th +++ * 000 ")
        # *** Можем обработать?
        if self.can_process_command(pchat_title, pmessage_text, UNIT_ID, COMMANDS) or \
            self.can_process_book(word_list[0]):

            # rint(f"+++ Th +++ th +++ * 111 ")
            # *** Если есть один параметр, то запрос помощи должен быть это
            if param_count == 1:

                if word_list[COMMAND_ARG] in COMMANDS[HINT_GROUP]:

                    return self.get_commands(pchat_title)
                # *** Либо запрос списка книг
                if word_list[COMMAND_ARG] in COMMANDS[BOOKS_GROUP]:

                    return self.get_books(pchat_title)
            # rint(f"+++ Th +++ th +++ * 111 ")
            # *** Если есть больше одного параметра, то смотрим, что там запросили
            if param_count > 1:

                # rint(f"+++ Th +++ th +++ * opt ")
                # *** Поищем, нет ли заданных опций
                for index, word in enumerate(word_list):

                    # *** Не запрошена ли полная выдача?
                    full_selection = FULL_SELECTION in word
                    if full_selection and number_of_lines == 1 and specified_line == 0:

                        word_list.remove(word)
                        break
                    # rint(f"+++ Th +++ th +++ numln * {specified_line=}")
                    # *** Возможно, есть запрос на количество строк...
                    if NUMBER_OF_LINES in word and not full_selection and specified_line == 0:

                        # *** если кроме ключа указано количество строк
                        if len(word_list) >= index + 1:

                            if word_list[index + 1].isdecimal():

                                number_of_lines = int(word_list[index + 1])
                                # rint(f"+++ Th +++ th +++ numln * {number_of_lines=}")
                                number_of_lines = min(number_of_lines, MAX_SEARCH_RESULT)
                        word_list.remove(word)
                        del word_list[index]  # +1 не нужно, так как один элемент мы уже удалили
                        break
                    # *** Возможно, указана конкретная строка, которую нужно вернуть
                    if SPECIFIED_LINE in word and not full_selection and number_of_lines == 1:

                        # *** если кроме ключа указан номер строки
                        if len(word_list) >= index + 1:

                            if word_list[index + 1].isdecimal():

                                specified_line = int(word_list[index + 1])
                        word_list.remove(word)
                        del word_list[index]
                        break
                # rint(f"+++ Th +++ th +++ * {word_list[0]=}")
                # %%%%%% Тут начинаем обрабатывать команды %%%%%%%%%%%%
                # *** Возможно, указана книга
                book_index = self.find_book_by_name(word_list[0])
                if book_index >= 0:

                    # *** Книгу и главу
                    # book_name = word_list[0].lower()
                    # rint(f"+++ Th +++ th +++ fbvn * {word_list=}")
                    # *** Если есть второй параметр, то это глава
                    if (len(word_list) > 1) and word_list[1].isdecimal():

                        chapter = word_list[1]
                        # rint(f"+++ Th +++ th +++ * {chapter=}")
                    # *** Если есть третий параметр, то это стих
                    if (len(word_list) > 2) and word_list[2].isdecimal():

                        verse = word_list[2]
                        # rint(f"+++ Th +++ th +++ * {verse=}")
                    answer = await self.find_by_verse_number(book_index, BOOKS_LIST[book_index][1],
                                                            chapter, verse, number_of_lines)
                    if not answer:

                        answer = "Нет такой главы и/или стиха в этой книге."

                # *** Если первый параметр найтинз/найтивз - команда поиска...
                if (word_list[0].lower() in COMMANDS[FIND_IN_NEW_GROUP]) or \
                (word_list[0].lower() in COMMANDS[FIND_IN_OLD_GROUP]):

                    # rint(f"+++ Th +++ th +++ * fino ")
                    # *** ..получим команду.
                    testament = word_list[0]
                    # rint(f"+++ Th +++ th +++ * fino {testament=}")
                    phrase = " ".join(word_list[1:]).lower()
                    # rint(f"+++ Th +++ th +++ * fino {phrase=}")
                    answer = await self.find_in_testament(testament, phrase, full_selection,
                                                        number_of_lines, specified_line)
            if len(answer) > 0:

                print(f"Theolog answers: {answer[:basis.OUT_MSG_LOG_LEN]}...")
            else:

                answer = "Ничего не нашёл."
        return answer[:MAXIMUM_ANSWER_LENGTH]
