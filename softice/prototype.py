#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль прототипа классов модулей бота."""

from abc import ABCMeta, abstractmethod  # , abstractproperty


class CPrototype:
    """Прототип классов модулей бота.. """
    __metaclass__ = ABCMeta

    def __init__(self, pconfig):
        pass


    @abstractmethod
    def can_process(self, pchat_title: str, punit_id: str,
                    pmessage_text: str, pcommands: list) -> bool:
        """Возвращает True, если модуль может обработать команду."""


    @abstractmethod
    def get_commands(self, pchat_title: str, punit_id: str, pcommands: list) -> str:
        """Возвращает список команд модуля, доступных пользователю."""


    @abstractmethod
    def get_hint(self, pchat_title: str, punit_id: str, phints: str) -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""


    @abstractmethod
    def identify_command(self, pword: str, pcommands : list) -> int:  # noqa
        """Распознает команду и возвращает её код, в случае неудачи  -1."""


    @abstractmethod
    def is_enabled(self, pchat_title: str, punit_id: str) -> bool:
        """Возвращает True, если на этом канале этот модуль разрешен."""


    @abstractmethod
    def is_master(self, puser_name: str) -> bool:
        """Проверяет, хозяин ли отдал команду."""


    @abstractmethod
    def load_from_file(self, pfile_name: str) -> list:
        """Загружает текстовый файл в список строк."""


    @abstractmethod
    def save_to_file(self, plist: list, pfile_name: str): # noqa
        """Сохраняет список строк в текстовый файл, """\
        """если файл с таким именем уже есть - переименовывает его."""


    @abstractmethod
    async def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""

    @abstractmethod
    def parse_input(self, pmessage_text: str) -> list:
        """Разбивает введённую строку на отдельные слова."""
