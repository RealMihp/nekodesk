# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_about_widget(object):
    def setupUi(self, about_widget):
        if not about_widget.objectName():
            about_widget.setObjectName(u"about_widget")
        about_widget.resize(700, 500)
        self.verticalLayout = QVBoxLayout(about_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.icon_label = QLabel(about_widget)
        self.icon_label.setObjectName(u"icon_label")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.horizontalLayout.addWidget(self.icon_label)

        self.app_name_label = QLabel(about_widget)
        self.app_name_label.setObjectName(u"app_name_label")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.app_name_label.setFont(font)

        self.horizontalLayout.addWidget(self.app_name_label)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.about_text_label = QLabel(about_widget)
        self.about_text_label.setObjectName(u"about_text_label")
        self.about_text_label.setTextFormat(Qt.TextFormat.RichText)
        self.about_text_label.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft)
        self.about_text_label.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.about_text_label)

        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(about_widget)

        QMetaObject.connectSlotsByName(about_widget)
    # setupUi

    def retranslateUi(self, about_widget):
        about_widget.setWindowTitle(QCoreApplication.translate("about_widget", u"About", None))
        self.icon_label.setText(QCoreApplication.translate("about_widget", u"Icon", None))
        self.app_name_label.setText(QCoreApplication.translate("about_widget", u"App Name", None))
        self.about_text_label.setText(QCoreApplication.translate("about_widget", u"About text", None))
    # retranslateUi

