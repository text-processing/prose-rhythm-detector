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
