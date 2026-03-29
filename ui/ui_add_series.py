# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_series.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QRadioButton, QSizePolicy, QTabWidget,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(723, 559)
        self.verticalLayout_3 = QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.engine_select_frame = QFrame(self.frame)
        self.engine_select_frame.setObjectName(u"engine_select_frame")
        self.engine_select_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.engine_select_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.engine_select_frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.TVDB_radioButton = QRadioButton(self.engine_select_frame)
        self.TVDB_radioButton.setObjectName(u"TVDB_radioButton")

        self.horizontalLayout.addWidget(self.TVDB_radioButton)

        self.TMDB_radioButton = QRadioButton(self.engine_select_frame)
        self.TMDB_radioButton.setObjectName(u"TMDB_radioButton")

        self.horizontalLayout.addWidget(self.TMDB_radioButton)

        self.AniList_radioButton = QRadioButton(self.engine_select_frame)
        self.AniList_radioButton.setObjectName(u"AniList_radioButton")

        self.horizontalLayout.addWidget(self.AniList_radioButton)

        self.MAL_radioButton = QRadioButton(self.engine_select_frame)
        self.MAL_radioButton.setObjectName(u"MAL_radioButton")

        self.horizontalLayout.addWidget(self.MAL_radioButton)


        self.verticalLayout_2.addWidget(self.engine_select_frame)

        self.tabWidget = QTabWidget(self.frame)
        self.tabWidget.setObjectName(u"tabWidget")
        self.scan_tab = QWidget()
        self.scan_tab.setObjectName(u"scan_tab")
        self.horizontalLayout_5 = QHBoxLayout(self.scan_tab)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.scan_frame = QFrame(self.scan_tab)
        self.scan_frame.setObjectName(u"scan_frame")
        self.scan_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.scan_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.scan_frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.scan_label = QLabel(self.scan_frame)
        self.scan_label.setObjectName(u"scan_label")

        self.verticalLayout_4.addWidget(self.scan_label)

        self.select_folder_frame = QFrame(self.scan_frame)
        self.select_folder_frame.setObjectName(u"select_folder_frame")
        self.select_folder_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.select_folder_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.select_folder_frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.scan_folder_lineEdit = QLineEdit(self.select_folder_frame)
        self.scan_folder_lineEdit.setObjectName(u"scan_folder_lineEdit")

        self.horizontalLayout_3.addWidget(self.scan_folder_lineEdit)

        self.scan_folder_browse_pushButton = QPushButton(self.select_folder_frame)
        self.scan_folder_browse_pushButton.setObjectName(u"scan_folder_browse_pushButton")

        self.horizontalLayout_3.addWidget(self.scan_folder_browse_pushButton)


        self.verticalLayout_4.addWidget(self.select_folder_frame)

        self.scan_start_pushButton = QPushButton(self.scan_frame)
        self.scan_start_pushButton.setObjectName(u"scan_start_pushButton")

        self.verticalLayout_4.addWidget(self.scan_start_pushButton)

        self.confirm_series_label = QLabel(self.scan_frame)
        self.confirm_series_label.setObjectName(u"confirm_series_label")

        self.verticalLayout_4.addWidget(self.confirm_series_label)

        self.scan_results_listWidget = QListWidget(self.scan_frame)
        self.scan_results_listWidget.setObjectName(u"scan_results_listWidget")
        self.scan_results_listWidget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        self.verticalLayout_4.addWidget(self.scan_results_listWidget)

        self.scan_add_pushButton = QPushButton(self.scan_frame)
        self.scan_add_pushButton.setObjectName(u"scan_add_pushButton")

        self.verticalLayout_4.addWidget(self.scan_add_pushButton)


        self.horizontalLayout_5.addWidget(self.scan_frame)

        self.tabWidget.addTab(self.scan_tab, "")
        self.search_tab = QWidget()
        self.search_tab.setObjectName(u"search_tab")
        self.horizontalLayout_4 = QHBoxLayout(self.search_tab)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.frame_4 = QFrame(self.search_tab)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.search_label = QLabel(self.frame_4)
        self.search_label.setObjectName(u"search_label")

        self.verticalLayout.addWidget(self.search_label)

        self.search_frame = QFrame(self.frame_4)
        self.search_frame.setObjectName(u"search_frame")
        self.search_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.search_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.search_frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.search_lineEdit = QLineEdit(self.search_frame)
        self.search_lineEdit.setObjectName(u"search_lineEdit")

        self.horizontalLayout_2.addWidget(self.search_lineEdit)

        self.search_pushButton = QPushButton(self.search_frame)
        self.search_pushButton.setObjectName(u"search_pushButton")

        self.horizontalLayout_2.addWidget(self.search_pushButton)


        self.verticalLayout.addWidget(self.search_frame)

        self.search_treeWidget = QTreeWidget(self.frame_4)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"Results")
        self.search_treeWidget.setHeaderItem(__qtreewidgetitem)
        self.search_treeWidget.setObjectName(u"search_treeWidget")

        self.verticalLayout.addWidget(self.search_treeWidget)

        self.search_add_pushButton = QPushButton(self.frame_4)
        self.search_add_pushButton.setObjectName(u"search_add_pushButton")

        self.verticalLayout.addWidget(self.search_add_pushButton)


        self.horizontalLayout_4.addWidget(self.frame_4)

        self.tabWidget.addTab(self.search_tab, "")

        self.verticalLayout_2.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(self.frame)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.verticalLayout_3.addWidget(self.frame)


        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Add series", None))
        self.TVDB_radioButton.setText(QCoreApplication.translate("Dialog", u"TVDB", None))
        self.TMDB_radioButton.setText(QCoreApplication.translate("Dialog", u"TMDB", None))
        self.AniList_radioButton.setText(QCoreApplication.translate("Dialog", u"AniList", None))
        self.MAL_radioButton.setText(QCoreApplication.translate("Dialog", u"MAL", None))
        self.scan_label.setText(QCoreApplication.translate("Dialog", u"Scan folder", None))
        self.scan_folder_browse_pushButton.setText(QCoreApplication.translate("Dialog", u"Browse", None))
        self.scan_start_pushButton.setText(QCoreApplication.translate("Dialog", u"Start scan", None))
        self.confirm_series_label.setText(QCoreApplication.translate("Dialog", u"Confirm series to search", None))
        self.scan_add_pushButton.setText(QCoreApplication.translate("Dialog", u"Add selected", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.scan_tab), QCoreApplication.translate("Dialog", u"Scan", None))
        self.search_label.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.search_pushButton.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.search_add_pushButton.setText(QCoreApplication.translate("Dialog", u"Add selected", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.search_tab), QCoreApplication.translate("Dialog", u"Search", None))
    # retranslateUi

