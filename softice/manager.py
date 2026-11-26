# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Игровой модуль."""
import asyncio
from pathlib import Path

# pylint: disable=import-error
from nio import AsyncClient
# pylint: enable=import-error

from softice import basis
from softice.config import Config
from softice.chat_functions import send_text_to_room


# pylint: disable=too-many-branches
# pylint: disable=too-many-nested-blocks


UNIT_ID: str = "manager"

COMMANDS: tuple = (("quit", "q", "выход", "вых"),
                   ("reset", "r", "рестарт", "рст"),
                   ("control", "управление")
                   )
QUIT_GROUP: int = 0
RESTART_GROUP: int = 1
HINT_GROUP: int = 2
QUIT_FLAG: str = "quit_by_demand.flg"
RESTART_FLAG: str = "restart_by_demand.flg"
OBSOLETE_PERIOD: int = 15000 # millisec


class CManager(basis.CBasis):
    """Класс управляющего."""

    def __init__(self, pconfig: Config, pclient: AsyncClient):

        assert pconfig is not None, \
            "Assert: [CManager.__init__] " \
            "Пропущен параметр <pconfig> !"
        assert pclient is not None, \
            "Assert: [CManager.__init__] " \
            "Пропущен параметр <pclient> !"

        super().__init__(pconfig)
        self.client: AsyncClient = pclient
        self.last_report: bool = False
        print("Менеджер стартовал.")


    def create_flag(self, pflag_name: str):
        """Функция создает флаг выхода или рестарта по запросу."""

        assert pflag_name is not None, \
            "Assert: [CManager.create_flag] " \
            "Пропущен параметр <pflag_name> !"

        with open(f"./flags/{pflag_name}", 'tw', encoding='utf-8'):

            pass


    def delete_restart_flag(self):
        """Функция удаляет флвг рестарта при старте программы"""

        for file in Path("./flags/").glob(RESTART_FLAG):

            file.unlink()


    def get_hint(self, proom_name: str, punit_id: str = "", phints: str = "") -> str:
        # """Возвращает список команд, поддерживаемых модулем.  """

        assert proom_name is not None, \
            "Assert: [CManager.get_hint] " \
            "Пропущен параметр <proom_name> !"

        return super().get_hint(proom_name, UNIT_ID, COMMANDS[HINT_GROUP])


    async def reload(self):
        """Пустая заглушка."""


    async def manager(self, proom_name: str, proom_id: str,
                      puser_name: str, pmessage_text: str) -> str:
        """Основной метод класса."""
        assert proom_name is not None, \
            "Assert: [CManager.manager] " \
            "Пропущен параметр <proom_name> !"
        assert proom_id is not None, \
            "Assert: [CManager.manager] " \
            "Пропущен параметр <proom_id> !"
        assert puser_name is not None, \
            "Assert: [CManager.manager] " \
            "Пропущен параметр <puser_name> !"
        assert pmessage_text is not None, \
            "Assert: [CManager.manager] " \
            "Пропущен параметр <pmessage_text> !"

        answer: str = ""
        word_list: list = self.parse_input(pmessage_text)
        if self.can_process_command(proom_name, pmessage_text, UNIT_ID, COMMANDS):

            if word_list[0] in COMMANDS[HINT_GROUP]:

                answer = self.get_commands(proom_name, UNIT_ID, [])
            else:

                # *** Получим код команды
                if word_list[0] in COMMANDS[QUIT_GROUP]:

                    # rint(f"+++ Mgr +++ 3 +++ Quit")
                    if self.is_master(puser_name):

                        # *** Запрошено отключение бота
                        self.create_flag(QUIT_FLAG)
                        if not self.last_report:

                            self.last_report = True
                            await send_text_to_room(self.client, proom_id, "Добби свободен!!")
                        await self.suicide()
                    else:

                        answer = "Вам недоступна эта возможность."
                elif word_list[0] in COMMANDS[RESTART_GROUP]:

                    if self.is_master(puser_name):

                        # *** Запрошен рестарт бота
                        self.create_flag(RESTART_FLAG)
                        if not self.last_report:

                            self.last_report = True
                            await send_text_to_room(self.client, proom_id, "Щасвирнус.")
                        await asyncio.sleep(OBSOLETE_PERIOD // 1000)
                        await self.suicide()
                    else:

                        answer = "Вам недоступна эта возможность."

            if answer:

                print("> Manager отвечает: ", answer[:basis.OUT_MSG_LOG_LEN])

        return answer

    async def suicide(self):
        """Выключение бота."""
        await asyncio.sleep(3)
        raise SystemExit
