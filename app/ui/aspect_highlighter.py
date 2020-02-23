# pylint: disable=R0903
"""
This module describes Aspect highlighter
"""

from PySide2.QtWidgets import QTextBrowser
from PySide2.QtGui import QColor, QTextCursor, QFont, QTextCharFormat

from ui.aspect_colors import ASPECT_COLORS
from models.document import Document
from models.feature import Feature


class AspectHighlighter:
    """    Class describes AspectHighlighter    """
    def __init__(self, text_content: QTextBrowser, document: Document):
        self.__text_content = text_content
        self.__document = document
        self.__origin_format = self.__text_content.currentCharFormat()
        self.__cur_format = self.__text_content.currentCharFormat()
        self.__cursor = self.__text_content.textCursor()

    def highlight_aspect(self, aspect: Feature):
        """ highlights the specified aspect in the full text window"""
        self.__init_new_format()
        self.__set_color_by_type(aspect.type())
        self.__highlight_aspect_words(aspect)
        self.__reset_origin_color_format()

    def __init_new_format(self):
        self.__text_content.setCurrentCharFormat(QTextCharFormat())
        self.__cur_format = self.__text_content.currentCharFormat()

    def __set_color_by_type(self, aspect_type: str):
        self.__cur_format.setForeground(QColor(ASPECT_COLORS.get(aspect_type)))

    def __character_count_in_text_within(self, begin: int, end: int) -> int:
        return len(' '.join(self.__document.full_text()[begin:end]))

    def __highlight_word(self, word_index: int):
        self.__cursor.setPosition(self.__character_count_in_text_within(0, word_index) + 1)
        self.__cursor.movePosition(
            QTextCursor.NextCharacter,
            QTextCursor.KeepAnchor,
            len(self.__document.word_by_index(word_index)) + 1
        )
        self.__cursor.mergeCharFormat(self.__cur_format)

    def __set_bold_font_style(self):
        self.__cur_format.setFontWeight(QFont.Bold)

    def __highlight_aspect_words(self, aspect: Feature):
        for word in aspect.words():
            self.__highlight_word(word)

    def __reset_origin_color_format(self):
        self.__text_content.setCurrentCharFormat(self.__origin_format)
