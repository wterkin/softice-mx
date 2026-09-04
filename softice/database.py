# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль функций, связанных с БД."""
from pathlib import Path

from sqlalchemy import Column, Integer, String, MetaData, ForeignKey, DateTime, exc, select, delete
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker # , AsyncSession
# py lint: disable=C0301
# py lint: disable=line-too-long

DATABASE_VERSION: int = 1
DATABASE_NAME: str = "softice"
STATUS_ACTIVE: int = 1
STATUS_INACTIVE: int = 0
# 'x3pr7d5iH9'

MUTE_PENALTY = 1
BAN_PENALTY = 2
RUSSIAN_DATETIME_FORMAT = "%d.%m.%Y %H:%M:%S"
WAITING_TIME: float = 0.1

ENGINE: str = "postgresql+asyncpg"
DB_USER: str = "softice"
DB_PASSWORD: str = "qz7$tEr"
DB_HOST: str = "localhost"
# DATABASE: str = "softice"
# DB_STRING: str = f"{ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DATABASE}"

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
    froomid = Column(String,
                     nullable=False,
                     unique=True)
    froomname = Column(String,
                       nullable=False,
                       index=True)

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
    fmatrixuserid = Column(String,
                           nullable=False,
                           unique=True)
    fusername = Column(String,
                       nullable=True,
                       default="",
                       index=True
                       )

    def __init__(self, pmatrix_user_id: str, puser_name: str = ""):
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
    __ffiles = Column(Integer, default=0)    # m.video

    def __init__(self, puser_id: int, proom_id: int, pdata_dict: dict):
        """Конструктор"""

        super().__init__()
        self.fuserid = puser_id
        self.froomid = proom_id
        self.set_all_fields(pdata_dict)

    @property
    def userid(self):
        """User ID"""

        return self.__fuserid


    @userid.setter
    def userid(self, puser_id):
        """User ID"""

        assert puser_id > 0, \
            "Идентификатор пользователя не может быть отрицательным"
        self.__fuserid = puser_id


    @property
    def roomid(self):
        """Room ID"""

        return self.__froomid


    @roomid.setter
    def roomid(self, proom_id):
        """Room ID"""

        assert proom_id > 0, \
            "Идентификатор комнаты не может быть отрицательным"
        self.__froomid = proom_id


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


    @property
    def audios(self):
        """Audios"""

        return self.__faudios


    @audios.setter
    def audios(self, paudios):
        """Audios"""

        assert paudios > 0, \
            "Количество звукозаписей не может быть отрицательным"
        self.__faudios = paudios


    @property
    def videos(self):
        """Videos"""

        return self.__fvideos

    @videos.setter
    def videos(self, pvideos):
        """Videos"""

        assert pvideos > 0, \
            "Количество видеозаписей не может быть отрицательным"
        self.__fvideos = pvideos

    @property
    def files(self):
        """Audios"""

        return self.__ffiles


    @files.setter
    def files(self, pfiles):
        """Files"""

        assert pfiles > 0, \
            "Количество файлов не может быть отрицательным"
        self.__faudios = pfiles


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


class CDataBase:
    """Класс для работы с базой данных."""

    def __init__(self, pconfig, pdatabase_name: str):
        """Конструктор класса."""
        self.config: dict = pconfig
        self.AsyncSessionLocal = None
        self.engine = None
        self.busy: bool = False
        self.database_name: str = pdatabase_name


    async def commit_changes(self, obj):
        """Сохраняет изменения в БД."""

        # *** Сохраняем данные
        try:

            async with self.AsyncSessionLocal() as session:

                async with session.begin:

                    session.add(obj)

        except exc.SQLAlchemyError:

            print("Database error! * database.commit_changes")


    async def connect(self):
        """Устанавливает соединение с БД."""

        result: bool = False
        try:

            db_string: str = (f"{ENGINE}://{DB_USER}:{DB_PASSWORD}@"
                              f"{DB_HOST}/{self.database_name}")
            self.engine = create_async_engine(db_string,
                                              echo=True,
                                              pool_size=10,
                                              max_overflow=20,
                                              pool_pre_ping=True,
                                              )
            self.AsyncSessionLocal = async_sessionmaker(bind=self.engine,
                                                        expire_on_commit=False)
            result = True
        except exc.SQLAlchemyError:

            print("Database error! * database.connect")
        return result


    async def create(self) -> bool:
        """Создает или изменяет БД в соответствии с описанной в классах структурой."""

        try:

            async with self.engine.begin() as conn:

                # Создать все таблицы
                await conn.run_sync(Base.metadata.create_all)
                return True
        except exc.SQLAlchemyError:

            print("Database error! * database.create")
            return False



    async def disconnect(self):
        """Разрывает соединение с БД."""

        await self.engine.dispose()


    async def get_session(self):

        """Возвращает экземпляр session."""
        #async with self.AsyncSessionLocal() as session:
        #return session
        return self.AsyncSessionLocal


    async def query_data(self, model_class):
        """Возвращает выборку заданнного класса."""

        try:

            # *** Теперь сами её залочим.
            async_session_class = await self.get_session()
            async with async_session_class() as session:

                return await session.execute(select(model_class))

        except exc.SQLAlchemyError:

            print("Database error! * database.query_data")
        return None


    async def wipe_table(self, model_class):
        """Уничтожает данные заданного класса. """
        try:

            async_session_class = await self.get_session()
            async with async_session_class() as session:

                # Используем новое имя параметра
                await session.execute(delete(model_class))
                await session.commit()
        except exc.SQLAlchemyError:

            # Тут я позволил себе поправить опечатку в скобке
            print("Database error! [database.wipe_table]")
