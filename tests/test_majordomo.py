from unittest import TestCase
import json
from sys import platform

import softice
from softice import majordomo
from softice import config
import asyncio

class CMfjordomo(TestCase):

    def setUp(self) -> None:

        self.config = config.Config("test_config.yaml")
        self.majordomo: majordomo.CMajordomo = majordomo.CMajordomo(self.config)


    def test_majordomo(self):

        asyncio.run(self.majordomo.reload())
        answer = asyncio.run(self.majordomo.majordomo("Ботовка", "!gt"))
        self.assertEqual(answer, "")
        result="Привет, Namo, вот и ты. Проходи, располагайся. Сейчас чейку бахнем ;)"
        answer = asyncio.run(self.majordomo.majordomo("Ботовка","!gt Namo"))
        
        self.assertEqual(answer, result)
