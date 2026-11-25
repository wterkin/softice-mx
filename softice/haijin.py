# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль - цитатник хокку. 俳人"""

from softice import basis
from softice.config import Config
from softice import librarian

# pylint: disable=too-many-branches

HAIJIN_FOLDER: str = "haijin/"
HAIJIN_FILE_NAME: str = "hokku.txt"

COMMANDS: tuple = (("hokkureload", "hkrl"),
                   ("hokkusave", "hksv"),
                   ("хокку", "hokku", "хк", "hk"),
                   ("хокку+", "hokku+", "хк+", "hk+"),
                   ("хокку-", "hokku-", "хк-", "hk-"),
                   ("хайдзин", "haijin", "хд", "hj"))

RELOAD_COMMANDS: int = 0
SAVE_COMMANDS: int = 1
ASK_COMMANDS: int = 2
ADD_COMMANDS: int = 3
DELETE_COMMANDS: int = 4
HINT_COMMANDS: int = 5

DESCRIPTIONS: tuple = ("",
                       "",
                       (f"{', '.join(COMMANDS[ASK_COMMANDS])} "
                         "[номер] [строка] : получить случайное хокку,"
                        f" либо с с заданным номером, либо содержащее заданную строку"),
                       f"{', '.join(COMMANDS[ADD_COMMANDS])} : добавить в базу новое хокку ",
                       f"{', '.join(COMMANDS[DELETE_COMMANDS])} : удалить хокку из базы")
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

    def __init__(self, pconfig: Config):

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


    def get_commands(self, proom_name: str, punit_id: str="", pdescriptions: list=None) -> str:
        """Пользователь запросил список команд."""

        assert proom_name is not None, \
            "Assert: [haijin.get_commands] " \
            "Пропущен параметр <proom_name> !"

        return super().get_commands(proom_name, UNIT_ID, DESCRIPTIONS)


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
                               f"{LEFT_BRACKET}{number}{DELIMITER}"
                               f"{len(self.hokku)}{RIGHT_BRACKET}")
            return result_text
        return ptext


    def get_hint(self, proom_name: str, punit_id: str = "", phints: str = "") -> str:
        """Возвращает список команд, поддерживаемых модулем.  """

        assert proom_name is not None, \
            "Assert: [haijin.get_hint] " \
            "Пропущен параметр <proom_name> !"

        return super().get_hint(proom_name, UNIT_ID, COMMANDS[HINT_COMMANDS])


    async def haijin(self, proom_name, puser_name: str,
                     pevent_sender: str, pmessage_text: str) -> str:
        """Процедура разбора запроса пользователя."""

        assert proom_name is not None, \
            "Assert: [haijin.haijin] " \
            "Пропущен параметр <proom_name> !"
        assert puser_name is not None, \
            "Assert: [haijin.haijin] " \
            "Пропущен параметр <puser_name> !"
        assert pevent_sender is not None, \
            "Assert: [haijin.haijin] " \
            "Пропущен параметр <pevent_sender> !"
        assert pmessage_text is not None, \
            "Assert: [haijin.haijin] " \
            "Пропущен параметр <pmessage_text> !"

        answer: str = ""
        unformatted_answer: str = ""
        word_list: list = self.parse_input(pmessage_text)
        # *** Мы можем обработать эту команду?
        if self.can_process_command(proom_name, pmessage_text, UNIT_ID, COMMANDS):

            command: int = self.identify_command(word_list[0], COMMANDS)

            # *** Возможно, запросили перезагрузку.
            if command == RELOAD_COMMANDS:

                # *** Пользователь хочет перезагрузить книгу хокку
                if self.is_master(pevent_sender):

                    await self.reload()
                    answer = "Книга загружена"
            elif command == SAVE_COMMANDS:

                # *** Пользователь хочет сохранить книгу хокку
                if self.is_master(pevent_sender):

                    await self.save_to_file_async(self.hokku, self.data_path + HAIJIN_FILE_NAME)
                    answer = "Книга сохранена"
            elif command == HINT_COMMANDS:

                # *** Пользователь хочет список команд
                answer = self.get_commands(proom_name)

            # *** Хокку запрашивали?
            elif command == ASK_COMMANDS:

                # *** Пользователь хочет хокку....
                answer = librarian.quote(self.hokku, word_list)
                if answer:

                    unformatted_answer = answer
                    answer = self.format_hokku(unformatted_answer)
                    if not answer:

                        answer = "Такого хокку нет в моей базе"
            elif command == ADD_COMMANDS:

                # *** Пользователь хочет добавить хокку в книгу
                text: str = " ".join(word_list[1:])
                if '(' not in text:

                    text += "(автор не  известен)"
                self.hokku.append(text)
                answer = (f"Спасибо, {puser_name},"
                           " хокку добавлено под номером "
                          f"{len(self.hokku)}")
            elif command == DELETE_COMMANDS:

                # *** Пользователь хочет удалить хокку из книги...
                if self.is_master(pevent_sender):

                    del self.hokku[int(word_list[1]) - 1]
                    answer = f"Хокку {word_list[1]} удалена."
                else:

                    # *** ... но не тут-то было...
                    print("> Haijin: Запрос на удаление хокку от "
                          f"нелегитимного лица {puser_name}.")
                    answer = (f"Извини, {puser_name}, "
                              f"только {self.config.master} может удалять хокку")
            if answer:

                if unformatted_answer:

                    print("> Haijin отвечает: ", unformatted_answer[:basis.OUT_MSG_LOG_LEN])
                else:

                    print("> Haijin отвечает: ", answer[:basis.OUT_MSG_LOG_LEN])
        return answer


    async def reload(self):
        """Перезагружает библиотеку."""

        self.hokku = await self.load_from_file_async(self.data_path + HAIJIN_FILE_NAME)
        print(f"> Haijin успешно (пере)загрузил {len(self.hokku)} хокку.")
