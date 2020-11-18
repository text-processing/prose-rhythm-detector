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
Module describes PreviewWindow controller
"""
from PySide2 import QtWidgets
from PySide2.QtCore import Slot
from PySide2.QtGui import QTextCursor
from PySide2.QtWidgets import QListWidgetItem, QDialog

from controllers.stop_word_editor_controller import StopWordEditorController
from models.preview_document.preview_document import PreviewDocument
from ui.forms.preview_document_window_form import Ui_Preview_window


class PreviewWindow(QtWidgets.QDialog, Ui_Preview_window):
    """ Class describes preview document window"""

    def __init__(self, preview_document: PreviewDocument, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.preview_document = preview_document
        self.preview_document.lang = self.selected_language()
        self.__set_content()
        self.chapter_list.itemClicked.connect(self.select_chapter)
        self.lang_box.currentIndexChanged.connect(self.set_new_lang_to_document)
        self.use_text_clean_up.stateChanged.connect(self.use_cleaned_text)
        self.edit_stop_wors.clicked.connect(self.__show_stop_word_edit_dialog)
        self.stop_word_editor = None

    def select_chapter(self, item):
        """ fast-forward text to the selected chapter on the preview window"""
        chapter_number = self.preview_document.chapter_index_by_chapter_title(item.text())
        self.preview_document_text.moveCursor(QTextCursor.End)
        paragraph_number = len(self.preview_document.
                               plain_text[self.preview_document.chapter_pointers[chapter_number]:].split('\n'))
        for _i in range(paragraph_number):
            self.preview_document_text.moveCursor(QTextCursor.PreviousBlock, QTextCursor.MoveAnchor)

    @Slot()
    def set_new_lang_to_document(self):
        """Sets the selected language to the preview document model"""
        self.preview_document.lang = self.selected_language()

    def selected_language(self):
        """
        :return: current selected language
        """
        if self.lang_box.currentText() == "Русский":
            return "ru"
        if self.lang_box.currentText() == "Французский":
            return "fr"
        if self.lang_box.currentText() == "Испанский":
            return "es"
        return "en"

    @Slot()
    def use_cleaned_text(self):
        """Sets to the windows the cleaned version of the text if use_text_clean_up is Checked
        else sets the original version of the text"""
        self.preview_document.use_cleaned_text(self.use_text_clean_up.isChecked())
        self.__set_content()

    def __set_content(self):
        """ sets specified content for showing on the Preview window"""
        self.__clear_content()
        chapters = [self.preview_document.plain_text[i:j]
                    for i, j in zip(self.preview_document.chapter_pointers,
                                    self.preview_document.chapter_pointers[1:] + [None])]
        for chapter, chapter_name in zip(chapters, self.preview_document.chapter_names):
            content_item = QListWidgetItem(chapter_name[:40] + (chapter_name[40:] and '..'))
            self.chapter_list.addItem(content_item)
            self.preview_document_text.insertPlainText(chapter)
        self.chapterCount.setText(str(self.chapter_list.count()))
        self.preview_document_text.moveCursor(QTextCursor.Start)
        self.preview_document_text.ensureCursorVisible()

    def __clear_content(self):
        """ Removes text and chapters from the window"""
        self.preview_document_text.clear()
        self.chapter_list.clear()

    def __show_stop_word_edit_dialog(self):
        """
        Show stop word edit dialog.
        If the dialog is accepted saves changes.
        """
        stop_word_editor_controller = StopWordEditorController(
            self.preview_document.stop_words[self.selected_language()],
            self.selected_language())
        if stop_word_editor_controller.exec_() == QDialog.Accepted:
            self.preview_document.stop_words[self.selected_language()] = stop_word_editor_controller.stop_words
