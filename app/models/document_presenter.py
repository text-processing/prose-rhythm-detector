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

from functools import reduce


class DocumentPresenter:
    """ Class for specific representations of Document for GUI needs """

    SENTENCE_SEP = " "
    CHAPTER_SEP = "\n\n"
    TITLE_ENDING = '\n'

    def __init__(self, document):
        self.__document = document
        sentences = reduce(lambda x, y: x + y, document.words_list)
        self.all_words = list(reduce(lambda x, y: x + y, sentences))
        self.words_positions = self.__calculate_words_positions(self.__document)

    def get_text(self):
        return self.CHAPTER_SEP.join(chapter.title + self.TITLE_ENDING +
                                     self.SENTENCE_SEP.join(sentence.text for sentence in chapter)
                                     for chapter in self.__document.chapters)

    def as_one_list(self):
        return self.all_words

    def word_by_index(self, index):
        """
        :return: word at index
        """
        return self.all_words[index]

    def words_by_indexes(self, indexes: list):
        """
        :return: list of words by indexes
        """
        return [self.word_by_index(index) for index in indexes]

    def words_from_to(self, begin: int, end: int):
        """
        :return: a fragment of the text by params
        """
        return self.words_by_indexes(list(range(begin, end + 1)))

    def word_start(self, word_index):
        """ number of characters before word with given index """
        return self.words_positions[word_index][0]

    def word_length(self, word_index):
        """ length of word with given index """
        return len(self.all_words[word_index])

    def word_end(self, word_index):
        """ number of characters before end of word with given index (including word's last
        character """
        return self.words_positions[word_index][1]

    def __calculate_words_positions(self, document):
        result = []
        offset = 0
        for chapter in document.chapters:
            offset += len(chapter.title + self.TITLE_ENDING)
            for i_s, sentence in enumerate(chapter.sentences):
                for i_w, word in enumerate(sentence.model.words):
                    if word.pos not in {"PUNCT", "SYM"}:
                        start, end = word.parent.start_char, word.parent.end_char
                        result.append((start + offset, end + offset))
            offset += len(chapter.model.text.strip() + self.CHAPTER_SEP)
        return result
