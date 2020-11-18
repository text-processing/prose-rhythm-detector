# pylint: disable=R0902
# pylint: disable=broad-except
"""
Main window of the app
"""
import os
import traceback

from PySide2.QtCore import Slot, SIGNAL, QThread
from PySide2.QtGui import QTextCursor
from PySide2.QtWidgets import QMainWindow, QFileDialog, QListWidget, QProgressBar, QLabel, QErrorMessage

from controllers.preview_window_controller import PreviewWindow
from models.aspect_finder.utils.alliteration_schema import alliteration_sounds
from models.aspect_finder.utils.assonance_schema import assonance_sounds
from models.document import Document
from models.document_html_presenter import DocumentHtmlPresenter
from models.document_presenter import DocumentPresenter
from models.document_saver import DocumentSaver
from models.feature import Feature
from models.preview_document.preview_document import PreviewDocument
from models.text_parser import TextParser
from models.workers.aspect_finder_worker import AspectFinderWorker
from models.workers.document_loader_worker import DocumentLoaderWorker
from models.workers.document_parser_worker import DocumentParserWorker
from models.workers.html_presenter_worker import PresenterWorker
from ui.aspect_sound_tree_widget_item import AspectSoundTreeWidgetItem
from ui.aspect_tree_widget import AspectTreeWidget
from ui.feature_list_item import FeatureListItem
from ui.forms.main_window_form import Ui_MainWindow


class MainWindow(QMainWindow):
    """
    Class that describes main window of the app
    """

    def signals(self, main_window_ui):
        """ Connect signals from ui """
        self.connect(main_window_ui.import_text, SIGNAL("triggered()"), self.import_text)
        self.connect(main_window_ui.open_document, SIGNAL("triggered()"), self.open_document)
        self.connect(main_window_ui.save_document, SIGNAL("triggered()"), self.save_document)
        self.main_window_ui.aspects_list.itemClicked.connect(self.select_aspect)
        self.main_window_ui.uncheck_all_aspects_btn.clicked.connect(self.aspect_tree.uncheck_all_aspects)
        self.main_window_ui.select_all_aspects_btn.clicked.connect(self.aspect_tree.select_all_aspects)
        self.main_window_ui.show_selected_aspects_btn.clicked.connect(self.show_selected_aspects)
        self.main_window_ui.stop_list_tree.stop_words_updated.connect(self.restart_aspect_searching)

    def __init__(self):
        """ Constructor of widget """
        main_window = QMainWindow()
        self.main_window_ui = Ui_MainWindow()
        self.main_window_ui.setupUi(main_window)
        QMainWindow.__init__(self)
        Ui_MainWindow.setupUi(self.main_window_ui, self)
        self.signals(self.main_window_ui)
        self.highlighting_thread = None
        self.aspect_finding_thread = None
        self.parse_document_thread = None
        self.document_loader_thread = None
        self.parsers = {}
        self.document = None
        self.preview_document = None
        self.presenter = None
        self.worker = None
        self.html_presenter = None
        self.main_window_ui.save_document.setDisabled(True)
        self.preview_window = None
        self.__hide_progress_bar_panel()
        self.__cur_file_name = None
        self.__windows_title = 'prose-rhythm-detector'
        self.setWindowTitle(self.__windows_title)
        self.main_window_ui.show_selected_aspects_btn.setEnabled(False)

    @Slot()
    def save_document(self):
        """  Save the document to a *.prd file"""
        file_name = QFileDialog.getSaveFileName(self, dir=self.tr("../"), filter=self.tr("*.prd"))
        if not file_name[0]:
            return
        DocumentSaver(self.document).save(file_name[0])

    @Slot()
    def import_text(self):
        """ Creates new document from a specified text file """
        file_name = self.__show_open_file_dialog("Выберите файл с текстом")
        if file_name[0] == '':
            return
        self.preview_document = PreviewDocument(self.__import_plain_text_from_file(file_name))
        if not self.preview_document.chapters:
            return
        if self.__open_preview_window():
            self.__add_file_name_to_title(self.__cur_file_name)
            self.__clean_up_main_page()
            self.main_window_ui.save_document.setDisabled(True)
            self.main_window_ui.show_selected_aspects_btn.setEnabled(False)
            self.__start_parse_document_thread(self.preview_document)

    def __add_file_name_to_title(self, file_name: str):
        self.setWindowTitle('{0} ({1})'.format(self.__windows_title, file_name))

    def __import_plain_text_from_file(self, filename: str) -> str:
        """ Reads the text from the specified file """
        self.__cur_file_name = os.path.basename(filename[0])
        return TextParser().parse_plain_text(filename[0])

    def __open_preview_window(self):
        """ Open preview document window """
        self.preview_window = PreviewWindow(self.preview_document)
        self.preview_window.setModal(True)
        self.preview_window.show()
        return self.preview_window.exec_() == 1

    def __add_stop_words_to_stop_word_tree(self):
        """ Adds the stop words from the documents to the stop list tree widget """
        self.main_window_ui.stop_list_tree.load_stop_words(self.document)

    def __start_parse_document_thread(self, preview_document):
        self.__enable_input_menu_items(False)
        self.__init_and_show_progress_bar("Обработка текста")
        self.parse_document_thread = QThread()
        self.worker = DocumentParserWorker(preview_document, self.parsers)
        self.worker.moveToThread(self.parse_document_thread)
        self.worker.finished.connect(self.__on_parse_document_finished)
        self.worker.error.connect(self.__on_error)
        self.parse_document_thread.started.connect(self.worker.start)
        self.parse_document_thread.start()

    @Slot(object)
    def __on_parse_document_finished(self, document: Document):
        self.parse_document_thread.quit()
        self.document = document
        self.__start_aspect_finding_thread(self.document)

    def __start_aspect_finding_thread(self, document):
        self.__init_and_show_progress_bar("Поиск аспектов")
        self.aspect_finding_thread = QThread()
        self.worker = AspectFinderWorker(document)
        self.worker.moveToThread(self.aspect_finding_thread)
        self.worker.finished.connect(self.__on_aspect_search_finished)
        self.worker.error.connect(self.__on_error)
        self.worker.update_progress.connect(self.__update_aspect_search_progress)
        self.aspect_finding_thread.started.connect(self.worker.start)
        self.aspect_finding_thread.start()

    @Slot(int, int)
    def __update_aspect_search_progress(self, processed, total):
        self.__progress_bar_label().setText(f"Поиск аспектов {processed} из {total}")

    @Slot()
    def __on_aspect_search_finished(self):
        """This method describes actions when the aspect search was finished"""
        try:
            if self.aspect_finding_thread:
                self.aspect_finding_thread.quit()
            self.__set_content_in_main_window()
            self.main_window_ui.save_document.setEnabled(True)
            self.__enable_input_menu_items(True)
        except Exception:
            traceback.print_exc()
            self.__on_error()

    def __set_content_in_main_window(self):
        """Set a content to main window"""
        self.presenter = DocumentPresenter(self.document)
        self.html_presenter = DocumentHtmlPresenter(self.document)
        self.__add_aspect_types_to_aspect_tree()
        self.__add_stop_words_to_stop_word_tree()
        self.show_selected_aspects()

    def select_aspect(self, item: FeatureListItem):
        """ fast-forward text to the selected aspect in the document"""
        self.main_window_ui.text_content.setFocus()
        cursor = self.main_window_ui.text_content.textCursor()
        cursor.setPosition(self.presenter.word_start(item.aspect().context_begin()))
        cursor.movePosition(
            QTextCursor.NextCharacter,
            QTextCursor.KeepAnchor,
            self.presenter.word_end(item.aspect().context_end()) - self.presenter.word_start(
                item.aspect().context_begin())
        )
        self.main_window_ui.text_content.setTextCursor(cursor)

    @Slot()
    def show_selected_aspects(self):
        """ Adds aspects with selected types to the aspect list"""
        self.aspect_list().clear()
        aspects = self.aspects_with_selected_types()
        for aspect in aspects:
            self.aspect_list().addItem(FeatureListItem(aspect, self.presenter))
        self.__start_aspect_highlighting_thread(aspects)

    def __start_aspect_highlighting_thread(self, aspects):
        self.main_window_ui.show_selected_aspects_btn.setEnabled(False)
        self.__init_and_show_progress_bar("Подготовка текста для отображения")
        self.highlighting_thread = QThread()
        self.worker = PresenterWorker(self.html_presenter, aspects)
        self.worker.moveToThread(self.highlighting_thread)
        self.worker.finished.connect(self.__add_text)
        self.worker.error.connect(self.__on_error)
        self.highlighting_thread.started.connect(self.worker.start)
        self.highlighting_thread.start()

    @Slot()
    def __on_error(self):
        """This method describes actions when an error appears"""
        self.__stop_all_worker_threads()
        self.__hide_progress_bar_panel()
        self.main_window_ui.show_selected_aspects_btn.setEnabled(False)
        self.__enable_input_menu_items(True)
        error_dialog = QErrorMessage()
        error_dialog.showMessage('Во время обработки текста произошла ошибка!')
        error_dialog.exec_()

    def __stop_all_worker_threads(self):
        """ Stops all worker threads if they are run """
        self.highlighting_thread.quit() if self.highlighting_thread else None
        self.aspect_finding_thread.quit() if self.aspect_finding_thread else None
        self.parse_document_thread.quit() if self.parse_document_thread else None
        self.document_loader_thread.quit() if self.document_loader_thread else None

    @Slot(str)
    def __add_text(self, text):
        self.main_window_ui.text_content.setHtml(text)
        self.__hide_progress_bar_panel()
        self.highlighting_thread.quit()
        self.main_window_ui.show_selected_aspects_btn.setEnabled(True)

    def aspects_with_selected_types(self) -> list:
        """ :return: aspects with selected types """
        aspects = list()
        for aspect_item in self.aspect_tree.selected_aspect_types():
            if aspect_item.has_children():
                for child in aspect_item.selected_child_aspect_types():
                    aspects.extend(self.document.features_with_type_and_transcription(
                        child.aspect_type, child.sound))
            else:
                aspects.extend(self.document.features_with_type(aspect_item.aspect_type))
        return aspects

    def __add_aspect_types_to_aspect_tree(self):
        """ Adds the aspect types and his count to the aspect types tree """
        self.__add_grammatical_types_to_aspect_tree()
        self.__add_phonetic_types_to_aspect_tree()

    def __add_grammatical_types_to_aspect_tree(self):
        """ Adds the grammatical aspect types and his count to the aspect types tree """
        for feature_type in Feature.GRAMMATICAL_TYPES:
            feature_count = len(self.document.features_with_type(feature_type))
            self.aspect_tree.add_top_level_aspect(feature_type, feature_count)

    def __add_phonetic_types_to_aspect_tree(self):
        """ Adds the phonetic aspect types and his count to the aspect types tree """
        phonetic_types = {'assonance': assonance_sounds(self.document.lang),
                          'alliteration': alliteration_sounds(self.document.lang)}
        for feature_type, sounds in phonetic_types.items():
            feature_count = len(self.document.features_with_type(feature_type))
            aspect_top_item = self.aspect_tree.add_top_level_aspect(feature_type, feature_count)
            for sound in sounds:
                sound_count = len(self.document.features_with_type_and_transcription(feature_type, sound))
                aspect_top_item.addChild(AspectSoundTreeWidgetItem(feature_type, sound_count, sound, aspect_top_item))

    def __hide_progress_bar_panel(self):
        self.__progress_bar_label().setVisible(False)
        self.__progress_bar().setVisible(False)

    def __enable_input_menu_items(self, value):
        self.main_window_ui.open_document.setEnabled(value)
        self.main_window_ui.import_text.setEnabled(value)

    def __init_and_show_progress_bar(self, label: str = ''):
        self.__progress_bar().setValue(0)
        self.__progress_bar().setMaximum(0)
        self.__progress_bar().setMinimum(0)
        self.__progress_bar_label().setText(label)
        self.__progress_bar_label().setVisible(True)
        self.__progress_bar().setVisible(True)

    def __progress_bar(self) -> QProgressBar:
        return self.main_window_ui.progress_bar

    def __progress_bar_label(self) -> QLabel:
        return self.main_window_ui.progress_label

    @Slot()
    def open_document(self):
        """ Open the document """
        file_name = self.__show_open_file_dialog("Выберите документ", "*.prd")
        if not file_name[0]:
            return
        self.__start_document_loader_thread(file_name[0])

    def __start_document_loader_thread(self, file_name):
        self.__enable_input_menu_items(False)
        self.__init_and_show_progress_bar("Загрузка документа")
        self.document_loader_thread = QThread()
        self.worker = DocumentLoaderWorker(file_name, self.parsers)
        self.worker.moveToThread(self.document_loader_thread)
        self.worker.finished.connect(self.__on_document_load_finished)
        self.worker.error.connect(self.__on_error)
        self.document_loader_thread.started.connect(self.worker.start)
        self.document_loader_thread.start()

    @Slot(object)
    def __on_document_load_finished(self, document: Document):
        """This method describes actions when the document was loaded"""
        self.document_loader_thread.quit()
        self.document = document
        self.__on_aspect_search_finished()

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

    def aspect_list(self) -> QListWidget:
        """ :return the aspect_list object of QListWidget class where store aspects"""
        return self.main_window_ui.aspects_list

    @property
    def aspect_tree(self) -> AspectTreeWidget:
        """ :return: the feature_tree object of the AspectTreeWidget class where stored aspect types"""
        return self.main_window_ui.aspect_tree

    def __clean_up_main_page(self):
        self.main_window_ui.text_content.clear()
        self.aspect_list().clear()
        self.aspect_tree.clear()
        self.main_window_ui.stop_list_tree.clear()

    @Slot(dict)
    def restart_aspect_searching(self, new_stop_words: dict):
        """ Restarts aspect searching after stop-word editing """
        self.document.set_stop_words(new_stop_words)
        self.document.features.clear()
        self.__clean_up_main_page()
        self.main_window_ui.save_document.setDisabled(True)
        self.main_window_ui.show_selected_aspects_btn.setEnabled(False)
        self.__start_aspect_finding_thread(self.document)
