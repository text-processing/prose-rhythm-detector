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


""" This module describes symploce parser """
from models.aspect_parser.utils.context_intersection import context_intersection
from models.feature import Feature


def parse(anaphoras: list, epistrophas: list) -> list:
    """
    Parses symploce from the specified document

    :param anaphoras: list with anaphoras
    :param epistrophas: list with epistrophas
    :return: list with epistrophe (Feature objects)
    """
    res = list()
    for anaphora in anaphoras:
        for epistrophe in epistrophas:
            intersection = context_intersection(anaphora, epistrophe)
            if intersection:
                inter_start, inter_end = intersection
                anaphora_words = [word for word in anaphora.words() if inter_start <= word <= inter_end]
                epistrophe_words = [word for word in epistrophe.words() if inter_start <= word <= inter_end]
                if anaphora_words and epistrophe_words:
                    if anaphora_words[-1] > epistrophe_words[0]:
                        res.append(Feature("symploce", words=sorted(anaphora_words + epistrophe_words),
                                           context=intersection))
    return res
