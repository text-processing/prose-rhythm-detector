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


# pylint: disable=R0903
"""
Statistic controller
"""

from models.statistic_aspect import StatisticAspect


class StatisticController:
    """
    Controller that manipulate with statistic
    """

    def __init__(self):
        self.aspects = {}

    def form_aspect_statistic(self, feature_list_original):
        """
        Form statistic for every aspect from feature lists
        :param feature_list_original: list of features of original text
        :param feature_list_translate: list of features of translated text
        """
        self.aspects = {}
        for feature in feature_list_original:
            if feature.type not in self.aspects:
                self.aspects[feature.type] = StatisticAspect(feature.type)
            self.aspects[feature.type].original_count = self.aspects[feature.type].original_count + 1
