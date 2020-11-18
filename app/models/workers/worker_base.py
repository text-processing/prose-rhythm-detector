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
This module describes WorkerBase class
"""
import traceback

from PySide2.QtCore import QObject, Slot, Signal


class WorkerBase(QObject):
    """ This class describes wrapper for a job that must be run in a separate thread """
    finished = Signal()
    update_progress = Signal(int, int)
    error = Signal()

    def __init__(self):
        super().__init__()

    def start(self):
        """ Starts the job """
        try:
            self.do_work()
            self.emit_finish()
        except Exception:
            traceback.print_exc()
            self.error.emit()

    @Slot(int, int)
    def on_update_progress(self, processed, total):
        """ This method emits the update_progress signal """
        self.update_progress.emit(processed, total)

    def do_work(self):
        """ This abstract method is describes your job. He must be overridden """
        pass

    def emit_finish(self):
        """ This method emits the finished signal. Can be overridden """
        self.finished.emit()
