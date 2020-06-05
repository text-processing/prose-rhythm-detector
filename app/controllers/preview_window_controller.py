""""
ProseRhythmDetector - the tool for extraction of rhythm features.
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
Module describes PreviewWindow controller
"""
from PySide2.QtGui import QTextCursor
from PySide2.QtWidgets import QListWidgetItem

from ui.forms.preview_document_window_form import Ui_Preview_window
from ui.forms.main_window_form import QtWidgets


class PreviewWindow(QtWidgets.QDialog, Ui_Preview_window):
    """
    Class that describes preview document window
    """
    def __init__(self, plain_text: list, chapter_pointers: list, chapter_names: list, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.__plain_text = plain_text
        self.__chapter_pointers = chapter_pointers
        self.__chapter_names = chapter_names
        self.__set_content()
        self.content.itemClicked.connect(self.select_chapter)

    def select_chapter(self, item):
        """ fast-forward text to the selected chapter on the preview window"""
        chapter_number = self.__chapter_names.index(item.text())
        self.preview_document.moveCursor(QTextCursor.End)
        paragraph_number = len(self.__plain_text[self.__chapter_pointers[chapter_number]:].split('\n'))
        for _i in range(paragraph_number):
            self.preview_document.moveCursor(QTextCursor.PreviousBlock, QTextCursor.MoveAnchor)

    def selected_language(self):
        """
        :return: current selected language
        """
        if self.langBox.currentText() == "Русский":
            return "ru"
        elif self.langBox.currentText() == "Французский":
            return "fr"
        elif self.langBox.currentText() == "Испанский":
            return "es"
        return "en"

    def __set_content(self):
        """ sets specified content for showing on the Preview window"""
        self.preview_document.clear()
        chapters = [self.__plain_text[i:j] for i, j in zip(self.__chapter_pointers,
                                                           self.__chapter_pointers[1:] + [None])]
        for chapter, chapter_name in zip(chapters, self.__chapter_names):
            content_item = QListWidgetItem(chapter_name[:40] + (chapter_name[40:] and '..'))
            self.content.addItem(content_item)
            self.preview_document.insertPlainText(chapter)
        self.contentCount.setText(str(self.content.count()))
        self.preview_document.moveCursor(QTextCursor.Start)
        self.preview_document.ensureCursorVisible()
