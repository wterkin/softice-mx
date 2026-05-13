# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль мажордома."""

import random

from softice.config import Config
from softice import basis

UNIT_ID = "majordomo"
HINT: list = ["мажордом", "majordomo"]
COMMANDS: list = [["greet", "gt"], ["привет", "пт"]]
MAJORDOMO_FOLDER: str = "majordomo/greetings.txt"


class CMajordomo(basis.CBasis):
    """Прототип классов модулей бота."""

    def __init__(self, pconfig: Config):

        assert pconfig is not None, \
            "Assert: [majordomo.__init__] " \
            "Пропущен параметр <pconfig> !"
        super().__init__(pconfig)
        self.data_path: str = self.config.data_folder + MAJORDOMO_FOLDER
        self.greetings: list = []


    async def reload(self) -> None:
        """Вызывает перезагрузку внешних данных модуля."""

        self.greetings = await self.load_from_file_async(self.data_path)

    def get_hint(self, pchat_title, punit_id: str = "", phints: str = "") -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""

        assert pchat_title is not None, \
            "Assert: [majordomo.get_hint] " \
            "Пропущен параметр <pchat_title> !"
        return super().get_hint(pchat_title, UNIT_ID, HINT)



    async def majordomo(self, pchat_title, pmessage_text) -> str:
        """Главная функция модуля."""

        assert pchat_title is not None, \
            "Assert: [majordomo.majordomo] " \
            "Пропущен параметр <pchat_title> !"
        assert pmessage_text is not None, \
            "Assert: [majordomo.majordomo] " \
            "Пропущен параметр <pmessage_text   > !"

        answer: str = ""
        word_list: list = self.parse_input(pmessage_text)
        # rint(f"+++ MjDm +++ 1 +++ {word_list=}")
        # *** Эта команда входит в список основных команд модуля?
        if self.can_process_command(pchat_title, pmessage_text, UNIT_ID, COMMANDS):

            # rint(f"+++ MjDm +++ 3 +++ process")
            # *** Ок. Указано, кого приветствовать?
            if len(word_list) > 1:

                # *** Приветствуем.
                answer = random.choice(self.greetings) % word_list[1]
                # rint(f"+++ MjDm +++ 4 +++ {answer=}")

        # *** Не запросили ли список команд?
        elif word_list[0] in HINT:

            # rint(f"+++ MjDm +++ 2 +++ {HINT=}")
            # *** Отправляем полный список команд
            answer = self.get_commands(pchat_title, UNIT_ID, COMMANDS)
        return answer
