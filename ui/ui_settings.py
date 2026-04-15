# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        if not SettingsWindow.objectName():
            SettingsWindow.setObjectName(u"SettingsWindow")
        SettingsWindow.resize(400, 484)
        self.verticalLayout = QVBoxLayout(SettingsWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.settings_tabWidget = QTabWidget(SettingsWindow)
        self.settings_tabWidget.setObjectName(u"settings_tabWidget")
        self.appearance_tab = QWidget()
        self.appearance_tab.setObjectName(u"appearance_tab")
        self.settings_tabWidget.addTab(self.appearance_tab, "")
        self.general_tab = QWidget()
        self.general_tab.setObjectName(u"general_tab")
        self.settings_tabWidget.addTab(self.general_tab, "")
        self.services_tab = QWidget()
        self.services_tab.setObjectName(u"services_tab")
        self.verticalLayout_4 = QVBoxLayout(self.services_tab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.serviceAniList_frame = QFrame(self.services_tab)
        self.serviceAniList_frame.setObjectName(u"serviceAniList_frame")
        self.serviceAniList_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.serviceAniList_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.serviceAniList_frame)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.serviceAniList_verticalLayout = QVBoxLayout()
        self.serviceAniList_verticalLayout.setObjectName(u"serviceAniList_verticalLayout")
        self.serviceAniList_label = QLabel(self.serviceAniList_frame)
        self.serviceAniList_label.setObjectName(u"serviceAniList_label")

        self.serviceAniList_verticalLayout.addWidget(self.serviceAniList_label)

        self.serviceAniList_horizontalLayout = QHBoxLayout()
        self.serviceAniList_horizontalLayout.setObjectName(u"serviceAniList_horizontalLayout")
        self.serviceAniList_lineEdit = QLineEdit(self.serviceAniList_frame)
        self.serviceAniList_lineEdit.setObjectName(u"serviceAniList_lineEdit")
        self.serviceAniList_lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.serviceAniList_lineEdit.setClearButtonEnabled(True)

        self.serviceAniList_horizontalLayout.addWidget(self.serviceAniList_lineEdit)

        self.serviceAniLis_Auth_pushButton = QPushButton(self.serviceAniList_frame)
        self.serviceAniLis_Auth_pushButton.setObjectName(u"serviceAniLis_Auth_pushButton")

        self.serviceAniList_horizontalLayout.addWidget(self.serviceAniLis_Auth_pushButton)


        self.serviceAniList_verticalLayout.addLayout(self.serviceAniList_horizontalLayout)


        self.verticalLayout_5.addLayout(self.serviceAniList_verticalLayout)


        self.verticalLayout_4.addWidget(self.serviceAniList_frame)

        self.serviceMAL_frame = QFrame(self.services_tab)
        self.serviceMAL_frame.setObjectName(u"serviceMAL_frame")
        self.serviceMAL_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.serviceMAL_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.serviceMAL_frame)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.serviceMAL_verticalLayout = QVBoxLayout()
        self.serviceMAL_verticalLayout.setObjectName(u"serviceMAL_verticalLayout")
        self.serviceMAL_label = QLabel(self.serviceMAL_frame)
        self.serviceMAL_label.setObjectName(u"serviceMAL_label")

        self.serviceMAL_verticalLayout.addWidget(self.serviceMAL_label)

        self.serviceMAL_horizontalLayout = QHBoxLayout()
        self.serviceMAL_horizontalLayout.setObjectName(u"serviceMAL_horizontalLayout")
        self.serviceMAL_lineEdit = QLineEdit(self.serviceMAL_frame)
        self.serviceMAL_lineEdit.setObjectName(u"serviceMAL_lineEdit")
        self.serviceMAL_lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.serviceMAL_lineEdit.setClearButtonEnabled(True)

        self.serviceMAL_horizontalLayout.addWidget(self.serviceMAL_lineEdit)

        self.serviceMAL_Auth_pushButton = QPushButton(self.serviceMAL_frame)
        self.serviceMAL_Auth_pushButton.setObjectName(u"serviceMAL_Auth_pushButton")

        self.serviceMAL_horizontalLayout.addWidget(self.serviceMAL_Auth_pushButton)


        self.serviceMAL_verticalLayout.addLayout(self.serviceMAL_horizontalLayout)


        self.verticalLayout_6.addLayout(self.serviceMAL_verticalLayout)


        self.verticalLayout_4.addWidget(self.serviceMAL_frame)

        self.serviceTVDB_frame = QFrame(self.services_tab)
        self.serviceTVDB_frame.setObjectName(u"serviceTVDB_frame")
        self.serviceTVDB_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.serviceTVDB_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.serviceTVDB_frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.serviceTVDB_label = QLabel(self.serviceTVDB_frame)
        self.serviceTVDB_label.setObjectName(u"serviceTVDB_label")

        self.verticalLayout_2.addWidget(self.serviceTVDB_label)

        self.serviceTVDB_lineEdit = QLineEdit(self.serviceTVDB_frame)
        self.serviceTVDB_lineEdit.setObjectName(u"serviceTVDB_lineEdit")
        self.serviceTVDB_lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.serviceTVDB_lineEdit.setClearButtonEnabled(True)

        self.verticalLayout_2.addWidget(self.serviceTVDB_lineEdit)


        self.verticalLayout_4.addWidget(self.serviceTVDB_frame)

        self.serviceTMDB_frame = QFrame(self.services_tab)
        self.serviceTMDB_frame.setObjectName(u"serviceTMDB_frame")
        self.serviceTMDB_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.serviceTMDB_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.serviceTMDB_frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.serviceTMDB_label = QLabel(self.serviceTMDB_frame)
        self.serviceTMDB_label.setObjectName(u"serviceTMDB_label")

        self.verticalLayout_3.addWidget(self.serviceTMDB_label)

        self.serviceTMDB_lineEdit = QLineEdit(self.serviceTMDB_frame)
        self.serviceTMDB_lineEdit.setObjectName(u"serviceTMDB_lineEdit")
        self.serviceTMDB_lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.serviceTMDB_lineEdit.setClearButtonEnabled(True)

        self.verticalLayout_3.addWidget(self.serviceTMDB_lineEdit)


        self.verticalLayout_4.addWidget(self.serviceTMDB_frame)

        self.settings_tabWidget.addTab(self.services_tab, "")

        self.verticalLayout.addWidget(self.settings_tabWidget)

        self.settings_buttonBox = QDialogButtonBox(SettingsWindow)
        self.settings_buttonBox.setObjectName(u"settings_buttonBox")
        self.settings_buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.settings_buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.settings_buttonBox)


        self.retranslateUi(SettingsWindow)
        self.settings_buttonBox.accepted.connect(SettingsWindow.accept)
        self.settings_buttonBox.rejected.connect(SettingsWindow.reject)

        self.settings_tabWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(SettingsWindow)
    # setupUi

    def retranslateUi(self, SettingsWindow):
        SettingsWindow.setWindowTitle(QCoreApplication.translate("SettingsWindow", u"Settings", None))
        self.settings_tabWidget.setTabText(self.settings_tabWidget.indexOf(self.appearance_tab), QCoreApplication.translate("SettingsWindow", u"Appearance", None))
        self.settings_tabWidget.setTabText(self.settings_tabWidget.indexOf(self.general_tab), QCoreApplication.translate("SettingsWindow", u"General", None))
        self.serviceAniList_label.setText(QCoreApplication.translate("SettingsWindow", u"AniList API Key", None))
        self.serviceAniList_lineEdit.setText("")
        self.serviceAniLis_Auth_pushButton.setText(QCoreApplication.translate("SettingsWindow", u"Auth", None))
        self.serviceMAL_label.setText(QCoreApplication.translate("SettingsWindow", u"MAL API Key", None))
        self.serviceMAL_lineEdit.setText("")
        self.serviceMAL_Auth_pushButton.setText(QCoreApplication.translate("SettingsWindow", u"Auth", None))
        self.serviceTVDB_label.setText(QCoreApplication.translate("SettingsWindow", u"TVDB API Key", None))
        self.serviceTVDB_lineEdit.setText("")
        self.serviceTMDB_label.setText(QCoreApplication.translate("SettingsWindow", u"TMDB API Key", None))
        self.serviceTMDB_lineEdit.setText("")
        self.settings_tabWidget.setTabText(self.settings_tabWidget.indexOf(self.services_tab), QCoreApplication.translate("SettingsWindow", u"Services", None))
    # retranslateUi

