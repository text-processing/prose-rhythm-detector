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

""" This module describes chiasmus finder """
from functools import partial

from models.feature import Feature


class ChiasmusFinder:

    def __init__(self, document):
        self.is_stop_word = partial(document.is_stop_word, 'chiasmus')
        self._features = []
        self.word_counter = 0
        for chapter in document:
            self.__find_inside_chapter(chapter)

    def __find_inside_chapter(self, chapter):
        for sentence_ix in range(len(chapter.sentences) - 1):
            self.__find_between_sentences(chapter[sentence_ix], chapter[sentence_ix + 1])
            self.word_counter += len(chapter[sentence_ix])

    def __find_between_sentences(self, first_sentence, second_sentence):
        if first_sentence[0] == second_sentence[-1] and first_sentence[-1] == second_sentence[0]:
            self._features.append(Feature('chiasmus',
                                          [self.word_counter, self.word_counter + len(first_sentence) - 1,
                                           self.word_counter + len(first_sentence),
                                           self.word_counter + len(first_sentence) + len(second_sentence) - 1],
                                          [self.word_counter,
                                           self.word_counter + len(first_sentence) + len(second_sentence) - 1]))

    @property
    def features(self):
        return self._features


def find(document) -> list:
    """
    :param document: document to find chiasmus in
    :return: list of chiasmus in given document
    """
    return ChiasmusFinder(document).features
