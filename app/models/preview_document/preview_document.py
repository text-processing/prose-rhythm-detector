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

""""
Module describes PreviewDocument model
"""
import json
import pathlib
import re

from clear_text_utils.clear_text import clear_line
from models.preview_document.text_info import TextInfo


class PreviewDocument:
    """ Class describes a preview document model """
    def __init__(self, plain_text: str, lang: str = None):
        self.__document_info = dict()
        self.original_text = TextInfo(plain_text)
        self.cleaned_text = TextInfo(self.__clear_text(plain_text))
        self.current_text = self.cleaned_text
        self.lang = lang
        self.stop_words = self.__read_stop_words()

    def __clear_text(self, original_text: str) -> str:
        """ :return: cleaned text """
        original_text = re.sub(r'([^\n])\n\n([^\n])', '\1\n\2', original_text)
        self.cleaned_plain_text = ''
        for line in original_text.split("\n"):
            self.cleaned_plain_text += clear_line(line) + "\n"
        return self.cleaned_plain_text

    def use_cleaned_text(self, value: bool):
        """Sets the cleaned version of the text as selected if specified value is True
            else sets the original text as selected"""
        if value:
            self.current_text = self.cleaned_text
        else:
            self.current_text = self.original_text

    def __getattr__(self, name):
        return getattr(self.current_text, name)

    def chapter_index_by_chapter_title(self, chapter_title: str) -> int:
        """ :return: index of a chapter with the specified chapter title. If not found returns None. """
        if chapter_title.endswith(".."):
            chapter_title = re.sub("\\.\\.$", '', chapter_title)
        for index, chapter_name in enumerate(self.chapter_names):
            if re.match(chapter_title, chapter_name):
                return index
        return None

    @classmethod
    def __read_stop_words(cls):
        with open(pathlib.Path(__file__).parent.parent.parent / 'stop_words.json', 'r',
                  encoding='utf-8') as json_file:
            stop_words = json.load(json_file)
        return stop_words
