# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov  pakhomenkov dog mail.ru
"""Модуль - цитатник для бота."""

import random

from softice import basis

# *** Команды для цитатника высказываний

#RELOAD_LIBRARY: list = ["lbreload", "lbrl"]
#SAVE_LIBRARY: list = ["lbsave", "lbsv"]
LIBRARIAN_FOLDER: str = "librarian/"
QUOTES_FILE_NAME: str = "quotes.txt"


COMMANDS: tuple = (("цитата", "цт", "quote", "qt"),
                   ("цитиск", "цт?", "quotefind", "qt?"),
                   ("цитдоб", "цт+", "quoteadd", "qt+"),
                   ("цитудал", "цт-", "quotedel", "qt-"),
                   ("lbreload", "lbrl"),
                   ("lbsave", "lbsv"),
                   ("библиотека", "биб", "library", "lib")
                  )

ASK_QUOTE_COMMAND: int = 0
FIND_QUOTE_COMMAND: int = 1
ADD_QUOTE_COMMAND: int = 2
DEL_QUOTE_COMMAND: int = 3
LOAD_COMMAND: int = 4
SAVE_COMMAND: int = 5
HINT_COMMAND: int = 6

DESCRIPTIONS: tuple = (f"{', '.join(COMMANDS[ASK_QUOTE_COMMAND])}: получить случайную цитату",
                       (f"{', '.join(COMMANDS[FIND_QUOTE_COMMAND])}: "
                        "найти цитату по фрагменту текста"),
                       f"{', '.join(COMMANDS[ADD_QUOTE_COMMAND])}: добавить цитату")

# HINT = []
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
    # rint(f"+++ Lib +++ 1 +++ ")
    if len(pword_list) > 1:

        found_list: list = []
        search_line: str = " ".join(pword_list[1:])
        for idx, line in enumerate(pbook):

            if search_line.upper() in line.upper():

                # rint(f"+++ Lib +++ 5 +++ {idx=}")
                # rint(f"+++ Lib +++ 6 +++ {line=}")
                found_list.append(f"[{idx+1}] {line}")

        if len(found_list) > 0:

            # rint(f"+++ Lib +++ 2 +++ {found_list=}")
            answer = random.choice(found_list)
            # rint(f"+++ Lib +++ 3 +++ {answer=}")

    if not answer:

        answer = basis.MESSAGE_NOT_FOUND
    # rint(f"+++ Lib +++ 3 +++ {answer=}")
    return answer


def get_command(pword: str) -> int:
    """Распознает команду и возвращает её код, в случае неудачи - None. """

    assert pword is not None, \
        "Assert: [librarian.get_command] " \
        "Пропущен параметр <pword> !"

    result: int = -1
    for command_idx, command in enumerate(COMMANDS):

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

    answer: str = ""
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
            # rint(f"+++ Lib +++ 10 +++ {answer=}")
    else:

        # *** случайную.
        answer = random.choice(pbook)
        answer = f"[{pbook.index(answer)+1}] {answer}"
        # rint(f"+++ Lib +++ 11 +++ {answer=}")
    return answer


class CLibrarian(basis.CBasis):
    """Класс библиотекаря."""

    def __init__(self, pconfig):

        assert pconfig is not None, \
        "Assert: [CLibrarian.__init__] " \
        "Пропущен параметр <pconfig> !"

        super().__init__(pconfig)
        self.data_path: str = self.config.data_folder + LIBRARIAN_FOLDER
        self.quotes: list = []
        print("Библиотекарь стартовал.")


    def can_process_command(self, pchat_title: str, pmessage: str,  punit_id: str = "",
                    pcommands: list = None) -> bool:
        """Процедура определяет, сможет ли данный модуль обработать данную команду."""

        assert pchat_title is not None, \
            "Assert: [CLibrarian.can_process_command] " \
            "Пропущен параметр <pchat_title> !"
        assert pmessage is not None, \
            "Assert: [CLibrarian.can_process_command] " \
            "Пропущен параметр <pmessage> !"

        return super().can_process_command(pchat_title, pmessage, UNIT_ID, COMMANDS)



    def execute_quotes_commands(self, puser_name: str, pword_list: list, pcommand: int) -> str:
        """Выполняет команды, касающиеся базы цитат."""

        assert puser_name is not None, \
            "Assert: [CLibrarian.execute_quotes_commands] " \
            "Пропущен параметр <puser_name> !"
        assert pword_list is not None, \
            "Assert: [CLibrarian.execute_quotes_commands] " \
            "Пропущен параметр <pword_list> !"
        assert pcommand is not None, \
            "Assert: [CLibrarian.execute_quotes_commands] " \
            "Пропущен параметр <pcommand> !"

        answer: str = ""
        # *** В зависимости от команды выполняем действия
        if pcommand == ASK_QUOTE_COMMAND:

            answer = quote(self.quotes, pword_list)
        elif pcommand == ADD_QUOTE_COMMAND:

            # *** Пользователь хочет добавить цитату в книгу
            self.quotes.append(" ".join(pword_list[1:]))
            answer = f"Спасибо, {puser_name}, цитата добавлена под номером {len(self.quotes)}."
        elif pcommand == DEL_QUOTE_COMMAND:

            # *** Пользователь хочет удалить цитату из книги...
            if self.is_master(puser_name):

                del self.quotes[int(pword_list[1])-1]
                answer = f"Цитата {pword_list[1]} удалена"
            else:

                # *** ... но не тут-то было...
                print(f"> Librarian: Запрос на удаление цитаты от "
                      f"нелегитимного лица {puser_name}.")
                answer = (f"Извини, {puser_name}, "
                          f"только {self.config.master} может удалять цитаты")
        elif pcommand == FIND_QUOTE_COMMAND:

            answer = find_in_book(self.quotes, pword_list)
        return answer


    def get_commands(self, pchat_title: str, punit_id: str="", pdescriptions: list=None) -> str:
        """Пользователь запросил список команд."""

        assert pchat_title is not None, \
            "Assert: [CLibrarian.get_commands] " \
            "Пропущен параметр <pchat_title> !"

        return super().get_commands(pchat_title, UNIT_ID, DESCRIPTIONS)


    def get_hint(self, pchat_title: str, punit_id: str = "", phints: str = "") -> str:
        """Возвращает список команд, поддерживаемых модулем.  """

        assert pchat_title is not None, \
            "Assert: [CLibrarian.get_hint] " \
            "Пропущен параметр <pchat_title> !"

        return super().get_hint(pchat_title, UNIT_ID, COMMANDS[HINT_COMMAND])


    async def librarian(self, pchat_title, puser_name: str, pmessage_text: str) -> str:
        """Процедура разбора запроса пользователя."""

        assert pchat_title is not None, \
            "Assert: [CLibrarian.librarian] " \
            "Пропущен параметр <pchat_title> !"
        assert puser_name is not None, \
            "Assert: [CLibrarian.librarian] " \
            "Пропущен параметр <puser_name> !"

        command: int
        answer: str = ""
        word_list: list = self.parse_input(pmessage_text)
        if self.can_process_command(pchat_title, pmessage_text):

            # *** Возможно, запросили перезагрузку.
            if word_list[0] in COMMANDS[LOAD_COMMAND]:

                # *** Пользователь хочет перезагрузить библиотеку
                can_reload = self.is_master(puser_name)
                if can_reload:

                    await self.reload()
                    answer = "Книга обновлена"
                else:

                    # *** ... но не тут-то было...
                    print(f"> Librarian: Запрос на перегрузку цитат от "
                          f"нелегитимного лица {puser_name}.")
                    answer = (f"Извини, {puser_name}, "
                              f"только {self.config.master} может перегружать цитаты!")
            elif word_list[0] in COMMANDS[SAVE_COMMAND]:

                # *** Пользователь хочет сохранить книгу хокку
                can_reload = self.is_master(puser_name)
                if can_reload:

                    await self.save_to_file_async(self.quotes, self.data_path + QUOTES_FILE_NAME)
                    answer = "Книга сохранена"
                else:

                    # *** ... но не тут-то было...
                    print(f"> Librarian: Запрос на сохранение цитат от "
                          f"нелегитимного лица {puser_name}.")
                    answer = (f"Извини, {puser_name}, "
                              f"только {self.config.master} может сохранять цитаты!")
            elif word_list[0] in COMMANDS[HINT_COMMAND]:

                answer = self.get_commands(pchat_title)
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
