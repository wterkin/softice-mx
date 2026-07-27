# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru

"""Модуль статистики для бота."""

from pathlib import Path

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError


from nio import RoomMessageText, RoomMessageVideo, RoomMessageAudio,\
                RoomMessageImage, RoomMessageFile

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


    def add_room_to_base(self, proom_id: int, proom_name: str) -> int:
        """Добавляет новую комнату в БД и возвращает его ID."""

        assert proom_id is not None, \
            "Assert: [statistic.add_chat_to_base] " \
            "Пропущен параметр <proom_id> !"
        assert proom_name is not None, \
            "Assert: [statistic.add_chat_to_base] " \
            "Пропущен параметр <proom_name> !"

        try:

            room = db.CRoom(proom_id, proom_name)
            self.database.commit_changes(room)
            return room.id
        except SQLAlchemyError:

            return ERROR_CODE

    """
    def add_user_stat(self, proom_id: int, puser_id: int, pstat: db.CStat) -> int:
        ""Добавляет новую запись статистики по человеку.""

        assert puser_id is not None, \
            "Assert: [statistic.add_user_stat] " \
            "Пропущен параметр <puser_id> !"
        assert proom_id is not None, \
            "Assert: [statistic.add_user_stat] " \
            "Пропущен параметр <proom_id> !"

        try:

            self.database.commit_changes(pstat)
            return pstat.id
        except SQLAlchemyError:

            return ERROR_CODE
    """

    def add_user_to_base(self, puser_id: int, puser_name: str) -> int:
        """"Добавляет нового пользователя в БД и возвращает его ID."""

        assert puser_id is not None, \
            "Assert: [statistic.add_user_to_base] " \
            "Пропущен параметр <puser_id> !"
        assert puser_name is not None, \
            "Assert: [statistic.add_user_to_base] " \
            "Пропущен параметр <puser_name> !"

        try:

            user = db.CUser(puser_id, puser_name)
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


    def get_room_by_id(self, proom_id) -> int:
        """Если чат уже есть в базе, возвращает его ID, если нет - None."""

        assert proom_id is not None, \
            "Assert: [statistic.get_room_id] " \
            "Пропущен параметр <proom_id> !"

        try:

            query = self.database.query_data(db.CRoom)
            query = query.filter_by(froomid=proom_id)
            room = query.first()
            if room is not None:

                return room.id
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

        return super().get_hint(pchat_title, UNIT_ID, COMMANDS[HINT_GROUP])


    def get_personal_information(self, proom_id: int, puser_name: str) -> str:
        """Возвращает информацию о пользователе"""

        assert proom_id is not None, \
            "Assert: [statistic.get_personal_information] " \
            "Пропущен параметр <proom_id> !"
        assert puser_name is not None, \
            "Assert: [statistic.get_personal_information] " \
            "Пропущен параметр <puser_name> !"

        answer: str = ""
        query = self.database.query_data(db.CUser)
        query = query.filter_by(fusername=puser_name)
        user = query.first()
        if user is not None:

            # *** Получим ID чата в базе
            query = self.database.query_data(db.CRoom)
            query = query.filter_by(froomid=proom_id)
            room = query.first()
            if room is not None:

                query = self.database.query_data(db.CStat)
                query = query.filter_by(fuserid=user.id)
                query = query.filter_by(fchatid=room.id)
                stat = query.first()
                if stat is not None:

                    answer = f"{puser_name} наговорил {stat.phrases} фраз, " \
                             f"{stat.words} слов, {stat.letters} букв, запостил " \
                             f"{0 if stat.images is None else stat.images} фоток, " \
                             f"{0 if stat.audios is None else stat.audios} аудио и " \
                             f"{0 if stat.videos is None else stat.videos} видео," \
                             f"{0 if stat.files is None else stat.files} файлов"

        return answer


    def get_statistic(self, proom_id: int, pcount: int, porder_by: int) -> str:
        """Получает из базы статистику по самым говорливым юзерам."""

        assert proom_id is not None, \
            "Assert: [statistic.get_statistic] " \
            "Пропущен параметр <proom_id> !"
        assert pcount is not None, \
            "Assert: [statistic.get_statistic] " \
            "Пропущен параметр <pcount> !"
        assert porder_by is not None, \
            "Assert: [statistic.get_statistic] " \
            "Пропущен параметр <porder_by> !"

        query = select(db.CRoom, db.CStat, db.CUser)
        query = query.filter_by(froomid=proom_id)
        query = query.join(db.CStat, db.CStat.froomid == db.CRoom.id)
        query = query.join(db.CUser, db.CUser.id == db.CStat.fuserid)
        if porder_by == 1:

            query = query.order_by(db.CStat.phrases.desc())
        elif porder_by == 2:

            query = query.order_by(db.CStat.words.desc())
        elif porder_by == 3:

            query = query.order_by(db.CStat.images.desc())
        elif porder_by == 4:

            query = query.order_by(db.CStat.audios.desc())
        elif porder_by == 5:

            query = query.order_by(db.CStat.videos.desc())
        elif porder_by == 6:

            query = query.order_by(db.CStat.files.desc())
        else:

            query = query.order_by(db.CStat.phrases.desc())
        stat = query.limit(pcount).all()
        answer = "Самые общительные:\n"
        for number, item in enumerate(stat):

            answer += f"{number + 1} : {item[2].fusername} : {item[1].phrases}" \
                      f" фраз, {item[1].fwords} слов, " \
                      f"{0 if item[1].files is None else item[1].files} файл., " \
                      f"{0 if item[1].images is None else item[1].images} картин., " \
                      f"{0 if item[1].audios is None else item[1].audios} звук. и " \
                      f"{0 if item[1].videos is None else item[1].videos} вид. \n"
        answer += f"Отсортировано по количеству {SORTED_BY[porder_by-1]}. \n"
        return answer


    def get_user_id(self, puser_id) -> int:
        """Если пользователь уже есть в базе, возвращает его ID, если нет - None."""

        assert puser_id is not None, \
            "Assert: [statistic.get_user_id] " \
            "Пропущен параметр <puser_id> !"


        query = self.database.query_data(db.CUser)
        query = query.filter_by(fuserid=puser_id)
        user = query.first()
        if user is not None:

            return user.id
        return None


    def get_user_stat(self, proom_id: int, puser_id: int) -> tuple:
        """Получает из базы статистику пользователя и возвращает её."""

        assert proom_id is not None, \
            "Assert: [statistic.get_user_stat] " \
            "Пропущен параметр <proom_id> !"
        assert puser_id is not None, \
            "Assert: [statistic.get_user_stat] " \
            "Пропущен параметр <puser_id> !"

        query = self.database.query_data(db.CStat)
        query = query.filter_by(fuserid=puser_id, froomid=proom_id)
        return query.first()


    def save_all_type_of_messages(self, proom_id: int, proom_name: str,
                                        puser_id: int, puser_name: str,
                                        pevent: RoomMessageText) -> bool:
        """Учитывает стикеры, видео, аудиосообщения."""

        assert proom_id is not None, \
            "Assert: [statistic.save_all_type_of_messages] " \
            "Пропущен параметр <proom_id> !"
        assert proom_name is not None, \
            "Assert: [statistic.save_all_type_of_messages] " \
            "Пропущен параметр <proom_name> !"
        assert puser_id is not None, \
            "Assert: [statistic.save_all_type_of_messages] " \
            "Пропущен параметр <puser_id> !"
        assert puser_name is not None, \
            "Assert: [statistic.save_all_type_of_messages] " \
            "Пропущен параметр <puser_name> !"

        result: bool = False
        if self.is_enabled(proom_name, UNIT_ID):

            # *** Это не бот написал? Чужой бот, не наш?
            if puser_name not in self.config.alien_bots:

                # Проверить, нет ли уже этого чата в таблице чатов
                room_id = self.get_room_by_id(proom_id)
                if room_id is None:

                    # *** Нету еще, новый чат - добавить, и получить id
                    room_id = self.add_room_to_base(proom_id, proom_name)
                # *** Проверить, нет ли юзера в таблице тг юзеров
                user_id = self.get_user_id(puser_id)
                if user_id is None:

                    # *** Нету, новый пользователь
                    user_id = self.add_user_to_base(puser_id, puser_name)
                # *** Имеется ли в БД статистика по этому пользователю?
                user_stat = self.get_user_stat(room_id, user_id)
                if user_stat is not None:

                    # *** Изменяем статистику юзера в зависимости от типа сообщения
                    if isinstance(pevent, RoomMessageText):

                        text: str = pevent.body.strip()
                        if text[0] != self.config.command_prefix:

                            user_stat.phrases += 1
                            user_stat.letters += len(text)
                            user_stat.words += len(text.split(" "))
                    elif isinstance(pevent, RoomMessageVideo):

                        user_stat.videos += 1
                    elif isinstance(pevent, RoomMessageAudio):

                        user_stat.audios += 1
                    elif isinstance(pevent, RoomMessageImage):

                        user_stat.audios += 1
                    elif isinstance(pevent, RoomMessageFile):

                        user_stat.files += 1
                    self.database.commit_changes(user_stat)
                    result = True
        return result


    def statistic(self, proom_id: int, proom_name: str, puser_name, pmessage_text: str) -> str:
        """Обработчик команд."""

        assert proom_id is not None, \
            "Assert: [statistic.statistic] " \
            "Пропущен параметр <proom_id> !"
        assert proom_name is not None, \
            "Assert: [statistic.statistic] " \
            "Пропущен параметр <proom_name> !"
        assert puser_name is not None, \
            "Assert: [statistic.statistic] " \
            "Пропущен параметр <puser_name> !"
        assert pmessage_text is not None, \
            "Assert: [statistic.statistic] " \
            "Пропущен параметр <pmessage_text> !"

        command: int
        answer: str = ""
        order_by: int = 0
        word_list: list = self.parse_input(pmessage_text)
        if self.can_process_command(proom_name, pmessage_text, UNIT_ID, COMMANDS):

            if word_list[0] in COMMANDS[HINT_GROUP]:

                answer = self.get_commands(proom_name)

            else:

                # *** Получим код команды
                command: int = self.identify_command(word_list[0], COMMANDS)
                if command >= 0:

                    if len(word_list) > 1 and word_list[1].isdigit():

                        order_by = int(word_list[1])
                        if order_by < 1 or order_by > 6:

                            order_by = 1
                    if command == TOP_10_GROUP:

                        answer = self.get_statistic(proom_id, 10, order_by)
                    elif command == TOP_25_GROUP:

                        answer = self.get_statistic(proom_id, 25, order_by)
                    elif command == TOP_50_GROUP:

                        answer = self.get_statistic(proom_id, 50, order_by)
                    elif command == PERSONAL_GROUP:

                        answer = self.get_personal_information(proom_id, puser_name)
        return answer


