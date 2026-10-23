# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru

"""Модуль статистики для бота."""

# import asyncio

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

PHRASES_ORDER: int = 1
WORDS_ORDER: int = 2
IMAGES_ORDER: int = 3
AUDIOS_ORDER: int = 4
VIDEOS_ORDER: int = 5
FILES_ORDER: int = 6


COMMANDS: tuple = (("первые10", "пв10", "top10"),
                   ("первые25", "пв25", "top25"),
                   ("первые50", "пв50", "top50"),
                   ("личные", "лич", "personal", "pers"),
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

DATABASE_NAME: str = "softice"

ERROR_CODE: int = -1


class CStatistic(basis.CBasis):
    """Класс статистика."""

    def __init__(self, pconfig: dict, pdatabase_name: str = DATABASE_NAME):

        super().__init__(pconfig)
        self.database: db.CDataBase = db.CDataBase(self.config, pdatabase_name)
        print("Статистик стартовал.")


    async def init(self) -> bool:
        """ Место для асинхронной инициализации."""

        result: bool = await self.database.connect()
        if result:

            result = await self.database.create()
        return result


    async def add_room_to_base(self, pmx_room_id: str, proom_name: str) -> int:
        """Добавляет новую комнату в БД и возвращает его ID."""

        assert pmx_room_id is not None, \
            "Assert: [statistic.add_chat_to_base] " \
            "Пропущен параметр <pmx_room_id> !"
        assert proom_name is not None, \
            "Assert: [statistic.add_chat_to_base] " \
            "Пропущен параметр <proom_name> !"

        room = db.CRoom(pmx_room_id, proom_name)
        await self.database.commit_changes(room)
        return room.id


    async def add_user_stat(self, pstat: db.CStat) -> int:
        """Добавляет новую запись статистики по человеку."""

        assert pstat is not None, \
            "Assert: [statistic.add_user_stat] " \
            "Пропущен параметр <pstat> !"

        await self.database.commit_changes(pstat)
        return pstat.id


    async def add_user_to_base(self, pmx_user_name: str) -> int:
        """"Добавляет нового пользователя в БД и возвращает его ID."""

        assert pmx_user_name is not None, \
            "Assert: [statistic.add_user_to_base] " \
            "Пропущен параметр <pmx_user_name> !"

        user = db.CUser(pmx_user_name)
        # rint(f"*** Statistic ** autb ** {pmx_user_name} **")
        # rint(f"*** Statistic ** autb ** {user} **")
        await self.database.commit_changes(user)
        return user.id


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


    async def get_room_id(self, pmx_room_id: str) -> int:
        """Если чат уже есть в базе, возвращает его ID, если нет - None."""

        assert pmx_room_id is not None, \
            "Assert: [statistic.get_room_id] " \
            "Пропущен параметр <pmx_room_id> !"

        result: int  = ERROR_CODE
        room: db.CRoom = None
        try:

            sel = self.database.query_data(db.CRoom)
            sel = sel.where(db.CRoom.froomid==pmx_room_id)
            sess = await self.database.get_session()
            async with sess() as session:

                value = await session.execute(sel)
                room = value.scalar_one_or_none()
                if room is not None:

                    result = room.id

        except SQLAlchemyError:

            result = ERROR_CODE
        return result


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


    async def get_personal_information(self, proom_id: str, pmx_user_name: str) -> str:
        """Возвращает информацию о пользователе"""

        assert proom_id is not None, \
            "Assert: [statistic.get_personal_information] " \
            "Пропущен параметр <proom_id> !"
        assert pmx_user_name is not None, \
            "Assert: [statistic.get_personal_information] " \
            "Пропущен параметр <pmx_user_name> !"

        answer: str = ""
        sess = await self.database.get_session()
        # *** Получим данные юзера
        #rint(f"*** Statistic ** gpi ** start ** {pmx_user_name}**")
        sel = self.database.query_data(db.CUser)
        sel = sel.where(db.CUser.fusername==pmx_user_name)
        async with sess() as session:

            user_result = await session.execute(sel)
            user = user_result.scalar_one_or_none()
            # rint(f"*** Statistic ** gpi ** {user=} **")
            if user is not None:

                # *** Получим ID чата в базе
                sel = self.database.query_data(db.CRoom)
                sel = sel.where(db.CRoom.froomid==proom_id)
                room_result = await session.execute(sel)
                room = room_result.scalar_one_or_none()
                # rint(f"*** Statistic ** gpi ** {room=} **")
                if room is not None:

                    # *** Получим статистику юзера в чате
                    sel = self.database.query_data(db.CStat) # .where(db.CStat.userid==user.id)
                    sel = sel.where(db.CStat._fuserid == user.id)
                    sel = sel.where(db.CStat._froomid == room.id)
                    stat_result = await session.execute(sel)
                    stat = stat_result.scalar_one_or_none()
                    # rint(f"*** Statistic ** gpi ** {stat=} **")

                    if stat is not None:

                        answer = f"{pmx_user_name} наговорил {stat.phrases} фраз, " \
                                 f"{stat.words} слов, {stat.letters} букв, запостил " \
                                 f"{0 if stat.images is None else stat.images} фоток, " \
                                 f"{0 if stat.audios is None else stat.audios} аудио и " \
                                 f"{0 if stat.videos is None else stat.videos} видео," \
                                 f"{0 if stat.files is None else stat.files} файлов"
        return answer


    async def get_statistic(self, pmx_room_id: str, pcount: int, porder_by: int) -> str:
        """Получает из базы статистику по самым говорливым юзерам."""

        assert pmx_room_id is not None, \
            "Assert: [statistic.get_statistic] " \
            "Пропущен параметр <pmx_room_id> !"
        assert pcount is not None, \
            "Assert: [statistic.get_statistic] " \
            "Пропущен параметр <pcount> !"
        assert porder_by is not None, \
            "Assert: [statistic.get_statistic] " \
            "Пропущен параметр <porder_by> !"

        room_id = await self.get_room_id(pmx_room_id)
        query = select(db.CRoom, db.CStat, db.CUser)
        query = query.where(db.CStat._froomid==room_id)
        query = query.join(db.CStat, db.CStat._froomid == db.CRoom.id)
        query = query.join(db.CUser, db.CStat._fuserid == db.CUser.id)
        if porder_by == PHRASES_ORDER:

            query = query.order_by(db.CStat._fphrases.desc())
        elif porder_by == WORDS_ORDER:

            query = query.order_by(db.CStat._fwords.desc())
        elif porder_by == IMAGES_ORDER:

            query = query.order_by(db.CStat._fimages.desc())
        elif porder_by == AUDIOS_ORDER:

            query = query.order_by(db.CStat._faudios.desc())
        elif porder_by == VIDEOS_ORDER:

            query = query.order_by(db.CStat._fvideos.desc())
        elif porder_by == FILES_ORDER:

            query = query.order_by(db.CStat._ffiles.desc())
        else:

            query = query.order_by(db.CStat._fphrases.desc())
            # stat = query.limit(pcount)
        query = query.limit(pcount)
        sess = await self.database.get_session()
        async with sess() as session:

            value = await session.execute(query)
            result = value.scalars().all()
        answer = "Самые общительные:\n"
        print(f"*** Statistic ** gst ** {result=} **")
        for number, item in enumerate(result):

            print(f"*** Statistic ** gst ** {item=} **")
            # answer += f"{number + 1} : {item[2].fusername} : {item[1].phrases}" \
                      # f" фраз, {item[1].fwords} слов, " \
                      # f"{0 if item[1].files is None else item[1].files} файл., " \
                      # f"{0 if item[1].images is None else item[1].images} картин., " \
                      # f"{0 if item[1].audios is None else item[1].audios} звук. и " \
                      # f"{0 if item[1].videos is None else item[1].videos} вид. \n"
            # answer += f"{number + 1} : {item.username} : {item.phrases}" \
                      # f" фраз, {item.words} слов, " \
                      # f"{0 if item.files is None else item.files} файл., " \
                      # f"{0 if item.images is None else item.images} картин., " \
                      # f"{0 if item.audios is None else item.audios} звук. и " \
                      # f"{0 if item.videos is None else item.videos} вид. \n"
        answer += f"Отсортировано по количеству {SORTED_BY[porder_by-1]}. \n"
        return answer


    async def get_user_id(self, pmx_user_name) -> int:
        """Если пользователь уже есть в базе, возвращает его ID, если нет - ERROR_CODE."""

        assert pmx_user_name is not None, \
            "Assert: [statistic.get_user_id] " \
            "Пропущен параметр <pmx_user_name> !"

        # rint(f"*** Statistic ** gui ** {pmx_user_name=}**")
        result: int = ERROR_CODE
        sel = self.database.query_data(db.CUser)
        sel = sel.where(db.CUser.fusername==pmx_user_name)
        sess = await self.database.get_session()
        async with sess() as session:

            res = await session.execute(sel)
            user = res.scalar_one_or_none()
            if user is not None:

                result = user.id
        # rint(f"*** Statistic ** gui ** {result=}**")
        return result


    async def get_user_stat(self, pmx_room_id: str, pmx_user_name: str) -> tuple:
        """Получает из базы статистику пользователя и возвращает её."""

        assert pmx_room_id is not None, \
            "Assert: [statistic.get_user_stat] " \
            "Пропущен параметр <pmx_room_id> !"
        assert pmx_user_name is not None, \
            "Assert: [statistic.get_user_stat] " \
            "Пропущен параметр <pmx_user_name> !"

        result: tuple = None
        # rint(f"*** Statistic ** gus ** {pmx_user_name=} **")
        user_id = await self.get_user_id(pmx_user_name)
        if user_id != ERROR_CODE:

            # rint(f"*** Statistic ** gus ** {user_id=} **")
            room_id = await self.get_room_id(pmx_room_id)
            if room_id != ERROR_CODE:

                # rint(f"*** Statistic ** gus ** {room_id=} **")

                sel = self.database.query_data(db.CStat)
                sel = sel.where(db.CStat._fuserid==user_id)
                sel = sel.where(db.CStat._froomid==room_id)
                sess = await self.database.get_session()
                async with sess() as session:

                    # rint(f"*** Statistic ** gus ** before exec **")
                    res = await session.execute(sel)
                    result = res.scalar_one_or_none()
        # rint(f"*** Statistic ** gus ** {result=} **")
        return result


    async def save_all_type_of_messages(self, pmx_room_id: int, pmx_room_name: str,
                                        pmx_user_name: str,
                                        pevent: RoomMessageText) -> bool:
        """Учитывает стикеры, видео, аудиосообщения."""

        assert pmx_room_id is not None, \
            "Assert: [statistic.save_all_type_of_messages] " \
            "Пропущен параметр <pmx_room_id> !"
        assert pmx_room_name is not None, \
            "Assert: [statistic.save_all_type_of_messages] " \
            "Пропущен параметр <pmx_room_name> !"
        assert pmx_user_name is not None, \
            "Assert: [statistic.save_all_type_of_messages] " \
            "Пропущен параметр <pmx_user_name> !"

        result: bool = False
        # rint(f"*** Statistic ** sat ** begin {pmx_user_name=}**")
        # *** Это не бот написал? Чужой бот, не наш?
        if pmx_user_name not in self.config.alien_bots:

            # rint(f"*** Statistic ** sat ** not bot **")
            # Проверить, нет ли уже этого чата в таблице чатов
            room_id = await self.get_room_id(pmx_room_name)
            if room_id == ERROR_CODE:

                # *** Нету еще, новый чат - добавить, и получить id
                # rint(f"*** Statistic ** sat ** {pmx_room_name=} **")
                room_id = await self.add_room_to_base(pmx_room_id, pmx_room_name)
            # rint(f"*** Statistic ** sat ** {room_id=} **")
            # *** Проверить, нет ли юзера в таблице тг юзеров
            # rint(f"*** Statistic ** sat ** {pmx_user_name=}**")
            user_id = await self.get_user_id(pmx_user_name)
            if user_id == ERROR_CODE:

                # *** Нету, новый пользователь
                user_id = await self.add_user_to_base(pmx_user_name)
                # rint(f"*** Statistic ** sat ** {user_id=} **")

            # *** Имеется ли в БД статистика по этому пользователю?
            # rint(f"*** Statistic ** sat ** before stat **")
            user_stat = await self.get_user_stat(pmx_room_id, pmx_user_name)
            if user_stat is None:

                user_stat = db.CStat(user_id, room_id)
                user_stat.phrases = 0
                user_stat.letters = 0
                user_stat.words = 0
                user_stat.videos = 0
                user_stat.audios = 0
                user_stat.images = 0
                user_stat.files = 0
            # *** Изменяем статистику юзера в зависимости от типа сообщения
            # rint(f"*** Statistic ** sat ** {user_stat=} **")
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

                user_stat.images += 1
            elif isinstance(pevent, RoomMessageFile):

                user_stat.files += 1
            # rint(f"*** Statistic ** sat ** finish {user_stat=} **")
            await self.database.commit_changes(user_stat)
            result = True
        return result


    async def statistic(self, pmx_room_id: int, pmx_room_name: str, pmx_user_name, pmessage_text: str) -> str:
        """Обработчик команд."""

        assert pmx_room_id is not None, \
            "Assert: [statistic.statistic] " \
            "Пропущен параметр <pmx_room_id> !"
        assert pmx_room_name is not None, \
            "Assert: [statistic.statistic] " \
            "Пропущен параметр <pmx_room_name> !"
        assert pmx_user_name is not None, \
            "Assert: [statistic.statistic] " \
            "Пропущен параметр <pmx_user_name> !"
        assert pmessage_text is not None, \
            "Assert: [statistic.statistic] " \
            "Пропущен параметр <pmessage_text> !"

        command: int
        answer: str = ""
        order_by: int = 0
        word_list: list = self.parse_input(pmessage_text)
        if self.can_process_command(pmx_room_name, pmessage_text, UNIT_ID, COMMANDS):

            # *** Если это запрос списка команд..
            if word_list[0] in COMMANDS[HINT_GROUP]:

                # *** Возвращаем список команд
                answer = self.get_commands(pmx_room_name)

            else:

                # *** Получим код команды
                command: int = self.identify_command(word_list[0], COMMANDS)
                if command >= 0:

                    # *** Если длина списка команд больше 1 - это указание сортировки
                    if len(word_list) > 1 and word_list[1].isdigit():

                        # *** Смотрим, как будем сортировать вывод
                        order_by = int(word_list[1])
                        if order_by < 1 or order_by > 6:

                            order_by = 1
                    if command == TOP_10_GROUP:

                        answer = await self.get_statistic(pmx_room_id, 10, order_by)
                    elif command == TOP_25_GROUP:

                        answer = await self.get_statistic(pmx_room_id, 25, order_by)
                    elif command == TOP_50_GROUP:

                        answer = await self.get_statistic(pmx_room_id, 50, order_by)
                    elif command == PERSONAL_GROUP:

                        # rint(f"*** Statistic ** stat ** persinf ** {pmx_user_name=} ***")
                        answer = await self.get_personal_information(pmx_room_id, pmx_user_name)
        return answer


    async def destroy(self):
        """Закрывает соединение с базой."""

        await self.database.destroy()
