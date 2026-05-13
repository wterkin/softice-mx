# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль - цитатник хокку. 俳人"""

from softice import librarian
from softice import basis

HAIJIN_FOLDER: str = "haijin/"
HAIJIN_FILE_NAME: str = "hokku.txt"

COMMANDS: tuple = (("hokkureload", "hkrl"),
                   ("hokkusave", "hksv"),
                   ("хк", "hk"),
                   ("хк+", "hk+"),
                   ("хк-", "hk-"),
                   ("хокку", "hokku"))

RELOAD_COMMANDS: int = 0
SAVE_COMMANDS: int = 1
ASK_COMMANDS: int = 2
ADD_COMMANDS: int = 3
DELETE_COMMANDS: int = 4
HINT_COMMANDS: int = 5

DESCRIPTIONS: tuple = ("",
                       "",
                       ("хк/hk [номер] [строка] : получить случайное хокку,"
                       " либо с с заданным номером, либо содержащее заданную строку"),
                       "хк+/hk+ : добавить в базу новое хокку ",
                       "хк-/hk- : удалить хокку из базы")
USER_RIGHTS: tuple = (False, False, True, True, False)

UNIT_ID = "haijin"
LEFT_PARENTHESIS: str = "("
RIGHT_PARENTHESIS: str = ")"
LEFT_BRACKET: str = "["
RIGHT_BRACKET: str = "]"
AUTHOR_INDENT: str = "     "
DELIMITER: str = "/"

class CHaijin(basis.CBasis):
    """Класс хайдзина."""

    def __init__(self, pconfig: dict):

        super().__init__(pconfig)
        self.data_path: str = self.config.data_folder + HAIJIN_FOLDER
        self.hokku: list = []
        print("Хайдзин стартовал.")


    def can_process_command(self, proom_name: str, pmessage: str,  punit_id: str = "",
                    pcommands: list = None) -> bool:
        """Процедура определяет, сможет ли данный модуль обработать данную команду."""

        assert proom_name is not None, \
            "Assert: [haijin.can_process_command] " \
            "Пропущен параметр <proom_name> !"
        assert pmessage is not None, \
            "Assert: [haijin.can_process_command] " \
            "Пропущен параметр <pmessage> !"
        return super().can_process_command(proom_name, pmessage, UNIT_ID, COMMANDS)


    def get_commands(self, pchat_title: str, punit_id: str="", pdescriptions: list=None) -> str:
        """Пользователь запросил список команд."""

        assert pchat_title is not None, \
            "Assert: [haijin.get_commands] " \
            "Пропущен параметр <pchat_title> !"

        return super().get_commands(pchat_title, UNIT_ID, DESCRIPTIONS)


    def format_hokku(self, ptext: str) -> str:
        """Форматирует хокку так, как нам хочется."""

        assert ptext is not None, \
            "Assert: [haijin.format_hokku] " \
            "Пропущен параметр <ptext> !"

        # *** Вырежем номер
        result_text: str = ""
        if "???" not in ptext:

            if LEFT_BRACKET in ptext and RIGHT_BRACKET in ptext:

                left_par: int = ptext.index(LEFT_BRACKET)
                right_par: int = ptext.index(RIGHT_BRACKET)
                number: str = ptext[left_par + 1:right_par].strip()
                text: str = ptext[right_par + 1:]
                # *** Вырежем автора
                left_par = text.index(LEFT_PARENTHESIS)
                right_par = text.index(RIGHT_PARENTHESIS)
                author = text[left_par + 1:right_par].strip()
                text = text[:left_par]
                # *** Разобьём текст на строки
                result_text = text.replace("/", "\n")
                result_text = (f"<i> {result_text[1:]} </i> \n"
                               f" {AUTHOR_INDENT}<b>{author}</b> "
                               f"{LEFT_BRACKET}{number}{DELIMITER}{len(self.hokku)}{RIGHT_BRACKET}")
            return result_text
        return ptext


    def get_hint(self, pchat_title: str, punit_id: str = "", phints: str = "") -> str:
        """Возвращает список команд, поддерживаемых модулем.  """

        assert pchat_title is not None, \
            "Assert: [haijin.get_hint] " \
            "Пропущен параметр <pchat_title> !"

        return super().get_hint(pchat_title, UNIT_ID, COMMANDS[HINT_COMMANDS])


    async def haijin(self, pchat_title, puser_name: str, pmessage_text: str) -> str:
        """Процедура разбора запроса пользователя."""

        assert pchat_title is not None, \
            "Assert: [haijin.haijin] " \
            "Пропущен параметр <pchat_title> !"
        assert puser_name is not None, \
            "Assert: [haijin.haijin] " \
            "Пропущен параметр <puser_name> !"
        assert pmessage_text is not None, \
            "Assert: [haijin.haijin] " \
            "Пропущен параметр <pmessage_text> !"

        answer: str = ""
        unformatted_answer: str = ""
        word_list: list = self.parse_input(pmessage_text)
        # *** Мы можем обработать эту команду?
        # rint(f"+++ Hjn +++ 1 +++ {word_list[0]=}")
        # rint(f"+++ Hjn +++ 2 +++ {COMMANDS[RELOAD_COMMANDS]=}")
        if self.can_process_command(pchat_title, pmessage_text, UNIT_ID, COMMANDS):

            # *** Возможно, запросили перезагрузку.
            if word_list[0] in COMMANDS[RELOAD_COMMANDS]:

                # *** Пользователь хочет перезагрузить книгу хокку
                if self.is_master(puser_name):

                    await self.reload()
                    answer = "Книга загружена"
            elif word_list[0] in COMMANDS[SAVE_COMMANDS]:

                # *** Пользователь хочет сохранить книгу хокку
                if self.is_master(puser_name):

                    await self.save_to_file_async(self.hokku, self.data_path + HAIJIN_FILE_NAME)
                    answer = "Книга сохранена"
            elif word_list[0] in COMMANDS[HINT_COMMANDS]:

                # *** Пользователь хочет список команд
                answer = self.get_commands(pchat_title)
            else:

                answer, unformatted_answer = await self.process_command(word_list, puser_name)
            if answer:

                if unformatted_answer:

                    print("> Haijin отвечает: ", unformatted_answer[:basis.OUT_MSG_LOG_LEN])
                else:

                    print("> Haijin отвечает: ", answer[:basis.OUT_MSG_LOG_LEN])
        return answer


    async def process_command(self, pcommand: list, puser_name: str):
        """Обрабатывает пользовательские команды."""

        assert pcommand is not None, \
            "Assert: [haijin.process_command] " \
            "Пропущен параметр <pcommand> !"
        assert puser_name is not None, \
            "Assert: [haijin.process_command] " \
            "Пропущен параметр <puser_name> !"

        # *** Получим код команды
        answer: str = ""
        unformatted_answer: str = ""
        command: int = self.identify_command(pcommand[0], COMMANDS)
        if command >= 0:

            # *** Хокку запрашивали?
            if command == ASK_COMMANDS:

                # *** Пользователь хочет хокку....
                answer = librarian.quote(self.hokku, pcommand)
                if answer:

                    unformatted_answer = answer
                    answer = self.format_hokku(unformatted_answer)
                    if not answer:

                        answer = "Такого хокку нет в моей базе"

            elif command == ADD_COMMANDS:

                # *** Пользователь хочет добавить хокку в книгу
                text: str = " ".join(pcommand[1:])
                if '(' not in text:

                    text += "(автор не  известен)"
                self.hokku.append(text)
                answer = f"Спасибо, {self.parse_nick(puser_name)}, хокку добавлено под номером " \
                         f"{len(self.hokku)}"
            elif command == DELETE_COMMANDS:

                # *** Пользователь хочет удалить хокку из книги...
                if self.is_master(puser_name):

                    del self.hokku[int(pcommand[1]) - 1]
                    answer = f"Хокку {pcommand[1]} удалена."
                else:

                    # *** ... но не тут-то было...
                    print("> Haijin: Запрос на удаление хокку от "
                          f"нелегитимного лица {self.parse_nick(puser_name)}.")
                    answer = (f"Извини, {self.parse_nick(puser_name)}, "
                              f"только {self.config.master} может удалять хокку")
        return answer, unformatted_answer


    async def reload(self):
        """Перезагружает библиотеку."""

        self.hokku = await self.load_from_file_async(self.data_path + HAIJIN_FILE_NAME)
        print(f"> Haijin успешно (пере)загрузил {len(self.hokku)} хокку.")
