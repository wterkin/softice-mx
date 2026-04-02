import logging
from typing import Any, Dict

# The latest migration version of the database.
#
# Database migrations are applied starting from the number specified in the database's
# `migration_version` table + 1 (or from 0 if this table does not yet exist) up until
# the version specified here.
#
# When a migration is performed, the `migration_version` table should be incremented.
latest_migration_version = 0

logger = logging.getLogger(__name__)


class Storage:

    def __init__(self, database_config: Dict[str, str]):
        """Настройка базы данных.

           Запускает начальную настройку или миграцию в зависимости от того, 
           был ли уже создан файл базы данных.

        Аргументы:
            database_config: словарь, содержащий следующие ключи:
                * Type: строка, например, "sqlite" или "postgres".
                * connection_string: строка, содержащая строку подключения, 
                  которая передается в метод "connect" каждой соответствующей
                  библиотеки базы данных.
        """
        
        self.conn = self._get_database_connection(
            database_config["type"], database_config["connection_string"]
        )
        self.cursor = self.conn.cursor()
        self.db_type = database_config["type"]

        # *** Проверим версию миграции
        migration_level = 0
        try:
        
            self._execute("SELECT version FROM migration_version")
            row = self.cursor.fetchone()
            migration_level = row[0]
        except Exception:
        
            # *** Фигня какая-то, надо создать базу
            self._initial_setup()
        finally:
            
            # *** Если версия миграции изменилась - мигрируем.
            if migration_level < latest_migration_version:
            
                self._run_migrations(migration_level)

        logger.info(f"Database initialization of type '{self.db_type}' complete")


    def _get_database_connection(
        self, database_type: str, connection_string: str
    ) -> Any:
        """Создаёт и возвращает соединение с БД. """
        if database_type == "sqlite":
        
            import sqlite3
            # *** Инициализируем и возвращаем соединение с sqlite, автокоммит включен
            return sqlite3.connect(connection_string, isolation_level=None)
        elif database_type == "postgres":

            import psycopg2
            # *** Инициализируем и возвращаеи соединение с postgres
            conn = psycopg2.connect(connection_string)
            # *** Включаем автокоммит
            conn.set_isolation_level(0)
            return conn


    def _initial_setup(self) -> None:
        """Начальная конфигурация БД."""
        logger.info("Performing initial database setup...")
        # *** Создаём таблицу версий миграции
        self._execute(
            """
            CREATE TABLE migration_version (
                version INTEGER PRIMARY KEY
            )
            """
        )
        # *** Сбрасываем начальную версию в ноль
        self._execute(
            """
            INSERT INTO migration_version (
                version
            ) VALUES (?)
            """,
            (0,),
        )

        # *** Создаём другие таблицы тут.
        logger.info("Database setup complete")


    def _run_migrations(self, current_migration_version: int) -> None:
        """Выполняем миграции. Мигрируем до версии, указанной в `latest_migration_version`. 
        Параметры:
            current_migration_version: Текущая версия миграции базы
        """
        logger.debug("Checking for necessary database migrations...")

        # if current_migration_version < 1:
        #    logger.info("Migrating the database from v0 to v1...")
        #
        #    # Add new table, delete old ones, etc.
        #
        #    # Update the stored migration version
        #    self._execute("UPDATE migration_version SET version = 1")
        #
        #    logger.info("Database migrated to v1")

    def _execute(self, *args) -> None:
        """Обёртка вокруг cursor.execute, которая заменяет ? to %s для постгресса.
        Это позволяет поддерживать запросы, совместимые как с postgres, так и с sqlite.
        Параметры:
            args: Аргументы, передаваемые в cursor.execute.
        """
        if self.db_type == "postgres":
        
            self.cursor.execute(args[0].replace("?", "%s"), *args[1:])
        else:
        
            self.cursor.execute(*args)
