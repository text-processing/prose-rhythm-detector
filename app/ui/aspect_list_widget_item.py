"""
Model of AspectListWidgetItem
"""
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QListWidgetItem
from PySide2.QtCore import Qt

from ui.aspect_colors import ASPECT_COLORS


class AspectListWidgetItem(QListWidgetItem):
    """
    Class describes a AspectListWidgetItem.
    """

    def type(self) -> str:
        """"
        :return: the type of of the aspect
        """
        return self.__aspect_type

    def __init__(self, aspect_type: str, count: int):
        self.__aspect_type = aspect_type
        self.__count = count
        super(AspectListWidgetItem, self).__init__('{0} ({1})'.format(self.__aspect_type, self.__count))
        self.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        self.setCheckState(Qt.Checked)
        self.setBackgroundColor(QColor(ASPECT_COLORS[self.__aspect_type]))
