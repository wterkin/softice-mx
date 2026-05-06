# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Игровой модуль."""
import asyncio
from softice import basis
from nio import AsyncClient
from softice.chat_functions import send_text_to_room

UNIT_ID: str = "manager"
HINT: tuple = ("управл", "control")
COMMANDS: tuple = ("q", "quit", "r", "rst")
QUIT_COMMANDS: int = 0
RESTART_COMMANDS: int = 2
QUIT_FLAG: str = "quit_by_demand.flg"
RESTART_FLAG: str = "restart_by_demand.flg"


class CManager(basis.CBasis):
    """Класс управляющего."""

    def __init__(self, pconfig: dict, pclient: AsyncClient):

        super().__init__(pconfig)
        self.client: AsyncClient = pclient
        print("Менеджер стартовал.")


    def create_flag(self, pflag_name: str):
        """Функция создает флаг выхода или рестарта по запросу."""

        with open(f"./flags/{pflag_name}", 'tw', encoding='utf-8'):

            pass


    def get_help(self, pchat_title: str) -> str:
        """Пользователь запросил список команд."""

        assert pchat_title is not None, \
            "Assert: [manager.get_help] " \
            "No <pchat_title> parameter specified!"

        command_list: str = ""
        if self.is_enabled(pchat_title, UNIT_ID):

            command_list += ", ".join(COMMANDS)
        return command_list


    def get_hint(self, pchat_title: str) -> str:  # [arguments-differ]
        """Возвращает список команд, поддерживаемых модулем.  """

        assert pchat_title is not None, \
            "Assert: [manager.get_hint] " \
            "Пропущен параметр <pchat_title> !"
        if self.is_enabled(pchat_title):

            return ", ".join(HINT)
        return ""


    def reload(self):
        """Пустая заглушка."""


    async def manager(self, room_name, room_id, puser_name, pmessage_text: str):
        """Основной метод класса."""

        answer: str = ""
        word_list: list = self.parse_input(pmessage_text)
        # print(f"!!!!!! 1 {room_name=} {UNIT_ID=} {pmessage_text=} {COMMANDS=}")
        if self.can_process(room_name, UNIT_ID, pmessage_text, COMMANDS):

            if word_list[0] in HINT:

                answer = self.get_help(room_name)
            else:

                #print("!!!!!! 1")
                # *** Получим код команды
                # print("!"*6, COMMANDS[:RESTART_COMMANDS])
                if word_list[0] in COMMANDS[:RESTART_COMMANDS]:

                    #print("!!!!!! Quit command detected. ")
                    if self.is_enabled(room_name, UNIT_ID):

                        #print("!!!!!! Enabled. ")
                        if self.is_master(puser_name):

                            # *** Запрошено отключение бота
                            self.create_flag(QUIT_FLAG)
                            # await send_text_to_room(self.client, room_id, "Добби свободен!!")
                            #print("!!!!!! Quit by demand. ")
                            await self.suicide()
                        else:

                            answer = "Вам недоступна эта возможность."
                elif word_list[0] in COMMANDS[RESTART_COMMANDS:]:

                    #print("!!!!!! Restart command detected. ")
                    if self.is_enabled(room_name, UNIT_ID):

                        #print("!!!!!! Enabled. ")
                        if self.is_master(puser_name):

                            # *** Запрошен рестарт бота
                            self.create_flag(RESTART_FLAG)
                            #c await end_text_to_room(self.client, room_id, "Щасвирнус.")
                            #print("!!!!!! Restart by demand. ")
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

