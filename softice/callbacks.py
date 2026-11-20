# -*- coding: utf-8 -*-
"""Основной модуль управления ботом."""
import logging
import os
from datetime import datetime

# pylint: disable=import-error
from nio import (
    AsyncClient,
    InviteMemberEvent,
    JoinError,
    MatrixRoom,
    MegolmEvent,
    RoomGetEventError,
    # RoomMessage,
    RoomMessageText,
    # RoomMessageImage,
    UploadResponse,
    UnknownEvent,
)  # noqa
# pylint: enable=import-error

from PIL import Image

from softice.chat_functions import make_pill, react_to_event, send_text_to_room
from softice.config import Config
from softice.storage import Storage
from softice.babbler import CBabbler
from softice.barman import CBarman
from softice.collector import CCollector
from softice.gambler import CGambler
from softice.haijin import CHaijin
from softice.librarian import CLibrarian
from softice.majordomo import CMajordomo
from softice.manager import CManager
from softice.meteorolog import CMeteorolog
from softice.moderator import CModerator
from softice.stargazer import CStarGazer
from softice.statistic import CStatistic
from softice.theolog import CTheolog

logger = logging.getLogger(__name__)

# pylint: disable=logging-fstring-interpolation

MINIMUM_USER_QUANTITY: int = 2
HELP_MESSAGE: str = ("Все команды к боту должны начинаться с ! (восклицательного знака). "
                     "Команда должна следовать сразу за восклицательным знаком, без пробела. "
                     "В настоящий момент я понимаю только следующие группы команд: \n")

OBSOLETE_PERIOD: int = 60000 # millisec
TIMESTAMP_FILE: str = "timestamp.json"
TIMESTAMP_SAVE_PERIOD: int = 60000 # millisec


# pylint: disable=too-many-instance-attributes
class Callbacks:
    """Класс обратных вызовов."""
    def __init__(self, client: AsyncClient, store: Storage, config: Config):
        """
        Args:
            client: nio client used to interact with matrix.
            store: Bot storage.
            config: Bot configuration parameters.
        """
        self.client = client
        self.store = store
        self.config = config
        self.command_prefix = config.command_prefix
        # *** Создаём объекты классов
        self.babbler: CBabbler = CBabbler(self.config)
        self.barman: CBarman = CBarman(self.config)
        self.collector: CCollector = CCollector(self.config)
        self.gambler: CGambler = CGambler(self.config)
        self.haijin: CHaijin = CHaijin(self.config)
        self.librarian: CLibrarian = CLibrarian(self.config)
        self.majordomo: CMajordomo = CMajordomo(self.config)
        self.manager: CManager = CManager(self.config, self.client)
        self.meteorolog: CMeteorolog = CMeteorolog(self.config)
        self.moderator: CModerator = CModerator(self.config, self.client)
        self.stargazer: CStarGazer = CStarGazer(self.config)
        self.statistic: CStatistic = CStatistic(self.config, "softice_mx")
        self.theolog: CTheolog = CTheolog(self.config)
        self.first_run: bool = True
        self.last_message: str = ""
        self.manager.delete_restart_flag()


    async def run_once(self):
        """Функция выполняется один раз в начале работы."""

        if self.first_run:

            self.first_run = False
            # print("*** Run once.")
            await self.babbler.reload()
            await self.barman.reload()
            await self.haijin.reload()
            await self.librarian.reload()
            await self.majordomo.reload()
            await self.moderator.reload()
            await self.statistic.init()


    async def is_obsolete(self, pevent: RoomMessageText) -> bool:
        """Возвращает True, если разница между временем события и текущим
           равна OBSOLETE_PERIOD и больше. """
        now_time: int = int(datetime.now().timestamp()*1000)
        delta: int = now_time - pevent.server_timestamp
        return delta >= OBSOLETE_PERIOD

    # pylint: disable=too-many-branches
    # *** Основная процедура вызывается при каждом пришедшем сообщении
    async def message(self, room: MatrixRoom, event: RoomMessageText) -> None:
        """Callback for when a message event is received
        Args:
            room: The room the event came from.
            event: The event defining the message.
        """
        # *** Вызываем процедуру, которая выполняется один раз.
        await self.run_once()
        answer: str = ""
        # *** Если это наше сообщение - игнорим его.
        if event.sender == self.client.user:

            return

        # *** В приватах мы работать не будем
        if room.member_count <= self.config.minimum_quantity:

            await send_text_to_room(self.client, room.room_id,
                "Извините, в привате не работаю.")
            return

        # *** Если сообщение не просрочено...
        if not await self.is_obsolete(event):

            # *** Получим текст сообщения
            message: str = event.body

            # rint(f":: clbk.message :: i :: {message}")
            # *** Выведем в лог отладочное сообщение
            logger.debug(
                f"Bot message received for room {room.display_name} | "
                f"{room.user_name(event.sender)}: {message}"
            )
            local_name: str = await self.get_display_name_in_room(room.room_id, event.sender)
            has_command_prefix = message.startswith(self.command_prefix)
            # *** Что у нас в сообщении?
            if has_command_prefix:

                # *** Может, запросили помощь?
                if "help" in message:

                    # *** Выведем подсказку
                    answer = self.send_hints(room.name)
                if not answer:

                    # *** Болтуну есть что сказать?
                    answer = await self.babbler.babbler(room.name, local_name, message)
                if not answer:

                    # *** Бармену есть что сказать?
                    answer = await self.barman.barman(room.name, local_name, message)
                if not answer:

                    # *** Игруну есть что сказать?
                    answer = self.gambler.gambler(room.name, message)
                if not answer:

                    # *** Хайдзину есть что сказать?
                    answer = await self.haijin.haijin(room.name, local_name, event.sender, message)
                if not answer:

                    # *** Библиотекарю есть что сказать?
                    answer = await self.librarian.librarian(room.name, local_name,
                                                            event.sender, message)
                if not answer:

                    # *** Мажордому есть что сказать?
                    answer = await self.majordomo.majordomo(room.name, message)
                if not answer:

                    # *** Менеджеру есть что сказать?
                    answer = await self.manager.manager(room.name, room.room_id,
                                                        event.sender, message)
                if not answer:

                    # *** Метеорологу есть что сказать?
                    answer = await self.meteorolog.meteorolog(room.name, message)
                if not answer:

                    # *** Модератору есть что сказать?
                    answer = await self.moderator.moderator(room.name, message,
                                                            local_name, event.sender)
                if not answer:

                    # *** Звездочёту есть что сказать?
                    answer = await self.stargazer.stargazer(room.name, message)
                if not answer:

                    # *** Статистику есть что сказать?
                    answer = await self.statistic.statistic(room.room_id, room.name,
                                                            event.sender, message)
                if not answer:

                    # *** Теологу есть что сказать?
                    answer = await self.theolog.theolog(room.name, message)
                # *** Коллектор вызывается последним.
                if not answer:

                    # *** Коллектору есть что сказать?
                    answer = self.collector.collector(answer)
            else:

                # *** Просто сообщение
                answer = await self.moderator.control_talking(room, event, local_name)
                if not answer:

                    answer, file_name = await self.babbler.talk(room.name, message)
                    if file_name:

                        self.send_jpg(room.room_id, file_name)
            if answer:

                if answer != self.last_message:

                    await send_text_to_room(self.client, room.room_id, answer.strip(), False, False)
                    self.last_message = answer
        return


    async def invite(self, room: MatrixRoom, event: InviteMemberEvent) -> None:
        """Callback for when an invite is received. Join the room specified in the invite.
        Args:
            room: The room that we are invited to.
            event: The invite event.
        """
        logger.debug(f"Got invite to {room.room_id} from {event.sender}.")

        # Attempt to join 3 times before giving up
        for attempt in range(3):

            result = await self.client.join(room.room_id)
            if isinstance(result, JoinError):

                logger.error(
                    f"Error joining room {room.room_id} (attempt %d): %s",
                    attempt,
                    result.message,
                )
            else:

                break
        else:

            logger.error("Unable to join room: %s", room.room_id)

        # Successfully joined room
        logger.info(f"Joined {room.room_id}")


    def send_hints(self, pchat_title: str) -> str:
        """Проверяет, не была ли запрошена подсказка."""

        # *** Собираем ответы модулей на запрос помощи
        answer: str = ""
        result: str = self.barman.get_hint(pchat_title)
        if result:

            answer += result + "\n"
        result = self.gambler.get_hint(pchat_title)
        if result:

            answer += result + "\n"
        result = self.haijin.get_hint(pchat_title)
        if result:

            answer += result + "\n"
        result = self.librarian.get_hint(pchat_title)
        if result:

            answer += result + "\n"
        result = self.majordomo.get_hint(pchat_title)
        if result:

            answer += result + "\n"
        result = self.meteorolog.get_hint(pchat_title)
        if result:

            answer += result + "\n"
        result = self.stargazer.get_hint(pchat_title)
        if result:

            answer += result + "\n"
        result = self.statistic.get_hint(pchat_title)
        if result:

            answer += result + "\n"
        result = self.theolog.get_hint(pchat_title)
        if result:

            answer += result + "\n"
        if answer:

            return HELP_MESSAGE + answer
        return answer


    async def invite_event_filtered_callback(
        self, room: MatrixRoom, event: InviteMemberEvent
    ) -> None:
        """
        Since the InviteMemberEvent is fired for every m.room.member state received
        in a sync response's `rooms.invite` section, we will receive some that are
        not actually our own invite event (such as the inviter's membership).
        This makes sure we only call `callbacks.invite` with our own invite events.
        """
        if event.state_key == self.client.user_id:
            # This is our own membership (invite) event
            await self.invite(room, event)


    async def _reaction(
        self, room: MatrixRoom, event: UnknownEvent, reacted_to_id: str
    ) -> None:
        """A reaction was sent to one of our messages. Let's send a reply acknowledging it.

        Args:
            room: The room the reaction was sent in.

            event: The reaction event.

            reacted_to_id: The event ID that the reaction points to.
        """
        logger.debug(f"Got reaction to {room.room_id} from {event.sender}.") # noqa

        # Get the original event that was reacted to
        event_response = await self.client.room_get_event(room.room_id, reacted_to_id)
        if isinstance(event_response, RoomGetEventError):
            logger.warning(
                "Error getting event that was reacted to (%s)", reacted_to_id
            )
            return
        reacted_to_event = event_response.event

        # Only acknowledge reactions to events that we sent
        if reacted_to_event.sender != self.config.user_id:
            return

        # Send a message acknowledging the reaction
        reaction_sender_pill = make_pill(event.sender)
        reaction_content = (
            event.source.get("content", {}).get("m.relates_to", {}).get("key")
        )
        message = (
            f"{reaction_sender_pill} reacted to this event with `{reaction_content}`!"
        )
        await send_text_to_room(
            self.client,
            room.room_id,
            message,
            reply_to_event_id=reacted_to_id,
        )


    async def decryption_failure(self, room: MatrixRoom, event: MegolmEvent) -> None:
        """Callback for when an event fails to decrypt. Inform the user.

        Args:
            room: The room that the event that we were unable to decrypt is in.

            event: The encrypted event that we were unable to decrypt.
        """
        logger.error(
            f"Failed to decrypt event '{event.event_id}' in room '{room.room_id}'!"
            f"\n\n"
            f"Tip: try using a different device ID in your config file and restart."
            f"\n\n"
            f"If all else fails, delete your store directory and let the bot recreate "
            f"it (your reminders will NOT be deleted, but the bot may respond to existing "
            f"commands a second time)."
        ) # noqa

        red_x_and_lock_emoji = "❌ 🔐"

        # React to the undecryptable event with some emoji
        await react_to_event(
            self.client,
            room.room_id,
            event.event_id,
            red_x_and_lock_emoji,
        )


    async def unknown(self, room: MatrixRoom, event: UnknownEvent) -> None:
        """Callback for when an event with a type that is unknown to matrix-nio is received.
        Currently this is used for reaction events, which are not yet part of a released
        matrix spec (and are thus unknown to nio).

        Args:
            room: The room the reaction was sent in.

            event: The event itself.
        """
        if event.type == "m.reaction":
            # Get the ID of the event this was a reaction to
            relation_dict = event.source.get("content", {}).get("m.relates_to", {})

            reacted_to = relation_dict.get("event_id")
            if reacted_to and relation_dict.get("rel_type") == "m.annotation":
                await self._reaction(room, event, reacted_to)
                return

        logger.debug(
            f"Got unknown event with type to {event.type} from {event.sender} in {room.room_id}."
        ) # noqa


    async def get_display_name_in_room(self, room_id: str, user_id: str) -> str:
        """ Функция возвращает локальное имя пользователя в заданной комнате. """

        assert room_id is not None, \
            "Assert: [callbacks.get_display_name_in_room] No <room_id> parameter specified!"
        assert user_id is not None, \
            "Assert: [callbacks.get_display_name_in_room] No <user_id> parameter specified!"

        fallback_name = user_id.split(":")[0][1:]
        # pylint: disable=broad-exception-caught
        try:

            state_resp = await self.client.room_get_state_event(room_id, "m.room.member", user_id)
            if hasattr(state_resp, 'content') and isinstance(state_resp.content, dict):

                # Пробуем все возможные ключи, которые использует Matrix
                local_name = (
                    state_resp.content.get("displayname") or
                    state_resp.content.get("display_name")
                )
                if local_name:

                    return local_name
        except Exception as e:
            print(f"[DEBUG] Ошибка запроса state: {e}")

        # Fallback
        return fallback_name


    async def send_jpg(self, proom_id: str, pimage: str):
        """Функция отправляет заданный JPG файл в заданную комнату"""

        # Получаем размеры изображения и вес файла
        with Image.open(pimage) as img:

            width, height = img.size
        file_size = os.path.getsize(pimage)

        # 1. Загружаем файл на медиа-сервер Matrix
        with open(pimage, "rb") as f:

            resp, _ = await self.client.upload(
                f,
                content_type="image/jpeg",
                filename=os.path.basename(pimage),
                filesize=file_size,
            )
        if isinstance(resp, UploadResponse):

            # 2. Отправляем событие m.image в комнату
            content = {

                "body": os.path.basename(pimage),
                "info": {
                    "size": file_size,
                    "mimetype": "image/jpeg",
                    "w": width,
                    "h": height,
                },
                "msgtype": "m.image",
                "url": resp.content_uri,  # mxc:// ссылка с сервера
            }
            await self.client.room_send(
                room_id=proom_id,
                message_type="m.room.message",
                content=content
            )
