# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль антимата для бота."""

import re
from pathlib import Path
from nio import MatrixRoom, AsyncClient, RoomMessageText, RoomRedactResponse
from softice import basis


RELOAD_GROUP: int = 0
COMMANDS: tuple = (("bwreload", "bwrl"))

UNIT_ID = "moderator"
DATA_FOLDER: str = "moderator"
BAD_WORDS_FILE: str = "bad_words.txt"
CENSOR_PREFIX = r"\[\*\*"
CENSOR_POSTFIX = r"\*\*\]"
CENSORED: str = "*beep*"


def replace_bad_words(pbad_word: str, ptext: str) -> str:
    """Заменяет мат в строке на безобидное слово."""

    assert pbad_word is not None, \
        "Assert: [moderator:replace_bad_words] " \
        "Пропущен параметр <pbad_word> !"
    assert ptext is not None, \
        "Assert: [moderator:replace_bad_words] " \
        "Пропущен параметр <ptext> !"

    words: list = ptext.split(" ")
    for wordindex, word in enumerate(words):

        if re.match(pbad_word, word) is not None:

            words[wordindex] = CENSORED
    return " ".join(words)


class CModerator(basis.CBasis):
    """Класс модератора."""

    def __init__(self, pconfig: dict, pclient: AsyncClient):

        super().__init__(pconfig)
        self.data_path: str = self.config.data_folder + DATA_FOLDER
        self.client = pclient
        self.bad_words: list = []


    def can_process_command(self, pchat_title: str, pmessage: str,  punit_id: str = "",
                    pcommands: list = None) -> bool:
        """Процедура определяет, сможет ли данный модуль обработать данную команду."""

        assert pchat_title is not None, \
            "Assert: [moderator.can_process_command] " \
            "Пропущен параметр <pchat_title> !"
        assert pmessage is not None, \
            "Assert: [moderator.can_process_command] " \
            "Пропущен параметр <pmessage> !"
        return super().can_process_command(pchat_title, pmessage, UNIT_ID, COMMANDS)


    def check_bad_words_ex(self, pmessage: str) -> str:
        """Проверяет сообщение на наличие мата."""

        assert pmessage is not None, \
            "Assert: [moderator.check_bad_words_ex] " \
            "Пропущен параметр <pmessage> !"

        # rint(f"+++ Mod +++ CBW +++ {pmessage=}")
        answer: str = ""
        detected: bool = False
        text_answer: str = ""
        if pmessage:

            text: str = pmessage.lower()
            # rint(f"+++ Mod +++ CBW +++ {text=}")
            for bad_word in self.bad_words:

                result: bool = True
                while result:

                    # result = re.match(bad_word, text) is not None
                    # rint(f"+++ Mod +++ CBW +++ {bad_word=}")

                    result: re.Search = re.search(bad_word, text, re.IGNORECASE & re.VERBOSE)
                    # rint(f"+++ Mod +++ CBW +++ {result=}")
                    if result:

                        detected = True
                        # rint(f"+++ Mod +++ CBW +++ Detected!!! ")
                        count: int = result.end()-result.start()
                        # rint(f"+++ Mod +++ CBW +++ {result.start()=}")
                        # rint(f"+++ Mod +++ CBW +++ {result.end()=}")
                        # rint(f"+++ Mod +++ CBW +++ {count=} ")
                        # rint(f"+++ Mod +++ CBW +++ {text[:result.start()]=}")
                        # rint(f"+++ Mod +++ CBW +++ {text[result.end():]=}")
                        text_answer = text[:result.start()]+ "*" * count + text[result.end():]
                        text = text_answer
                        # rint(f"+++ Mod +++ CBW +++ {text_answer=}")
                       
                        # text[result.start():result.end()+1] = "*"*count
            if detected:

                answer = text_answer
        print(f"+++ Mod +++ CBW +++ {answer=}")
        return answer


    def control_talking(self, proom: MatrixRoom, pevent: RoomMessageText, plocal_name: str) -> str:
        """Следит за матершинниками."""

        assert proom is not None, \
            "Assert: [moderator.control_talking] " \
            "Пропущен параметр <proom> !"
        assert pevent is not None, \
            "Assert: [moderator.control_talking] " \
            "Пропущен параметр <pevent> !"
        assert plocal_name is not None, \
            "Assert: [moderator.control_talking] " \
            "Пропущен параметр <plocal_name> !"

        answer: str = ""
        text: str
        if self.is_enabled(proom.name, UNIT_ID):

            text = self.check_bad_words_ex(pevent.body)
            if text:
                if self.client:

                    self.delete_message(proom, pevent)
                print(f"Пользователь {plocal_name} матерился в чате {proom.name}.")
                print(f"Он сказал: {text}")
                answer = f"{plocal_name} хотел сказать \"{text}\""
        return answer


    async def delete_message(self, proom: MatrixRoom, pevent: RoomMessageText):
        """Удаляет сообщение с матом."""

        response = await self.client.room_redact(proom.room_id, pevent.event_id, "(мат)")
        # *** Проверяем результат и реагируем
        if isinstance(response, RoomRedactResponse):

            print(f"Сообщение удалено. Ответ сервера: {response}")
            #warning_text = (
            #        f"⚠️ @{event.sender.split(':')[0][1:]}, пожалуйста, "
            #        "следите за культурой общения в этом чате. Нецензурная лексика запрещена."
            #    )
            #    await self.client.room_send(
            #        room_id=room.room_id,
            #        message_type="m.room.message",
            #        content={"msgtype": "m.text", "body": warning_text}
            #    )
        else:
            print(f"Не удалось удалить сообщение. Ответ сервера: {response}")


    async def moderator(self, pchat_title: str, pmessage: str, plocal_name: str, puser_name: str) -> str:
        """Процедура разбора запроса пользователя."""

        assert pchat_title is not None, \
            "Assert: [moderator.moderator] " \
            "Пропущен параметр <pchat_title> !"
        assert pmessage is not None, \
            "Assert: [moderator.moderator] " \
            "Пропущен параметр <pmessage> !"
        assert plocal_name is not None, \
            "Assert: [moderator.moderator] " \
            "Пропущен параметр <plocal_name> !"
        assert puser_name is not None, \
            "Assert: [moderator.moderator] " \
            "Пропущен параметр <puser_name> !"

        answer: str = ""
        if pmessage:

            # *** Порядок. Возможно, запрошена команда. Мы ее умеем?
            if self.can_process_command(pchat_title, pmessage, UNIT_ID, COMMANDS):

                # *** Пользователь хочет перезагрузить словарь мата.
                can_reload = self.is_master(puser_name)
                if can_reload:

                    await self.reload()
                    answer = "Словарь мата обновлен"
                else:

                    # *** ... но не тут-то было...
                    print(f"> Moderator: Запрос на перегрузку словаря мата от "
                          f"нелегитимного лица {plocal_name}.")
                    answer = (f"Извини, {plocal_name}, "
                              f"только {self.config.master} может перегружать словарь мата!")
        return answer


    async def reload(self):
        """Загружает словарь антимата."""

        # *** Собираем пути
        assert Path(self.data_path).is_dir(), f"{DATA_FOLDER} must be folder"
        data_path = Path(self.data_path) / BAD_WORDS_FILE
        self.bad_words.clear()
        self.bad_words = await self.load_from_file_async(str(data_path))
        print(f"> Moderator успешно (пере)загрузил {len(self.bad_words)} "
              "регэкспов матерных выражений.")
