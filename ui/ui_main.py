# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 720)
        self.action1 = QAction(MainWindow)
        self.action1.setObjectName(u"action1")
        self.actionAdd_new_folder = QAction(MainWindow)
        self.actionAdd_new_folder.setObjectName(u"actionAdd_new_folder")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionSelect_folder = QAction(MainWindow)
        self.actionSelect_folder.setObjectName(u"actionSelect_folder")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.left_frame = QFrame(self.centralwidget)
        self.left_frame.setObjectName(u"left_frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.left_frame.sizePolicy().hasHeightForWidth())
        self.left_frame.setSizePolicy(sizePolicy)
        self.left_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.left_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.left_frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.path_lineEdit = QLineEdit(self.left_frame)
        self.path_lineEdit.setObjectName(u"path_lineEdit")
        self.path_lineEdit.setReadOnly(True)

        self.verticalLayout.addWidget(self.path_lineEdit)

        self.btn_frame = QFrame(self.left_frame)
        self.btn_frame.setObjectName(u"btn_frame")
        self.btn_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.btn_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.btn_frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.back_pushButton = QPushButton(self.btn_frame)
        self.back_pushButton.setObjectName(u"back_pushButton")

        self.horizontalLayout_2.addWidget(self.back_pushButton)

        self.forward_pushButton = QPushButton(self.btn_frame)
        self.forward_pushButton.setObjectName(u"forward_pushButton")

        self.horizontalLayout_2.addWidget(self.forward_pushButton)

        self.refresh_pushButton = QPushButton(self.btn_frame)
        self.refresh_pushButton.setObjectName(u"refresh_pushButton")

        self.horizontalLayout_2.addWidget(self.refresh_pushButton)


        self.verticalLayout.addWidget(self.btn_frame)

        self.files_treeWidget = QTreeWidget(self.left_frame)
        self.files_treeWidget.setObjectName(u"files_treeWidget")
        self.files_treeWidget.setLineWidth(1)

        self.verticalLayout.addWidget(self.files_treeWidget)


        self.horizontalLayout.addWidget(self.left_frame)

        self.right_frame = QFrame(self.centralwidget)
        self.right_frame.setObjectName(u"right_frame")
        sizePolicy.setHeightForWidth(self.right_frame.sizePolicy().hasHeightForWidth())
        self.right_frame.setSizePolicy(sizePolicy)
        self.right_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.right_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.right_frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pushButton = QPushButton(self.right_frame)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_2.addWidget(self.pushButton)

        self.library_treeWidget = QTreeWidget(self.right_frame)
        self.library_treeWidget.setObjectName(u"library_treeWidget")

        self.verticalLayout_2.addWidget(self.library_treeWidget)


        self.horizontalLayout.addWidget(self.right_frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1280, 33))
        self.menuLibrary = QMenu(self.menubar)
        self.menuLibrary.setObjectName(u"menuLibrary")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuLibrary.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuLibrary.addSeparator()
        self.menuLibrary.addAction(self.actionSelect_folder)
        self.menuLibrary.addAction(self.actionExit)
        self.menuTools.addAction(self.actionSettings)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action1.setText(QCoreApplication.translate("MainWindow", u"1.", None))
        self.actionAdd_new_folder.setText(QCoreApplication.translate("MainWindow", u"Add new folder...", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.actionSelect_folder.setText(QCoreApplication.translate("MainWindow", u"Select folder", None))
        self.path_lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Path", None))
        self.back_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u2b60", None))
        self.forward_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u2b62", None))
        self.refresh_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u27f3", None))
        ___qtreewidgetitem = self.files_treeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Folder", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Add anime", None))
        ___qtreewidgetitem1 = self.library_treeWidget.headerItem()
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"Library", None))
        self.menuLibrary.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

