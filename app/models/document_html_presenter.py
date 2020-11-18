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

from models.document_presenter import DocumentPresenter
from models.feature import Feature


class DocumentHtmlPresenter(DocumentPresenter):
    """ Class represents a Document object as a HTML document """

    SENTENCE_SEP = " "
    CHAPTER_SEP = "<br><br>"
    TITLE_ENDING = '<br>'
    ASPECT_COLORS = {
        'anaphora': '#c876a7',
        'epiphora': '#007C7C',
        'anadiplosis': '#df5b05',
        'diacope': '#7448ff',
        'polysyndeton': '#ff2400',
        'symploce': '#0072c0',
        'epizeuxis': '#88b04b',
        'epanalepsis': '#52b0ae',
        'chiasmus': '#18e1ff',
        'assonance': '#d40bb2',
        'alliteration': '#229f07',
        'aposiopesis': '#0bda51',
        'repeating exclamatory sentences': '#deaa88',
        'repeating interrogative sentences': '#deaf88'
    }

    def __init__(self, document):
        super().__init__(document)
        self.tag_length = len(self.__generate_html_tag('', '#000000'))

    def get_text_with_highlighted_aspects(self, aspects: list):
        """ :return: text with wrapped aspects in colorized html tags """
        aspect_words = self.__aspects_to_word_dict(aspects)
        offset = 0
        text = self.get_text()
        for word_index in sorted(aspect_words.keys()):
            tag = self.__word_to_colorized_html_tag(text[self.word_start(word_index) + offset:
                                                         self.word_end(word_index) + offset],
                                                    aspect_words[word_index])
            text = "".join((text[:self.word_start(word_index) + offset],
                            tag,
                            text[self.word_end(word_index) + offset:]))
            offset += self.__compute_offset(aspect_words[word_index])
        return text

    @classmethod
    def __aspects_to_word_dict(cls, aspects: list) -> dict:
        """
        :return: representation of aspects as a hash with format:
        word_index: {aspect_type: str, sound: {symbol_index: type}}
        """
        aspect_words = dict()
        for aspect in aspects:
            if aspect.type() not in Feature.PHONETIC_TYPES:
                for word in aspect.words():
                    if word not in aspect_words:
                        aspect_words[word] = {'type': None, 'sound': dict()}
                    aspect_words[word]['type'] = aspect.type()
            else:
                for word, sound_indexes in aspect.letters():
                    if word not in aspect_words:
                        aspect_words[word] = {'type': None, 'sound': dict()}
                    for symbol in sound_indexes:
                        aspect_words[word]['sound'][symbol] = dict()
                        aspect_words[word]['sound'][symbol]['type'] = aspect.type()
        return aspect_words

    def __word_to_colorized_html_tag(self, word, word_info: dict) -> str:
        """ :return: html tag of word with all sounds """
        colorized_word = ''
        for index in range(len(word)):
            if index in word_info['sound']:
                colorized_word += self.__generate_html_tag(word[index],
                                                           self.ASPECT_COLORS[word_info['sound'][index]['type']])
            else:
                colorized_word += word[index]
        if word_info['type']:
            return self.__generate_html_tag(colorized_word, self.ASPECT_COLORS[word_info['type']])
        else:
            return colorized_word

    def __compute_offset(self, word_info) -> int:
        """ :return: offset that takes into the length of the word tag and the length of each sound """
        offset = 0
        if word_info['type']:
            offset += self.tag_length
        offset += len(word_info['sound']) * self.tag_length
        return offset

    @classmethod
    def __generate_html_tag(cls, word: str, color: str):
        """
        :return: text the specified word wrapped in a colorized html tags with the specified color
        :param word: is a string for colorizing
        :param color: is a color in hex format. For instance: #000000
        """
        return f'<span style=\" color: {color};\">{word}</span>'
