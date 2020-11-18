# pylint: disable=too-few-public-methods
"""
Module describes StopWordTreeWidget
"""
from PySide2.QtCore import Qt, Slot, Signal
from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu, QAction, QDialog

from controllers.stop_word_editor_controller import StopWordEditorController
from models.document import Document


class StopWordTreeWidget(QTreeWidget):
    """ Class describes a StopWordTreeWidget. """
    DEFAULT_COLUMN = 0
    stop_words_updated = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.document = None
        self.stop_words = None
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__open_menu)

    def __open_menu(self, point):
        """ Initializes and shows context menu """
        menu = QMenu()
        selected_item = self.itemAt(point)
        if selected_item:
            edit_question = QAction('Редактировать список стоп-слов', menu)
            edit_question.triggered.connect(self.__open_stop_word_edit_dialog)
            menu.addAction(edit_question)
        menu.exec_(self.mapToGlobal(point))

    @Slot()
    def __open_stop_word_edit_dialog(self):
        """
        Opens stop word edit dialog.
        If changes are accepted emits the stop_words_updated signal with new stop word list
        """
        stop_word_editor_controller = StopWordEditorController(self.stop_words, self.document.lang)
        if stop_word_editor_controller.exec_() == QDialog.Accepted:
            self.stop_words = stop_word_editor_controller.stop_words
            self.stop_words_updated.emit(self.stop_words)

    def __add_speech_part(self, speech_part: str, aspect_item: QTreeWidgetItem) -> QTreeWidgetItem:
        """
        Adds a QTreeWidgetItem with specified text to the aspect item
        :return: added QTreeWidgetItem item
        """
        item = QTreeWidgetItem()
        item.setText(self.DEFAULT_COLUMN, speech_part)
        aspect_item.addChild(item)
        return item

    def __add_aspect_type(self, aspect_type: str) -> QTreeWidgetItem:
        """
        Adds a QTreeWidgetItem with specified text aspect tree
        :return: added QTreeWidgetItem item
        """
        item = QTreeWidgetItem()
        item.setText(self.DEFAULT_COLUMN, aspect_type)
        self.addTopLevelItem(item)
        return item

    def __add_words_to_speech_part(self, speech_part_item: QTreeWidgetItem, words: list):
        """
        Adds words as a QTreeWidgetItem objects to the specified speech part item
        """
        for word in words:
            word_item = QTreeWidgetItem(word)
            word_item.setText(self.DEFAULT_COLUMN, word)
            speech_part_item.addChild(word_item)

    def load_stop_words(self, document: Document):
        """
        Adds and shows stop-words from the document
        """
        self.document = document
        self.stop_words = document.stop_words
        for aspect_type, speech_parts in self.stop_words.items():
            aspect_type_item = self.__add_aspect_type(aspect_type)
            for speech_part, words in speech_parts.items():
                speech_part_item = self.__add_speech_part(speech_part, aspect_type_item)
                self.__add_words_to_speech_part(speech_part_item, words)
