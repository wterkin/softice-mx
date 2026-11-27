# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль звонаря."""

import datetime as dtime
from datetime import datetime as dt

from softice import basis
from softice import database as db
from softice import statistic

COMMANDS: tuple = (("звонить", "звон", "ring", "rg"),
                   ("тихо", "тх", "quiet", "qt"),
                   ("звонарь", "ringer"))
RING_GROUP: int = 0
QUIET_GROUP: int = 1
HINT_GROUP: int = 2
DESCRIPTIONS: tuple = ( (f"{', '.join(COMMANDS[RING_GROUP])} :"
                         f" Вызвать для игры активных пользователей чата"),
                       (f"{', '.join(COMMANDS[QUIET_GROUP])} :"
                        f" Исключить себя из списка активных пользователей чата"
                         " - при первом слове, сказанном вами, статус сбрасывается"),
                        "")


UNIT_ID: str = "bellringer"
# MAFIA_CHANNELS: list = ["Асы мафии", "TestPlace"]

class CBellRinger(basis.CBasis):
    """Класс звонаря."""

    def __init__(self, pconfig, pstatistic: statistic.CStatistic):

        assert pconfig is not None, \
            "Assert: [CBellRinger.__init__] " \
            "Пропущен параметр <pconfig> !"
        super().__init__(pconfig)
        self.statistic: statistic.CStatistic = pstatistic
        # self.data_path = pdata_path + BELLRINGER_FOLDER


    async def bellringer(self, proom_name: str, proom_id: str, puser_name: str,
                         pmessage_text: str):
        """Основная функция модуля."""

        assert proom_name is not None, \
            "Assert: [CBellRinger.bellringer] "\
            "Пропущен параметр <proom_name> !"
        assert puser_name is not None, \
            "Assert: [CBellRinger.bellringer] " \
            "Пропущен параметр <puser_name> !"
        assert pmessage_text is not None, \
            "Assert: [CBellRinger.bellringer] " \
            "Пропущен параметр <pmessage_text> !"

        answer: str = ""
        player_list: list
        word_list: list = self.parse_input(pmessage_text)
        if self.can_process_command(proom_name, pmessage_text):

            if word_list[0] in COMMANDS[HINT_GROUP]:

                answer = self.get_commands(proom_name)

            elif word_list[0] in COMMANDS[RING_GROUP]:

                player_list = await self.get_active_user_list(proom_id)
                answer = ", ".join(player_list) + " Подъём, банда! "
            elif word_list[0] in COMMANDS[QUIET_GROUP]:

                # *** Отключаем товарищу звон
                pass
        if answer:

            print(f"BellRinger отвечает: {answer[self.OUT_MSG_LOG_LEN]}")
        return answer


    def can_process_command(self, proom_name: str, pmessage: str,  punit_id: str = "",
                    pcommands: list = None) -> bool:
        """Процедура определяет, сможет ли данный модуль обработать данную команду."""

        assert proom_name is not None, \
            "Assert: [CBarman.can_process_command] " \
            "Пропущен параметр <proom_name> !"
        assert pmessage is not None, \
            "Assert: [CBarman.can_process_command] " \
            "Пропущен параметр <pmessage> !"

        return super().can_process_command(proom_name, pmessage, UNIT_ID, COMMANDS)


    def get_commands(self, proom_name: str, punit_id: str="", pdescriptions: list=None) -> str:
        """Пользователь запросил список команд."""

        assert proom_name is not None, \
            "Assert: [CBarman.get_commands] " \
            "Пропущен параметр <proom_name> !"

        return super().get_commands(proom_name, UNIT_ID, DESCRIPTIONS)


    def get_hint(self, proom_name: str, punit_id: str = "",
                 phints: str = "") -> str:
        """Возвращает команду, которая возвращает полныйй список команд, поддерживаемых модулем."""

        assert proom_name is not None, \
            "Assert: [CBarman.get_hint] " \
            "Пропущен параметр <room_name> !"

        return super().get_hint(proom_name, UNIT_ID, COMMANDS[HINT_GROUP])


    async def get_active_user_list(self, pmx_room_id: str) -> list:
        """Выбирает из БД список пользователей, которые были
           активны в течении последней недели"""
        result: list = []
        base = self.statistic.database
        week_date = dt.now - dtime.timedelta(days=7)
        room_id = await self.statistic.get_room_id(pmx_room_id)
        if room_id != self.statistic.ERROR_CODE:

            sel = base.query_data(db.CStat.userid)
            sel = sel.where(db.CStat.roomid==room_id)
            sel = sel.where(db.CStat.fupdated>=week_date)
            sel = sel.where(db.CStat.silence is False)
            sess = await base.get_session()
            async with sess() as session:

                res = await session.execute(sel)
                result = res.all()
                print(result)
        return result


    async def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""
