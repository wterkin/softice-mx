# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль антимата для бота."""

import re
from pathlib import Path
from softice import basis
from nio import MatrixRoom, RoomMessageText,


RELOAD_BAD_WORDS: list = ["bwreload", "bwrl"]
HINT = ["адм", "adm"]
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

        answer: str = ""
        detected: bool = False
        if pmessage:

            text: str = pmessage.lower()
            for bad_word in self.bad_words:

                result: bool = True
                while result:

                    # result = re.match(bad_word, text) is not None
                    result: re.Match = re.search(bad_word, text, re.IGNORECASE & re.VERBOSE)
                    if result:

                        
                        print(f"bad word detected. {bad_word=} {text=}")
                        detected = True
                        count: int = result.end()-result.start()
                        text[result.start():result.end()+1] = "*"*count
            if detected:

                answer = text
        return answer


    def control_talking(self, pchat_title: str, pmessage: str) -> str:
        """Следит за матершинниками."""

        assert pchat_title is not None, \
            "Assert: [moderator.control_talking] " \
            "Пропущен параметр <pchat_title> !"
        assert pmessage is not None, \
            "Assert: [moderator.control_talking] " \
            "Пропущен параметр <pmessage> !"

        answer: str = ""
        text: str
        if self.is_enabled(pchat_title):

            text = self.check_bad_words_ex(pmessage)
            if text:

                self.delete_message()
                answer = prec[cn.MUSER_TITLE]
                if prec[cn.MUSER_LASTNAME]:

                    answer += " " + prec[cn.MUSER_LASTNAME]
                print(f"Пользователь {answer} матерился в чате {prec[cn.MCHAT_TITLE]}.")
                print(f"Он сказал: {source_text}")
                answer += f" хотел сказать \"{text}\""
        return answer


    await def delete_message(proom: MatrixRoom, pevent: RoomMessageText):
        """Удаляет сообщение с матом."""

        response = await self.client.room_redact(proom.room_id, pevent.event_id, reason)
            
            # 5. Проверяем результат и реагируем
            if isinstance(response, RoomRedactResponse):
                print(f"✅ Сообщение {event.event_id} успешно удалено.")
                	
                # Опционально: отправить предупреждение нарушителю или в чат
                warning_text = (
                    f"⚠️ @{event.sender.split(':')[0][1:]}, пожалуйста, "
                    "следите за культурой общения в этом чате. Нецензурная лексика запрещена."
                )
                await self.client.room_send(
                    room_id=room.room_id,
                    message_type="m.room.message",
                    content={"msgtype": "m.text", "body": warning_text}
                )
            else:
                print(f"❌ Не удалось удалить сообщение. Ответ сервера: {response}")
                # Частая причина: у бота нет прав на redact (нужен уровень 50)
        


    def get_help(self, pchat_title: str) -> str:
        """Возвращает список команд модуля, доступных пользователю."""

        return ""


    def get_hint(self, pchat_title: str) -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""

        return ", ".join(HINT)


    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если на этом канале этот модуль разрешен."""

        if pchat_title in self.config["chats"]:

            return UNIT_ID in self.config["chats"][pchat_title]
        return False

    def is_master(self, puser_name, puser_title):
        """Проверяет, является ли пользователь хозяином бота."""

        if puser_name == self.config["master"]:

            return True, ""
        # *** Низзя
        print("> Moderator: Запрос на перезагрузку регэкспов "
              f"матерных выражений от нелегитимного лица {puser_title}.")
        return False, f"У вас нет на это прав, {puser_title}."


    def moderator(self, prec) -> str:
        """Процедура разбора запроса пользователя."""

        # *** Проверим, всё ли в порядке в чате
        answer: str = self.control_talking(prec)
        # message = event.body
        if not answer:

            if prec[cn.MTEXT] is not None:

                # *** Порядок. Возможно, запрошена команда. Мы ее умеем?
                if self.can_process(prec[cn.MCHAT_TITLE], prec[cn.MTEXT]):

                    # *** Да. Возможно, запросили перезагрузку.
                    word_list: list = func.parse_input(prec[cn.MTEXT])
                    if word_list[0] in RELOAD_BAD_WORDS:

                        # *** Пользователь хочет перезагрузить словарь мата.
                        can_reload, answer = self.is_master(prec[cn.MUSER_NAME],
                                                            prec[cn.MUSER_TITLE])
                        if can_reload:

                            self.reload()
                            answer = "Словарь мата обновлен"
                        else:

                            # *** ... но не тут-то было...
                            print(f"> Moderator: Запрос на перегрузку словаря мата от "
                                  f"нелегитимного лица {prec[cn.MUSER_TITLE]}.")
                            answer = (f"Извини, {prec[cn.MUSER_TITLE]}, "
                                      f"только {self.config['master_name']} может "
                                      "перегружать словарь мата!")
        return answer


    def reload(self):
        """Загружает словарь антимата."""

        # *** Собираем пути
        assert Path(self.data_path).is_dir(), f"{DATA_FOLDER} must be folder"
        data_path = Path(self.data_path) / BAD_WORDS_FILE
        self.bad_words.clear()
        self.bad_words = func.load_from_file(str(data_path))
        print(f"> Moderator успешно (пере)загрузил {len(self.bad_words)} "
              "регэкспов матерных выражений.")
"""
import re
import nio
from nio import RoomMessageText, RoomRedactResponse

class ProfanityFilter:
    def __init__(self, client):
        self.client = client
        
        # Список запрещённых слов (в нижнем регистре)
        # Лучше использовать основы слов или точные совпадения
        self.bad_words = ["плохое_слово", "сквернословие", "нецензурно"]
        
        # Компилируем регулярное выражение для точного совпадения слов.
        # \b означает границу слова, чтобы не удалять "класс" из-за "лас"
        # Флаг re.IGNORECASE делает проверку нечувствительной к регистру
        pattern = r"\b(" + "|".join(self.bad_words) + r")\b"
        self.bad_word_regex = re.compile(pattern, re.IGNORECASE)

    async def on_message(self, room: nio.MatrixRoom, event: RoomMessageText):
        # 1. Игнорируем сообщения самого бота, чтобы не уйти в бесконечный цикл
        if event.sender == self.client.user:
            return

        # 2. Игнорируем системные сообщения или изменения состояния комнаты
        if not isinstance(event, RoomMessageText):
            return

        # 3. Проверяем текст сообщения
        if self.bad_word_regex.search(event.body):
            print(f"⚠️ Обнаружен мат от {event.sender} в комнате {room.room_id}")
            
            # 4. УДАЛЯЕМ (редактируем) исходное сообщение
            reason = "Сообщение удалено автоматическим фильтром чата."
            response = await self.client.room_redact(room.room_id, event.event_id, reason)
            
            # 5. Проверяем результат и реагируем
            if isinstance(response, RoomRedactResponse):
                print(f"✅ Сообщение {event.event_id} успешно удалено.")
                
                # Опционально: отправить предупреждение нарушителю или в чат
                warning_text = (
                    f"⚠️ @{event.sender.split(':')[0][1:]}, пожалуйста, "
                    "следите за культурой общения в этом чате. Нецензурная лексика запрещена."
                )
                await self.client.room_send(
                    room_id=room.room_id,
                    message_type="m.room.message",
                    content={"msgtype": "m.text", "body": warning_text}
                )
            else:
                print(f"❌ Не удалось удалить сообщение. Ответ сервера: {response}")
                # Частая причина: у бота нет прав на redact (нужен уровень 50)

Поскольку логика у тебя уже готова, тебе нужно лишь заменить в коде:
bot.delete_message(chat_id, message_id)
на
await client.room_redact(room.room_id, event.event_id, "Нарушение правил чата")
"""
