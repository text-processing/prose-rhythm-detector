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


# pylint: disable=R0902
"""
Main window of the app
"""
import os
from concurrent.futures import ProcessPoolExecutor, Future

from PySide2.QtCore import Slot, SIGNAL
from PySide2.QtGui import QTextCursor
from PySide2.QtWidgets import QMainWindow, QFileDialog, QListWidget, QProgressBar, QLabel

from controllers.preview_window_controller import PreviewWindow
from models.aspect_parser.aspect_parser import AspectParser
from models.communicate import Communicate
from models.document import Document
from models.text_parser import TextParser
from ui.FeatureListItem import FeatureListItem
from ui.aspect_check_box import AspectCheckBox
from ui.aspect_highlighter import AspectHighlighter
from ui.forms.main_window_form import QtWidgets, Ui_MainWindow


class MainWindow(QMainWindow):
    """
    Class that describes main window of the app
    """

    def signals(self, main_window_ui):
        """ Connect signals from ui """
        self.connect(main_window_ui.import_text, SIGNAL("triggered()"), self.import_text)
        self.connect(main_window_ui.open_document, SIGNAL("triggered()"), self.open_document)
        self.connect(main_window_ui.save_document, SIGNAL("triggered()"), self.save_document)
        self.communicate.update_progress.connect(self.update_aspect_parser_progress)
        self.main_window_ui.aspects_list.itemClicked.connect(self.select_aspect)

    def __init__(self):
        """ Constructor of widget """
        main_window = QtWidgets.QMainWindow()
        self.main_window_ui = Ui_MainWindow()
        self.main_window_ui.setupUi(main_window)
        QMainWindow.__init__(self)
        Ui_MainWindow.setupUi(self.main_window_ui, self)
        self.communicate = Communicate()
        self.signals(self.main_window_ui)
        self.document = None
        self.main_window_ui.save_document.setDisabled(True)
        self.preview_window = None
        self.progress = 0
        self.progress_max = 4
        self.__hide_progress_bar_panel()
        self.__cur_file_name = None
        self.__windows_title = 'prose-rhythm-detector'
        self.setWindowTitle(self.__windows_title)

    @Slot()
    def save_document(self):
        """  Save the document in JSON file"""
        file_name = QFileDialog.getSaveFileName(self, dir=self.tr("../"), filter=self.tr("*.prd"))
        if not file_name[0]:
            return
        self.document.save_to_file(file_name[0])

    @Slot()
    def import_text(self):
        """ Creates new document from a specified text file """
        plain_text = self.__import_plain_text("Выберите файл с текстом")
        if not plain_text:
            return
        chapter_pointers = TextParser().get_chapter_pointers(plain_text)
        chapters = self.__import_text(plain_text)
        if not chapters:
            return
        text_accepted = self.__open_preview_window(plain_text, chapter_pointers)
        if text_accepted:
            self.setWindowTitle('{0} ({1})'.format(self.__windows_title, self.__cur_file_name))
            self.__clean_up_main_page()
            self.document = Document(plain_text=plain_text, chapter_pointers=chapter_pointers,
                                     chapters=chapters, language=self.preview_window.selected_language())
            self.__parse_features(self.document)

    def select_aspect(self, item: FeatureListItem):
        """ fast-forward text to the selected aspect in the document"""
        self.main_window_ui.text_content.setFocus()
        self.main_window_ui.text_content.moveCursor(QTextCursor.Start)
        context_begin = item.aspect().context_begin()
        context_end = item.aspect().context_end() + 1
        text_before_aspect = ' '.join(self.document.full_text()[0:context_begin])
        last_paragraph_ind = text_before_aspect.rfind('\n')
        beg_ind = len(text_before_aspect)
        end_ind = len(' '.join(self.document.full_text()[0:context_end]))
        self.__move_cursor_from_begin(text_before_aspect.count('\n', 0, beg_ind), beg_ind - last_paragraph_ind)
        self.__select_text_by_characters(end_ind - beg_ind)

    def __move_cursor_from_begin(self, num_blocks, num_characters):
        for _i in range(num_blocks):
            self.main_window_ui.text_content.moveCursor(QTextCursor.NextBlock, QTextCursor.MoveAnchor)
        for _i in range(num_characters):
            self.main_window_ui.text_content.moveCursor(QTextCursor.NextCharacter, QTextCursor.MoveAnchor)

    def __select_text_by_characters(self, num_characters):
        for _i in range(num_characters):
            self.main_window_ui.text_content.moveCursor(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)

    @Slot()
    def __show_or_hide_aspects_with_specified_type(self, _state):
        aspect = self.sender()
        if aspect.isChecked():
            self.__add_aspects_with_specified_type(aspect.type())
        else:
            self.__remove_aspects_with_specified_type(aspect.type())

    def __add_aspects_with_specified_type(self, aspect_type: str):
        for aspect in self.document.features_with_type(aspect_type):
            self.aspect_list().addItem(FeatureListItem(aspect, self.document))

    def __remove_aspects_with_specified_type(self, aspect_type: str):
        aspects_for_removing = self.__aspects_with_specified_type(aspect_type)
        for aspect in aspects_for_removing:
            self.aspect_list().takeItem(self.aspect_list().row(aspect))

    def __aspects_with_specified_type(self, aspect_type: str) -> list:
        aspects = list()
        for aspect_index in range(self.aspect_list().count()):
            aspect = self.aspect_list().item(aspect_index)
            if aspect.aspect().type() == aspect_type:
                aspects.append(aspect)
        return aspects

    def __set_content_in_main_window(self):
        """Set a content to main window"""
        self.__add_feature_to_feature_list()
        self.__add_aspects_to_aspect_list()
        self.__add_text()
        self.__add_aspect_highlighting()

    def __add_feature_to_feature_list(self):
        feature_list = self.feature_list()
        for feature_type in self.document.feature_types():
            feature_count = len(self.document.features_with_type(feature_type))
            aspect_widget_item = QtWidgets.QListWidgetItem()
            feature_list.addItem(aspect_widget_item)
            aspect_check_box = AspectCheckBox(feature_type, feature_count)
            aspect_check_box.clicked.connect(self.__show_or_hide_aspects_with_specified_type)
            feature_list.setItemWidget(aspect_widget_item, aspect_check_box)

    def __add_aspects_to_aspect_list(self):
        for aspect in self.document.features():
            self.aspect_list().addItem(FeatureListItem(aspect, self.document))

    def __add_text(self):
        self.main_window_ui.text_content.insertPlainText(' ' + ' '.join(self.document.full_text()))

    def __add_aspect_highlighting(self):
        highlighter = AspectHighlighter(self.main_window_ui.text_content, self.document)
        for aspect in self.document.features():
            highlighter.highlight_aspect(aspect)

    @Slot(list)
    def update_aspect_parser_progress(self, aspect_list):
        """ Updates the progress bar after completion of searching each aspect """
        self.progress += 1
        self.document.add_feature(aspect_list)
        if self.progress == self.progress_max:
            self.__set_content_in_main_window()
            self.main_window_ui.save_document.setDisabled(False)
            self.__enable_input_menu_items(True)
            self.__hide_progress_bar_panel()

    def __hide_progress_bar_panel(self):
        self.__progress_bar().setValue(0)
        self.__progress_bar_label().setVisible(False)
        self.__progress_bar().setVisible(False)

    def __enable_input_menu_items(self, value):
        self.main_window_ui.open_document.setEnabled(value)
        self.main_window_ui.import_text.setEnabled(value)

    def __init_and_show_progress_bar(self):
        self.progress = 0
        self.__progress_bar().setValue(0)
        self.__progress_bar().setMaximum(0)
        self.__progress_bar().setMinimum(0)
        self.__progress_bar_label().setVisible(True)
        self.__progress_bar().setVisible(True)

    def __emit_update_progress_bar(self, future: Future):
        """ emit update_aspect_parser_progress slot"""
        self.communicate.update_progress.emit(future.result())

    def __parse_features(self, document):
        """ Parses feature from text """
        self.__init_and_show_progress_bar()
        self.__enable_input_menu_items(False)
        aspect_parser = AspectParser(document)
        executor = ProcessPoolExecutor(max_workers=5)
        futures = list()
        futures.append(executor.submit(aspect_parser.parse_recurring_sentence_parts_features))
        futures.append(executor.submit(aspect_parser.parse_anadiplosis))
        futures.append(executor.submit(aspect_parser.parse_polysyndeton))
        futures.append(executor.submit(aspect_parser.parse_diacope))
        futures.append(executor.submit(aspect_parser.parse_epizeuxis))
        futures.append(executor.submit(aspect_parser.parse_epanalepsis))
        self.progress_max = len(futures)
        for future in futures:
            future.add_done_callback(self.__emit_update_progress_bar)

    def __progress_bar(self) -> QProgressBar:
        return self.main_window_ui.progress_bar

    def __progress_bar_label(self) -> QLabel:
        return self.main_window_ui.progress_label

    def __import_plain_text(self, title):
        """ Open a dialog for choosing file with text on the specified language"""
        file_name = self.__show_open_file_dialog(title)
        if not file_name[0]:
            return None
        self.__cur_file_name = os.path.basename(file_name[0])
        return TextParser().parse_plain_text(file_name[0])

    @classmethod
    def __import_text(cls, plain_text):
        """ Open a dialog for choosing file with text on the specified language"""
        return TextParser().parse_chapters(plain_text)

    @Slot()
    def open_document(self):
        """ Open the document """
        file_name = self.__show_open_file_dialog("Выберите документ", "*.prd")
        if not file_name[0]:
            return
        self.document = Document.open_from_file(file_name[0])
        self.__set_content_in_main_window()
        self.main_window_ui.save_document.setDisabled(False)

    def __show_open_file_dialog(self, title, file_type="*.txt"):
        """
            Open the dialog to select the name of file
            :param title: the title of the open file dialog
            :param file_type: the type of the file (sample "*.txt, *.json")
            :return a selected file
        """
        file_name = QFileDialog.getOpenFileName(self, self.tr(title),
                                                self.tr("../"),
                                                self.tr(file_type))
        return file_name

    def __open_preview_window(self, plain_text, chapter_pointers):
        """ Open preview document window """
        self.preview_window = PreviewWindow(plain_text, chapter_pointers,
                                            TextParser.get_chapter_names(plain_text, chapter_pointers))
        self.preview_window.setModal(True)
        self.preview_window.show()
        return self.preview_window.exec_() == 1

    def aspect_list(self) -> QListWidget:
        """ :return the aspect_list object of QListWidget class where store aspects"""
        return self.main_window_ui.aspects_list

    def feature_list(self) -> QListWidget:
        """ :return the aspect_list object of QListWidget class where store aspects"""
        return self.main_window_ui.feature_list

    def __clean_up_main_page(self):
        self.main_window_ui.text_content.clear()
        self.aspect_list().clear()
        self.feature_list().clear()
