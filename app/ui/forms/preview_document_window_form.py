# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preview_document_window_form.ui',
# licensing of 'preview_document_window_form.ui' applies.
#
# Created: Tue Jan 14 22:23:37 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Preview_window(object):
    def setupUi(self, Preview_window):
        Preview_window.setObjectName("Preview_window")
        Preview_window.resize(794, 815)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Preview_window.sizePolicy().hasHeightForWidth())
        Preview_window.setSizePolicy(sizePolicy)
        Preview_window.setAcceptDrops(False)
        self.gridLayout = QtWidgets.QGridLayout(Preview_window)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.contentsLabel = QtWidgets.QLabel(Preview_window)
        self.contentsLabel.setObjectName("contentsLabel")
        self.horizontalLayout.addWidget(self.contentsLabel)
        self.contentCountLabel = QtWidgets.QLabel(Preview_window)
        self.contentCountLabel.setObjectName("contentCountLabel")
        self.horizontalLayout.addWidget(self.contentCountLabel)
        self.contentCount = QtWidgets.QLabel(Preview_window)
        self.contentCount.setObjectName("contentCount")
        self.horizontalLayout.addWidget(self.contentCount)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.content = QtWidgets.QListWidget(Preview_window)
        self.content.setObjectName("content")
        self.verticalLayout_2.addWidget(self.content)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.text_label = QtWidgets.QLabel(Preview_window)
        self.text_label.setObjectName("text_label")
        self.verticalLayout.addWidget(self.text_label)
        self.preview_document = QtWidgets.QTextBrowser(Preview_window)
        self.preview_document.setObjectName("preview_document")
        self.verticalLayout.addWidget(self.preview_document)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.documen_language_label = QtWidgets.QLabel(Preview_window)
        self.documen_language_label.setObjectName("documen_language_label")
        self.horizontalLayout_2.addWidget(self.documen_language_label)
        self.langBox = QtWidgets.QComboBox(Preview_window)
        self.langBox.setObjectName("langBox")
        self.langBox.addItem("")
        self.langBox.addItem("")
        self.langBox.addItem("")
        self.langBox.addItem("")
        self.horizontalLayout_2.addWidget(self.langBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(Preview_window)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.retranslateUi(Preview_window)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Preview_window.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Preview_window.reject)
        QtCore.QMetaObject.connectSlotsByName(Preview_window)

    def retranslateUi(self, Preview_window):
        Preview_window.setWindowTitle(QtWidgets.QApplication.translate("Preview_window", "Предпросмотр документа", None, -1))
        self.contentsLabel.setText(QtWidgets.QApplication.translate("Preview_window", "Содержание", None, -1))
        self.contentCountLabel.setText(QtWidgets.QApplication.translate("Preview_window", "Количество глав: ", None, -1))
        self.contentCount.setText(QtWidgets.QApplication.translate("Preview_window", "TextLabel", None, -1))
        self.text_label.setText(QtWidgets.QApplication.translate("Preview_window", "Текст", None, -1))
        self.documen_language_label.setText(QtWidgets.QApplication.translate("Preview_window", "Язык документа", None, -1))
        self.langBox.setItemText(0, QtWidgets.QApplication.translate("Preview_window", "Русский", None, -1))
        self.langBox.setItemText(1, QtWidgets.QApplication.translate("Preview_window", "Английский", None, -1))
        self.langBox.setItemText(2, QtWidgets.QApplication.translate("Preview_window", "Французский", None, -1))
        self.langBox.setItemText(3, QtWidgets.QApplication.translate("Preview_window", "Испанский", None, -1))

