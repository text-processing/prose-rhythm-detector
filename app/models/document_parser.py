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

import pathlib
import re

import stanza

from models.chapter import Chapter
from models.document import Document
from models.sentence import Sentence

USE_GPU = False

CHAPTER_TITLES = {'en': 'CHAPTER', 'es': 'CHAPTER', 'fr': 'CHAPTER', 'ru': 'ГЛАВА'}


class DocumentParser:
    PIPELINE_CFG = {"dir": str(pathlib.Path(__file__).parent.parent / 'stanza_resources'),
                    "processors": 'tokenize,pos,lemma,depparse',
                    "use_gpu": USE_GPU}

    def __init__(self, lang, pipeline=None):
        if not pipeline:
            if lang in ['es', 'fr']:
                self.PIPELINE_CFG["processors"] = 'tokenize,mwt,pos,lemma,depparse'
            pipeline = stanza.Pipeline(**self.PIPELINE_CFG, lang=lang)
        self.pipeline = pipeline
        self.lang = lang
        self.chapter_title = CHAPTER_TITLES[lang]

    def parse_plain_text(self, text) -> Document:
        chapters = self.__create_chapters(text)
        document = Document(chapters, self.lang)
        return document

    def parse_document(self, filepath) -> Document:
        return self.parse_plain_text(self.__get_plain_text(filepath))

    def parse_chapter(self, text, title=None):
        model = self.pipeline(text)
        return Chapter(model, title if title else self.chapter_title, self.lang)

    def parse_sentence(self, text):
        return Sentence(self.pipeline(text))

    @staticmethod
    def __get_plain_text(filepath):
        with open(filepath, 'r') as file:
            plain_text = "\n".join(filter(lambda s: len(s) > 0, map(str.strip, file.readlines())))
        return plain_text

    def __create_chapters(self, text):
        chapters = re.split(r"(^{} .+)\n*".format(self.chapter_title), text, flags=re.MULTILINE)
        chapters = list(filter(lambda x: len(x) > 0, chapters))
        if len(chapters) == 1:
            chapters = [self.parse_chapter(chapters[0])]
        else:
            chapters = [self.parse_chapter(text, title)
                        for title, text in zip(chapters[::2], chapters[1::2])]
        return chapters
