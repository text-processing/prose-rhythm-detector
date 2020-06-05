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


"""
Model of FeatureListItem
"""
from PySide2.QtWidgets import QListWidgetItem

from models.feature import Feature


class FeatureListItem(QListWidgetItem):
    """
    Class describes a feature.
    """

    def __get_aspect_string(self, document):
        words = ""
        if self.__aspect.type() == "anaphora":
            anaphora_indexes = list()
            for word_index in self.__aspect.words():
                anaphora_indexes.append(word_index)
            words = " ".join(document.words_by_indexes(sorted(anaphora_indexes)))
        else:
            for word_index in self.__aspect.words():
                words += document.word_by_index(word_index) + " "
        context = " ".join(document.words_from_to(self.__aspect.context_begin(), self.__aspect.context_end()))
        return "".join(words.strip() + "\n" + context.strip())

    def aspect(self) -> Feature:
        """ :return: the Feature model"""
        return self.__aspect

    def __init__(self, aspect, document):
        self.__aspect = aspect
        super(FeatureListItem, self).__init__(self.__get_aspect_string(document))
