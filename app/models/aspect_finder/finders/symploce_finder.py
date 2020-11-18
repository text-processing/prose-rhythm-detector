""""
ProseRhythmDetector - the tool for extraction of rhythm features and computation of stylometric features for texts.
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

""" This module describes symploce finder """
from models.aspect_finder.utils.context_intersection import context_intersection
from models.feature import Feature


def find(anaphoras: list, epiphoras: list) -> list:
    """
    Finds symploce between previously found anaphoras and epiphoras

    :param anaphoras: list with anaphoras
    :param epiphoras: list with epiphoras
    :return: list with symploces (Feature objects)
    """
    res = list()
    for anaphora in anaphoras:
        for epiphora in epiphoras:
            intersection = context_intersection(anaphora, epiphora)
            if intersection:
                inter_start, inter_end = intersection
                anaphora_words = [word for word in anaphora.words() if inter_start <= word <= inter_end]
                epiphora_words = [word for word in epiphora.words() if inter_start <= word <= inter_end]
                if anaphora_words and epiphora_words:
                    if anaphora_words[-1] > epiphora_words[0]:
                        res.append(Feature("symploce", words=sorted(anaphora_words + epiphora_words),
                                           context=intersection))
    return res
