"""
Model of AspectListWidgetItem
"""
from PySide2.QtWidgets import QCheckBox

from ui.aspect_colors import ASPECT_COLORS


class AspectCheckBox(QCheckBox):
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
        super(AspectCheckBox, self).__init__('{0} ({1})'.format(self.__aspect_type, self.__count))
        self.setChecked(True)
        self.setStyleSheet("background-color: {0};".format(ASPECT_COLORS[self.__aspect_type]))
