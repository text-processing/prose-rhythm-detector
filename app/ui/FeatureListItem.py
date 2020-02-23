"""
Model of FeatureListItem
"""
from PySide2.QtWidgets import QListWidgetItem

from models.feature import Feature


class FeatureListItem(QListWidgetItem):
    """
    Class describes a feature.
    """

    def __get_aspect_string(self, document):
        words = ""
        if self.__aspect.type() == "anaphora":
            anaphora_indexes = list()
            for word_index in self.__aspect.words():
                anaphora_indexes.append(word_index)
            words = " ".join(document.words_by_indexes(sorted(anaphora_indexes)))
        else:
            for word_index in self.__aspect.words():
                words += document.word_by_index(word_index) + " "
        context = " ".join(document.words_from_to(self.__aspect.context_begin(), self.__aspect.context_end()))
        return "".join(words.strip() + "\n" + context.strip())

    def aspect(self) -> Feature:
        """ :return: the Feature model"""
        return self.__aspect

    def __init__(self, aspect, document):
        self.__aspect = aspect
        super(FeatureListItem, self).__init__(self.__get_aspect_string(document))
