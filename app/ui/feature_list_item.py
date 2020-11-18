"""
Model of FeatureListItem
"""
from PySide2.QtWidgets import QListWidgetItem

from models.document_presenter import DocumentPresenter
from models.feature import Feature


class FeatureListItem(QListWidgetItem):
    """
    Class describes a feature.
    """

    def __get_aspect_string(self, presenter: DocumentPresenter):
        words = ""
        if self.__aspect.type() == "anaphora":
            anaphora_indexes = list(self.__aspect.words())
            words = ", ".join(presenter.words_by_indexes(sorted(anaphora_indexes)))
        else:
            words = ", ".join([presenter.word_by_index(word_index) for word_index in self.__aspect.words()])
        context = presenter.get_text()[presenter.word_start(self.__aspect.context_begin()):
                                       presenter.word_end(self.__aspect.context_end())]
        if self.__aspect.type() in Feature.PHONETIC_TYPES:
            words = f"[{self.__aspect.transcription}]: {words}"
        return f"{words}\n{context}"

    def aspect(self) -> Feature:
        """ :return: the Feature model"""
        return self.__aspect

    def __init__(self, aspect, presenter):
        self.__aspect = aspect
        super(FeatureListItem, self).__init__(self.__get_aspect_string(presenter))
