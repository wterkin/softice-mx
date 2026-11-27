# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль болтуна."""

import random
import string
from datetime import datetime, timedelta
from pathlib import Path
import asyncio

from softice.config import Config
from softice import basis

# pylint: disable=too-many-nested-blocks
# *** Команда перегрузки текстов
COMMANDS: tuple = (("blreload", "blrl"),
                   ("stoptalk", "st", "молчи", "мч"),
                   ("letstalk", "lt", "болтай", "бт"),
                   ("babbler", "болтун"))

RELOAD_GROUP: int = 0
QUIET_GROUP: int = 1
TALK_GROUP: int = 2
HINT_GROUP: int = 3

DESCRIPTIONS: tuple = ("",
                       (f"{', '.join(COMMANDS[QUIET_GROUP])} : "
                        f"[1-15 (минут)] Отключение болтуна на указанное "),
                        ""
                       )


# *** Ключ для списка доступных чатов в словаре конфига
UNIT_ID = "babbler"
BABBLER_PATH: str = "babbler/"
BABBLER_PERIOD_KEY = "period"
TRIGGERS_FOLDER: str = "triggers"
TRIGGERS_INDEX: int = 0
REACTIONS_FOLDER: str = "reactions"
REACTIONS_INDEX: int = 1
BABBLER_EMODJI: list = ["😎", "😊", "☺", "😊", "😋"]
NICKNAMES: list = ["softicebot","softice", "софтик", "софтайсик", "ботик", "бот"]
AT_CHAR: str = "@"
DELIMITER: str = "//"
QUIET_TIME: int = 7  # min
MAX_QUIET_TIME: int = 15  # min
class CBabbler(basis.CBasis):
    """Класс болтуна."""

    def __init__(self, pconfig: Config):
        """Конструктор."""

        assert pconfig is not None, \
            "Assert: [CBabbler.__init__] " \
            "Пропущен параметр <pconfig> !"

        super().__init__(pconfig)
        self.data_path: str = self.config.data_folder + BABBLER_PATH
        self.mind: list = []
        self.last_phrase_time: datetime = datetime.now()
        print("Болтун стартовал.")


    async def babbler(self, proom_name: str, puser_name: str, pmessage: str) -> str:
        """Обработчик команд болтуна"""

        assert proom_name is not None, \
            "Assert: [CBabbler.babbler] " \
            "Пропущен параметр <proom_name> !"
        assert puser_name is not None, \
            "Assert: [CBabbler.babbler] " \
            "Пропущен параметр <puser_name> !"
        assert pmessage is not None, \
            "Assert: [CBabbler.babbler] " \
            "Пропущен параметр <pmessage> !"

        answer: str = ""
        delay: int = QUIET_TIME
        word_list: list = self.parse_input(pmessage)
        if self.can_process_command(proom_name, pmessage, UNIT_ID, COMMANDS):

            # *** Если это запрос списка команд..
            if word_list[0] in COMMANDS[HINT_GROUP]:

                # *** Возвращаем список команд
                answer = self.get_commands(proom_name)
            elif word_list[0] in COMMANDS[RELOAD_GROUP]:

                if self.is_master(puser_name):

                    await self.reload()
                    answer = "База болтуна обновлена"
                else:

                    print(f"> Babbler: Запрос на перезагрузку конфига от "
                          f"нелегитимного лица {puser_name}.")
                    answer = f"У вас нет на это прав, {puser_name}."
            elif word_list[0] in COMMANDS[QUIET_GROUP]:

                if len(word_list) > 1:

                    if word_list[1].isdigit():

                        value: int = int(word_list[1])
                        if MAX_QUIET_TIME > value > 0:

                            delay = value
                answer = "молчу, молчу..."
                self.last_phrase_time += timedelta(minutes=delay)
            elif word_list[0] in COMMANDS[TALK_GROUP]:

                answer = "что, уже можно?"
                self.last_phrase_time=datetime.now()
        return answer


    def get_commands(self, proom_name: str, punit_id: str="", pdescriptions: list=None) -> str:
        """Пользователь запросил список команд."""

        assert proom_name is not None, \
            "Assert: [CBabbler.get_commands] " \
            "Пропущен параметр <proom_name> !"

        return super().get_commands(proom_name, UNIT_ID, DESCRIPTIONS)


    def get_hint(self, proom_name: str, punit_id: str = "", phints: str = "") -> str:
        """Возвращает список команд, поддерживаемых модулем.  """

        assert proom_name is not None, \
            "Assert: [CBabbler.get_hint] " \
            "Пропущен параметр <proom_name> !"

        return super().get_hint(proom_name, UNIT_ID, COMMANDS[HINT_GROUP])


    def is_personal(self, pword_list: list) -> bool:
        """Определяет, есть ли во входном сообщении имя бота."""

        assert pword_list is not None, \
            "Assert: [CBabbler.is_personal] " \
            "Пропущен параметр <pword_list> !"

        personal: bool = False
        for nick in NICKNAMES:


            personal = nick in pword_list
            if personal:

                break
        return personal


    async def talk(self, proom_name: str, pmessage: str) -> str:
        """Улучшенная версия болтуна."""

        assert proom_name is not None, \
            "Assert: [CBabbler.talk] " \
            "Пропущен параметр <proom_name> !"
        assert pmessage is not None, \
            "Assert: [CBabbler.talk] " \
            "Пропущен параметр <pmessage> !"

        answer: str = ""
        file_name: str = ""

        if self.is_enabled(proom_name, UNIT_ID):

            # *** Заданный период времени с последней фразы прошел?
            minutes: float = (datetime.now() - self.last_phrase_time).total_seconds() / \
                                int(self.config.babbler[BABBLER_PERIOD_KEY])
            if minutes > 1:

                answer, file_name = await self.think(pmessage)
            if answer:

                print(f"> Babbler отвечает: {answer[:basis.OUT_MSG_LOG_LEN]}...")
                self.last_phrase_time = datetime.now()
        return answer, file_name


    async def reload(self):
        """Загружает тексты болтуна."""

        result: bool = False
        # *** Собираем пути
        triggers_path = Path(self.data_path) / TRIGGERS_FOLDER
        assert triggers_path.is_dir(), f"{TRIGGERS_FOLDER} must be folder"
        reactions_path = Path(self.data_path) / REACTIONS_FOLDER
        assert reactions_path.is_dir(), f"{REACTIONS_FOLDER} must be folder"

        # *** Очищаем список блоков
        self.mind.clear()
        # *** Заполняем список блоков триггеров/реакций
        for trigger in triggers_path.iterdir():

            if trigger.is_file():

                module = Path(trigger).resolve().name
                reaction = reactions_path / module
                if reaction.is_file():

                    trigger_content = await self.load_from_file_async(str(trigger))
                    block: list = [trigger_content]
                    reaction_content: list = await self.load_from_file_async(str(reaction))
                    block.append(reaction_content)
                    self.mind.append(block)
                    result = True
        if self.mind:

            print(f"\n> Babbler успешно (пере)загрузил {len(self.mind)} реакций.")
        return result


    async def think(self, pmessage: str):
        """Процесс принятия решений =)"""

        assert pmessage is not None, \
            "Assert: [CBabbler.think] " \
            "Пропущен параметр <pmessage> !"

        reactions_path: Path = Path(self.data_path) / REACTIONS_FOLDER
        word_list: list = pmessage.split(" ")
        answer: str = ""
        file_name: str = ""
        # *** Если в сообщении указано имя бота..
        personal_appeal: bool = self.is_personal(pmessage.lower().split(" "))
        # *** Перебираем сообщение по словам
        for word in word_list:

            # *** Убираем из слова знаки пунктуации и пробелы,
            #     переводим в нижний регистр
            clean_word: str = word.rstrip(string.punctuation).lower().strip()
            # *** Если что-то осталось, двигаемся дальше.
            if len(clean_word) > 1:

                # *** Перебираем блоки памяти бота
                for block in self.mind:

                    # *** Получим список триггеров текущего блока
                    triggers: list = block[TRIGGERS_INDEX]
                    # *** Если в списке триггеров есть такое слово
                    if (clean_word in triggers) or ((AT_CHAR + clean_word) in triggers):

                        # *** Если в триггере указано запрошенное слово с
                        #     собачкой "@" впереди...
                        if AT_CHAR in "".join(triggers):

                            # *** Если в сообщении есть имя бота...
                            if personal_appeal:

                                # *** Выводим ответ
                                answer = f"{random.choice(block[REACTIONS_INDEX])}"
                                await asyncio.sleep(1)
                                break
                        else:

                            answer = f"{random.choice(block[REACTIONS_INDEX])}"
                        # *** Если в ответе есть разделитель...
                        if DELIMITER in answer:

                            file_name, answer = answer.split(DELIMITER)
                            file_name = f"{str(reactions_path)}/{file_name}"
                        await asyncio.sleep(1)
                        break

                    if answer:

                        break
            if answer:

                break
        return answer, file_name.replace("\\", "/")
