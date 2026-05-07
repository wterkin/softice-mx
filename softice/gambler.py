# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Игровой модуль."""

import random
from softice import basis


UNIT_ID: str = "gambler"
HINT: tuple = ("игры", "games")
ROCKSCIPAP_COMMANDS: tuple = ("камень", "ножницы", "бумага")
ROCKSCIPAP_SHORT_COMMANDS: tuple = ("кам", "нож", "бум")
ROCKSCIPAPLIZSPOCK_COMMANDS: tuple = ("камень", "ножницы", "бумага", "ящерица", "спок")
ROCKSCIPAPLIZSPOCK_SHORT_COMMANDS: tuple = ("кам", "нож", "бум", "ящер", "спок")
THROW_COIN_COMMANDS: tuple = ("монета", "coin")
ROCK_COMMAND: int = 0
SCISSORS_COMMAND: int = 1
PAPER_COMMAND: int = 2
LIZARD_COMMAND: int = 3
SPOCK_COMMAND: int = 4

EMODJIES: tuple = ("👊🏻", "✌🏻", "✋🏻", "🦎", "🖖🏻")
THUMBS_UP: str = "👍🏻"
THUMBS_DOWN: str = "👎🏻"


class CGambler(basis.CBasis):
    """Класс игрока."""

    def __init__(self, pconfig):

        super().__init__(pconfig)
        print("Игрун стартовал.")

    def can_class_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если игрок может обработать эту команду."""

        assert pchat_title is not None, \
            "Assert: [gambler.can_class_process] " \
            "Пропущен параметр <pchat_title> !"
        assert pmessage_text is not None, \
            "Assert: [gambler.can_class_process] " \
            "Пропущен параметр <pmessage_text> !"
        found: bool = False
        if self.is_enabled(pchat_title, UNIT_ID):

            word_list: list = self.parse_input(pmessage_text)
            for command in ROCKSCIPAPLIZSPOCK_COMMANDS:

                found = word_list[0] in command
                if found:

                    break
            if not found:

                for command in ROCKSCIPAPLIZSPOCK_SHORT_COMMANDS:

                    found = word_list[0] in command
                    if found:

                        break
            if not found:

                for command in THROW_COIN_COMMANDS:

                    found = word_list[0] in command
                    # print(f"** gmb:cnprc: {word_list[0]=} {command=} {found=}")
                    #print(f" {command} {word_list[0]} {found}")
                    if found:

                        break
            if not found:

                found = word_list[0] in HINT
        # print(f"** gmb:cnprc: {found=}")
        return found

    def get_help(self, pchat_title: str) -> str:
        """Пользователь запросил список команд."""

        assert pchat_title is not None, \
            "Assert: [gambler.get_help] " \
            "No <pchat_title> parameter specified!"
        command_list: str = ""
        if self.is_enabled(pchat_title, UNIT_ID):

            command_list += ", ".join(ROCKSCIPAPLIZSPOCK_COMMANDS)+"\n"
            command_list += ", ".join(THROW_COIN_COMMANDS)
        return command_list


    def get_hint(self, pchat_title: str, punit_id: str = "", phints: str = "") -> str:
        """Возвращает список команд, поддерживаемых модулем.  """

        assert pchat_title is not None, \
            "Assert: [gambler.get_hint] " \
            "Пропущен параметр <pchat_title> !"
        return super().get_hint(pchat_title, UNIT_ID, HINT)


    async def reload(self):
        """Пустая заглушка."""

    def rock_scissors_paper(self, pcommand: int):
        """Камень-ножницы-бумага."""

        answer = f"Ваш выбор {EMODJIES[pcommand]} {ROCKSCIPAP_COMMANDS[pcommand]}\n"
        turn = random.randint(0,2)
        if pcommand == turn:

            answer += f"Я выбрал также {EMODJIES[turn]}{ROCKSCIPAP_COMMANDS[turn]}. Ничья. 🤝"
        else:

            answer += f"Я выбираю {EMODJIES[turn]} {ROCKSCIPAP_COMMANDS[turn]}."
            if turn == ROCK_COMMAND:

                # *** Камень
                if pcommand == SCISSORS_COMMAND:

                    answer += " Камень тупит ножницы. Вы проиграли. 👎🏻"
                else:

                    answer += " Бумага обёртывает камень. Вы выиграли. 👍🏻"
            elif turn == SCISSORS_COMMAND:

                # *** Ножницы
                if pcommand == PAPER_COMMAND:

                    answer +=  " Ножницы режут бумагу. Вы проиграли. 👎🏻"
                else:

                    answer += " Камень тупит ножницы. Вы выиграли. 👍🏻"
            else:

                # *** Бумага.
                if pcommand == ROCK_COMMAND:

                    answer +=  " Бумага обёртывает камень. Вы проиграли. 👎🏻"
                else:

                    answer += " Ножницы режут бумагу. Вы выиграли. 👍🏻"
        return answer


    def rock_scissors_paper_lizard_spock(self, pcommand: int):
        """Камень-ножницы-бумага."""

        answer = f"Ваш выбор {EMODJIES[pcommand]} {ROCKSCIPAPLIZSPOCK_COMMANDS[pcommand]}\n"
        turn = random.randint(0,4)
        if pcommand == turn:

            answer += (f"Я выбрал также {EMODJIES[turn]}"
                       f"{ROCKSCIPAPLIZSPOCK_COMMANDS[turn]}. Ничья. 🤝")
        else:

            answer += f"Я выбираю {EMODJIES[turn]} {ROCKSCIPAPLIZSPOCK_COMMANDS[turn]}."
            if turn == ROCK_COMMAND:

                if pcommand == SCISSORS_COMMAND:

                    answer += f" Камень тупит ножницы. Вы проиграли. {THUMBS_DOWN}"
                elif pcommand == PAPER_COMMAND:

                    answer += f" Бумага обёртывает камень. Вы выиграли. {THUMBS_UP}"
                elif pcommand == LIZARD_COMMAND:

                    answer += f" Камень давит ящерицу. Вы проиграли. {THUMBS_DOWN}"
                elif pcommand == SPOCK_COMMAND:

                    answer += f" Спок испаряет камень. Вы выиграли. {THUMBS_UP}"

            elif turn == SCISSORS_COMMAND:

                if pcommand == ROCK_COMMAND:

                    answer += f" Камень тупит ножницы. Вы выиграли. {THUMBS_UP}"
                elif pcommand == PAPER_COMMAND:

                    answer += f" Ножницы режут бумагу. Вы проиграли. {THUMBS_DOWN}"
                elif pcommand == LIZARD_COMMAND:

                    answer += f" Ножницы убивают ящерицу. Вы проиграли. {THUMBS_DOWN}"
                elif pcommand == SPOCK_COMMAND:

                    answer += f" Спок ломает ножницы. Вы выиграли. {THUMBS_UP}"

            elif turn == PAPER_COMMAND:

                if pcommand == ROCK_COMMAND:

                    answer += f" Бумага обёртывает камень. Вы проиграли. {THUMBS_DOWN}"
                elif pcommand == SCISSORS_COMMAND:

                    answer += f" Ножницы режут бумагу. Вы выиграли. {THUMBS_UP}"
                elif pcommand == LIZARD_COMMAND:

                    answer += f" Ящерица съедает бумагу. Вы выиграли. {THUMBS_UP}"
                elif pcommand == SPOCK_COMMAND:

                    answer += f" Бумага обвиняет Спока. Вы проиграли. {THUMBS_DOWN}"

            elif turn == LIZARD_COMMAND:

                if pcommand == ROCK_COMMAND:

                    answer += f" Камень давит ящерицу. Вы выиграли. {THUMBS_UP}"
                elif pcommand == SCISSORS_COMMAND:

                    answer += f" Ножницы убивают ящерицу. Вы выиграли. {THUMBS_UP}"
                elif pcommand == PAPER_COMMAND:

                    answer += f" Ящерица съедает бумагу. Вы проиграли. {THUMBS_DOWN}"
                elif pcommand == SPOCK_COMMAND:

                    answer += f" Ящерица кусает Спока. Вы проиграли. {THUMBS_DOWN}"

            elif turn == SPOCK_COMMAND:

                if pcommand == ROCK_COMMAND:

                    answer += f" Спок испаряет камень. Вы проиграли. {THUMBS_DOWN}"
                elif pcommand == SCISSORS_COMMAND:

                    answer += f" Спок ломает ножницы. Вы проиграли. {THUMBS_DOWN}"
                elif pcommand == PAPER_COMMAND:

                    answer += f" Бумага обвиняет Спока. Вы выиграли. {THUMBS_UP}"
                elif pcommand == LIZARD_COMMAND:

                    answer += f" Ящерица кусает Спока. Вы выиграли. {THUMBS_UP}"

        return answer


    def gambler(self, pchat_title, pmessage_text: str):
        """Основной метод класса."""

        answer: str = ""
        word_list: list = self.parse_input(pmessage_text)
        if self.can_class_process(pchat_title, pmessage_text):

            if word_list[0] in HINT:

                answer = self.get_help(pchat_title)
            else:

                # *** Получим код команды
                if word_list[0] in ROCKSCIPAPLIZSPOCK_COMMANDS:

                    answer = self.rock_scissors_paper_lizard_spock( \
                             ROCKSCIPAPLIZSPOCK_COMMANDS.index(word_list[0]))
                elif word_list[0] in ROCKSCIPAPLIZSPOCK_SHORT_COMMANDS:

                    answer = self.rock_scissors_paper_lizard_spock( \
                             ROCKSCIPAPLIZSPOCK_SHORT_COMMANDS.index(word_list[0]))
                elif word_list[0] in THROW_COIN_COMMANDS:

                    answer = self.throw_coin()
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
