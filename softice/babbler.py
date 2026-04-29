# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль болтуна."""

import random
import string
from datetime import datetime
from pathlib import Path
import asyncio

from softice.config import Config
from softice import basis

# *** Команда перегрузки текстов
COMMANDS: list = ["blreload", "blrl"]
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
DELIMIGHTER: str = "//"


class CBabbler(basis.CBasis):
    """Класс болтуна."""

    def __init__(self, pconfig: Config):
        """"Конструктор."""

        super().__init__(pconfig)
        # self.config: Config = pconfig
        self.data_path: str = self.config.data_folder + BABBLER_PATH  # pdata_path + BABBLER_PATH
        self.mind: list = []
        self.last_phrase_time: datetime = datetime.now()


    async def babbler(self, proom: str, psender: str, pmessage: str) -> str:
        """Обработчик команд болтуна"""

        answer: str = ""
        word_list: list = self.parse_input(pmessage)
        if self.can_process(proom, UNIT_ID, pmessage, COMMANDS):

            # *** Возможно, запросили перезагрузку базы.
            if word_list[0] in COMMANDS:

                if self.is_master(psender):

                    await self.reload()
                    answer = "База болтуна обновлена"
                else:

                    print(f"> Babbler: Запрос на перезагрузку конфига от "
                          f"нелегитимного лица {psender}.")
                    answer = f"У вас нет на это прав, {psender}."
        return answer


    def is_personal(self, pword_list: list) -> bool:
        """Определяет, есть ли во входном сообщении имя бота."""

        personal: bool = False
        for nick in NICKNAMES:


            personal = nick in pword_list
            if personal:

                break
        return personal


    async def talk(self, proom: str, pmessage: str) -> str:
        """Улучшенная версия болтуна."""

        answer: str = ""
        file_name: str = ""
        if self.is_enabled(proom, UNIT_ID):

            #:: Babbler is enabled here")
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
                        if DELIMIGHTER in answer:

                            file_name, answer = answer.split(DELIMIGHTER)
                            file_name = f"{str(reactions_path)}/{file_name}"
                        await asyncio.sleep(1)
                        break

                    if answer:

                        break
            if answer:

                break
        return answer, file_name.replace("\\", "/")
