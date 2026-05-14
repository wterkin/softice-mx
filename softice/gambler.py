# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Игровой модуль."""

import random
from softice import basis


UNIT_ID: str = "gambler"
HINT: tuple = ("игры", "games")

COMMANDS: tuple = (("камень", "кам"),
                   ("ножницы", "нож"),
                   ("бумага", "бум"),
                   ("ящерица", "ящер"),
                   ("спок", "спок"),
                   ("монета", "coin"),
                   ("игры", "games"))
DESCRIPTIONS: tuple = ("камень - вы выбираете игровой жест 'камень', 👊🏻",
                       "ножницы - вы выбираете игровой жест 'ножницы', ✌🏻",
                       "бумага - вы выбираете игровой жест 'бумага', ✋🏻",
                       "ящерица - вы выбираете игровой жест 'ящерица', 🦎",
                       "спок - вы выбираете игровой жест 'спок', 🖖🏻",
                       "монета - вы выбрали подбросить монету"
                      )


ROCK_COMMANDS: int = 0
SCISSORS_COMMANDS: int = 1
PAPER_COMMANDS: int = 2
LIZARD_COMMANDS: int = 3
SPOCK_COMMANDS: int = 4
COIN_COMMANDS: int = 5
HINT_COMMANDS: int = 6

EMODJIES: tuple = ("👊🏻", "✌🏻", "✋🏻", "🦎", "🖖🏻")
THUMBS_UP: str = "👍🏻"
THUMBS_DOWN: str = "👎🏻"


class CGambler(basis.CBasis):
    """Класс игрока."""

    def __init__(self, pconfig):

        super().__init__(pconfig)
        print("Игрун стартовал.")


    def can_process_command(self, pchat_title: str, pmessage: str,  punit_id: str = "",
                    pcommands: list = None) -> bool:

        assert pchat_title is not None, \
            "Assert: [gambler.can_class_process] " \
            "Пропущен параметр <pchat_title> !"
        assert pmessage is not None, \
            "Assert: [gambler.can_class_process] " \
            "Пропущен параметр <pmessage> !"

        # rint(f"+++ Gmb +++ cpc +++ {COMMANDS=}")
        return super().can_process_command(pchat_title, pmessage, UNIT_ID, COMMANDS)


    def get_commands(self, pchat_title: str, punit_id: str="", pdescriptions: list=None) -> str:
        """Пользователь запросил список команд."""

        assert pchat_title is not None, \
            "Assert: [gambler.get_command] " \
            "Пропущен параметр <pchat_title> !"

        # rint(f"+++ Gmb +++ gc +++")
        return super().get_commands(pchat_title, UNIT_ID, DESCRIPTIONS)


    def get_hint(self, pchat_title: str, punit_id: str = "", phints: str = "") -> str:
        """Возвращает список команд, поддерживаемых модулем.  """

        assert pchat_title is not None, \
            "Assert: [gambler.get_hint] " \
            "Пропущен параметр <pchat_title> !"

        return super().get_hint(pchat_title, UNIT_ID, COMMANDS[HINT_COMMANDS])


    async def reload(self):
        """Пустая заглушка."""


    def rock_scissors_paper_lizard_spock(self, pcommand: int):
        """Камень-ножницы-бумага."""

        answer = f"Ваш выбор {EMODJIES[pcommand]} {COMMANDS[pcommand][0]}\n"
        turn = random.randint(0,4)
        if pcommand == turn:

            answer += (f"Я выбрал также {EMODJIES[turn]}"
                       #f"{ROCKSCIPAPLIZSPOCK_COMMANDS[turn]}. Ничья. 🤝")
                       f"{COMMANDS[turn][0]}. Ничья. 🤝")
        else:

            answer += f"Я выбираю {EMODJIES[turn]} {COMMANDS[turn][0]}."
            if turn == ROCK_COMMANDS:

                if pcommand == SCISSORS_COMMANDS:

                    answer += f" Камень тупит ножницы. Вы проиграли. {THUMBS_DOWN}"
                elif pcommand == PAPER_COMMANDS:

                    answer += f" Бумага обёртывает камень. Вы выиграли. {THUMBS_UP}"
                elif pcommand == LIZARD_COMMANDS:

                    answer += f" Камень давит ящерицу. Вы проиграли. {THUMBS_DOWN}"
                elif pcommand == SPOCK_COMMANDS:

                    answer += f" Спок испаряет камень. Вы выиграли. {THUMBS_UP}"

            elif turn == SCISSORS_COMMANDS:

                if pcommand == ROCK_COMMANDS:

                    answer += f" Камень тупит ножницы. Вы выиграли. {THUMBS_UP}"
                elif pcommand == PAPER_COMMANDS:

                    answer += f" Ножницы режут бумагу. Вы проиграли. {THUMBS_DOWN}"
                elif pcommand == LIZARD_COMMANDS:

                    answer += f" Ножницы убивают ящерицу. Вы проиграли. {THUMBS_DOWN}"
                elif pcommand == SPOCK_COMMANDS:

                    answer += f" Спок ломает ножницы. Вы выиграли. {THUMBS_UP}"

            elif turn == PAPER_COMMANDS:

                if pcommand == ROCK_COMMANDS:

                    answer += f" Бумага обёртывает камень. Вы проиграли. {THUMBS_DOWN}"
                elif pcommand == SCISSORS_COMMANDS:

                    answer += f" Ножницы режут бумагу. Вы выиграли. {THUMBS_UP}"
                elif pcommand == LIZARD_COMMANDS:

                    answer += f" Ящерица съедает бумагу. Вы выиграли. {THUMBS_UP}"
                elif pcommand == SPOCK_COMMANDS:

                    answer += f" Бумага обвиняет Спока. Вы проиграли. {THUMBS_DOWN}"

            elif turn == LIZARD_COMMANDS:

                if pcommand == ROCK_COMMANDS:

                    answer += f" Камень давит ящерицу. Вы выиграли. {THUMBS_UP}"
                elif pcommand == SCISSORS_COMMANDS:

                    answer += f" Ножницы убивают ящерицу. Вы выиграли. {THUMBS_UP}"
                elif pcommand == PAPER_COMMANDS:

                    answer += f" Ящерица съедает бумагу. Вы проиграли. {THUMBS_DOWN}"
                elif pcommand == SPOCK_COMMANDS:

                    answer += f" Ящерица кусает Спока. Вы проиграли. {THUMBS_DOWN}"

            elif turn == SPOCK_COMMANDS:

                if pcommand == ROCK_COMMANDS:

                    answer += f" Спок испаряет камень. Вы проиграли. {THUMBS_DOWN}"
                elif pcommand == SCISSORS_COMMANDS:

                    answer += f" Спок ломает ножницы. Вы проиграли. {THUMBS_DOWN}"
                elif pcommand == PAPER_COMMANDS:

                    answer += f" Бумага обвиняет Спока. Вы выиграли. {THUMBS_UP}"
                elif pcommand == LIZARD_COMMANDS:

                    answer += f" Ящерица кусает Спока. Вы выиграли. {THUMBS_UP}"

        return answer


    def gambler(self, pchat_title, pmessage_text: str):
        """Основной метод класса."""

        answer: str = ""
        word_list: list = self.parse_input(pmessage_text)
        # if self.can_class_process(pchat_title, pmessage_text):
        # rint("+++ Gmb +++ gmbl +++ ")

        if self.can_process_command(pchat_title, pmessage_text):

            # *** Получим код команды
            command: int = self.identify_command(word_list[0], COMMANDS)
            if ROCK_COMMANDS <= command <= SPOCK_COMMANDS:

                #answer = self.rock_scissors_paper_lizard_spock(COMMANDS.index(word_list[0]))
                answer = self.rock_scissors_paper_lizard_spock(command)
            elif command == COIN_COMMANDS:

                answer = self.throw_coin()
            elif command == HINT_COMMANDS:

                answer = self.get_commands(pchat_title)
            else:

                answer = "Я не знаю такой игры"
            if answer:

                print("> Gambler отвечает: ", answer[:basis.OUT_MSG_LOG_LEN])

        return answer

    def throw_coin(self):
        """Орёл или решка."""
        answer: str = ""
        turn: int = random.randint(0,99)
        if turn % 2 == 0:

            answer =  "Выпала решка"
        else:

            answer = "Выпал орёл"
        return answer
