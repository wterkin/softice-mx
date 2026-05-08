#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль прототипа классов модулей бота."""

import asyncio
import os
from datetime import datetime as dtime
from softice import prototype

BACKSLASH: str = "\\"
OUT_MSG_LOG_LEN = 60
MESSAGE_NOT_FOUND: str = "Извините, по вашему запросу ничего не найдено"


class CBasis(prototype.CPrototype):
    """Базовый класс для классов модулей бота.. """

    def __init__(self, pconfig):
        self.config = pconfig


    def can_process(self, pchat_title: str, punit_id: str,
                    pmessage_text: str, pcommands: list) -> bool:
        """Возвращает True, если модуль может обработать команду."""
        assert pchat_title is not None, \
            "Assert: [CBasis.can_process] Пропущен параметр <pchat_title> !"
        assert punit_id is not None, \
            "Assert: [CBasis.can_process] Пропущен параметр <punit_id> !"
        assert pmessage_text is not None, \
            "Assert: [CBasis.can_process] Пропущен параметр <pmessage_text> !"

        found: bool = False
        # rint(f"+++ Bas +++ 1 +++ {pchat_title=}")
        # rint(f"+++ Bas +++ 2 +++ {punit_id=}")
        if self.is_enabled(pchat_title, punit_id):

            word_list: list = self.parse_input(pmessage_text)
            # rint(f"+++ Bas +++ 2 +++ {word_list=}")
            for command in pcommands:

                # rint(f"+++ Bas +++ 2 +++ {word_list[0]=}")
                # rint(f"+++ Bas +++ 2 +++ {command=}")
                found = word_list[0] == command
                # rint(f"+++ Bas +++ 3 +++ {found=}")
                if found:

                    break
        return found



    def can_process_command(self, proom_name: str, pmessage: str, 
                            punit_id: str, pcommands: list) -> bool:
        """Возвращает True, если хайдзин может обработать эту команду."""

        assert proom_name is not None, \
            "Assert: [haijin.can_class_process] " \
            "Пропущен параметр <proom_name> !"
        assert pmessage is not None, \
            "Assert: [haijin.can_class_process] " \
            "Пропущен параметр <pmessage> !"

        can_process: bool = False
        # *** Мы можем обрабатывать команды из этой комнаты?
        if self.is_enabled(proom_name, punit_id):
        
            # *** Парсим сообщение
            word_list: list = self.parse_input(pmessage)
            for command in pcommands:
            
                can_process = word_list[0] in command
                if can_process:
                    
                    break
        return can_process

    
    def get_commands(self, pchat_title: str, punit_id: str, pdescriptions: list) -> str:
        """Пользователь запросил список команд."""

        assert pchat_title is not None, \
            "Assert: [haijin.get_command] " \
            "Пропущен параметр <pchat_title> !"

        commands: str = ""
        
        if self.is_enabled(pchat_title, punit_id):

            for command in pdescriptions:

                commands += command + "\n"
        return commands


    def get_hint(self, pchat_title: str, punit_id: str, phints: str) -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""

        assert pchat_title is not None, \
            "Assert: [basis.get_hint] " \
            "Пропущен параметр <pchat_title> !"
        assert punit_id is not None, \
            "Assert: [basis.get_hint] " \
            "Пропущен параметр <punit_id> !"
        assert phints is not None, \
            "Assert: [basis.get_hint] " \
            "Пропущен параметр <phints> !"

        if self.is_enabled(pchat_title, punit_id):

            return ", ".join(phints)
        return ""




    def identify_command(self, pword: str, pcommands : list) -> int:  # noqa
        """Распознает команду и возвращает её код, в случае неудачи  -1."""

        assert pword is not None, \
            "Assert: [CBasis.identify_command] " \
            "No <pword> parameter specified!"
        assert pcommands is not None, \
            "Assert: [CBasis.identify_command] " \
            "No <pcommands> parameter specified!"

        result: int = -1
        for command_idx, command in enumerate(pcommands):

            if pword in command:

                result = command_idx
                break
        return result


    def is_enabled(self, pchat_title: str, punit_id: str) -> bool:
        """Возвращает True, если в этом чате даный модуль разрешен."""

        assert pchat_title is not None, \
            "Assert: [CBasis.is_enabled] Пропущен параметр <pchat_title> !"
        assert punit_id is not None, \
            "Assert: [CBasis.is_enabled] Пропущен параметр <punit_id> !"

        if pchat_title in self.config.chats:

            return punit_id in self.config.chats[pchat_title]
        return False


    def is_master(self, puser_name: str) -> bool:
        """Проверяет, хозяин ли отдал команду."""
        assert puser_name is not None, \
            "Assert: [CBasis.is_master] Пропущен параметр <puser_name> !"

        return puser_name == self.config.master


    async def load_from_file_async(self, pfile_name):
        """Асинхронная обёртка через потоки."""

        # *** Патч для питона 3.8.2
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.load_from_file, pfile_name)
        # return await asyncio.to_thread(self.load_from_file, pfile_name)
        # return await self.load_from_file, pfile_name



    def load_from_file(self, pfile_name: str) -> list:

        assert pfile_name is not None, \
            "Assert: [CBasis.load_from_file] Пропущен параметр <pfile_name> !"

        content: list = []
        # *** откроем файл
        try:

            with open(pfile_name, encoding="utf8") as text_file:

                # *** читаем в список
                for line in text_file:

                    if line:

                        content.append(line.strip())
        except FileNotFoundError:

            return content
        return content


    def parse_nick(self, pnick: str) -> str:
        """Вытаскивает из полного адреса имя пользователя и капитализирует его."""
        nick: str = pnick.split(":")[0]
        if nick[0] == "@":
            nick = nick[1:]
        return nick.capitalize()

    async def save_to_file_async(self, plist: list, pfile_name: str):
        """Асинхронное сохранение списка в файл."""

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.save_to_file, plist, pfile_name)


    def save_to_file(self, plist: list, pfile_name: str): # noqa
        """Сохраняет список строк в текстовый файл, если файл с таким именем уже есть""" \
        """ - переименовывает его."""

        assert plist is not None, \
            "Assert: [CBasis.save_to_file] Пропущен параметр <plist> !"
        assert pfile_name is not None, \
            "Assert: [CBasis.save_to_file] Пропущен параметр <pfile_name> !"

        new_file_name: str = f"{pfile_name}_{dtime.now().strftime('%Y%m%d-%H%M%S')}"
        if os.path.exists(pfile_name):

            os.rename(pfile_name, new_file_name)
        with open(pfile_name, "w", encoding="utf8") as out_file:

            for line in plist:

                out_file.write(line + "\n")


    def parse_input(self, pmessage_text: str) -> list:
        """Разбивает введённую строку на отдельные слова."""

        assert pmessage_text is not None, \
            "Assert: [CBasis.parse_input] Пропущен параметр <pmessage_text> !"

        #: list = []
        # if pmessage_text is not None:
        return pmessage_text[1:].strip().split(" ")
        # return answer


    async def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""        
