# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov  pakhomenkov dog mail.ru
"""Модуль - цитатник для бота."""

import random

from softice import basis

# *** Команды для цитатника высказываний
ASK_QUOTE_CMD: int = 0
FIND_QUOTE_CMD: int = 1
ADD_QUOTE_CMD: int = 2
DEL_QUOTE_CMD: int = 3

RELOAD_LIBRARY: list = ["lbreload", "lbrl"]
SAVE_LIBRARY: list = ["lbsave", "lbsv"]
LIBRARIAN_FOLDER: str = "librarian/"
QUOTES_FILE_NAME: str = "quotes.txt"

QUOTES_DESC: list = [" : получить случайную цитату",
                     " : найти цитату по фрагменту текста",
                     " : добавить цитату"]

QUOTES_COMMANDS: list = [["цитата", "цт", "quote", "qt"],
                         ["цитиск", "цт?", "quotefind", "qt?"],
                         ["цитдоб", "цт+", "quoteadd", "qt+"],
                         ["цитудал", "цт-", "quotedel", "qt-"]
                         ]

HINT = ["библиотека", "биб", "library", "lib"]
UNIT_ID = "librarian"


def find_in_book(pbook: list, pword_list: list) -> str:
    """Ищет цитату в книге по заданной строке"""

    assert pbook is not None, \
        "Assert: [librarian.find_in_book] " \
        "Пропущен параметр <pbook> parameter !"
    assert pword_list is not None, \
        "Assert: [librarian.find_in_book] " \
        "Пропущен параметр <pword_list> !"

    answer: str = ""
    if len(pword_list) > 1:

        found_list: list = []
        search_line: str = " ".join(pword_list[1:])
        for idx, line in enumerate(pbook):

            if search_line.upper() in line.upper():

                found_list.append(f"[{idx+1}]{line}")

        if len(found_list) > 0:

            answer = random.choice(found_list)

    if not answer:

        answer = basis.MESSAGE_NOT_FOUND
    return answer


def get_command(pword: str) -> int:
    """Распознает команду и возвращает её код, в случае неудачи - None. """

    assert pword is not None, \
        "Assert: [librarian.get_command] " \
        "Пропущен параметр <pword> !"
    result: int = -1
    for command_idx, command in enumerate(QUOTES_COMMANDS):

        if pword in command:

            result = command_idx
            break
    return result


def quote(pbook: list, pword_list: list) -> str:
    """ Возвращает хокку или цитату с заданным номером, если номер не задан, то случайную."""

    assert pbook is not None, \
        "Assert: [librarian.quote] " \
        "Пропущен параметр <pbook> !"
    assert pword_list is not None, \
        "Assert: [librarian.quote] " \
        "Пропущен параметр <pword_list> !"

    answer: str
    if len(pword_list) > 1:

        # *** ... с заданным номером.
        if pword_list[1].isdigit():

            number: int = abs(int(pword_list[1]))
            if number > 0:

                if len(pbook) >= number:

                    answer = f"[{number}] {pbook[number-1]}"
                else:

                    answer = f"Номер должен быть от 1 до {len(pbook)}"
            else:

                answer = "Номер должен быть больше нуля"
        else:

            answer = find_in_book(pbook, pword_list)
    else:

        # *** случайную.
        answer = random.choice(pbook)
        answer = f"[{pbook.index(answer)+1}] {answer}"
    return answer


class CLibrarian(basis.CBasis):
    """Класс библиотекаря."""

    def __init__(self, pconfig):

        super().__init__(pconfig)
        self.data_path: str = self.config.data_folder + LIBRARIAN_FOLDER
        self.quotes: list = []
        print("Библиотекарь стартовал.")


    def can_class_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если библиотекарь может обработать эту команду."""

        assert pchat_title is not None, \
            "Assert: [librarian.can_class_process] " \
            "Пропущен параметр <pchat_title> !"
        assert pmessage_text is not None, \
            "Assert: [librarian.can_class_process] " \
            "Пропущен параметр <pmessage_text> !"

        found: bool = False
        if self.is_enabled(pchat_title, UNIT_ID):

            word_list: list = self.parse_input(pmessage_text)
            for command in QUOTES_COMMANDS:

                found = word_list[0] in command
                if found:

                    break
            if not found:

                found = word_list[0] in HINT
                if not found:

                    found = word_list[0] in RELOAD_LIBRARY
                    if not found:

                        found = word_list[0] in SAVE_LIBRARY
        return found


    def execute_quotes_commands(self, puser_name: str, pword_list: list, pcommand: int) -> str:
        """Выполняет команды, касающиеся базы цитат."""

        assert pword_list is not None, \
            "Assert: [librarian.execute_quotes_commands] " \
            "Пропущен параметр <pword_list> !"
        assert pcommand is not None, \
            "Assert: [librarian.execute_quotes_commands] " \
            "Пропущен параметр <pcommand> !"

        answer: str = ""
        # *** В зависимости от команды выполняем действия
        if pcommand == ASK_QUOTE_CMD:

            answer = quote(self.quotes, pword_list)
        elif pcommand == ADD_QUOTE_CMD:

            # *** Пользователь хочет добавить цитату в книгу
            self.quotes.append(" ".join(pword_list[1:]))
            answer = f"Спасибо, {puser_name}, цитата добавлена под номером {len(self.quotes)}."
        elif pcommand == DEL_QUOTE_CMD:

            # *** Пользователь хочет удалить цитату из книги...
            if puser_name == self.config.master:

                del self.quotes[int(pword_list[1])-1]
                answer = f"Цитата {pword_list[1]} удалена"
            else:

                # *** ... но не тут-то было...
                print(f"> Librarian: Запрос на удаление цитаты от "
                      f"нелегитимного лица {puser_name}.")
                answer = (f"Извини, {puser_name}, "
                          f"только {self.config.master} может удалять цитаты")
        elif pcommand == FIND_QUOTE_CMD:

            answer = find_in_book(self.quotes, pword_list)
        return answer


    def get_help(self, pchat_title: str) -> str:
        """Пользователь запросил список команд."""

        assert pchat_title is not None, \
            "Assert: [librarian.get_help] " \
            "No <pchat_title> parameter specified!"

        command_list: str = ""
        if self.is_enabled(pchat_title, UNIT_ID):

            for command in QUOTES_COMMANDS:

                command_list += ", ".join(command)
                command_list += "\n"
        return command_list


    def get_hint(self, pchat_title: str) -> str:  # [arguments-differ]
        """Возвращает список команд, поддерживаемых модулем.  """

        assert pchat_title is not None, \
            "Assert: [librarian.get_hint] " \
            "Пропущен параметр <pchat_title> !"

        if self.is_enabled(pchat_title, UNIT_ID):

            return ", ".join(HINT)
        return ""


    def is_master(self, puser_name):
        """Проверяет, является ли пользователь хозяином бота."""

        if puser_name == self.config.master:

            return True, ""
        # *** Низзя
        print(f"> Librarian: Запрос на удаление цитаты от нелегитимного лица {puser_name}.")
        return False, f"У вас нет на это прав, {puser_name}."


    async def librarian(self, pchat_title, puser_name: str, pmessage_text: str) -> str:
        """Процедура разбора запроса пользователя."""

        assert pchat_title is not None, \
            "Assert: [librarian.librarian] " \
            "Пропущен параметр <pchat_title> !"

        command: int
        answer: str = ""
        word_list: list = self.parse_input(pmessage_text)

        if self.can_class_process(pchat_title, pmessage_text):

            # *** Возможно, запросили перезагрузку.
            if word_list[0] in RELOAD_LIBRARY:

                # *** Пользователь хочет перезагрузить библиотеку
                can_reload, answer = self.is_master(puser_name)
                if can_reload:

                    await self.reload()
                    answer = "Книга обновлена"
                else:

                    # *** ... но не тут-то было...
                    print(f"> Librarian: Запрос на перегрузку цитат от "
                          f"нелегитимного лица {puser_name}.")
                    answer = (f"Извини, {puser_name}, "
                              f"только {self.config.master} может перегружать цитаты!")
            elif word_list[0] in SAVE_LIBRARY:

                # *** Пользователь хочет сохранить книгу хокку
                can_reload, answer = self.is_master(puser_name)
                if can_reload:

                    await self.save_to_file_async(self.quotes, self.data_path + QUOTES_FILE_NAME)
                    answer = "Книга сохранена"
                else:

                    # *** ... но не тут-то было...
                    print(f"> Librarian: Запрос на сохранение цитат от "
                          f"нелегитимного лица {puser_name}.")
                    answer = (f"Извини, {puser_name}, "
                              f"только {self.config.master} может сохранять цитаты!")
            elif word_list[0] in HINT:

                answer = self.get_help(pchat_title)
            else:

                # *** Получим код команды
                command = get_command(word_list[0])
                if command >= 0:

                    answer = self.execute_quotes_commands(puser_name, word_list, command)
            if answer:

                print("> Librarian отвечает: ", answer[:basis.OUT_MSG_LOG_LEN])
        return answer


    async def reload(self):
        """Перезагружает библиотеку."""

        self.quotes = await self.load_from_file_async(self.data_path + QUOTES_FILE_NAME)
        print(f"> Librarian успешно (пере)загрузил {len(self.quotes)} цитат(ы)")
