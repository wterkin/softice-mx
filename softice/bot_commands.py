from nio import AsyncClient, MatrixRoom, RoomMessageText

from softice.chat_functions import react_to_event, send_text_to_room
from softice.config import Config
from softice.storage import Storage

from datetime import datetime

OBSOLETE_PERIOD: int = 63000 # 3000 


class Command:
    def __init__(
        self,
        client: AsyncClient,
        store: Storage,
        config: Config,
        command: str,
        room: MatrixRoom,
        event: RoomMessageText,
    ):
        """A command made by a user.

        Args:
            client: The client to communicate to matrix with.

            store: Bot storage.

            config: Bot configuration parameters.

            command: The command and arguments.

            room: The room the command was sent in.

            event: The event describing the command.
        """
        self.client = client
        self.store = store
        self.config = config
        self.command = command
        self.room = room
        self.event = event
        self.args = self.command.split()[1:]
        print(f"@@@ {self.command=}")
        print(f"@@@ {self.room=}")
        print(f"@@@ {self.event=}")
        print(f"@@@ {self.args=}")
    """    
    self.event=RoomMessageText(
        source={
            'content': {
                'body': '!bye', 'm.mentions': {}, 'msgtype': 'm.text'
                       }, '
             origin_server_ts': 1774363005203, 
             'sender': '@namo:sibnsk.net', 
             'type': 'm.room.message', 
             'unsigned': {'membership': 'join'}, 
             'event_id': '$B-tpCjEQB_la1fMaIWaJTxx6-7gGu5PFyByi1xgNVdQ'}, 
              event_id='$B-tpCjEQB_la1fMaIWaJTxx6-7gGu5PFyByi1xgNVdQ', 
              sender='@namo:sibnsk.net', 
              server_timestamp=1774363005203, 
              decrypted=False, 
              verified=False, 
              sender_key=None, 
              session_id=None, 
              transaction_id=None, 
              body='!bye', 
              formatted_body=None, 
              format=None
              )
    """
        
    async def is_obsolete(self) -> bool:
        """Возвращает True, если разница между временем события и текущим равна OBSOLETE_PERIOD и больше. """
        now_time: int = int(datetime.now().timestamp()*1000)
        delta: int = now_time - self.event.server_timestamp
        return delta >= OBSOLETE_PERIOD

    async def process(self):
        """Process the command"""
        if not await self.is_obsolete():
        
            # *** Вызываем обработчика болтуна
            # # MTEXT MCHAT_TITLE MUSER_NAME
            self.babbler.babbler(self.room, self.event.source["sender"], message)
            # print(f"@@@ {self.command=}")
            if self.command.startswith("echo"):
                await self._echo()
            elif self.command.startswith("react"):
                await self._react()
            elif self.command.startswith("help"):
                await self._show_help()
            elif self.command.startswith("ping") or self.command.startswith("пинг"):

                await self._ping()
            elif self.command.startswith("bye") or self.command.startswith("!!"):

                await self._exit()
            else:
            
                await send_text_to_room(self.client, self.room.room_id, "Message obsolete...")
        #    await self._unknown_command()

    async def _exit(self):
        """Завершает работу бота."""

        print("Quitting...")
        # await self.client.aclose()
        # if self.client.client_session:
        
        # await self.client.close()
        await self.client.client_session.close()
        # self.client.client_session = None
            
            
            
    async def _ping(self):
        """Возвращает ответ на пинг."""
        response = "Понг."


    async def _echo(self):
        """Echo back the command's arguments"""
        response = " ".join(self.args)
        await send_text_to_room(self.client, self.room.room_id, response)


    async def _react(self):
        """Make the bot react to the command message"""
        # React with a start emoji
        reaction = "⭐"
        await react_to_event(
            self.client, self.room.room_id, self.event.event_id, reaction
        )

        # React with some generic text
        reaction = "Some text"
        await react_to_event(
            self.client, self.room.room_id, self.event.event_id, reaction
        )

    async def _show_help(self):
        """Show the help text"""
        if not self.args:
            text = (
                "Hello, I am a bot made with matrix-nio! Use `help commands` to view "
                "available commands."
            )
            await send_text_to_room(self.client, self.room.room_id, text)
            return

        topic = self.args[0]
        if topic == "rules":
            text = "These are the rules!"
        elif topic == "commands":
            text = "Available commands: ..."
        else:
            text = "Unknown help topic!"
        await send_text_to_room(self.client, self.room.room_id, text)

    async def _unknown_command(self):

        await send_text_to_room(
            self.client,
            self.room.room_id,
            f"Unknown command '{self.command}'. Try the 'help' command for more information.",
        )
