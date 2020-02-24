""""
ProseRhythmDetector - the tool for extraction of rhythm features.
    Copyright (C) 2020  Vladislav Larionov, Vladislav Petryakov, Anatoly Poletaev, Ksenia Lagutina, Alla Manakhova, Nadezhda Lagutina, Elena Boychuk.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    
    The corresponding author: Ksenia Lagutina, lagutinakv@mail.ru
"""


# pylint: disable=too-few-public-methods
""" This module describes aspect parser """

from models.aspect_parser.parsers import anaphora_parser, anadiplosis_parser, polysyndeton_parser, epiphora_parser, \
    symploce_parser, diacope_parser, epizeuxis_parser, epanalepsis_parser


class AspectParser:
    """ Class describes Aspect Parser """

    def __init__(self, document):
        self.__document = document

    def parse_anaphora(self) -> list:
        """
        Parses anaphora from the document

        :return: list with anaphora (list of Feature objects)
        """
        return anaphora_parser.parse(self.__document)

    def parse_anadiplosis(self) -> list:
        """
        Parses anadiplosis from the document

        :return: list with anadiplosis (list of Feature objects)
        """
        return anadiplosis_parser.parse(self.__document)

    def parse_polysyndeton(self) -> list:
        """
        Parses polysyndeton from the document

        :return: list with polysyndeton (list of Feature objects)
        """
        return polysyndeton_parser.parse(self.__document)

    def parse_epiphora(self) -> list:
        """
        Parses epistrophe from the document

        :return: list with epistrophe (list of Feature objects)
        """
        return epiphora_parser.parse(self.__document)

    @staticmethod
    def parse_symploce(anaphoras: list, epistrophas: list) -> list:
        """
        Parses symploce from the document

        :param anaphoras: list with anaphora found in the document
        :param epistrophas: list with epistrophas found in the document
        :return: list with symploce (list of Feature objects)
        """
        return symploce_parser.parse(anaphoras, epistrophas)

    def parse_recurring_sentence_parts_features(self) -> list:
        """
        Parses recurring sentence parts features (anaphora, epistrophe and symploce) from the document

        :return: list with anaphora, epistrophe and symploce
        """
        anaphoras = self.parse_anaphora()
        epiphoras = self.parse_epiphora()
        symploces = self.parse_symploce(anaphoras, epiphoras)
        return anaphoras + epiphoras + symploces

    def parse_epizeuxis(self) -> list:
        """
        Parses epizeuxis from the document

        :return: list with epizeuxis (Feature objects)
        """
        return epizeuxis_parser.parse(self.__document)

    def parse_diacope(self) -> list:
        """
        Parses diacope from the document

        :return: list with diacope (Feature objects)
        """
        return diacope_parser.parse(self.__document)

    def parse_epanalepsis(self) -> list:
        """
        Parses epanalepsis from the document

        :return: list with epanalepsis (Feature objects)
        """
        return epanalepsis_parser.parse(self.__document)
