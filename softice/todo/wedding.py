"""
Юмористическая игра 'Мафия' для Telegram.
Использует pyTelegramBotAPI (telebot).
"""
# pylint: disable=pointless-string-statement
"""
Краткое описание игры
В игре принимают участие от 4 человек до 20
Игра представляет собой свадьбу. На свадьбе присутствуют положительные
персонажи - Жених, Невеста, Гость, Свекровь, Тамада, Подружка Невесты,
Бабушка и Свидетель. Им весело, они хотят провести свадьбу так, чтобы никто
и ничто этому не помешало. Но на свадьбе присутствуют и отрицательные
персонажи - Буян, Тёща, Подруга Тёщи, Дедушка-склерозник и Тесть. Они
хотят сорвать свадьбу и начистить физиономию жениху, что приведет к
отмене свадьбы. Также на свадьбе присутствуют и нейтральные персонажи -
Клоун, Гость с Юга, Хулиганка (она же подружка невесты), Непьющий Гость
и Забулдыга. Если отрицательные персонажи удалены со свадьбы, или их
осталось в 2 раза меньше положительных - свадьба удалась. Если
положительных персонажей не осталось, или осталось в 2 раза меньше,
чем отрицательных, свадьба сорвана. Если жениху начистили физиономию
Буяны, Забулдыга или Тёща попала в него закруткой - свадьба провалена.

*** Положительные персонажи
(4) Жених - может только голосовать днём, ночью неактивен. [0]
(4) Невеста - телохранитель жениха. Может играть ночью и голосовать днём. [1]
                Цель игры - найти жениха. Если нашла и на него нападают,
                жених остаётся жив и невеста палит нападающего. Нельзя
                охранять жениха два хода подряд
              Начало действия: Невеста задержалась в дверях, подумала и
                                 достала из стола увесистый кастет.
                                 Жениха защитить - дело нелёгкое.
                               Невеста накинула куртку и посмотрела, на месте
                                 ли перцовый баллончик. Если она не защитит
                                 Жениха - кто тогда?
                               Невеста подошла к шкафу и вытащила из ящика
                                 здоровенный шокер. Защита Женихов - самое
                                 важное дело, тут мелочей не бывает.
              Конец действия -:  В эту ночь никто не пытался убить Жениха.
                                  Ну и ладно.
                             +: {Subject} лежал неподвижно и только слегка
                                  постанывал. А нечего тут на Жениха наезжать.
                                  Невеста узнала его - это был {Role}
              Атакует: того, кто атакует Жениха
(4) Гость - может только голосовать днём. Ночью неактивен. [2]
(5) Свекровь - Может играть ночью и голосовать днём. Если выбирает персонажа, [3]
               которого выбрали и отрицательные - выполняет функцию доктора,
               поит пострадавшего рассолом и тот оживает.
	           Начало действия: Свекровь взяла бинт, зелёнку, банку рассола и
                                  пошла на поиски страждущих.
                                Свекровь услышала крики о помощи и поспешила
                                  помогать.
                                Свекровь услышала в коридоре какой-то
                                  кипиш и решила, что её помощь пригодится.
               Конец действия -: В эту ночь помощь Свекрови никому не
                                   пригодилась.
                              +: Свекровь подошла к бесчувственному телу
                                   {Subject} и сделала ему непрямой масссаж
                                   сердца. Тело задышало и зашевелилось.
              Атакует всех, подвергшихся атаке
(7) Тамада -  Может играть ночью и голосовать днём. Его цель - спасти свадьбу. [4]
              Ищет отрицательных персонажей и вышибает со свадьбы.
              Начало действия: Тамада вышел из комнаты и пошел на звук драки.
                                 - Сейчас кто-то у нас огребёт - подумал он
                                 мрачно.
                               Тамада взял фонарик, бейсбольную биту, и пошел
                                 на ночную вахту. Мало ли что случится.
                               Тамада услышал крик в ночи и пошел посмотреть,
                                 что, собственно, случилось.
	      Конец действия -: Эта ночь для Тамады прошла спокойно
                             +: Этой ночью Тамаде пришлось поработать - он
                                 разоблачил {Subject} как {Role} и
                                 выкинул его со свадьбы.
              Атакует отрицательных персонажей
(9) Подружка невесты - Может играть ночью и голосовать днём. Выводит из строя
                         выбранного персонажа на одну ночь.
                       Начало действия: Подружка невесты ищет себе компанб

(11) Бабушка - Может играть ночью и голосовать днём. Даёт выбранному персонажу
                 иммунитет на эту ночь. Никто его не сможет успешно атаковать.
                 Ходит через раз.
               Начало действия: Бабуля выходит из своей комнатушки и начинает
                                  искать, кто там еще бродит и нарывается на
                                  мордобой.
                                Бабуля в полной темноте ищет бедолагу,
                                  которого нужно срочно спасти.
               Конец действия -: Бабуля бродила всю ночь, но так никого и не
                                   нашла..
                              +: Бабуле сегодня подфартило, она поймала
                                   {Subject} и помогла ему дойти туда, куда
                                   он направлялся, без всяких неприятностей.

              Атакует - всех
(13) Свидетель – Может играть ночью и голосовать днём. Наблюдает за игроками
                   ночью, может один раз за ночь проверить, кто противник.
                 Начало действия: Свидетель заснул за столом, а когда жажда
                                    стала совсем невыносима, стал искать кран,
                                    и всю ночь бродил по дому.
                                  Свидетеля разбудил чей-то отчаянный крик,
                                    заснуть он уже не смог и пошел искать,
                                    кто это орал, где и почему.
                                  Свидетель увидел во сне маму, проснулся
                                    и стал искать телефон, чтобы позвонить ей.
                 Конец действия -: Свидетель блуждал по дому, пока сон не
                                   сморил его.
                                +: Свидетел в своих блужданиях по дому
                                    случайно увидел {Subject}. Да он же
                                    {Role}, догадался свидетель.
                 Атакует всех
*** Отрицательные персонажи
(4) Буян - Может играть ночью и голосовать днём. Жаждет начистить физиономию
             жениху и сорвать свадьбу.
           Начало действия: Буян пошел искать ненавистного Жениха
                            Буян пошел искать Жениха. Ну или Тамаду на
                              крайняк.
                            Буян пошел искать хоть кого-нибудь, на ком
                              можно выместить злобу.
           Конец действия -: Буян блуждал по дому до глубокой ночи,
                               но так никого и не встретил
                          +: Буяну попался {Subject}, лицо которого было
                               с удовольствием набито.
           Атакует всех, кроме Буянов
(6) Тёща - Может играть ночью и голосовать днём. Кидается закатками. очень
             опасна. одно попадание и человеку уже не до свадьбы, он выбывает
           Начало действия: Тёща вооружилась двумя литровыми банками
                              маринованных огурцов и отправилась искать
                              заплутавших гостей.
                            Тёща отправилась на поиски Жениха, ну или Гостя.
                              Для верности она прихватила с собой трёхлитровую
                              баночку маринованных помидоров. Пощады не будет.
                            В глухую полночь Тёщу понесло за приключениями.
                              В руке у неё была зажата поллитровая баночка
                              маринованных грибков. Убойное оружие.
           Атакует Положительных персонажей
(8) Подруга тёщи - Может играть ночью и голосовать днём. Разведчик врага.
                   Начало действия: Подруга тёщи на цыпочках вышла из своей
                                      комнаты и пошла подслушивать,
                                      подглядывать и заниматься прочей
                                      разведдеятельностью
                   Конец действия: Подруга тёщи подслушала интереснейший
                                     разговор о {Subject}, из которого узнала,
                                     что он - {Role}
                   Атакует: Положительных персонажей
(10) Дедушка-склерозник - Может играть ночью и голосовать днём. выводит из
       строя персонажа на 2 ночи (рассказывает ему всякую чепуху). Играет
       через раз.
(12) Тесть - адвокат. Может играть ночью и голосовать днём. Защищает отрицательных персонажей.
       Играет через раз

*** Нейтральные персонажи
(14) Клоун - Может играть ночью и голосовать днём. Приходит в гости к кому угодно
             и отвлекает его, мешая ему выполнять задания
             Начало действия: Клоун решил сегодня устроить маленький кошмар…
	                      Клоун достал красный нос и готовит сюрприз...
                              Клоун сегодня приготовил для гостей что-то интересное.
	     Конец действия +: Клоун поймал {Subject} и до утра развлекал его своими ужимками
             Атакует всех.

(15) Гость с Юга - Может играть ночью и голосовать днём. при каждом ходе с вероятностью 1/3
       может раскрыть роль игрока
(16) Хулиганка – Может играть ночью и голосовать днём. поит персонажа, к которому приходит,
        и тот путает цель.
(17) Непьющий Гость - Может играть ночью и голосовать днём. Желает уйти со свадьбы и делает всё,
         чтоб его заподозрили в принадлежности к Буянам
(18) Забулдыга - Может играть ночью и голосовать днём. Незваный гость. Пристает ко всем и бьёт
       им... лица
"""
# pylint: disable=wrong-import-position
import logging
from enum import Enum
from typing import Dict, List, Optional
from telebot import TeleBot
from telebot.types import Message

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Role(Enum):
    """Роли игроков."""
    GROOM = "жених"
    BRIDE = "невеста"
    GUEST = "гость"
    KIND_MOTHER_IN_LAW = "свекровь"
    TOASTMASTER = "тамада"
    BRAWLER = "буян"
    EVIL_MOTHER_IN_LAW = "тёща"
    CLOWN = "клоун"

# *** Константы ролей
ROLES_TOTAL: int = 17
UNASSIGNED: int = 0
GROOM: int = 1  # Жених +
BRIDE: int = 2  # Невеста +
GUEST: int = 3  # Гость +
KIND_MIL: int = 4  # Свекровь +
TOASTMASTER: int = 5  # Тамада +
BRIDESMAID: int = 6  # Подружка невесты +
GRANDMOTHER: int = 7  # Бабушка +
WITNESS: int = 8  # Свидетель +
BRAWLER: int = 9 # Буян
EVIL_MIL: int = 10  # Тёща +
EVIL_MIL_MAID: int = 11  # Подруга тёщи +
GRANDFATHER: int = 12  # Дедушка +
CLOWN: int = 13  # Клоун +
SOUTHGUEST: int = 14  # Гость с юга +
BULLYMAIDEN: int = 15  # Хулиганка +
ABSTAINER: int = 16  # Трезвенник
DRUNKARD: int = 17  # Алкаш - забулдыга +

DARK_SIDE_ROLES: int = -1
NEUTRAL_ROLES: int = 0
LIGHT_SIDE_ROLES: int = 1

INACTIVE_ROLE: int = 0
ACTIVE_ROLE: int = 1
SPY: bool = True
SIMPLE: bool = False


PROP_ROLE_NAME: int = 0
PROP_ACTIVITY: int = 1
PROP_SIDE: int = 2
PROP_PLAYERS_COUNT:int = 3
PROP_SPY: int = 4
PROP_QUESTION: int = 5

ROLES: tuple = (("Не определено", INACTIVE_ROLE, NEUTRAL_ROLES, 4, SIMPLE,""),
                ("Жених", INACTIVE_ROLE, LIGHT_SIDE_ROLES, 4, SIMPLE, ""),
                ("Невеста", ACTIVE_ROLE, LIGHT_SIDE_ROLES, 4, SPY, "Кого проверим?"),
                ("Гость", INACTIVE_ROLE, LIGHT_SIDE_ROLES, 4, SIMPLE, ""),
                ("Свекровь", ACTIVE_ROLE, LIGHT_SIDE_ROLES, 8, SIMPLE, "Кого полечим?"),
                ("Тамада", ACTIVE_ROLE, LIGHT_SIDE_ROLES, 6, SPY, "Кого защитим?"),
                ("Подружка невесты", ACTIVE_ROLE, NEUTRAL_ROLES, 9, SIMPLE, "Кого заморочим?"),
                ("Бабушка", ACTIVE_ROLE, NEUTRAL_ROLES, 11, SIMPLE, "Кого защитим?"),
                ("Свидетель", ACTIVE_ROLE, LIGHT_SIDE_ROLES, 10, SPY, "К кому наведаемся?"),
                ("Буян", ACTIVE_ROLE, DARK_SIDE_ROLES, 4, SIMPLE, "Кого побьём?"),
                ("Тёща", ACTIVE_ROLE, DARK_SIDE_ROLES, 5, SIMPLE, "Кого покалечим?"),
                ("Подруга тёщи", ACTIVE_ROLE, DARK_SIDE_ROLES, 12, SPY, "К кому пойдём шпионить?"),
                ("Дедушка", ACTIVE_ROLE, NEUTRAL_ROLES, 13, SIMPLE, "Кому голову задурим?"),
                ("Клоун", ACTIVE_ROLE, NEUTRAL_ROLES, 14, SIMPLE, "Кого повеселим?"),
                ("Гость с юга", ACTIVE_ROLE, NEUTRAL_ROLES, 16, SPY, "К кому пойдём на разведку?"),
                ("Хулиганка", ACTIVE_ROLE, DARK_SIDE_ROLES, 7, SIMPLE, "Кого напоим?"),
                ("Трезвенник", INACTIVE_ROLE, NEUTRAL_ROLES, 17, SIMPLE, ""),
                ("Забулдыга", ACTIVE_ROLE, DARK_SIDE_ROLES, 15, SIMPLE, "Кому лицо набьём?")
               )

class CPlayer:
    """Игрок в игре."""

    def __init__(self, user_id: int, name: str):

        self.user_id: int = user_id
        self.name: str = name
        self.role: int = UNASSIGNED
        self.is_alive: bool = True
        # self.is_voted_out = False  # для шута

    def __repr__(self):
        return f"<Player {self.name} ({self.user_id})>"


class CGameState(Enum):
    """Состояния игры."""
    LOBBY = "набор игроков"
    NIGHT = "ночь"
    DAY = "день"
    VOTING = "голосование"
    FINISHED = "игра окончена"


class CMafiaGame:
    """
    Основной класс игры 'Мафия'.
    Управляет состоянием, игроками, ночными/дневными действиями.
    """

    def __init__(self, bot: TeleBot, chat_id: int):

        self.bot: Telebot = bot
        self.chat_id: int = chat_id
        # self.players: Dict[int, CPlayer] = {}  # user_id -> Player
        self.players: list = []
        self.state: CGameState = CGameState.LOBBY
        self.round_number: int = 0 # N раунда
        self.roles_issued: list = []

        # *** Ночные цели активных персонажей
        self.night_targets: dict

        logger.info(f"Новая игра создана в чате {chat_id}")

    def add_player(self, user_id: int, name: str) -> bool:
        """Добавить игрока в игру."""

        # *** Если игра не в состоянии набора игроков - не принимаем
        if self.state != CGameState.LOBBY:

            return False
        # *** Если игрок уже в игре - не принимаем
        for player in self.players:

            if player.id == user_id:

                return False
        # *** Добавляем нового игрока в список
        self.players.append(Player(user_id, name))
        logger.info(f"Игрок {name} присоединился")
        return True

    def start_game(self) -> bool:
        """Начать игру: раздать роли, отправить приветственные сообщения."""
        # *** Если игра не в состоянии набора игроков или игроков меньше трёх - не проканывает
        if self.state != CGameState.LOBBY or len(self.players) < 3:

            return False
        # *** Распределяем роли
        self._assign_roles()
        # *** Переходим в режим ночи
        self.state = CGameState.NIGHT
        self.round_number = 1

        # *** Отправим каждому игроку его роль
        for player in self.players:

            # *** Если игрок живой
            if player.is_alive:

                self.bot.send_message(player.user_id,
                                      f"Твоя роль: *{player.role.value}*!\n"
                                      f"Игра началась в чате {self.chat_id}.",
                                      parse_mode="Markdown"
                                     )
        # *** Переходим к ночной игре
        self._start_night_phase()
        return True

    def _assign_roles(self):
        """Раздать роли. Пример: 1 мафия, 1 шериф, остальные — мирные (+ шут при >=5)."""

        # *** Создаём список игроков
        #players_list = list(self.players.values())
        players_count = len(players_list)
        # self.night
        # *** Всем игрокам присваиваем нераспределённую роль
        for role in range(0, players_count+1):

            roles_issued.append(UNASSIGNED)
        # *** Список индексов ролей, доступных при данном количестве игроков
        roles: list
        # *** Заполняем этот список индексами доступных ролей
        """
        for role in players_count:

           if ROLES[role][1] <= players_count:

               roles.append(ROLES_BY_PLAYERS[role][0])
        """
        for roleindex, role in enumeration(ROLES):

            if role[PROP_PLAYERS_COUNT] <= players_count:

                roles.append(roleindex)

        # *** Раздаём роли
        from random import shuffle
        shuffle(roles)
        for index, player in enumerate(self.players):

            player.role = roles[index]


    def _start_night_phase(self):
        """Начать ночную фазу: отправить инструкции ролям."""

        self.bot.send_message(self.chat_id, (" Наступает ночь... Все засыпают, "
                                             "но некоторые товарищи не спят..."))

        # *** Формируем списки для атак
        light_players: list = []
        all_players: list = []
        for player in self.players:

            # *** Если игрок жив...
            if player.is_alive:

                all_players.append(player)
                # *** Если игрок на светлой стороне..
                if ROLES[player.role][PROP_SIDE] == LIGHT_SIDE_ROLES:

                    light_players.append(player)
        # *** Ходы персонажей
        for player in self.players:

            # *** Если игрок жив..
            if player.is_alive:

                # *** Если игрок на тёмной стороне..
                if ROLE[player.role][PROP_SIDE] == DARK_SIDE_ROLES:

                    # *** атакуем светлых
                    self._send_target_selection(player, ROLE[player.role][PROP_QUESTION],
                                                light_players)
                else:

                    # *** атакуем всех
                    self._send_target_selection(player, ROLE[player.role][PROP_QUESTION],
                                                all_players)


    def _send_target_selection(self, player: Player, text: str, callback, players: list):
        """Отправить игроку список целей для выбора."""
        #live_players = [p for p in self.players.values() if p.is_alive and
        # p.user_id != player.user_id]
        #f not alive_players:
        #    return

        buttons = "\n".join([f"/choose_{pl.user_id} — {pl.name}" for pl in players])
        msg = f"{text}\n\n{buttons}"
        self.bot.send_message(player.user_id, msg)

        # Здесь можно сохранить callback по user_id для обработки /choose_*
        # Для простоты — обработка будет в основном хендлере бота

   # --- Обработчики действий (вызываются извне) ---
    def handle_mafia_choice(self, mafia_id: int, target_id: int):
        if self.state == CGameState.NIGHT and self.players[mafia_id].role == Role.MAFIA:
            self.mafia_target = target_id
    def handle_sheriff_choice(self, sheriff_id: int, target_id: int):
        if self.state == CGameState.NIGHT and self.players[sheriff_id].role == Role.SHERIFF:
            self.sheriff_check = target_id
    def handle_doctor_choice(self, doctor_id: int, target_id: int):
        if self.state == CGameState.NIGHT and self.players[doctor_id].role == Role.DOCTOR:
            self.doctor_heal = target_id

    def process_night_actions(self):
        """Обработать результаты ночи."""

        # *** Разведчики получают инфу
        for player in self.playeers:

            if player.is_alive:

                if ROLES[player.role][PROP_SPY]:

                    target_role = self.players[self.sheriff_check].role
                    self.bot.send_message(player.user_id,
                    f" {self.players[self.sheriff_check].name} — {target_role.value}")
         # Мафия убивает (если не вылечен)
        if self.mafia_target and self.mafia_target in self.players:
            victim = self.players[self.mafia_target]
            if self.doctor_heal != self.mafia_target:
                victim.is_alive = False
                self.bot.send_message(self.chat_id, f" Утром найден труп {victim.name}!")
            else:
                self.bot.send_message(self.chat_id, " Чудо! Никто не погиб этой ночью!")
        # Сбросить действия
        self.mafia_target = None
        self.sheriff_check = None
        self.doctor_heal = None

        # Проверка победы
        if self._check_win():
            return

        self.state = CGameState.DAY
        self.bot.send_message(self.chat_id, " Наступает день. Обсуждение!")

    def _check_win(self) -> bool:
        """Проверить, есть ли победитель."""
        alive = [p for p in self.players.values() if p.is_alive]
        mafia = [p for p in alive if p.role == Role.MAFIA]
        civilians = [p for p in alive if p.role != Role.MAFIA]
        if not mafia:
            self.bot.send_message(self.chat_id, " Мирные жители победили!")
            self.state = CGameState.FINISHED
            return True
        if len(mafia) >= len(civilians):
            self.bot.send_message(self.chat_id, " Мафия захватила город!")
            self.state = CGameState.FINISHED
            return True
        return False

    def start_voting(self):
        """Начать голосование за изгнание."""
        if self.state != CGameState.DAY:
            return
        self.state = CGameState.VOTING
        self.bot.send_message(self.chat_id, " Кого выгоним из города?")

        # Здесь можно реализовать систему голосования
        # Например, через команды /vote_user123

    def end_game(self):
        """Завершить игру."""
        self.state = CGameState.FINISHED
        self.bot.send_message(self.chat_id, "Игра окончена. Спасибо за участие!")

# --- Пример использования в основном боте ---
if __name__ == "__main__":
    # Это только для демонстрации — в реальном проекте импортируйте класс
    print("Этот модуль предназначен для импорта в основной бот.")
