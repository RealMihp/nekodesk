# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pin_dialog.ui'
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
    QFrame, QLabel, QLineEdit, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_PIN_Dialog(object):
    def setupUi(self, PIN_Dialog):
        if not PIN_Dialog.objectName():
            PIN_Dialog.setObjectName(u"PIN_Dialog")
        PIN_Dialog.resize(306, 120)
        self.verticalLayout_2 = QVBoxLayout(PIN_Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.AniList_Auth_frame = QFrame(PIN_Dialog)
        self.AniList_Auth_frame.setObjectName(u"AniList_Auth_frame")
        self.AniList_Auth_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.AniList_Auth_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.AniList_Auth_frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.AniList_Auth_label = QLabel(self.AniList_Auth_frame)
        self.AniList_Auth_label.setObjectName(u"AniList_Auth_label")

        self.verticalLayout.addWidget(self.AniList_Auth_label)

        self.AniList_Auth_lineEdit = QLineEdit(self.AniList_Auth_frame)
        self.AniList_Auth_lineEdit.setObjectName(u"AniList_Auth_lineEdit")

        self.verticalLayout.addWidget(self.AniList_Auth_lineEdit)


        self.verticalLayout_2.addWidget(self.AniList_Auth_frame)

        self.AniList_Auth_buttonBox = QDialogButtonBox(PIN_Dialog)
        self.AniList_Auth_buttonBox.setObjectName(u"AniList_Auth_buttonBox")
        self.AniList_Auth_buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.AniList_Auth_buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Save)

        self.verticalLayout_2.addWidget(self.AniList_Auth_buttonBox)


        self.retranslateUi(PIN_Dialog)
        self.AniList_Auth_buttonBox.accepted.connect(PIN_Dialog.accept)
        self.AniList_Auth_buttonBox.rejected.connect(PIN_Dialog.reject)

        QMetaObject.connectSlotsByName(PIN_Dialog)
    # setupUi

    def retranslateUi(self, PIN_Dialog):
        PIN_Dialog.setWindowTitle(QCoreApplication.translate("PIN_Dialog", u"PIN Dialog", None))
        self.AniList_Auth_label.setText(QCoreApplication.translate("PIN_Dialog", u"Enter your PIN from the browser:", None))
    # retranslateUi

