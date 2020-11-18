# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'stop_word_editor_form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_StopWordEditor(object):
    def setupUi(self, StopWordEditor):
        if not StopWordEditor.objectName():
            StopWordEditor.setObjectName(u"StopWordEditor")
        StopWordEditor.resize(754, 470)
        self.gridLayout = QGridLayout(StopWordEditor)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(StopWordEditor)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 15))

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 3)

        self.aspect_type_list = QListWidget(StopWordEditor)
        self.aspect_type_list.setObjectName(u"aspect_type_list")
        self.aspect_type_list.setMaximumSize(QSize(220, 16777215))

        self.gridLayout.addWidget(self.aspect_type_list, 1, 0, 1, 1)

        self.speech_type_list = QListWidget(StopWordEditor)
        self.speech_type_list.setObjectName(u"speech_type_list")
        self.speech_type_list.setMaximumSize(QSize(220, 16777215))

        self.gridLayout.addWidget(self.speech_type_list, 1, 1, 1, 1)

        self.control_buttons = QDialogButtonBox(StopWordEditor)
        self.control_buttons.setObjectName(u"control_buttons")
        self.control_buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok|QDialogButtonBox.RestoreDefaults)

        self.gridLayout.addWidget(self.control_buttons, 3, 0, 1, 3)

        self.label = QLabel(StopWordEditor)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(StopWordEditor)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.label_4 = QLabel(StopWordEditor)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)

        self.stop_word_browser = QTextEdit(StopWordEditor)
        self.stop_word_browser.setObjectName(u"stop_word_browser")

        self.gridLayout.addWidget(self.stop_word_browser, 1, 2, 1, 1)


        self.retranslateUi(StopWordEditor)

        QMetaObject.connectSlotsByName(StopWordEditor)
    # setupUi

    def retranslateUi(self, StopWordEditor):
        StopWordEditor.setWindowTitle(QCoreApplication.translate("StopWordEditor", u"Dialog", None))
        self.label_3.setText(QCoreApplication.translate("StopWordEditor", u"* \u041a\u0430\u0436\u0434\u0430\u044f \u0441\u0442\u0440\u043e\u0447\u043a\u0430 \u0441\u043e\u043e\u0442\u0432\u0435\u0442\u0441\u0442\u0432\u0443\u0435\u0442 \u043e\u0434\u043d\u043e\u043c\u0443 \u0441\u0442\u043e\u043f-\u0441\u043b\u043e\u0432\u0443", None))
        self.label.setText(QCoreApplication.translate("StopWordEditor", u"\u0422\u0438\u043f \u0430\u0441\u043f\u0435\u043a\u0442\u0430", None))
        self.label_2.setText(QCoreApplication.translate("StopWordEditor", u"\u0427\u0430\u0441\u0442\u044c \u0440\u0435\u0447\u0438", None))
        self.label_4.setText(QCoreApplication.translate("StopWordEditor", u"\u0421\u0442\u043e\u043f \u0441\u043b\u043e\u0432\u0430*", None))
    # retranslateUi

