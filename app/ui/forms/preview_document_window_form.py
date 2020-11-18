# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preview_document_window_form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Preview_window(object):
    def setupUi(self, Preview_window):
        if not Preview_window.objectName():
            Preview_window.setObjectName(u"Preview_window")
        Preview_window.resize(816, 749)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Preview_window.sizePolicy().hasHeightForWidth())
        Preview_window.setSizePolicy(sizePolicy)
        Preview_window.setAcceptDrops(False)
        self.gridLayout = QGridLayout(Preview_window)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.contentsLabel = QLabel(Preview_window)
        self.contentsLabel.setObjectName(u"contentsLabel")

        self.horizontalLayout.addWidget(self.contentsLabel)

        self.contentCountLabel = QLabel(Preview_window)
        self.contentCountLabel.setObjectName(u"contentCountLabel")

        self.horizontalLayout.addWidget(self.contentCountLabel)

        self.chapterCount = QLabel(Preview_window)
        self.chapterCount.setObjectName(u"chapterCount")

        self.horizontalLayout.addWidget(self.chapterCount)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.chapter_list = QListWidget(Preview_window)
        self.chapter_list.setObjectName(u"chapter_list")

        self.verticalLayout_2.addWidget(self.chapter_list)


        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.text_label = QLabel(Preview_window)
        self.text_label.setObjectName(u"text_label")

        self.verticalLayout.addWidget(self.text_label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.preview_document_text = QTextBrowser(Preview_window)
        self.preview_document_text.setObjectName(u"preview_document_text")

        self.horizontalLayout_2.addWidget(self.preview_document_text)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 4, 1)

        self.use_text_clean_up = QCheckBox(Preview_window)
        self.use_text_clean_up.setObjectName(u"use_text_clean_up")
        self.use_text_clean_up.setChecked(True)

        self.gridLayout.addWidget(self.use_text_clean_up, 1, 0, 1, 1)

        self.edit_stop_wors = QPushButton(Preview_window)
        self.edit_stop_wors.setObjectName(u"edit_stop_wors")

        self.gridLayout.addWidget(self.edit_stop_wors, 2, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.documen_language_label = QLabel(Preview_window)
        self.documen_language_label.setObjectName(u"documen_language_label")

        self.horizontalLayout_3.addWidget(self.documen_language_label)

        self.lang_box = QComboBox(Preview_window)
        self.lang_box.addItem("")
        self.lang_box.addItem("")
        self.lang_box.addItem("")
        self.lang_box.addItem("")
        self.lang_box.setObjectName(u"lang_box")

        self.horizontalLayout_3.addWidget(self.lang_box)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.gridLayout.addLayout(self.horizontalLayout_3, 3, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(Preview_window)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setLayoutDirection(Qt.LeftToRight)
        self.buttonBox.setAutoFillBackground(False)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 4, 1, 1, 1)


        self.retranslateUi(Preview_window)
        self.buttonBox.accepted.connect(Preview_window.accept)
        self.buttonBox.rejected.connect(Preview_window.reject)

        QMetaObject.connectSlotsByName(Preview_window)
    # setupUi

    def retranslateUi(self, Preview_window):
        Preview_window.setWindowTitle(QCoreApplication.translate("Preview_window", u"\u041f\u0440\u0435\u0434\u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430", None))
        self.contentsLabel.setText(QCoreApplication.translate("Preview_window", u"\u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435", None))
        self.contentCountLabel.setText(QCoreApplication.translate("Preview_window", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0433\u043b\u0430\u0432: ", None))
        self.chapterCount.setText(QCoreApplication.translate("Preview_window", u"0", None))
        self.text_label.setText(QCoreApplication.translate("Preview_window", u"\u0422\u0435\u043a\u0441\u0442", None))
        self.use_text_clean_up.setText(QCoreApplication.translate("Preview_window", u"\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u044c \u043f\u0440\u0435\u0434\u0432\u0430\u0440\u0438\u0442\u0435\u043b\u044c\u043d\u0443\u044e \u043e\u0447\u0438\u0441\u0442\u043a\u0443 \u0442\u0435\u043a\u0441\u0442\u0430", None))
        self.edit_stop_wors.setText(QCoreApplication.translate("Preview_window", u"\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0441\u043f\u0438\u0441\u043e\u043a \u0441\u0442\u043e\u043f-\u0441\u043b\u043e\u0432", None))
        self.documen_language_label.setText(QCoreApplication.translate("Preview_window", u"\u042f\u0437\u044b\u043a \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430:", None))
        self.lang_box.setItemText(0, QCoreApplication.translate("Preview_window", u"\u0420\u0443\u0441\u0441\u043a\u0438\u0439", None))
        self.lang_box.setItemText(1, QCoreApplication.translate("Preview_window", u"\u0410\u043d\u0433\u043b\u0438\u0439\u0441\u043a\u0438\u0439", None))
        self.lang_box.setItemText(2, QCoreApplication.translate("Preview_window", u"\u0424\u0440\u0430\u043d\u0446\u0443\u0437\u0441\u043a\u0438\u0439", None))
        self.lang_box.setItemText(3, QCoreApplication.translate("Preview_window", u"\u0418\u0441\u043f\u0430\u043d\u0441\u043a\u0438\u0439", None))

    # retranslateUi

