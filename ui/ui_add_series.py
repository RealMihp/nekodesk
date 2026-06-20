# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_series.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_AddSeriesWindow(object):
    def setupUi(self, AddSeriesWindow):
        if not AddSeriesWindow.objectName():
            AddSeriesWindow.setObjectName(u"AddSeriesWindow")
        AddSeriesWindow.resize(750, 900)
        self.verticalLayout_3 = QVBoxLayout(AddSeriesWindow)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame = QFrame(AddSeriesWindow)
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
        self.AniList_radioButton = QRadioButton(self.engine_select_frame)
        self.AniList_radioButton.setObjectName(u"AniList_radioButton")
        self.AniList_radioButton.setEnabled(True)

        self.horizontalLayout.addWidget(self.AniList_radioButton)

        self.MAL_radioButton = QRadioButton(self.engine_select_frame)
        self.MAL_radioButton.setObjectName(u"MAL_radioButton")
        self.MAL_radioButton.setEnabled(True)

        self.horizontalLayout.addWidget(self.MAL_radioButton)


        self.verticalLayout_2.addWidget(self.engine_select_frame)

        self.tabWidget = QTabWidget(self.frame)
        self.tabWidget.setObjectName(u"tabWidget")
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
        self.search_pushButton.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.search_pushButton)


        self.verticalLayout.addWidget(self.search_frame)

        self.search_treeWidget = QTreeWidget(self.frame_4)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"Title")
        self.search_treeWidget.setHeaderItem(__qtreewidgetitem)
        self.search_treeWidget.setObjectName(u"search_treeWidget")
        self.search_treeWidget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.search_treeWidget.setSortingEnabled(True)
        self.search_treeWidget.header().setProperty(u"showSortIndicator", True)
        self.search_treeWidget.header().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.search_treeWidget)

        self.search_add_pushButton = QPushButton(self.frame_4)
        self.search_add_pushButton.setObjectName(u"search_add_pushButton")
        self.search_add_pushButton.setEnabled(False)

        self.verticalLayout.addWidget(self.search_add_pushButton)


        self.horizontalLayout_4.addWidget(self.frame_4)

        self.tabWidget.addTab(self.search_tab, "")
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
        self.scan_folder_lineEdit.setEnabled(False)

        self.horizontalLayout_3.addWidget(self.scan_folder_lineEdit)

        self.scan_folder_browse_pushButton = QPushButton(self.select_folder_frame)
        self.scan_folder_browse_pushButton.setObjectName(u"scan_folder_browse_pushButton")
        self.scan_folder_browse_pushButton.setEnabled(True)

        self.horizontalLayout_3.addWidget(self.scan_folder_browse_pushButton)


        self.verticalLayout_4.addWidget(self.select_folder_frame)

        self.scan_start_pushButton = QPushButton(self.scan_frame)
        self.scan_start_pushButton.setObjectName(u"scan_start_pushButton")
        self.scan_start_pushButton.setEnabled(False)

        self.verticalLayout_4.addWidget(self.scan_start_pushButton)

        self.confirm_series_label = QLabel(self.scan_frame)
        self.confirm_series_label.setObjectName(u"confirm_series_label")

        self.verticalLayout_4.addWidget(self.confirm_series_label)

        self.scan_results_treeWidget = QTreeWidget(self.scan_frame)
        self.scan_results_treeWidget.setObjectName(u"scan_results_treeWidget")
        self.scan_results_treeWidget.setDefaultDropAction(Qt.DropAction.IgnoreAction)
        self.scan_results_treeWidget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.scan_results_treeWidget.setSortingEnabled(True)
        self.scan_results_treeWidget.setSupportedDragActions(Qt.DropAction.IgnoreAction)
        self.scan_results_treeWidget.header().setStretchLastSection(False)

        self.verticalLayout_4.addWidget(self.scan_results_treeWidget)

        self.scan_add_pushButton = QPushButton(self.scan_frame)
        self.scan_add_pushButton.setObjectName(u"scan_add_pushButton")
        self.scan_add_pushButton.setEnabled(False)

        self.verticalLayout_4.addWidget(self.scan_add_pushButton)


        self.horizontalLayout_5.addWidget(self.scan_frame)

        self.tabWidget.addTab(self.scan_tab, "")

        self.verticalLayout_2.addWidget(self.tabWidget)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.statusbar_label = QLabel(self.frame)
        self.statusbar_label.setObjectName(u"statusbar_label")

        self.horizontalLayout_6.addWidget(self.statusbar_label)

        self.buttonBox = QDialogButtonBox(self.frame)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.horizontalLayout_6.addWidget(self.buttonBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)


        self.verticalLayout_3.addWidget(self.frame)


        self.retranslateUi(AddSeriesWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(AddSeriesWindow)
    # setupUi

    def retranslateUi(self, AddSeriesWindow):
        AddSeriesWindow.setWindowTitle(QCoreApplication.translate("AddSeriesWindow", u"Add series", None))
        self.AniList_radioButton.setText(QCoreApplication.translate("AddSeriesWindow", u"AniList", None))
        self.MAL_radioButton.setText(QCoreApplication.translate("AddSeriesWindow", u"MAL", None))
        self.search_label.setText(QCoreApplication.translate("AddSeriesWindow", u"Search", None))
        self.search_pushButton.setText(QCoreApplication.translate("AddSeriesWindow", u"Search", None))
        ___qtreewidgetitem = self.search_treeWidget.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("AddSeriesWindow", u"Status", None))
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("AddSeriesWindow", u"Year", None))
        self.search_add_pushButton.setText(QCoreApplication.translate("AddSeriesWindow", u"Add selected", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.search_tab), QCoreApplication.translate("AddSeriesWindow", u"Search", None))
        self.scan_label.setText(QCoreApplication.translate("AddSeriesWindow", u"Scan folder", None))
        self.scan_folder_browse_pushButton.setText(QCoreApplication.translate("AddSeriesWindow", u"Browse", None))
        self.scan_start_pushButton.setText(QCoreApplication.translate("AddSeriesWindow", u"Start scan", None))
        self.confirm_series_label.setText(QCoreApplication.translate("AddSeriesWindow", u"Results", None))
        ___qtreewidgetitem1 = self.scan_results_treeWidget.headerItem()
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("AddSeriesWindow", u"Status", None))
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("AddSeriesWindow", u"Year", None))
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("AddSeriesWindow", u"Title", None))
        self.scan_add_pushButton.setText(QCoreApplication.translate("AddSeriesWindow", u"Add selected", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.scan_tab), QCoreApplication.translate("AddSeriesWindow", u"Scan", None))
        self.statusbar_label.setText("")
    # retranslateUi

