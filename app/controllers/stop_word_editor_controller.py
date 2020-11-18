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
Module describes StopWordEditor controller
"""
import copy
import json
import pathlib

from PySide2 import QtWidgets
from PySide2.QtWidgets import QDialogButtonBox, QMessageBox

from models.stop_word_types import STOP_WORD_TYPES
from ui.forms.stop_word_editor_form import Ui_StopWordEditor, QListWidgetItem, Slot


class StopWordEditorController(QtWidgets.QDialog, Ui_StopWordEditor):
    """ Class describes StopWordEditor сontroller """
    def __init__(self, stop_words: dict, language: str, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.language = language
        self.stop_words = copy.deepcopy(stop_words)
        self.__init_stop_word_lists()
        self.__last_selected_speech_type = self.__selected_speech_type()
        self.__last_selected_aspect = self.__selected_aspect_type()
        self.control_buttons.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)
        self.control_buttons.button(QDialogButtonBox.Ok).clicked.connect(self.__on_click_ok_button)
        self.control_buttons.button(QDialogButtonBox.RestoreDefaults) \
                            .clicked.connect(self.__restore_default_stop_words)
        self.aspect_type_list.itemSelectionChanged.connect(self.__update_stop_word_lists)
        self.speech_type_list.itemSelectionChanged.connect(self.__update_stop_word_lists)

    def closeEvent(self, event):
        """ Overrides behavior of thw dialog closing. """
        self.__on_click_ok_button()
        event.ignore()

    @Slot()
    def __on_click_ok_button(self):
        """
        Shows confirmation dialog and if the user confirms
        saves or not the result and closes the dialog
        """
        confirmation = self.__show_close_confirmation_dialog()
        if confirmation == QMessageBox.Cancel:
            return
        if confirmation == QMessageBox.Yes:
            self.__save_stop_words()
        self.accept()

    def __show_close_confirmation_dialog(self):
        """ Shows confirmation dialog to save changes """
        return QMessageBox.question(self, "Выход",
                                          "Сохранить последнее изменение?",
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

    def __init_stop_word_lists(self):
        """ Initializes the aspect list type, the speech type list and the stop words input field """
        for aspect_type in self.stop_words:
            self.aspect_type_list.addItem(QListWidgetItem(aspect_type))
        for speech_type in STOP_WORD_TYPES:
            self.speech_type_list.addItem(QListWidgetItem(speech_type))
        self.aspect_type_list.item(0).setSelected(True)
        self.speech_type_list.item(0).setSelected(True)
        stop_words = self.stop_words[self.__selected_aspect_type()].get(self.__selected_speech_type(), list())
        self.stop_word_browser.setText("\n".join(stop_words))

    @Slot()
    def __update_stop_word_lists(self):
        """ Show stop words on change of selected aspect or speech type"""
        if len(self.aspect_type_list.selectedItems()) > 0 \
                and len(self.speech_type_list.selectedItems()) > 0:
            self.__save_stop_words()
            self.__last_selected_aspect = self.__selected_aspect_type()
            self.__last_selected_speech_type = self.__selected_speech_type()
            self.stop_word_browser.clear()
            stop_words = self.stop_words[self.__last_selected_aspect].get(self.__last_selected_speech_type, list())
            self.stop_word_browser.setText("\n".join(stop_words))

    @Slot()
    def __save_stop_words(self):
        """ Saves current stop word list """
        if len(self.aspect_type_list.selectedItems()) > 0 \
                and len(self.speech_type_list.selectedItems()) > 0:
            stop_words = list(filter(lambda x: len(x) > 0, self.stop_word_browser.toPlainText().split("\n")))
            self.stop_words[self.__last_selected_aspect][self.__last_selected_speech_type] = stop_words

    def __selected_speech_type(self):
        """ :return: selected speech type. If speech type is not selected returns None """
        if len(self.speech_type_list.selectedItems()) == 0:
            return None
        return self.speech_type_list.selectedItems()[0].text()

    def __selected_aspect_type(self):
        """ :return: selected aspect type. If aspect type is not selected returns None """
        if len(self.aspect_type_list.selectedItems()) == 0:
            return None
        return self.aspect_type_list.selectedItems()[0].text()

    @Slot()
    def __restore_default_stop_words(self):
        """ Reset stop word list to default """
        confirmation = QMessageBox.question(self, "Восстановить настройки",
                                            "Восстановить ВСЕ настройки по умолчанию?",
                                            QMessageBox.Yes | QMessageBox.Cancel)
        if confirmation == QMessageBox.Yes:
            self.aspect_type_list.clear()
            self.speech_type_list.clear()
            with open(pathlib.Path(__file__).parent.parent / 'stop_words.json', 'r',
                      encoding='utf-8') as json_file:
                stop_words = json.load(json_file)
            self.stop_words = copy.deepcopy(stop_words[self.language])
            self.__init_stop_word_lists()
