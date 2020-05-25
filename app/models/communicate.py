"""
Model of Communicate
"""
from PySide2.QtCore import Signal, QObject


class Communicate(QObject):
    """ Class describes the signals fot connection"""
    update_progress = Signal(list)
