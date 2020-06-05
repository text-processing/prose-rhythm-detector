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


# pylint: disable=too-few-public-methods
"""
Model of feature
"""


class Feature:
    """
    Class describes a feature.
    """

    def __init__(self, feature_type: str, words: list = None, context: list = None):
        """
        :param feature_type: the type of feature (anaphora, simple repeat, etc)
        :param words: the list of words that uses in feature
        :param context: the list that displays interval of that feature
        """
        if words is None:
            words = list()
        if context is None:
            context = list()
        self.__type = feature_type.lower()
        self.__words = words
        self.__context = context

    def word_at_index(self, index: int):
        """ :return word at index"""
        if not self.__words:
            return None
        return self.__words[index]

    def words_length(self):
        """ :return number of the words in this aspect"""
        return len(self.__words)

    def words(self):
        """ iterator for the words in the feature"""
        for index in self.__words:
            yield index

    def last_word(self):
        """ :return last word in this aspect. None if there are no words"""
        if self.__words:
            return self.__words[-1]
        return None

    def has_word(self, word):
        """ :return True if feature words contain specified word. False else. """
        return word in self.__words

    def has_context_index(self, index):
        """ :return True if feature context indexes contain specified index. False else. """
        return index in self.__context

    def add_context(self, index_begin, index_end):
        """ Adds context"""
        self.__context.append(index_begin)
        self.__context.append(index_end)

    def extend_context(self, new_end):
        """
            Replace right border of context with new border
            :param: new_end - new right border
        """
        self.__context.pop()
        self.__context.append(new_end)

    def context_index_length(self):
        """ :return count of the indexes in context"""
        return len(self.__context)

    def add_word(self, index):
        """ Adds word"""
        self.__words.append(index)

    def type(self):
        """ :return the feature type"""
        return self.__type

    def context_begin(self):
        """ :return the first value of the context or None if context is empty"""
        if self.__context:
            return self.__context[0]
        return None

    def context_end(self):
        """ :return the last value of the context or None if context is empty"""
        if self.__context:
            return self.__context[len(self.__context) - 1]
        return None

    def __str__(self):
        return "Aspect: {name}\nWords: {words}\nContext: {context}" \
            .format(name=self.__type, words=self.__words, context=self.__context)

    def to_hash(self):
        """ :return representation of the aspect in hash"""
        return dict(type=self.__type, words=self.__words, context=self.__context)

    def __eq__(self, other):
        if not isinstance(other, Feature):
            return False

        if not self.__type == other.type():
            return False

        if not (self.words_length() == other.words_length()
                or self.context_index_length() == other.context_index_length()):
            return False

        for word in self.__words:
            if not other.has_word(word):
                return False

        for context in self.__context:
            if not other.has_context_index(context):
                return False
        return True
