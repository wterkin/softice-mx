#!/usr/bin/env python3
#
import asyncio
import logging
import sys
from time import sleep

from aiohttp import ClientConnectionError, ServerDisconnectedError
from nio import (
    AsyncClient,
    AsyncClientConfig,
    InviteMemberEvent,
    LocalProtocolError,
    LoginError,
    MegolmEvent,
    RoomMessageText,
    UnknownEvent,
)

from softice.callbacks import Callbacks
from softice.config import Config
from softice.storage import Storage

logger = logging.getLogger(__name__)

CONFIG_FILE: str = "config.yaml"

LOGIN_FAILED_PAUSE: int = 15

async def main():
    """The first function that is run when starting the bot"""

    # *** Если в командной строке указан иной конфиг..
    if len(sys.argv) > 1:
    	
      	# *** ... берём его.
        config_path = sys.argv[1]
    else:
    
    	# *** ...иначе берём стандартный
        config_path = CONFIG_FILE
    # *** Читаем конфиг, парсим его и создаем объект, хранящий конфигурацию.
    config = Config(config_path)
    # *** Конфигурируем базу данных
    store = Storage(config.database)
    # *** Опции AsyncClient. Шифрование я отключил.
    client_config = AsyncClientConfig(
        max_limit_exceeded=0,
        max_timeouts=0,
        store_sync_tokens=True,
        encryption_enabled=False, 
    )
    # *** Создаем основной объект бота типа AsyncClient
    client = AsyncClient(
        config.homeserver_url,
        config.user_id,
        device_id=config.device_id,
        store_path=config.store_path,
        config=client_config,
    )
    # *** Если есть токен пользователя - используем его.
    if config.user_token:
    
        client.access_token = config.user_token
        client.user_id = config.user_id

    # *** Вешаем обработчики событий
    callbacks = Callbacks(client, store, config)
    # Обработчик сообщений
    client.add_event_callback(callbacks.message, (RoomMessageText,))
    # Обработчик приглашений
    client.add_event_callback(
        callbacks.invite_event_filtered_callback, (InviteMemberEvent,)
    )
    # Обработчик ошибок расшифровки
    client.add_event_callback(callbacks.decryption_failure, (MegolmEvent,))
    # Обработчик неизвестных событий
    client.add_event_callback(callbacks.unknown, (UnknownEvent,))

    # self.barman: barman.CBarman = barman.CBarman(self.config, self.data_path
    # self.bellringer: bellringer.CBellRinger = bellringer.CBellRinger(self.co
    # self.collector: collector.CCollector = collector.CCollector(self.config)
    # self.gambler: gambler.CGambler = gambler.CGambler(self.config)
    # self.haijin: haijin.CHaijin = haijin.CHaijin(self.config, self.data_path
    # self.librarian: librarian.CLibrarian = librarian.CLibrarian(self.config,
    # self.majordomo: majordomo.CMajordomo = majordomo.CMajordomo(self.config,
    # self.meteorolog: meteorolog.CMeteorolog = meteorolog.CMeteorolog(self.co
    # self.moderator: moderator.CModerator = moderator.CModerator(self.robot,
    # self.statistic: statistic.CStatistic = statistic.CStatistic(self.config,
    # self.stargazer: stargazer.CStarGazer = stargazer.CStarGazer(self.config,
    # self.theolog: theolog.CTheolog = theolog.CTheolog(self.config, self.data

    # *** Бесконечный цикл попыток подключения.
    while True:
    
        try:
	
    	    # *** Если есть токен пользователя...
            if config.user_token:

                # *** непонятно
                client.load_store()

                # *** Если клиент должен выгрузить ключи...
                if client.should_upload_keys:
                    
                    # *** Ожидаем выгрузки
                    await client.keys_upload()
            else:
            
                # *** Логинимся с использованием имени пользователя и пароля
                try:
                    
                    # *** Ждём ответа от сервера.
                    login_response = await client.login(
                        password=config.user_password,
                        device_name=config.device_name,
                    )
                    # *** Если залогиниться не удалось, пишем в лог.
                    if type(login_response) == LoginError:
                    
                        logger.error("Failed to login: %s", login_response.message)
                        return False
                except LocalProtocolError as e:

                    # *** Если не хватает каких-то пакетов - жалуемся.
                    logger.fatal(
                        "Failed to login. Have you installed the correct dependencies? "
                        "https://github.com/poljar/matrix-nio#installation "
                        "Error: %s",
                        e,
                    )
                    return False

            # *** Ура, мы залогинились!
            logger.info(f"Logged in as {config.user_id}")
            # *** Ждём синхронизации
            await client.sync_forever(timeout=30000, full_state=True)
        except (ClientConnectionError, ServerDisconnectedError):
            # *** Залогиниться не удалось, пишем в лог...
            logger.warning("Unable to connect to homeserver, retrying in 15s...")
            # Ждём 15 секунд и повторяем попытку
            sleep(LOGIN_FAILED_PAUSE)
        finally:

            # *** Закрываем соединение
            await client.close()

# *** Запускаем основную функцию в асинхронном цикле
asyncio.get_event_loop().run_until_complete(main())
