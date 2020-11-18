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

""" This module saves Document to .prd file """
import json

from models.document import Document
from models.document_presenter import DocumentPresenter


class DocumentSaver:

    def __init__(self, document: Document):
        self.document = document
        self.features = [feature.to_hash() for feature in document.features]

    def save(self, file_name="document.prd"):
        """ Saves document to specified file """
        if not file_name.endswith(".prd"):
            file_name += ".prd"

        with open(file_name, "w", encoding='utf8') as file:
            file.write(json.dumps({
                "metadata": dict(version=self.document.version, language=self.document.lang),
                "plain_text": DocumentPresenter(self.document).get_text(),
                "text": [chapter.title + '\n' +
                         ' '.join(sentence.text for sentence in chapter) for chapter in self.document.chapters],
                "features": self.features,
                "stop_words": self.document.stop_words},
                indent=4, ensure_ascii=False))
