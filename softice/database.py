# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль функций, связанных с БД."""
from pathlib import Path
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, MetaData, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import exc
from sqlalchemy.sql import func
# py lint: disable=C0301
# py lint: disable=line-too-long

DATABASE_VERSION: int = 1
DATABASE_NAME: str = "softice.db"
STATUS_ACTIVE: int = 1
STATUS_INACTIVE: int = 0

#STAT_USERID: str = "userid"
#STAT_LETTERS: str = "letters"
#STAT_WORDS: str = "words"
#STAT_PHRASES: str = "phrases"
#STAT_PICTURES: str = "pictures"
#STAT_STICKERS: str = "stickers"
#STAT_AUDIOS: str = "audios"
#STAT_VIDEOS: str = "videos"

MUTE_PENALTY = 1
BAN_PENALTY = 2
RUSSIAN_DATETIME_FORMAT = "%d.%m.%Y %H:%M:%S"
WAITING_TIME: float = 0.1

convention = {
    "all_column_names": lambda constraint, table: "_".join([
        column.name for column in constraint.columns.values()
    ]),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "cq": "cq__%(table_name)s__%(constraint_name)s",
    "fk": ("fk__%(table_name)s__%(all_column_names)s__"
           "%(referred_table_name)s"),
    "pk": "pk__%(table_name)s"
}

meta_data = MetaData(naming_convention=convention)
Base = declarative_base(metadata=meta_data)

# pylint: disable=not-callable
class CAncestor(Base):
    """Класс-предок всех классов-моделей таблиц SQLAlchemy."""

    __abstract__ = True
    id = Column(Integer,
                autoincrement=True,
                nullable=False,
                primary_key=True,
                unique=True)
    fstatus = Column(Integer,
                     nullable=False,
                     )
    fcreated = Column(DateTime(),
                      default=func.now())
    fupdated = Column(DateTime(),
                      default=func.now(),
                      onupdate=func.now())

    def __init__(self):
        """Конструктор."""

        self.fstatus = STATUS_ACTIVE

    def __repr__(self):
        """Repr"""
        return f"""ID:{self.id},
                   Status:{self.fstatus}"""

    def __str__(self):
        """Str"""

        return f"* Ancest: {self.id} * {self.fstatus} *"

    def null(self):
        """Чтоб линтер был щаслиф."""


class CRoom(CAncestor):
    """Класс справочника чатов."""

    __tablename__ = 'tbl_rooms'
    froomid = Column(Integer,
                     nullable=False,
                     unique=True,
                     index=True)
    froomname = Column(String,
                       nullable=False,
                       )

    def __init__(self, proom_id: int, proom_name: str):
        """Конструктор"""

        super().__init__()
        self.froomid = proom_id
        self.froomname = proom_name

    def __repr__(self):

        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Chat ID:{self.froomid}
                   Chat Name:{self.froomname}"""

    def __str__(self):
        """Str"""

        return f"* Room: {self.id} * {self.fstatus} * {self.froomid} * {self.froomname} *"

    def null(self):
        """Чтоб линтер был щаслив."""


class CUser(CAncestor):
    """Класс модели таблицы справочника ID пользователей телеграмма."""

    __tablename__ = 'tbl_users'
    fmatrixuserid = Column(Integer,
                           nullable=False,
                           unique=True,
                           index=True)
    fusername = Column(String,
                       nullable=True,
                       default="",
                       index=True
                       )

    def __init__(self, pmatrix_user_id: int, puser_name: str = ""):
        """Конструктор"""

        super().__init__()
        self.fmatrixuserid = pmatrix_user_id
        self.fuser_name = puser_name

    def __repr__(self):

        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                    Matrix user ID:{self.fmatrixuserid},
                    User name:{self.fusername}"""

    def __str__(self):
        """Str"""

        return (f"* User: {self.id} * {self.fstatus} * {self.fmatrixuserid}"
                f" * {self.fusername} *")

    def null(self):
        """Чтоб линтер был щаслив."""


class CStat(CAncestor):
    """Класс статистики."""

    __tablename__ = 'tbl_stat'
    __fuserid = Column(Integer, ForeignKey(CUser.id))
    __froomid = Column(Integer, ForeignKey(CRoom.id))
    __fletters = Column(Integer, default=0)   # m.text
    __fwords = Column(Integer, default=0)     # m.text
    __fphrases = Column(Integer, default=0)   # m.text
    __femotes = Column(Integer, default=0)    # m.emote
    __fnotices = Column(Integer, default=0)   # m.notice
    __fimages = Column(Integer, default=0)    # m.image
    __faudios = Column(Integer, default=0)    # m.audio
    __fvideos = Column(Integer, default=0)    # m.video

    def __init__(self, puser_id: int, proom_id: int, pdata_dict: dict):
        """Конструктор"""

        super().__init__()
        self.fuserid = puser_id
        self.froomid = proom_id
        self.set_all_fields(pdata_dict)

    @property
    def letters(self):
        """Letters"""
        return self.__fletters

    @letters.setter
    def letters(self, pletters):
        """Letters"""

        assert pletters > 0, \
            "Количество букв не может быть отрицательным"
        self.__fletters = pletters

    @property
    def words(self):
        """Words"""
        return self.__fwords

    @words.setter
    def words(self, pwords):
        """Words"""

        assert pwords > 0, \
            "Количество слов не может быть отрицательным"
        self.__fwords = pwords

    @property
    def phrases(self):
        """Phrases"""
        return self.__fphrases

    @phrases.setter
    def phrases(self, pphrases):
        """Phrases"""

        assert pphrases > 0, \
            "Количество предложений не может быть отрицательным"
        self.__fphrases = pphrases

    @property
    def emotes(self):
        """Emotes"""
        return self.__femotes

    @emotes.setter
    def emotes(self, pemotes):
        """Emotes"""

        assert pemotes > 0, \
            "Количество эмоций не может быть отрицательным"
        self.__femotes = pemotes

    @property
    def notices(self):
        """Notices"""
        return self.__fnotices

    @notices.setter
    def notices(self, pnotices):
        """Notices"""

        assert pnotices > 0, \
            "Количество примечаний не может быть отрицательным"
        self.__fnotices = pnotices

    @property
    def images(self):
        """Images"""
        return self.__fimages

    @images.setter
    def images(self, pimages):
        """Images"""

        assert pimages > 0, \
            "Количество изображений не может быть отрицательным"
        self.__fimages = pimages

    def __repr__(self):
        """Repr"""

        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   User id:{self.fuserid}
                   Letters:{self.fletters},
                   Words: {self.fwords},
                   Sentences: {self.fphrases},
                   Stickers: {self.fstickers},
                   Pictures: {self.fpictures},
                   Audios: {self.faudios},
                   Videos: {self.fvideos}"""
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


class CRights(CAncestor):
    """Класс модели таблицы прав пользователей."""

    __tablename__ = 'tbl_rights'
    fuserid = Column(Integer, ForeignKey(CUser.id))
    fchatid = Column(Integer, ForeignKey(CRoom.id))
    fkarma = Column(Integer, default=1000)
    fadmin = Column(Boolean, default=True)

    def __init__(self, puser_id: int, pchat_id: int):
        """Конструктор"""

        super().__init__()
        self.fuserid = puser_id
        self.fchatid = pchat_id

    def __repr__(self):

        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   User ID:{self.fuserid}
                   Chat ID:{self.fchatid}
                   Karma:{self.fkarma}
                   Is admin:{self.fadmin}"""


class CSignal(CAncestor):
    """Класс таблицы сигнальщика."""

    __tablename__ = 'tbl_signal'
    fuserid = Column(Integer, ForeignKey(CUser.id))
    fword = Column(String)

    def __init__(self, puserid: int, pword: str):
        """Конструктор"""

        super().__init__()
        self.fuserid = puserid
        self.fword = pword


    def __repr__(self):

        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   User id:{self.fuserid}
                   Word:{self.fword}"""


class CDataBase:
    """Класс."""

    def __init__(self, pconfig, pdata_path, pdatabase_name=DATABASE_NAME):
        """Конструктор класса."""
        self.application_folder = Path.cwd()
        self.config: dict = pconfig
        self.data_path: str = pdata_path
        self.session = None
        self.engine = None
        self.busy: bool = False
        self.database_name: str = pdatabase_name
        self.connect()


    def commit_changes(self, obj):
        """Сохраняет изменения в БД."""

        # *** Если база залочена - подождем.
        delayed: int = 0
        while self.busy:

            sleep(WAITING_TIME)
            delayed += 1
        # *** Теперь сами её залочим.
        self.busy = True
        # *** Сохраняем данные
        try:

            self.session.add(obj)
            self.session.commit()
            if delayed > 0:

                print(f"* Commit paused for {delayed//10} second.")
        except exc.SQLAlchemyError:

            print("Ошибка!!!")
        finally:

            # *** Разлочим базу
            self.busy = False


    def connect(self):
        """Устанавливает соединение с БД."""

        result: bool = False
        try:
            alchemy_echo: bool = self.config["alchemy_echo"] == "1"
            # print(f"{alchemy_echo=} {self.config['alchemy_echo']=}")
            self.engine = create_engine('sqlite:///' + self.data_path + self.database_name,
                                        echo=alchemy_echo,
                                        connect_args={'check_same_thread': False})
            session = sessionmaker()
            session.configure(bind=self.engine)
            self.session = session()
            Base.metadata.bind = self.engine
            result = True
        except exc.SQLAlchemyError:

            print("Ошибка подключения к БД!")
        return result


    def create(self):
        """Создает или изменяет БД в соответствии с описанной в классах структурой."""

        Base.metadata.create_all(self.engine)


    def disconnect(self):

        """Разрывает соединение с БД."""
        self.session.close()
        self.engine.dispose()


    def exists(self):
        """Проверяет наличие базы данных по пути в конфигурации."""

        return Path(self.data_path + self.database_name).exists()


    def get_session(self):

        """Возвращает экземпляр session."""
        return self.session


    def query_data(self, cls):
        """Возвращает выборку заданнного класса."""

        # *** Если база залочена - подождем.
        while self.busy:

            sleep(WAITING_TIME)

        try:

            # *** Теперь сами её залочим.
            self.busy = True
            query = self.session.query(cls)
        finally:

            # *** Разлочим базу
            self.busy = False
        return query
