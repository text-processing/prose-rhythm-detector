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
from models.document_loader import DocumentLoader
from models.workers.worker_base import WorkerBase


class DocumentLoaderWorker(WorkerBase):
    """ Class-worker for a DocumentParser object. An object of this class must be used in a separate thread """
    finished = Signal(object)

    def __init__(self, file_name: str, parsers: dict):
        """
        :param file_name: is the path of a file with text
        :param parsers: is a dict with parsers.
        If a parser doesn't exist for the specified lang it will be created and saved in the specified dict.
        """
        super().__init__()
        self.parsers = parsers
        self.document = None
        self.file_name = file_name

    def do_work(self):
        """ Starts document parsing. Emits the finished signal with a new document object in parameters as result"""
        self.document = DocumentLoader(self.file_name, self.parsers).load()

    def emit_finish(self):
        self.finished.emit(self.document)
