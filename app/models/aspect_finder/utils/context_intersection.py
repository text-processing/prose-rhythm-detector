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

""" This module describes context intersection between two Features """

from models.feature import Feature


def context_intersection(first: Feature, second: Feature) -> list:
    """
    Returns context intersection between two features

    :param first: first feature
    :param second: second feature
    :return: context intersection
    """
    first_beg, first_end = first.context_begin(), first.context_end()
    second_beg, second_end = second.context_begin(), second.context_end()
    if first_beg > second_end or second_beg > first_end:
        return []
    return [max(first_beg, second_beg), min(first_end, second_end)]
