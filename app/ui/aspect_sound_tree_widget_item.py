"""
Model of AspectSoundTreeWidgetItem
"""

from ui.aspect_tree_widget_item import AspectTreeWidgetItem


class AspectSoundTreeWidgetItem(AspectTreeWidgetItem):
    """ Class describes a AspectSoundTreeWidgetItem. """
    def __init__(self, aspect_type: str, count: int, sound: str, parent=None):
        super().__init__(aspect_type, count, parent)
        self.sound = sound
        self.setText(self.DEFAULT_COLUMN, '[{0}] ({1})'.format(self.sound, self.aspect_count))
