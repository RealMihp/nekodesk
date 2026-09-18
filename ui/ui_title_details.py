# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'title_details.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractScrollArea, QApplication, QDialogButtonBox,
    QFrame, QHBoxLayout, QLabel, QLayout,
    QScrollArea, QSizePolicy, QSpacerItem, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_details_widget(object):
    def setupUi(self, details_widget):
        if not details_widget.objectName():
            details_widget.setObjectName(u"details_widget")
        details_widget.resize(800, 700)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(details_widget.sizePolicy().hasHeightForWidth())
        details_widget.setSizePolicy(sizePolicy)
        details_widget.setMinimumSize(QSize(800, 700))
        details_widget.setMaximumSize(QSize(800, 700))
        self.verticalLayout_3 = QVBoxLayout(details_widget)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 6)
        self.main_verticalLayout = QVBoxLayout()
        self.main_verticalLayout.setObjectName(u"main_verticalLayout")
        self.banner_label = QLabel(details_widget)
        self.banner_label.setObjectName(u"banner_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.banner_label.sizePolicy().hasHeightForWidth())
        self.banner_label.setSizePolicy(sizePolicy1)
        self.banner_label.setMinimumSize(QSize(0, 0))
        self.banner_label.setMaximumSize(QSize(798, 146))
        self.banner_label.setFrameShape(QFrame.Shape.StyledPanel)
        self.banner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_verticalLayout.addWidget(self.banner_label)

        self.info_horizontalLayout = QHBoxLayout()
        self.info_horizontalLayout.setObjectName(u"info_horizontalLayout")
        self.info_horizontalLayout.setContentsMargins(-1, -1, 0, -1)
        self.poster_frame = QFrame(details_widget)
        self.poster_frame.setObjectName(u"poster_frame")
        self.poster_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.poster_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.poster_frame)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.poster_label = QLabel(self.poster_frame)
        self.poster_label.setObjectName(u"poster_label")
        sizePolicy1.setHeightForWidth(self.poster_label.sizePolicy().hasHeightForWidth())
        self.poster_label.setSizePolicy(sizePolicy1)
        self.poster_label.setMinimumSize(QSize(0, 0))
        self.poster_label.setMaximumSize(QSize(16777215, 16777215))
        self.poster_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.poster_label.setFrameShape(QFrame.Shape.StyledPanel)
        self.poster_label.setScaledContents(False)
        self.poster_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.poster_label.setOpenExternalLinks(True)

        self.verticalLayout_5.addWidget(self.poster_label)

        self.poster_verticalSpacer = QSpacerItem(20, 119, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.poster_verticalSpacer)

        self.verticalLayout_5.setStretch(0, 5)
        self.verticalLayout_5.setStretch(1, 4)

        self.info_horizontalLayout.addWidget(self.poster_frame)

        self.main_info_verticalLayout = QVBoxLayout()
        self.main_info_verticalLayout.setSpacing(0)
        self.main_info_verticalLayout.setObjectName(u"main_info_verticalLayout")
        self.main_info_verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.main_info_verticalLayout.setContentsMargins(0, -1, 9, -1)
        self.title_label = QLabel(details_widget)
        self.title_label.setObjectName(u"title_label")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet(u"")
        self.title_label.setMargin(0)
        self.title_label.setIndent(0)

        self.main_info_verticalLayout.addWidget(self.title_label)

        self.tabWidget = QTabWidget(details_widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabBarAutoHide(True)
        self.main_info_tab = QWidget()
        self.main_info_tab.setObjectName(u"main_info_tab")
        self.verticalLayout_4 = QVBoxLayout(self.main_info_tab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.synonyms_verticalLayout = QVBoxLayout()
        self.synonyms_verticalLayout.setSpacing(2)
        self.synonyms_verticalLayout.setObjectName(u"synonyms_verticalLayout")
        self.synonyms_header_label = QLabel(self.main_info_tab)
        self.synonyms_header_label.setObjectName(u"synonyms_header_label")
        font1 = QFont()
        font1.setBold(True)
        font1.setUnderline(False)
        self.synonyms_header_label.setFont(font1)

        self.synonyms_verticalLayout.addWidget(self.synonyms_header_label)

        self.synonyms_line = QFrame(self.main_info_tab)
        self.synonyms_line.setObjectName(u"synonyms_line")
        self.synonyms_line.setFrameShape(QFrame.Shape.HLine)
        self.synonyms_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.synonyms_verticalLayout.addWidget(self.synonyms_line)

        self.synonyms_scrollArea = QScrollArea(self.main_info_tab)
        self.synonyms_scrollArea.setObjectName(u"synonyms_scrollArea")
        sizePolicy1.setHeightForWidth(self.synonyms_scrollArea.sizePolicy().hasHeightForWidth())
        self.synonyms_scrollArea.setSizePolicy(sizePolicy1)
        self.synonyms_scrollArea.setMaximumSize(QSize(16777215, 35))
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush)
        self.synonyms_scrollArea.setPalette(palette)
        self.synonyms_scrollArea.setStyleSheet(u"")
        self.synonyms_scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.synonyms_scrollArea.setFrameShadow(QFrame.Shadow.Sunken)
        self.synonyms_scrollArea.setLineWidth(1)
        self.synonyms_scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.synonyms_scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.synonyms_scrollArea.setWidgetResizable(True)
        self.synonyms_scrollAreaWidgetContents = QWidget()
        self.synonyms_scrollAreaWidgetContents.setObjectName(u"synonyms_scrollAreaWidgetContents")
        self.synonyms_scrollAreaWidgetContents.setGeometry(QRect(0, 0, 556, 35))
        self.synonyms_scrollAreaWidgetContents.setMaximumSize(QSize(16777215, 16777215))
        self.synonyms_scrollAreaWidgetContents.setAutoFillBackground(True)
        self.verticalLayout_2 = QVBoxLayout(self.synonyms_scrollAreaWidgetContents)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.synonyms_label = QLabel(self.synonyms_scrollAreaWidgetContents)
        self.synonyms_label.setObjectName(u"synonyms_label")
        self.synonyms_label.setMaximumSize(QSize(16777215, 16777215))
        self.synonyms_label.setMargin(0)

        self.verticalLayout_2.addWidget(self.synonyms_label)

        self.synonyms_scrollArea.setWidget(self.synonyms_scrollAreaWidgetContents)

        self.synonyms_verticalLayout.addWidget(self.synonyms_scrollArea)

        self.synonyms_verticalLayout.setStretch(0, 1)
        self.synonyms_verticalLayout.setStretch(1, 1)
        self.synonyms_verticalLayout.setStretch(2, 1)

        self.verticalLayout_4.addLayout(self.synonyms_verticalLayout)

        self.details_verticalLayout = QVBoxLayout()
        self.details_verticalLayout.setSpacing(2)
        self.details_verticalLayout.setObjectName(u"details_verticalLayout")
        self.details_header_label = QLabel(self.main_info_tab)
        self.details_header_label.setObjectName(u"details_header_label")
        font2 = QFont()
        font2.setBold(True)
        self.details_header_label.setFont(font2)

        self.details_verticalLayout.addWidget(self.details_header_label)

        self.details_header_line = QFrame(self.main_info_tab)
        self.details_header_line.setObjectName(u"details_header_line")
        self.details_header_line.setFrameShape(QFrame.Shape.HLine)
        self.details_header_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.details_verticalLayout.addWidget(self.details_header_line)

        self.type_label = QLabel(self.main_info_tab)
        self.type_label.setObjectName(u"type_label")

        self.details_verticalLayout.addWidget(self.type_label)

        self.episodes_label = QLabel(self.main_info_tab)
        self.episodes_label.setObjectName(u"episodes_label")

        self.details_verticalLayout.addWidget(self.episodes_label)

        self.status_label = QLabel(self.main_info_tab)
        self.status_label.setObjectName(u"status_label")

        self.details_verticalLayout.addWidget(self.status_label)

        self.score_label = QLabel(self.main_info_tab)
        self.score_label.setObjectName(u"score_label")

        self.details_verticalLayout.addWidget(self.score_label)

        self.season_label = QLabel(self.main_info_tab)
        self.season_label.setObjectName(u"season_label")

        self.details_verticalLayout.addWidget(self.season_label)

        self.genres_label = QLabel(self.main_info_tab)
        self.genres_label.setObjectName(u"genres_label")

        self.details_verticalLayout.addWidget(self.genres_label)

        self.studio_label = QLabel(self.main_info_tab)
        self.studio_label.setObjectName(u"studio_label")

        self.details_verticalLayout.addWidget(self.studio_label)


        self.verticalLayout_4.addLayout(self.details_verticalLayout)

        self.desc_verticalLayout = QVBoxLayout()
        self.desc_verticalLayout.setSpacing(2)
        self.desc_verticalLayout.setObjectName(u"desc_verticalLayout")
        self.desc_header_label = QLabel(self.main_info_tab)
        self.desc_header_label.setObjectName(u"desc_header_label")
        self.desc_header_label.setFont(font2)

        self.desc_verticalLayout.addWidget(self.desc_header_label)

        self.desc_header_line = QFrame(self.main_info_tab)
        self.desc_header_line.setObjectName(u"desc_header_line")
        self.desc_header_line.setFrameShape(QFrame.Shape.HLine)
        self.desc_header_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.desc_verticalLayout.addWidget(self.desc_header_line)

        self.desc_scrollArea = QScrollArea(self.main_info_tab)
        self.desc_scrollArea.setObjectName(u"desc_scrollArea")
        palette1 = QPalette()
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush)
        self.desc_scrollArea.setPalette(palette1)
        self.desc_scrollArea.setStyleSheet(u"")
        self.desc_scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.desc_scrollArea.setFrameShadow(QFrame.Shadow.Sunken)
        self.desc_scrollArea.setWidgetResizable(True)
        self.desc_scrollAreaWidgetContents = QWidget()
        self.desc_scrollAreaWidgetContents.setObjectName(u"desc_scrollAreaWidgetContents")
        self.desc_scrollAreaWidgetContents.setGeometry(QRect(0, 0, 556, 189))
        self.desc_scrollAreaWidgetContents.setAutoFillBackground(True)
        self.verticalLayout = QVBoxLayout(self.desc_scrollAreaWidgetContents)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.desc_label = QLabel(self.desc_scrollAreaWidgetContents)
        self.desc_label.setObjectName(u"desc_label")
        self.desc_label.setTextFormat(Qt.TextFormat.RichText)
        self.desc_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.desc_label.setWordWrap(True)
        self.desc_label.setOpenExternalLinks(True)
        self.desc_label.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout.addWidget(self.desc_label)

        self.desc_scrollArea.setWidget(self.desc_scrollAreaWidgetContents)

        self.desc_verticalLayout.addWidget(self.desc_scrollArea)

        self.desc_verticalLayout.setStretch(2, 5)

        self.verticalLayout_4.addLayout(self.desc_verticalLayout)

        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(1, 4)
        self.verticalLayout_4.setStretch(2, 6)
        self.tabWidget.addTab(self.main_info_tab, "")

        self.main_info_verticalLayout.addWidget(self.tabWidget)

        self.main_info_verticalLayout.setStretch(0, 1)
        self.main_info_verticalLayout.setStretch(1, 10)

        self.info_horizontalLayout.addLayout(self.main_info_verticalLayout)

        self.info_horizontalLayout.setStretch(0, 2)
        self.info_horizontalLayout.setStretch(1, 6)

        self.main_verticalLayout.addLayout(self.info_horizontalLayout)

        self.main_verticalLayout.setStretch(0, 2)
        self.main_verticalLayout.setStretch(1, 7)

        self.verticalLayout_3.addLayout(self.main_verticalLayout)

        self.buttonBox_horizontalLayout = QHBoxLayout()
        self.buttonBox_horizontalLayout.setSpacing(0)
        self.buttonBox_horizontalLayout.setObjectName(u"buttonBox_horizontalLayout")
        self.buttonBox = QDialogButtonBox(details_widget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.buttonBox_horizontalLayout.addWidget(self.buttonBox)

        self.horizontalSpacer = QSpacerItem(9, 0, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.buttonBox_horizontalLayout.addItem(self.horizontalSpacer)

        self.buttonBox_horizontalLayout.setStretch(0, 1)

        self.verticalLayout_3.addLayout(self.buttonBox_horizontalLayout)


        self.retranslateUi(details_widget)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(details_widget)
    # setupUi

    def retranslateUi(self, details_widget):
        details_widget.setWindowTitle(QCoreApplication.translate("details_widget", u"Details", None))
        self.banner_label.setText("")
        self.poster_label.setText("")
        self.title_label.setText(QCoreApplication.translate("details_widget", u"Title", None))
        self.synonyms_header_label.setText(QCoreApplication.translate("details_widget", u"Synonyms", None))
        self.synonyms_label.setText(QCoreApplication.translate("details_widget", u"Synonyms", None))
        self.details_header_label.setText(QCoreApplication.translate("details_widget", u"Details", None))
        self.type_label.setText(QCoreApplication.translate("details_widget", u"Type: ", None))
        self.episodes_label.setText(QCoreApplication.translate("details_widget", u"Episodes: ", None))
        self.status_label.setText(QCoreApplication.translate("details_widget", u"Status:", None))
        self.score_label.setText(QCoreApplication.translate("details_widget", u"Avg. Score:", None))
        self.season_label.setText(QCoreApplication.translate("details_widget", u"Season: ", None))
        self.genres_label.setText(QCoreApplication.translate("details_widget", u"Genres: ", None))
        self.studio_label.setText(QCoreApplication.translate("details_widget", u"Studio:", None))
        self.desc_header_label.setText(QCoreApplication.translate("details_widget", u"Description", None))
        self.desc_label.setText(QCoreApplication.translate("details_widget", u"Description", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.main_info_tab), QCoreApplication.translate("details_widget", u"Main Info", None))
    # retranslateUi

