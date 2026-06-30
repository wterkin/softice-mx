# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru

"""Модуль статистики для бота."""

from pathlib import Path

from sqlalchemy.exc import SQLAlchemyError

from softice import basis
from softice import database as db

TOP_10_GROUP: int = 0
TOP_25_GROUP: int = 1
TOP_50_GROUP: int = 2
PERSONAL_GROUP: int = 3
HINT_GROUP: int = 4


COMMANDS: tuple = (("пер10", "top10"),
                   ("пер25", "top25"),
                   ("пер50", "top50"),
                   ("личные", "pers"),
                   ("статистика", "стат", "statistic", "stat"))

DESCRIPTIONS: tuple = ("",
                       "",
                       (f"{', '.join(COMMANDS[TOP_10_GROUP])} :"
                        f" Получить статистику по 10 самым общительным пользователям"),
                       (f"{', '.join(COMMANDS[TOP_25_GROUP])} :"
                        f" Получить статистику по 25 самым общительным пользователям"),
                       (f"{', '.join(COMMANDS[TOP_50_GROUP])} :"
                        f" Получить статистику по 50 самым общительным пользователям"),
                       (f"{', '.join(COMMANDS[PERSONAL_GROUP])} :"
                        f" Получить персональную статистику"),
                       )


UNIT_ID: str = "statistic"

SORTED_BY: tuple = ("фраз", "слов", "стикеров", "картинок",
                    "звуковых сообщений", "видео сообщений")

DATABASE_NAME: str = "softice.db"

ERROR_CODE: int = -1


"""
   content_dict = parsed_dict["content"]

    if content_dict["msgtype"] == "m.text":
        event = RoomMessageText.from_dict(parsed_dict)
    elif content_dict["msgtype"] == "m.emote":
        event = RoomMessageEmote.from_dict(parsed_dict)
    elif content_dict["msgtype"] == "m.notice":
        event = RoomMessageNotice.from_dict(parsed_dict)
    elif content_dict["msgtype"] == "m.image":
        event = RoomMessageImage.from_dict(parsed_dict)
    elif content_dict["msgtype"] == "m.audio":
        event = RoomMessageAudio.from_dict(parsed_dict)
    elif content_dict["msgtype"] == "m.video":
        event = RoomMessageVideo.from_dict(parsed_dict)
    elif content_dict["msgtype"] == "m.file":
        event = RoomMessageFile.from_dict(parsed_dict)
    else:
        event = RoomMessageUnknown.from_dict(parsed_dict)

"""



class CStatistic(basis.CBasis):
    """Класс статистика."""

    def __init__(self, pconfig: dict):

        super().__init__(pconfig)
        self.data_path: str = self.config.data_folder
        self.database: db.CDataBase = db.CDataBase(self.config, self.data_path, DATABASE_NAME)
        file_name =  Path(self.data_path) / DATABASE_NAME
        if not file_name.is_file():

            self.database.create()
            print("База данных создана.")
        print("Статистик стартовал.")


    def add_chat_to_base(self, proom_name: str, proom_id: int) -> int:
        """Добавляет новую комнату в БД и возвращает его ID."""

        assert proom_name is not None, \
            "Assert: [statistic.add_chat_to_base] " \
            "Пропущен параметр <proom_name> !"
        assert proom_id is not None, \
            "Assert: [statistic.add_chat_to_base] " \
            "Пропущен параметр <proom_id> !"

        try:

            room = db.CRoom(ptg_chat_id, ptg_chat_title)
            self.database.commit_changes(room)
            return room.id
        except SQLAlchemyError:

            return ERROR_CODE

    """
    if content_dict["msgtype"] == "m.text":
                event = RoomMessageText.from_dict(parsed_dict)
            elif content_dict["msgtype"] == "m.emote":
                event = RoomMessageEmote.from_dict(parsed_dict)
            elif content_dict["msgtype"] == "m.notice":
                event = RoomMessageNotice.from_dict(parsed_dict)
            elif content_dict["msgtype"] == "m.image":
                event = RoomMessageImage.from_dict(parsed_dict)
            elif content_dict["msgtype"] == "m.audio":
                event = RoomMessageAudio.from_dict(parsed_dict)
            elif content_dict["msgtype"] == "m.video":
                event = RoomMessageVideo.from_dict(parsed_dict)
            elif content_dict["msgtype"] == "m.file":
                event = RoomMessageFile.from_dict(parsed_dict)
            else:
                event = RoomMessageUnknown.from_dict(parsed_dict)
    """


    def add_user_stat(self, puser_id: int, proom_id: int, pstatfields: dict):
        """Добавляет новую запись статистики по человеку."""

        assert puser_id is not None, \
            "Assert: [statistic.add_user_stat] " \
            "Пропущен параметр <puser_id> !"
        assert proom_id is not None, \
            "Assert: [statistic.add_user_stat] " \
            "Пропущен параметр <proom_id> !"
        assert puser_id is not None, \
            "Assert: [statistic.add_user_stat] " \
            "Пропущен параметр <puser_id> !"


        try:

            stat = db.CStat(puser_id, pchat_id, pstatfields)
            self.database.commit_changes(stat)
            return stat.id
        except SQLAlchemyError:

            return ERROR_CODE


    def add_user_to_base(self, ptg_user_id: int, ptg_user_title: str):
        """Добавляет нового пользователя в БД и возвращает его ID."""

        try:

            user = db.CUser(ptg_user_id, ptg_user_title)
            self.database.commit_changes(user)
            return user.id
        except SQLAlchemyError:

            return ERROR_CODE


    def can_process_command(self, pchat_title: str, pmessage: str,  punit_id: str = "",
                    pcommands: list = None) -> bool:
        """Процедура определяет, сможет ли данный модуль обработать данную команду."""

        assert pchat_title is not None, \
            "Assert: [statistic.can_process_command] " \
            "Пропущен параметр <pchat_title> !"
        assert pmessage is not None, \
            "Assert: [statistic.can_process_command] " \
            "Пропущен параметр <pmessage> !"
        return super().can_process_command(pchat_title, pmessage, UNIT_ID, COMMANDS)


    def get_chat_id(self, ptg_chat_id):
        """Если чат уже есть в базе, возвращает его ID, если нет - None."""

        try:

            query = self.database.query_data(db.CChat)
            query = query.filter_by(fchatid=ptg_chat_id)
            chat = query.first()
            if chat is not None:

                return chat.id
            return ERROR_CODE
        except SQLAlchemyError:

            return ERROR_CODE


    def get_commands(self, pchat_title: str, punit_id: str="", pdescriptions: list=None) -> str:
        """Пользователь запросил список команд."""

        assert pchat_title is not None, \
            "Assert: [statistic.get_commands] " \
            "Пропущен параметр <pchat_title> !"

        return super().get_commands(pchat_title, UNIT_ID, DESCRIPTIONS)


    def get_hint(self, pchat_title: str, punit_id: str = "", phints: str = "") -> str:
        """Возвращает список команд, поддерживаемых модулем.  """

        assert pchat_title is not None, \
            "Assert: [statistic.get_hint] " \
            "Пропущен параметр <pchat_title> !"

        return super().get_hint(pchat_title, UNIT_ID, COMMANDS[HINT_COMMANDS])


    def get_personal_information(self, ptg_chat_id: int, puser_title: str):
        """Возвращает информацию о пользователе"""

        answer: str = ""
        query = self.database.query_data(db.CUser)
        query = query.filter_by(fusername=puser_title)
        user = query.first()
        if user is not None:

            # *** Получим ID чата в базе
            query = self.database.query_data(db.CChat)
            query = query.filter_by(fchatid=ptg_chat_id)
            chat = query.first()
            if chat is not None:

                query = self.database.query_data(db.CStat)
                query = query.filter_by(fuserid=user.id)
                query = query.filter_by(fchatid=chat.id)
                stat = query.first()
                if stat is not None:

                    answer = f"{puser_title} наболтал {stat.fphrases} фраз, " \
                             f"{stat.fwords} слов, {stat.fletters} букв, запостил " \
                             f"{0 if stat.fstickers is None else stat.fstickers} стик., " \
                             f"{0 if stat.fpictures is None else stat.fpictures} фоток, " \
                             f"{0 if stat.faudios is None else stat.faudios} аудио и " \
                             f"{0 if stat.fvideos is None else stat.fvideos} видео,"

        return answer


    def get_statistic(self, ptg_chat_id: int, pcount: int, porder_by: int):
        """Получает из базы статистику по самым говорливым юзерам."""

        session = self.database.get_session()
        query = session.query(db.CChat, db.CStat, db.CUser)
        query = query.filter_by(fchatid=ptg_chat_id)
        query = query.join(db.CStat, db.CStat.fchatid == db.CChat.id)
        query = query.join(db.CUser, db.CUser.id == db.CStat.fuserid)
        # print(f"0 {porder_by}")
        if porder_by == 1:

            query = query.order_by(db.CStat.fphrases.desc())
        elif porder_by == 2:

            query = query.order_by(db.CStat.fwords.desc())
        elif porder_by == 3:

            query = query.order_by(db.CStat.fstickers.desc())
        elif porder_by == 4:

            query = query.order_by(db.CStat.fpictures.desc())
        elif porder_by == 5:

            query = query.order_by(db.CStat.faudios.desc())
        elif porder_by == 6:

            query = query.order_by(db.CStat.fvideos.desc())
        else:

            query = query.order_by(db.CStat.fphrases.desc())
        stat = query.limit(pcount).all()
        answer = "Самые говорливые:\n"
        for number, item in enumerate(stat):

            # print(f"{number} {porder_by}")
            answer += f"{number + 1} : {item[2].fusername} : {item[1].fphrases}" \
                      f" фраз, {item[1].fwords} слов, " \
                      f"{0 if item[1].fstickers is None else item[1].fstickers} стик., " \
                      f"{0 if item[1].fpictures is None else item[1].fpictures} фоток, " \
                      f"{0 if item[1].faudios is None else item[1].faudios} звук. и " \
                      f"{0 if item[1].fvideos is None else item[1].fvideos} вид. \n"
        answer += f"Отсортировано по количеству {SORTED_BY[porder_by-1]}. \n"
        return answer


    def get_user_id(self, ptg_user_id):
        """Если пользователь уже есть в базе, возвращает его ID, если нет - None."""

        query = self.database.query_data(db.CUser)
        query = query.filter_by(ftguserid=ptg_user_id)
        user = query.first()
        if user is not None:

            return user.id
        return None


    def get_user_stat(self, pchat_id: int, puser_id: int):
        """Получает из базы статистику пользователя и возвращает её."""

        query = self.database.query_data(db.CStat)
        query = query.filter_by(fuserid=puser_id, fchatid=pchat_id)
        return query.first()


    def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""


    def save_all_type_of_messages(self, pevent: dict) -> bool:
        """Учитывает стикеры, видео, аудиосообщения."""

        # print(f"**** stat:sav 00 {pevent[cn.MCHAT_TITLE]= }")
        result: bool = False
        if self.is_enabled(pevent[cn.MCHAT_TITLE]):

            # print(f"**** stat:sav 01 {pevent[cn.MUSER_NAME]= }")
            # *** Получим текстовое сообщение из события
            if cn.MTEXT in pevent:

                message_text: str = pevent[cn.MTEXT]
            else:

                message_text: str = pevent[cn.MCAPTION]
            # *** Получим остальные данные
            tg_chat_id: int = pevent[cn.MCHAT_ID]
            tg_chat_title: str = pevent[cn.MCHAT_TITLE]
            tg_user_id: int = pevent[cn.MUSER_ID]
            tg_user_name: str = ""
            # *** Если есть имя пользователя (а может не быть?) - берем его
            if cn.MUSER_NAME in pevent:

                tg_user_name = pevent[cn.MUSER_NAME]
            # print(f"**** stat:sav 01 {tg_user_name= }")

            # *** Создаём пустой словарь для статистических данных
            statfields: dict = {db.STATUSERID: 0,
                                db.STATLETTERS: 0,
                                db.STATWORDS: 0,
                                db.STATPHRASES: 0,
                                db.STATPICTURES: 0,
                                db.STATSTICKERS: 0,
                                db.STATAUDIOS: 0,
                                db.STATVIDEOS: 0}
            # *** Получаем другие имеющиеся имена пользователя
            tg_user_title = extract_user_name(pevent)
            # *** Это не бот написал? Чужой бот, не наш?
            if tg_user_name not in self.config[FOREIGN_BOTS]:

                # print("**** stat:sav 02")
                # Проверить, нет ли уже этого чата в таблице чатов
                chat_id = self.get_chat_id(tg_chat_id)
                if chat_id is None:

                    # *** Нету еще, новый чат - добавить, и получить id
                    chat_id = self.add_chat_to_base(tg_chat_id, tg_chat_title)
                # *** Проверить, нет ли юзера в таблице тг юзеров
                user_id = self.get_user_id(tg_user_id)
                # print(f"**** stat:sav 03 {user_id=}")
                if user_id is None:

                    # *** Нету, новый пользователь
                    user_id = self.add_user_to_base(tg_user_id, tg_user_title)
                # *** Имеется ли в БД статистика по этому пользователю?
                user_stat = self.get_user_stat(chat_id, user_id)
                if user_stat is not None:

                    statfields = user_stat.get_all_fields()  # !!! тут
                # *** Изменяем статистику юзера в зависимости от типа сообщения
                if pevent[cn.MCONTENT_TYPE] in ["video", "video_note"]:

                    statfields[db.STATVIDEOS] += 1
                elif pevent[cn.MCONTENT_TYPE] in ["audio", "voice"]:

                    statfields[db.STATAUDIOS] += 1
                elif pevent[cn.MCONTENT_TYPE] == "photo":

                    statfields[db.STATPICTURES] += 1
                elif pevent[cn.MCONTENT_TYPE] == "sticker":

                    statfields[db.STATSTICKERS] += 1
                elif pevent[cn.MCONTENT_TYPE] == "text":

                    # *** Если это не команда боту...
                    if message_text[0] != "!":

                        statfields[db.STATLETTERS] += len(message_text)
                        statfields[db.STATWORDS] += len(message_text.split(" "))
                        statfields[db.STATPHRASES] += 1

                # *** Если информации о юзере нет в базе, добавляем, иначе апдейтим
                if user_stat is None:

                    self.add_user_stat(user_id, chat_id, statfields)

                else:

                    self.update_user_stat(user_id, chat_id, statfields)

                result = True
        return result


    def statistic(self, pchat_id: int, pchat_title: str, puser_title, pmessage_text: str):
        """Обработчик команд."""

        command: int
        answer: str = ""
        order_by: int = 0
        word_list: list = func.parse_input(pmessage_text)
        if self.can_process_command(pchat_title, pmessage_text, UNIT_ID, COMMANDS):

            if word_list[0] in COMMANDS[HINT_GROUP]:

                answer = self.get_commands(pchat_title)

            else:

                # *** Получим код команды
                command: int = self.identify_command(word_list[0], COMMANDS)
                if command >= 0:

                    if len(word_list) > 1 and word_list[1].isdigit():

                        order_by = int(word_list[1])
                        if order_by < 1 or order_by > 6:

                            order_by = 1
                    if command in TOP_10_COMMAND:

                        answer = self.get_statistic(pchat_id, 10, order_by)
                    elif command in TOP_25_COMMAND:

                        answer = self.get_statistic(pchat_id, 25, order_by)
                    elif command in TOP_50_COMMAND:

                        answer = self.get_statistic(pchat_id, 50, order_by)
                    elif command in PERS_COMMAND:

                        answer = self.get_personal_information(pchat_id, puser_title)
        return answer


    def update_user_stat(self, puser_id: int, pchat_id: int, pstatfields: dict):
        """Изменяет запись статистики по человеку."""

        query = self.database.query_data(db.CStat)
        query = query.filter_by(fuserid=puser_id)
        query = query.filter_by(fchatid=pchat_id)
        stat: db.CStat = query.first()
        if stat:

            stat.set_all_fields(pstatfields)
            self.database.commit_changes(stat)
