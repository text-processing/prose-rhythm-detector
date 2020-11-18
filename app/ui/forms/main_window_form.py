# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window_form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ui.aspect_tree_widget import AspectTreeWidget
from ui.stop_word_tree_widget import StopWordTreeWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(943, 778)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.open_document = QAction(MainWindow)
        self.open_document.setObjectName(u"open_document")
        self.import_text = QAction(MainWindow)
        self.import_text.setObjectName(u"import_text")
        self.save_document = QAction(MainWindow)
        self.save_document.setObjectName(u"save_document")
        self.central_widget = QWidget(MainWindow)
        self.central_widget.setObjectName(u"central_widget")
        self.central_widget.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.central_widget.sizePolicy().hasHeightForWidth())
        self.central_widget.setSizePolicy(sizePolicy1)
        self.gridLayout = QGridLayout(self.central_widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.progress_bar_layout = QHBoxLayout()
        self.progress_bar_layout.setObjectName(u"progress_bar_layout")
        self.progress_bar_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.progress_bar = QProgressBar(self.central_widget)
        self.progress_bar.setObjectName(u"progress_bar")
        sizePolicy1.setHeightForWidth(self.progress_bar.sizePolicy().hasHeightForWidth())
        self.progress_bar.setSizePolicy(sizePolicy1)
        self.progress_bar.setValue(0)

        self.progress_bar_layout.addWidget(self.progress_bar)

        self.progress_label = QLabel(self.central_widget)
        self.progress_label.setObjectName(u"progress_label")

        self.progress_bar_layout.addWidget(self.progress_label)


        self.gridLayout.addLayout(self.progress_bar_layout, 1, 0, 1, 1)

        self.splited_widget = QSplitter(self.central_widget)
        self.splited_widget.setObjectName(u"splited_widget")
        sizePolicy.setHeightForWidth(self.splited_widget.sizePolicy().hasHeightForWidth())
        self.splited_widget.setSizePolicy(sizePolicy)
        self.splited_widget.setOrientation(Qt.Horizontal)
        self.document_splitter = QSplitter(self.splited_widget)
        self.document_splitter.setObjectName(u"document_splitter")
        self.document_splitter.setOrientation(Qt.Vertical)
        self.layoutWidget1 = QWidget(self.document_splitter)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.document_wedget = QVBoxLayout(self.layoutWidget1)
        self.document_wedget.setObjectName(u"document_wedget")
        self.document_wedget.setContentsMargins(0, 0, 0, 0)
        self.document = QLabel(self.layoutWidget1)
        self.document.setObjectName(u"document")

        self.document_wedget.addWidget(self.document)

        self.text_content = QTextBrowser(self.layoutWidget1)
        self.text_content.setObjectName(u"text_content")
        self.text_content.setMaximumSize(QSize(16777215, 16777215))

        self.document_wedget.addWidget(self.text_content)

        self.document_splitter.addWidget(self.layoutWidget1)
        self.layoutWidget2 = QWidget(self.document_splitter)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.aspects_list_widget = QVBoxLayout(self.layoutWidget2)
        self.aspects_list_widget.setObjectName(u"aspects_list_widget")
        self.aspects_list_widget.setContentsMargins(0, 0, 0, 0)
        self.aspects_in_document = QLabel(self.layoutWidget2)
        self.aspects_in_document.setObjectName(u"aspects_in_document")

        self.aspects_list_widget.addWidget(self.aspects_in_document)

        self.aspects_list = QListWidget(self.layoutWidget2)
        self.aspects_list.setObjectName(u"aspects_list")
        self.aspects_list.setTextElideMode(Qt.ElideNone)
        self.aspects_list.setWordWrap(True)

        self.aspects_list_widget.addWidget(self.aspects_list)

        self.document_splitter.addWidget(self.layoutWidget2)
        self.splited_widget.addWidget(self.document_splitter)
        self.main_aspect_splitter = QSplitter(self.splited_widget)
        self.main_aspect_splitter.setObjectName(u"main_aspect_splitter")
        self.main_aspect_splitter.setOrientation(Qt.Vertical)
        self.aspect_splitter = QSplitter(self.main_aspect_splitter)
        self.aspect_splitter.setObjectName(u"aspect_splitter")
        self.aspect_splitter.setOrientation(Qt.Vertical)
        self.layoutWidget3 = QWidget(self.aspect_splitter)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.aspects_widget = QVBoxLayout(self.layoutWidget3)
        self.aspects_widget.setObjectName(u"aspects_widget")
        self.aspects_widget.setContentsMargins(0, 0, 0, 0)
        self.feature_list_label = QLabel(self.layoutWidget3)
        self.feature_list_label.setObjectName(u"feature_list_label")

        self.aspects_widget.addWidget(self.feature_list_label)

        self.aspect_tree = AspectTreeWidget(self.layoutWidget3)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.aspect_tree.setHeaderItem(__qtreewidgetitem)
        self.aspect_tree.setObjectName(u"aspect_tree")
        self.aspect_tree.setHeaderHidden(True)

        self.aspects_widget.addWidget(self.aspect_tree)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.select_all_aspects_btn = QPushButton(self.layoutWidget3)
        self.select_all_aspects_btn.setObjectName(u"select_all_aspects_btn")

        self.horizontalLayout.addWidget(self.select_all_aspects_btn)

        self.uncheck_all_aspects_btn = QPushButton(self.layoutWidget3)
        self.uncheck_all_aspects_btn.setObjectName(u"uncheck_all_aspects_btn")

        self.horizontalLayout.addWidget(self.uncheck_all_aspects_btn)


        self.aspects_widget.addLayout(self.horizontalLayout)

        self.show_selected_aspects_btn = QPushButton(self.layoutWidget3)
        self.show_selected_aspects_btn.setObjectName(u"show_selected_aspects_btn")

        self.aspects_widget.addWidget(self.show_selected_aspects_btn)

        self.aspect_splitter.addWidget(self.layoutWidget3)
        self.layoutWidget = QWidget(self.aspect_splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.stop_words_widget = QVBoxLayout(self.layoutWidget)
        self.stop_words_widget.setObjectName(u"stop_words_widget")
        self.stop_words_widget.setContentsMargins(0, 0, 0, 0)
        self.stop_list_label = QLabel(self.layoutWidget)
        self.stop_list_label.setObjectName(u"stop_list_label")

        self.stop_words_widget.addWidget(self.stop_list_label)

        self.stop_list_tree = StopWordTreeWidget(self.layoutWidget)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"1");
        self.stop_list_tree.setHeaderItem(__qtreewidgetitem1)
        self.stop_list_tree.setObjectName(u"stop_list_tree")
        self.stop_list_tree.header().setVisible(False)

        self.stop_words_widget.addWidget(self.stop_list_tree)

        self.aspect_splitter.addWidget(self.layoutWidget)
        self.main_aspect_splitter.addWidget(self.aspect_splitter)
        self.statistic_btn = QPushButton(self.main_aspect_splitter)
        self.statistic_btn.setObjectName(u"statistic_btn")
        self.statistic_btn.setMaximumSize(QSize(16777215, 16777215))
        self.main_aspect_splitter.addWidget(self.statistic_btn)
        self.splited_widget.addWidget(self.main_aspect_splitter)

        self.gridLayout.addWidget(self.splited_widget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.central_widget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 943, 22))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        self.menu = QMenu(self.menuBar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menu.menuAction())
        self.menuFile.addAction(self.open_document)
        self.menuFile.addAction(self.save_document)
        self.menu.addAction(self.import_text)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.open_document.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442", None))
        self.import_text.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043c\u043f\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0442\u0435\u043a\u0441\u0442", None))
        self.save_document.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442", None))
#if QT_CONFIG(tooltip)
        self.progress_bar.setToolTip(QCoreApplication.translate("MainWindow", u"\u044b\u0432\u0430", None))
#endif // QT_CONFIG(tooltip)
        self.progress_bar.setFormat(QCoreApplication.translate("MainWindow", u"%p%", None))
        self.progress_label.setText("")
        self.document.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u043a\u0443\u043c\u0435\u043d\u0442", None))
        self.aspects_in_document.setText(QCoreApplication.translate("MainWindow", u"\u0410\u0441\u043f\u0435\u043a\u0442\u044b \u0432 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0435", None))
        self.feature_list_label.setText(QCoreApplication.translate("MainWindow", u"\u0410\u0441\u043f\u0435\u043a\u0442\u044b", None))
        self.select_all_aspects_btn.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0432\u0441\u0435", None))
        self.uncheck_all_aspects_btn.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0431\u0440\u0430\u0442\u044c \u0432\u0441\u0435", None))
        self.show_selected_aspects_btn.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.stop_list_label.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043f\u0438\u0441\u043e\u043a \u0441\u043b\u043e\u0432 \u0438\u0441\u043a\u043b\u044e\u0447\u0451\u043d\u043d\u044b\u0445 \u0438\u0437 \u0430\u0441\u043f\u0435\u043a\u0442\u043e\u0432", None))
        self.statistic_btn.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u0422\u0435\u043a\u0441\u0442", None))
    # retranslateUi

