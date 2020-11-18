"""
Model of AspectTreeWidgetItem
"""
from PySide2.QtCore import Qt
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QTreeWidgetItem

from models.document_html_presenter import DocumentHtmlPresenter


class AspectTreeWidgetItem(QTreeWidgetItem):
    """Class describes a AspectTreeWidgetItem."""
    DEFAULT_COLUMN = 0

    def __init__(self, aspect_type: str, aspect_count: int, parent=None):
        super().__init__(parent)
        self.aspect_type = aspect_type
        self.aspect_count = aspect_count
        self.setText(self.DEFAULT_COLUMN, '{0} ({1})'.format(self.aspect_type, self.aspect_count))
        self.setBackgroundColor(self.DEFAULT_COLUMN, QColor(DocumentHtmlPresenter.ASPECT_COLORS[self.aspect_type]))
        self.setFlags(self.flags() | Qt.ItemIsTristate)
        self.setCheckState(self.DEFAULT_COLUMN, Qt.Checked)

    def selected_child_aspect_types(self):
        """ This method describes an iterator by child tree items that have
            the Qt.Checked or the Qt.PartiallyChecked state.
            The iterator yield an AspectSoundTreeWidgetItem object. """
        for child_index in range(self.childCount()):
            item = self.child(child_index)
            if item.is_checked():
                yield item

    def has_children(self) -> bool:
        """ This method returns True if the object has children elements."""
        return self.childCount() > 0

    def is_checked(self) -> bool:
        """ This method returns True if the object has the Qt.Checked or the Qt.PartiallyChecked state."""
        return self.checkState(self.DEFAULT_COLUMN) != Qt.Unchecked
