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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        if not SettingsWindow.objectName():
            SettingsWindow.setObjectName(u"SettingsWindow")
        SettingsWindow.resize(638, 484)
        self.verticalLayout = QVBoxLayout(SettingsWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.settings_tabWidget = QTabWidget(SettingsWindow)
        self.settings_tabWidget.setObjectName(u"settings_tabWidget")
        self.appearance_tab = QWidget()
        self.appearance_tab.setObjectName(u"appearance_tab")
        self.verticalLayout_7 = QVBoxLayout(self.appearance_tab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.theme_label = QLabel(self.appearance_tab)
        self.theme_label.setObjectName(u"theme_label")

        self.verticalLayout_2.addWidget(self.theme_label)

        self.theme_select_frame = QFrame(self.appearance_tab)
        self.theme_select_frame.setObjectName(u"theme_select_frame")
        self.theme_select_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.theme_select_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.theme_select_frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.theme_system_radioButton = QRadioButton(self.theme_select_frame)
        self.theme_system_radioButton.setObjectName(u"theme_system_radioButton")
        self.theme_system_radioButton.setEnabled(True)

        self.horizontalLayout_3.addWidget(self.theme_system_radioButton)

        self.theme_light_radioButton = QRadioButton(self.theme_select_frame)
        self.theme_light_radioButton.setObjectName(u"theme_light_radioButton")
        self.theme_light_radioButton.setEnabled(True)

        self.horizontalLayout_3.addWidget(self.theme_light_radioButton)

        self.theme_dark_radioButton = QRadioButton(self.theme_select_frame)
        self.theme_dark_radioButton.setObjectName(u"theme_dark_radioButton")
        self.theme_dark_radioButton.setEnabled(True)

        self.horizontalLayout_3.addWidget(self.theme_dark_radioButton)


        self.verticalLayout_2.addWidget(self.theme_select_frame)


        self.verticalLayout_7.addLayout(self.verticalLayout_2)

        self.settings_tabWidget.addTab(self.appearance_tab, "")
        self.general_tab = QWidget()
        self.general_tab.setObjectName(u"general_tab")
        self.verticalLayout_3 = QVBoxLayout(self.general_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.files_template_verticalLayout = QVBoxLayout()
        self.files_template_verticalLayout.setObjectName(u"files_template_verticalLayout")
        self.files_template_horizontalLayout = QHBoxLayout()
        self.files_template_horizontalLayout.setObjectName(u"files_template_horizontalLayout")
        self.files_template_label = QLabel(self.general_tab)
        self.files_template_label.setObjectName(u"files_template_label")

        self.files_template_horizontalLayout.addWidget(self.files_template_label)

        self.files_template_pushButton = QPushButton(self.general_tab)
        self.files_template_pushButton.setObjectName(u"files_template_pushButton")
        self.files_template_pushButton.setMaximumSize(QSize(30, 30))

        self.files_template_horizontalLayout.addWidget(self.files_template_pushButton)


        self.files_template_verticalLayout.addLayout(self.files_template_horizontalLayout)

        self.files_template_lineEdit = QLineEdit(self.general_tab)
        self.files_template_lineEdit.setObjectName(u"files_template_lineEdit")

        self.files_template_verticalLayout.addWidget(self.files_template_lineEdit)


        self.verticalLayout_3.addLayout(self.files_template_verticalLayout)

        self.folder_template_verticalLayout = QVBoxLayout()
        self.folder_template_verticalLayout.setObjectName(u"folder_template_verticalLayout")
        self.folder_template_horizontalLayout = QHBoxLayout()
        self.folder_template_horizontalLayout.setObjectName(u"folder_template_horizontalLayout")
        self.folder_template_label = QLabel(self.general_tab)
        self.folder_template_label.setObjectName(u"folder_template_label")

        self.folder_template_horizontalLayout.addWidget(self.folder_template_label)

        self.folder_template_pushButton = QPushButton(self.general_tab)
        self.folder_template_pushButton.setObjectName(u"folder_template_pushButton")
        self.folder_template_pushButton.setMaximumSize(QSize(30, 30))

        self.folder_template_horizontalLayout.addWidget(self.folder_template_pushButton)


        self.folder_template_verticalLayout.addLayout(self.folder_template_horizontalLayout)

        self.folder_template_lineEdit = QLineEdit(self.general_tab)
        self.folder_template_lineEdit.setObjectName(u"folder_template_lineEdit")

        self.folder_template_verticalLayout.addWidget(self.folder_template_lineEdit)


        self.verticalLayout_3.addLayout(self.folder_template_verticalLayout)

        self.offline_mode_horizontalLayout = QHBoxLayout()
        self.offline_mode_horizontalLayout.setObjectName(u"offline_mode_horizontalLayout")
        self.offline_mode_checkBox = QCheckBox(self.general_tab)
        self.offline_mode_checkBox.setObjectName(u"offline_mode_checkBox")

        self.offline_mode_horizontalLayout.addWidget(self.offline_mode_checkBox)

        self.offline_mode_pushButton = QPushButton(self.general_tab)
        self.offline_mode_pushButton.setObjectName(u"offline_mode_pushButton")
        self.offline_mode_pushButton.setMaximumSize(QSize(30, 30))

        self.offline_mode_horizontalLayout.addWidget(self.offline_mode_pushButton)


        self.verticalLayout_3.addLayout(self.offline_mode_horizontalLayout)

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

        self.settings_tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(SettingsWindow)
    # setupUi

    def retranslateUi(self, SettingsWindow):
        SettingsWindow.setWindowTitle(QCoreApplication.translate("SettingsWindow", u"Settings", None))
        self.theme_label.setText(QCoreApplication.translate("SettingsWindow", u"Theme", None))
        self.theme_system_radioButton.setText(QCoreApplication.translate("SettingsWindow", u"System", None))
        self.theme_light_radioButton.setText(QCoreApplication.translate("SettingsWindow", u"Light", None))
        self.theme_dark_radioButton.setText(QCoreApplication.translate("SettingsWindow", u"Dark", None))
        self.settings_tabWidget.setTabText(self.settings_tabWidget.indexOf(self.appearance_tab), QCoreApplication.translate("SettingsWindow", u"Appearance", None))
        self.files_template_label.setText(QCoreApplication.translate("SettingsWindow", u"Files Template :", None))
        self.files_template_pushButton.setText(QCoreApplication.translate("SettingsWindow", u"?", None))
        self.folder_template_label.setText(QCoreApplication.translate("SettingsWindow", u"Folder Template :", None))
        self.folder_template_pushButton.setText(QCoreApplication.translate("SettingsWindow", u"?", None))
        self.offline_mode_checkBox.setText(QCoreApplication.translate("SettingsWindow", u"Offline mode", None))
        self.offline_mode_pushButton.setText(QCoreApplication.translate("SettingsWindow", u"?", None))
        self.settings_tabWidget.setTabText(self.settings_tabWidget.indexOf(self.general_tab), QCoreApplication.translate("SettingsWindow", u"General", None))
        self.serviceAniList_label.setText(QCoreApplication.translate("SettingsWindow", u"AniList", None))
        self.serviceAniList_lineEdit.setText("")
        self.serviceAniLis_Auth_pushButton.setText(QCoreApplication.translate("SettingsWindow", u"Auth", None))
        self.serviceMAL_label.setText(QCoreApplication.translate("SettingsWindow", u"MyAnimeList (MAL)", None))
        self.serviceMAL_lineEdit.setText("")
        self.serviceMAL_Auth_pushButton.setText(QCoreApplication.translate("SettingsWindow", u"Auth", None))
        self.settings_tabWidget.setTabText(self.settings_tabWidget.indexOf(self.services_tab), QCoreApplication.translate("SettingsWindow", u"Services", None))
    # retranslateUi

