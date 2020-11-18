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

""" This module loads Document from .prd file """
import json

import stanza

from models.chapter import Chapter
from models.document import Document
from models.document_parser import DocumentParser
from models.feature import Feature


class DocumentLoader:

    def __init__(self, file_name, parsers=None):
        self.file_name = file_name
        self.language = None
        if not parsers:
            parsers = dict()
        self.pipeline = parsers

    def load(self):
        """ Loads Document from specified file """
        with open(self.file_name, "r", encoding='utf8') as file:
            json_doc = json.loads(file.read())
        self.language = json_doc["metadata"]["language"]
        features = [Feature(feature['type'], feature['words'], feature['context'],
                            self.__letters_to_int(feature['letters']), feature['transcription'])
                    for feature in json_doc["features"]]
        chapters = self.__load_chapters(json_doc["text"])
        stop_words = json_doc["stop_words"]
        return Document(chapters, self.language, features, stop_words)

    @classmethod
    def __letters_to_int(cls, letters):
        res = {}
        for letter in letters:
            res[int(letter)] = letters[letter]
        return res

    def __load_chapters(self, chapters_texts):
        if self.language not in self.pipeline:
            self.pipeline[self.language] = stanza.Pipeline(**DocumentParser.PIPELINE_CFG, lang=self.language)
        res = []
        for chapter_text in chapters_texts:
            title, text = chapter_text.split('\n', 1)
            model = self.pipeline[self.language](text)
            res.append(Chapter(model, title, self.language))
        return res
