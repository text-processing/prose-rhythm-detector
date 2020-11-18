"""
Model of AspectTreeWidget
"""
from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem

from ui.aspect_tree_widget_item import AspectTreeWidgetItem


class AspectTreeWidget(QTreeWidget):
    """ Class describes a AspectTreeWidget. """
    DEFAULT_COLUMN = 0

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.itemPressed.connect(self.__change_item_check_state_by_item_pressed)

    @classmethod
    @Slot(QTreeWidgetItem, int)
    def __change_item_check_state_by_item_pressed(cls, item: QTreeWidgetItem, col):
        if item.checkState(col) == Qt.Checked:
            item.setCheckState(col, Qt.Unchecked)
        else:
            item.setCheckState(col, Qt.Checked)

    @Slot()
    def uncheck_all_aspects(self):
        """ Sets to all aspect types the Qt.Unchecked state. """
        for index in range(self.topLevelItemCount()):
            self.topLevelItem(index).setCheckState(self.DEFAULT_COLUMN, Qt.Unchecked)

    @Slot()
    def select_all_aspects(self):
        """ Sets to all aspect types the Qt.Checked state. """
        for index in range(self.topLevelItemCount()):
            self.topLevelItem(index).setCheckState(self.DEFAULT_COLUMN, Qt.Checked)

    def add_top_level_aspect(self, aspect_type: str, aspect_count: int) -> AspectTreeWidgetItem:
        """ Creates and adds to the tree a new AspectTreeWidgetItem with the specified aspect type and count.
            :return: the added AspectTreeWidgetItem. """
        item = AspectTreeWidgetItem(aspect_type, aspect_count, self)
        self.addTopLevelItem(item)
        return item

    def selected_aspect_types(self):
        """ This method describes an iterator by the tree items that have the Qt.Checked or the
            Qt.PartiallyChecked state.
            The iterator yield an AspectTreeWidgetItem object. """
        for index in range(self.topLevelItemCount()):
            item = self.topLevelItem(index)
            if item.is_checked():
                yield item
