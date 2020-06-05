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
Module describes text parser
"""

import re


class TextParser:
    """
    Class describes text parser
    """

    def __parse_chapters(self, text, begin, chapters, chapter_level):
        end = len(text)
        while begin < end:
            text[begin] = text[begin].strip(self.characters_for_strip())
            if self.is_chapter(text[begin]):
                while begin < end and len(text[begin].strip(".").split(".")) > chapter_level and self.is_chapter(
                        text[begin]):
                    chapter = list()
                    begin = self.__parse_chapters(text, begin + 1, chapter, chapter_level + 1)
                    chapters.append(chapter)
                return begin
            if text[begin]:
                chapters.append(text[begin] + '\n')
            begin += 1
        return begin

    @classmethod
    def parse_plain_text(cls, file_with_text):
        """
        :param file_with_text: file with text
        :return: Array with parsed chapters
        """
        text = ''
        with open(file_with_text, 'r', encoding='utf8') as file:
            strings_from_file = file.readlines()
            text = text.join(strings_from_file)
        return text.replace('\ufeff', '')

    @classmethod
    def get_chapter_pointers(cls, plain_text):
        """
        :param plain_text: string with text
        :return: Array with parsed chapters
        """
        chapter_pointers = list()
        if 'CHAPTER' in plain_text:
            chapter_pointers = [iterator.start() for iterator in re.finditer('CHAPTER', plain_text)]
        elif 'ГЛАВА' in plain_text:
            chapter_pointers = [iterator.start() for iterator in re.finditer('ГЛАВА', plain_text)]
        chapter_pointers = [pointer for pointer in chapter_pointers if plain_text[pointer - 1] == '\n']
        if not chapter_pointers:
            chapter_pointers.append(0)
        return chapter_pointers

    @classmethod
    def get_chapter_names(cls, plain_text, chapter_pointers):
        """
        :param plain_text: string with text
        :param chapter_pointers: list of chapters pointers
        :return: Array with parsed chapters
        """
        chapters = [plain_text[i:j] for i, j in zip(chapter_pointers, chapter_pointers[1:] + [None])]
        return [i.split('\n', 1)[0] for i in chapters]

    def parse_chapters(self, plain_text):
        """
        :param plain_text: string with text
        :return: Array with parsed chapters
        """
        text = list()
        text.append('chapter')
        strings_from_file = plain_text.split('\n')
        if strings_from_file:
            if self.is_chapter(strings_from_file[0]):
                text = strings_from_file
            else:
                text.extend(strings_from_file)
        chapters = list()
        self.__parse_chapters(text, 0, chapters, 0)
        return chapters

    @staticmethod
    def is_chapter(string):
        """
        :return: true if string contains the word "глава" or "chapter",
                 false else
        """
        return string.lower().strip(".").startswith("глава") or string.lower().strip(".").startswith("chapter")

    @staticmethod
    def split_chapter_by_words(chapter):
        """
        Splits specified chapter by words
        """
        words = list()
        if isinstance(chapter, list):
            for sub_chapter in chapter:
                words.extend(TextParser.split_chapter_by_words(sub_chapter))
        else:
            words.extend(re.split("[  ]+", chapter))
        return words

    @staticmethod
    def characters_for_strip():
        """
        :return: the string with characters for striping of a string
        '"`.,()!?:;«»  \n\t
        """
        return '\'\"`.,()!?:;«»”“  \n\t'

    @staticmethod
    def sentence_separators():
        """
        :return: the reg exp with sentence separators
        """
        return '(?<=\\w\\w)(?<!Mrs)(?<!Mr)[\\.\\!\\?]\\s'

    @staticmethod
    def strip_str(string: str):
        """
        Strips the specified string
        :return: the stripped string
        """
        while string and (string[0] in TextParser.characters_for_strip() or string[len(string) - 1]
                          in TextParser.characters_for_strip()):
            string = string.strip(TextParser.characters_for_strip())
        return string

    @staticmethod
    def split_chapter_by_paragraphs(chapter):
        """
        Splits specified chapter by paragraphs
        """
        paragraphs = list()
        for paragraph in chapter:
            if isinstance(paragraph, list):
                paragraphs.extend(TextParser.split_chapter_by_paragraphs(paragraph))
            else:
                paragraphs.append(paragraph)
        return paragraphs

    @staticmethod
    def split_text_to_sentences(document) -> list:
        """ Splits text to list of sentences
            :return: list of lists of sentences for each chapter
        """

        def split_fragment_to_sentences(fragment):
            """ supply function, splits text fragment to sentences
            :param fragment: text fragment to parse
            :return: list of sentences in fragment
            """
            if isinstance(fragment, str):
                return [sen.strip(TextParser.characters_for_strip()) for sen in
                        re.split(TextParser.sentence_separators(), fragment)]
            if isinstance(fragment, list):
                res = []
                for frag in fragment:
                    res.extend(split_fragment_to_sentences(frag))
                return res
            raise Exception("Unknown fragment format")

        return [split_fragment_to_sentences(chapter) for chapter in document.chapters()]

    @staticmethod
    def split_sentence_to_words(sentence: str) -> list:
        """
        :param sentence: sentence as string
        :return: sentence as list of words
        """
        return [word.strip(TextParser.characters_for_strip()) for word in sentence.split()]

    @staticmethod
    def split_list_on_parts(lst, chunk_size: int) -> list:
        """
        splits list on parts with the specified size
        """
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
