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
This module describes AspectFinder worker
"""
from models.aspect_finder.aspect_finder import AspectFinder
from models.document import Document
from models.workers.worker_base import WorkerBase


class AspectFinderWorker(WorkerBase):
    """ Class-worker for an AspectFinder object. An object of this class must be used in a separate thread """

    def __init__(self, document: Document):
        super().__init__()
        self.document = document
        self.aspect_finder = None

    def do_work(self):
        """ Starts aspect search. Found aspects adds to the document. """
        self.aspect_finder = AspectFinder(self.document)
        self.aspect_finder.update_progress.connect(self.on_update_progress)
        features = self.aspect_finder.find()
        self.document.features.extend(features)
