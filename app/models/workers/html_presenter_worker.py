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
from models.workers.worker_base import WorkerBase


class PresenterWorker(WorkerBase):
    """ Class-wrapper for a DocumentHtmlPresenter object """
    finished = Signal(str)

    def __init__(self, presenter, aspects: list):
        super().__init__()
        self.presenter = presenter
        self.aspects = aspects
        self.text = None

    def do_work(self):
        """
        Adds colorized tags to aspect words.
        Emits the finished signal with the text in the html format as result.
        """
        self.text = self.presenter.get_text_with_highlighted_aspects(self.aspects)

    def emit_finish(self):
        self.finished.emit(self.text)
