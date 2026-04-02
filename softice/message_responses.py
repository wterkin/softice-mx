import logging

from nio import AsyncClient, MatrixRoom, RoomMessageText

from datetime import datetime

from softice.chat_functions import send_text_to_room
from softice.config import Config
from softice.storage import Storage
from softice import bot_commands as cmd
from softice import babbler

logger = logging.getLogger(__name__)

OBSOLETE_PERIOD: int = 63000 # 3000 

class Message:
    def __init__(
        self,
        client: AsyncClient,
        store: Storage,
        config: Config,
        message_content: str,
        room: MatrixRoom,
        event: RoomMessageText,
    ):
        """Initialize a new Message

        Args:
            client: nio client used to interact with matrix.

            store: Bot storage.

            config: Bot configuration parameters.

            message_content: The body of the message.

            room: The room the event came from.

            event: The event defining the message.
        """
        self.client = client
        self.store = store
        self.config = config
        self.message_content = message_content
        self.room = room
        self.event = event
        self.first_run: Bool = True
        # *** Поехали создавать объекты модулей =)
        self.babbler: babbler.CBabbler = babbler.CBabbler(self.config)
    
    """
    *** self.event=RoomMessageText(
      source={'content': {'body': 'bye', 'm.mentions': {}, 'msgtype': 'm.text'}, 
              'origin_server_ts': 1773755927587, 
              'sender': '@namo:sibnsk.net', 
              'type': 'm.room.message', 
              'unsigned': {'membership': 'join'}, 
              'event_id': '$Ge3kcprKtxlcLD0LLCgM4931JH_LcY50YTZ_30GpGbY'
             }, 
      event_id='$Ge3kcprKtxlcLD0LLCgM4931JH_LcY50YTZ_30GpGbY', 
      sender='@namo:sibnsk.net', 
      server_timestamp=1773755927587, 
      decrypted=False, 
      verified=False, 
      sender_key=None, 
      session_id=None, 
      transaction_id=None, 
      body='bye', 
      formatted_body=None, 
      format=None)
    """
    
    async def run_once(self):
        """Функция выполняется один раз в начале работы."""

        if self.first_run:
        
            self.first_run = False
            print("*** Run once.")
            await self.babbler.reload()

        
    async def is_obsolete(self) -> bool:
        """Возвращает True, если разница между временем события и текущим равна OBSOLETE_PERIOD и больше. """
        now_time: int = int(datetime.now().timestamp()*1000)
        delta: int = now_time - self.event.server_timestamp
        return delta >= OBSOLETE_PERIOD


        """
        !!!!!!!!!!!!!!!!!!!!!!!!! self.chats={'Арда': 'babbler', 'Ботовка': 'babbler'}
        !!!!!!!!!!!!!!!!!!!!!!!!! self.meteorolog={'api_key': '3c15fe44d0d0d93e28fd81b00a8e46bf'}
        !!!!!!!!!!!!!!!!!!!!!!!!! self.babbler={'period': 8}
        """
    async def process(self) -> None:
        """Обработка и возврат ответа модулей бота на сообщения и команды """

        await self.run_once()    
        # *** Если сообщение не из незапамятных времён...
        if not await self.is_obsolete():
   
            # *** Получим текст сообщения в нижнем регистре
            message: str = self.message_content.lower()
            # *** Пусть болтун отреагирует
            self.babbler.talk(self.room, message)
            # *** Это не команда, случайно?
            has_command_prefix = msg.startswith(self.command_prefix)
            if has_command_prefix:

                # *** Удаляем префикс команды
                msg = msg[len(self.command_prefix) :]
                command: cmd.Command = cmd.Command(self.client, self.store, self.config, msg, room, event)
                await command.process()
            elif message == "ping" or message == "пинг":

                await self._ping()
                print("--> Ping")
        return 
    
    
    async def _exit(self) -> None:
        """Завершает работу бота."""
        answer = "Добби свободен!!"
        print(answer)
        await send_text_to_room(self.client, self.room.room_id, answer)
        if self.client.client_session:
        
            await self.client.client_session.close()
            self.client_session = None
        # await self.client.close()  
        
    async def _ping(self):
        """Возвращает ответ на пинг."""
        answer = "Понг!"
        print(f"{answer=}")
        await send_text_to_room(self.client, self.room.room_id, answer)
        
    async def _hello_world(self) -> None:
        """Say hello"""
        text = "Hello, world!"
        await send_text_to_room(self.client, self.room.room_id, text)
