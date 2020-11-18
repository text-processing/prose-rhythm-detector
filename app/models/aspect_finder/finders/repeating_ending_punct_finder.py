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

""" This module finds repeating sentence ending punctuation """
from models.feature import Feature


class RepeatingEndingPunctFinder:
    """ Finder for sentences which ends with similar punctuation symbols """

    def __init__(self, document, endings_to_find: set, feature_name: str):
        self.doc = document
        self.endings = endings_to_find
        self._word_count = 0
        self.features = []
        self.feature_name = feature_name

    def find(self):
        """ Finds repeating sentences with initialized ending
        (found Features objects could be accessed via `features` attribute"""
        self._word_count = 0
        self.features.clear()
        for chapter in self.doc.chapters:
            self.__find_inside_chapter(chapter)

    def __find_inside_chapter(self, chapter):
        self.__reset_pointers()
        for sentence in chapter.sentences:
            if sentence.ending_punct in self.endings:
                if self._feature_start is None:
                    self._feature_start = self._word_count
                else:
                    self._in_repetition = True
            else:
                self.__add_feature_if_exists()
            self._word_count += len(sentence)
        self.__add_feature_if_exists()

    def __add_feature_if_exists(self):
        if self._in_repetition:
            self.features.append(Feature(self.feature_name,
                                         context=[self._feature_start,
                                                  self._word_count - 1]))
        self.__reset_pointers()

    def __reset_pointers(self):
        self._feature_start, self._in_repetition = None, False
