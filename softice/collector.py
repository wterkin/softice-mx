# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль выпрашивания пожертвований ;) """

from datetime import datetime
from random import randint

from softice import basis


UNIT_ID = "collector"
WORK_HOURS: tuple = (12, 13, 14, 15, 16, 17, 18)
PROBABILITY: int = 16
CHANCE_VALUE: int = 8
DONATE_MESSAGE: str = ("\n\nНравится SoftIce? Поддержи проект! Пожертвуй 56 рублей,"
                       "этих денег хватит на неделю содержания бота, это очень просто: \n"
                       "https://yoomoney.ru/to/41001510609674/51")


class CCollector(basis.CBasis):
    """Класс сборщика пожертвований"""

    def __init__(self, pconfig):

        assert pconfig is not None, \
        "Assert: [CCollector.__init__] " \
        "Пропущен параметр <pconfig> !"

        super().__init__(pconfig)
        print("Коллектор стартовал.")


    def collector(self, panswer: str) -> str:
        """Функция будет в определенные часы просить пожертвований."""

        assert panswer is not None, \
        "Assert: [CCollector.__init__] " \
        "Пропущен параметр <panswer> !"

        # *** Время рабочее?
        just_now = datetime.now()
        if just_now.hour in WORK_HOURS:

            # *** Запросим случайное число
            chance: int = randint(1, PROBABILITY)
            if chance == CHANCE_VALUE:

                # *** Сформируем ответ
                panswer = panswer + DONATE_MESSAGE
        return panswer


    async def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""
