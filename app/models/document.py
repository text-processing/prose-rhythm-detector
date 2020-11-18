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

"""
This module describes document
"""
from collections import defaultdict
from copy import deepcopy
from functools import reduce
from operator import or_


VERSION = 1.2


class Document:
    """
    Program representation of text in natural language.
    Contains list of Chapter objects and some additional information.
    """

    def __init__(self, chapters, lang, features=None, stop_words=None):
        self.chapters = chapters
        self.lang = lang
        self.features = features if features else []
        self.stop_words = stop_words if stop_words else defaultdict(dict)
        self.version = VERSION

    def set_stop_words(self, stop_words: dict):
        """ Set the specified stop words to the document """
        self.stop_words = deepcopy(stop_words)

    # Interface
    @property
    def words_list(self):
        """ :return document as list of chapters as list of sentences as list of words """
        return [chapter.words_list for chapter in self.chapters]

    def __as_one_list(self):
        sentences = reduce(lambda x, y: x + y, self.words_list)
        return reduce(lambda x, y: x + y, sentences)

    def feature_types(self):
        """
        :return: list with all types of the features in the document
        """
        return list({feature.type() for feature in self.features})

    def features_with_type(self, feature_type):
        """
        :return: list of features with the specified type
        """
        return list(filter(lambda x: x.type() == feature_type, self.features))

    def features_with_type_and_transcription(self, feature_type, transcription):
        """
        :return: list of features with the specified type and transcription
        """
        return list(filter(lambda x: x.type() == feature_type and x.transcription == transcription, self.features))

    def word_by_index(self, index):
        """
        :return: word at index
        """
        return self.__as_one_list()[index]

    def __getitem__(self, key):
        return self.chapters[key]

    def is_stop_word(self, feature: str, word: str):
        """
        :param feature: feature to test stop word to
        :param word: word from text
        :return: is word is stop word for feature
        """
        if feature in self.stop_words.keys():
            stop_words = reduce(or_, [set(i) for i in self.stop_words[feature].values()])
        else:
            stop_words = reduce(or_, [set(i) for i in self.stop_words['anaphora'].values()])
        return word in stop_words

    def __len__(self):
        return sum(len(chapter) for chapter in self.chapters)

    def __str__(self):
        return "[" + "\n".join(str(chapter) for chapter in self.chapters) + "]"
