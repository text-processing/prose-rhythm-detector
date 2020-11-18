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
This module describes DocumentParser worker
"""
from PySide2.QtCore import Signal
from models.document_parser import DocumentParser
from models.preview_document.preview_document import PreviewDocument
from models.workers.worker_base import WorkerBase


class DocumentParserWorker(WorkerBase):
    """ Class-worker for a DocumentParser object. An object of this class must be used in a separate thread """
    finished = Signal(object)

    def __init__(self, preview_document: PreviewDocument, parsers: dict):
        """
        :param preview_document: is a PreviewDocument object with information about the loaded text
        :param parsers: is a dict with parsers.
        If a parser doesn't exist for the specified lang it will be created and saved in the specified dict.
        """
        super().__init__()
        self.parsers = parsers
        self.parser = None
        self.document = None
        self.lang = preview_document.lang
        self.stop_words = preview_document.stop_words[self.lang]
        self.plain_text = preview_document.plain_text

    def do_work(self):
        """ Starts document parsing. Emits the finished signal with a new document object in parameters as result"""
        if self.lang not in self.parsers:
            self.parsers[self.lang] = DocumentParser(self.lang)
        self.parser = self.parsers[self.lang]
        self.document = self.parser.parse_plain_text(self.plain_text)
        self.document.set_stop_words(self.stop_words)

    def emit_finish(self):
        self.finished.emit(self.document)
