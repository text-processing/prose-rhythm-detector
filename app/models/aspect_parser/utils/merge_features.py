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


""" This module describes merging two or more Features """

from itertools import chain

from models.feature import Feature


def merge_features(*features) -> Feature:
    """
    Merges two or more Features of one type into one

    :param features: list of features to merge
    :returns: Feature
    """
    feature_type = features[0].type()
    context_start = min(feature.context_begin() for feature in features)
    context_end = max(feature.context_end() for feature in features)
    words = sorted(chain.from_iterable(diac.words() for diac in features))
    return Feature(feature_type=feature_type, context=[context_start, context_end], words=words)
