# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru

"""Модуль статистики для бота."""

from pathlib import Path

from sqlalchemy.exc import SQLAlchemyError

from nio import RoomMessageText

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
    else:
        event = RoomMessageUnknown.from_dict(parsed_dict)

RoomMessageVideo(source={'unsigned': {'membership': 'join'}, 'content': {'body': 'we_and_penguin.mp4', 'info': {'duration': 5459, 'h': 768, 'mimetype': 'video/mp4', 'size': 511978, 'thumbnail_info': {'h': 600, 'mimetype': 'image/jpeg', 'size': 175495, 'w': 400}, 'thumbnail_url': 'mxc://sibnsk.net/OGFIGpTYtfhHoeQZsKdSdjMU', 'w': 512, 'xyz.amorgan.blurhash': 'TpJ8kaRP?b-;M{Rj~qWBM{t7t7ax'}, 'm.mentions': {}, 'msgtype': 'm.video', 'url': 'mxc://sibnsk.net/idvjZMIwupHYsEgndCyrEpas'}, 'origin_server_ts': 1782996328242, 'sender': '@namo:sibnsk.net', 'type': 'm.room.message', 'event_id': '$jRckPbSoq8PIIb84k7oAExq2ugoxJY7Y4fEz07y0PjQ'}, event_id='$jRckPbSoq8PIIb84k7oAExq2ugoxJY7Y4fEz07y0PjQ', sender='@namo:sibnsk.net', server_timestamp=1782996328242, decrypted=False, verified=False, sender_key=None, session_id=None, transaction_id=None, url='mxc://sibnsk.net/idvjZMIwupHYsEgndCyrEpas', body='we_and_penguin.mp4')
RoomMessageImage(source={'unsigned': {'membership': 'join'}, 'content': {'body': 'getImage.gif', 'info': {'h': 720, 'mimetype': 'image/gif', 'org.matrix.msc4230.is_animated': False, 'size': 23346, 'w': 938, 'xyz.amorgan.blurhash': 'LCSF;LWA%M_3-;?bIU9Z~qNGM{WA'}, 'm.mentions': {}, 'msgtype': 'm.image', 'url': 'mxc://sibnsk.net/oekOtgYvuWqSwZNWDatKLHcO'}, 'origin_server_ts': 1782996112426, 'sender': '@namo:sibnsk.net', 'type': 'm.room.message', 'event_id': '$42UhlIsI-depk-UfEfW4bofEm73X7-OiVgs-fzDJl9c'}, event_id='$42UhlIsI-depk-UfEfW4bofEm73X7-OiVgs-fzDJl9c', sender='@namo:sibnsk.net', server_timestamp=1782996112426, decrypted=False, verified=False, sender_key=None, session_id=None, transaction_id=None, url='mxc://sibnsk.net/oekOtgYvuWqSwZNWDatKLHcO', body='getImage.gif')
RoomMessageAudio(source={'unsigned': {'membership': 'join'}, 'content': {'body': 'forest_sounds.flac', 'info': {'duration': 243294, 'mimetype': 'audio/flac', 'size': 31217543}, 'm.mentions': {}, 'msgtype': 'm.audio', 'url': 'mxc://sibnsk.net/zwYAqRoIKqNCeEFCrcKCGscb'}, 'origin_server_ts': 1782996432895, 'sender': '@namo:sibnsk.net', 'type': 'm.room.message', 'event_id': '$3klkKhwO8KdkNaWvJpf62bc2J8xvhO8u7REySdcY2do'}, event_id='$3klkKhwO8KdkNaWvJpf62bc2J8xvhO8u7REySdcY2do', sender='@namo:sibnsk.net', server_timestamp=1782996432895, decrypted=False, verified=False, sender_key=None, session_id=None, transaction_id=None, url='mxc://sibnsk.net/zwYAqRoIKqNCeEFCrcKCGscb', body='forest_sounds.flac')
RoomMessageFile(source={'unsigned': {'membership': 'join'}, 'content': {'body': 'pgsocworkpay-flask_20260609_1704.7z', 'info': {'mimetype': 'application/x-7z-compressed', 'size': 2961234}, 'm.mentions': {}, 'msgtype': 'm.file', 'url': 'mxc://sibnsk.net/VonMMDvUDefrZMRHMftHipyh'}, 'origin_server_ts': 1782996768265, 'sender': '@namo:sibnsk.net', 'type': 'm.room.message', 'event_id': '$ibi4BGDj544zkTGhY0-q-GZb-JweFvOyRJXBUIVYsPw'}, event_id='$ibi4BGDj544zkTGhY0-q-GZb-JweFvOyRJXBUIVYsPw', sender='@namo:sibnsk.net', server_timestamp=1782996768265, decrypted=False, verified=False, sender_key=None, session_id=None, transaction_id=None, url='mxc://sibnsk.net/VonMMDvUDefrZMRHMftHipyh', body='pgsocworkpay-flask_20260609_1704.7z')
RoomMessageAudio(source={'unsigned': {'membership': 'join'}, 'content': {'body': 'Voice message', 'info': {'duration': 6931, 'mimetype': 'audio/ogg', 'size': 12004}, 'm.mentions': {}, 'msgtype': 'm.audio', 'org.matrix.msc1767.audio': {'duration': 6931, 'waveform': [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0]}, 'org.matrix.msc1767.file': {'mimetype': 'audio/ogg', 'name': 'Voice message.ogg', 'size': 12004, 'url': 'mxc://sibnsk.net/IocSSaMvXDkCZOgQHqTJmvez'}, 'org.matrix.msc1767.text': 'Voice message', 'org.matrix.msc3245.voice': {}, 'url': 'mxc://sibnsk.net/IocSSaMvXDkCZOgQHqTJmvez'}, 'origin_server_ts': 1782996912468, 'sender': '@namo:sibnsk.net', 'type': 'm.room.message', 'event_id': '$KagU_DTSXfo5e642aFOkSALvHHBK5-9-bqbNtINnLbA'}, event_id='$KagU_DTSXfo5e642aFOkSALvHHBK5-9-bqbNtINnLbA', sender='@namo:sibnsk.net', server_timestamp=1782996912468, decrypted=False, verified=False, sender_key=None, session_id=None, transaction_id=None, url='mxc://sibnsk.net/IocSSaMvXDkCZOgQHqTJmvez', body='Voice message'
async def on_message(room: nio.MatrixRoom, event):
    # Игнорируем сообщения бота
    if event.sender == self.client.user:
        return

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

            room = db.CRoom(proom_id, proom_name)
            self.database.commit_changes(room)
            return room.id
        except SQLAlchemyError:

            return ERROR_CODE


    def add_user_stat(self, puser_id: int, proom_id: int, pstatfields: dict):
        """Добавляет новую запись статистики по человеку."""

        assert puser_id is not None, \
            "Assert: [statistic.add_user_stat] " \
            "Пропущен параметр <puser_id> !"
        assert proom_id is not None, \
            "Assert: [statistic.add_user_stat] " \
            "Пропущен параметр <proom_id> !"

        try:

            stat = db.CStat(puser_id, proom_id, pstatfields)
            self.database.commit_changes(stat)
            return stat.id
        except SQLAlchemyError:

            return ERROR_CODE


    def add_user_to_base(self, puser_id: int, puser_name: str) -> int:
        """Добавляет нового пользователя в БД и возвращает его ID."""

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


    def get_room_id(self, proom_id) -> int:
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


    def get_personal_information(self, proom_id: int, puser_name: str):
        """Возвращает информацию о пользователе"""

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

                    answer = f"{puser_name} наболтал {stat.fphrases} фраз, " \
                             f"{stat.fwords} слов, {stat.fletters} букв, запостил " \
                             f"{0 if stat.fstickers is None else stat.fstickers} стик., " \
                             f"{0 if stat.fpictures is None else stat.fpictures} фоток, " \
                             f"{0 if stat.faudios is None else stat.faudios} аудио и " \
                             f"{0 if stat.fvideos is None else stat.fvideos} видео,"

        return answer


    def get_statistic(self, ptg_chat_id: int, pcount: int, porder_by: int):
        """Получает из базы статистику по самым говорливым юзерам."""

        session = self.database.get_session()
        query = session.query(db.CRoom, db.CStat, db.CUser)
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


    def get_user_stat(self, pchat_id: int, puser_id: int) -> tuple:
        """Получает из базы статистику пользователя и возвращает её."""

        query = self.database.query_data(db.CStat)
        query = query.filter_by(fuserid=puser_id, fchatid=pchat_id)
        return query.first()


    def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""


    def save_all_type_of_messages(self, proom_id: int,  proom_name: str,
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
                room_id = self.get_room_id(proom_id)
                if room_id is None:

                    # *** Нету еще, новый чат - добавить, и получить id
                    room_id = self.add_room_to_base(proom_id, proom_title)
                # *** Проверить, нет ли юзера в таблице тг юзеров
                user_id = self.get_user_id(puser_id)
                # print(f"**** stat:sav 03 {user_id=}")
                if user_id is None:

                    # *** Нету, новый пользователь
                    user_id = self.add_user_to_base(puser_id, puser_name)
                # *** Имеется ли в БД статистика по этому пользователю?
                user_stat = self.get_user_stat(room_id, user_id)
                if user_stat is not None:

                # *** Изменяем статистику юзера в зависимости от типа сообщения
                if isinstance(event, nio.RoomMessageText):

                    if pevent.body.strip()[0] <> config.command_prefix:

                        user_stat.phrases += 1
                        user_stat.letters += len(pevent.body)
                        user_stat.words += len(message_text.split(" "))
                elif isinstance(event, nio.RoomMessageVideo):

                    user_stat.videos += 1
                elif isinstance(event, nio.RoomMessageAudio):

                    user_stat.audios += 1
                elif isinstance(event, nio.RoomMessageImage):

                    user_stat.audios += 1
                elif isinstance(event, nio.RoomMessageFile):

                    user_stat.files += 1
                # *** Если информации о юзере нет в базе, добавляем, иначе апдейтим
                if user_stat is None:

                    self.add_user_stat(user_id, room_id, user_stat)

                else:

                    self.update_user_stat(user_id, room_id, user_stat)

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
        if self.can_process_command(proom_title, pmessage_text, UNIT_ID, COMMANDS):

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
                    if command in TOP_10_GROUP:

                        answer = self.get_statistic(pchat_id, 10, order_by)
                    elif command in TOP_25_GROUP:

                        answer = self.get_statistic(pchat_id, 25, order_by)
                    elif command in TOP_50_GROUP:

                        answer = self.get_statistic(pchat_id, 50, order_by)
                    elif command in PERSONAL_GROUP:

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
