# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rename_dialog.ui'
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
    QDialogButtonBox, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QLayout, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_RenameDialog(object):
    def setupUi(self, RenameDialog):
        if not RenameDialog.objectName():
            RenameDialog.setObjectName(u"RenameDialog")
        RenameDialog.resize(1000, 800)
        RenameDialog.setMaximumSize(QSize(1000, 800))
        RenameDialog.setSizeGripEnabled(False)
        self.verticalLayout_7 = QVBoxLayout(RenameDialog)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.banner_label = QLabel(RenameDialog)
        self.banner_label.setObjectName(u"banner_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.banner_label.sizePolicy().hasHeightForWidth())
        self.banner_label.setSizePolicy(sizePolicy)
        self.banner_label.setMinimumSize(QSize(0, 0))
        self.banner_label.setMaximumSize(QSize(998, 183))
        self.banner_label.setFrameShape(QFrame.Shape.StyledPanel)
        self.banner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.banner_label)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.title_horizontalLayout = QHBoxLayout()
        self.title_horizontalLayout.setObjectName(u"title_horizontalLayout")
        self.title_label = QLabel(RenameDialog)
        self.title_label.setObjectName(u"title_label")

        self.title_horizontalLayout.addWidget(self.title_label)

        self.title_lineEdit = QLineEdit(RenameDialog)
        self.title_lineEdit.setObjectName(u"title_lineEdit")

        self.title_horizontalLayout.addWidget(self.title_lineEdit)


        self.verticalLayout_6.addLayout(self.title_horizontalLayout)

        self.line = QFrame(RenameDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_6.addWidget(self.line)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.season_num_horizontalLayout = QHBoxLayout()
        self.season_num_horizontalLayout.setObjectName(u"season_num_horizontalLayout")
        self.season_num_label = QLabel(RenameDialog)
        self.season_num_label.setObjectName(u"season_num_label")

        self.season_num_horizontalLayout.addWidget(self.season_num_label)

        self.season_num_lineEdit = QLineEdit(RenameDialog)
        self.season_num_lineEdit.setObjectName(u"season_num_lineEdit")
        self.season_num_lineEdit.setClearButtonEnabled(False)

        self.season_num_horizontalLayout.addWidget(self.season_num_lineEdit)


        self.verticalLayout.addLayout(self.season_num_horizontalLayout)

        self.season_horizontalLayout = QHBoxLayout()
        self.season_horizontalLayout.setObjectName(u"season_horizontalLayout")
        self.season_label = QLabel(RenameDialog)
        self.season_label.setObjectName(u"season_label")

        self.season_horizontalLayout.addWidget(self.season_label)

        self.season_lineEdit = QLineEdit(RenameDialog)
        self.season_lineEdit.setObjectName(u"season_lineEdit")

        self.season_horizontalLayout.addWidget(self.season_lineEdit)

        self.season_year_label = QLabel(RenameDialog)
        self.season_year_label.setObjectName(u"season_year_label")

        self.season_horizontalLayout.addWidget(self.season_year_label)

        self.season_year_lineEdit = QLineEdit(RenameDialog)
        self.season_year_lineEdit.setObjectName(u"season_year_lineEdit")

        self.season_horizontalLayout.addWidget(self.season_year_lineEdit)


        self.verticalLayout.addLayout(self.season_horizontalLayout)

        self.type_horizontalLayout = QHBoxLayout()
        self.type_horizontalLayout.setObjectName(u"type_horizontalLayout")
        self.type_label = QLabel(RenameDialog)
        self.type_label.setObjectName(u"type_label")

        self.type_horizontalLayout.addWidget(self.type_label)

        self.type_lineEdit = QLineEdit(RenameDialog)
        self.type_lineEdit.setObjectName(u"type_lineEdit")

        self.type_horizontalLayout.addWidget(self.type_lineEdit)


        self.verticalLayout.addLayout(self.type_horizontalLayout)

        self.studio_horizontalLayout = QHBoxLayout()
        self.studio_horizontalLayout.setObjectName(u"studio_horizontalLayout")
        self.studio_label = QLabel(RenameDialog)
        self.studio_label.setObjectName(u"studio_label")

        self.studio_horizontalLayout.addWidget(self.studio_label)

        self.studio_lineEdit = QLineEdit(RenameDialog)
        self.studio_lineEdit.setObjectName(u"studio_lineEdit")

        self.studio_horizontalLayout.addWidget(self.studio_lineEdit)


        self.verticalLayout.addLayout(self.studio_horizontalLayout)

        self.duration_horizontalLayout = QHBoxLayout()
        self.duration_horizontalLayout.setObjectName(u"duration_horizontalLayout")
        self.duration_label = QLabel(RenameDialog)
        self.duration_label.setObjectName(u"duration_label")

        self.duration_horizontalLayout.addWidget(self.duration_label)

        self.duration_lineEdit = QLineEdit(RenameDialog)
        self.duration_lineEdit.setObjectName(u"duration_lineEdit")

        self.duration_horizontalLayout.addWidget(self.duration_lineEdit)


        self.verticalLayout.addLayout(self.duration_horizontalLayout)

        self.source_horizontalLayout = QHBoxLayout()
        self.source_horizontalLayout.setObjectName(u"source_horizontalLayout")
        self.source_label = QLabel(RenameDialog)
        self.source_label.setObjectName(u"source_label")

        self.source_horizontalLayout.addWidget(self.source_label)

        self.source_lineEdit = QLineEdit(RenameDialog)
        self.source_lineEdit.setObjectName(u"source_lineEdit")

        self.source_horizontalLayout.addWidget(self.source_lineEdit)


        self.verticalLayout.addLayout(self.source_horizontalLayout)

        self.resolution_horizontalLayout = QHBoxLayout()
        self.resolution_horizontalLayout.setObjectName(u"resolution_horizontalLayout")
        self.resolution_label = QLabel(RenameDialog)
        self.resolution_label.setObjectName(u"resolution_label")

        self.resolution_horizontalLayout.addWidget(self.resolution_label)

        self.resolution_lineEdit = QLineEdit(RenameDialog)
        self.resolution_lineEdit.setObjectName(u"resolution_lineEdit")

        self.resolution_horizontalLayout.addWidget(self.resolution_lineEdit)


        self.verticalLayout.addLayout(self.resolution_horizontalLayout)

        self.fansub_horizontalLayout = QHBoxLayout()
        self.fansub_horizontalLayout.setObjectName(u"fansub_horizontalLayout")
        self.fansub_label = QLabel(RenameDialog)
        self.fansub_label.setObjectName(u"fansub_label")

        self.fansub_horizontalLayout.addWidget(self.fansub_label)

        self.fansub_lineEdit = QLineEdit(RenameDialog)
        self.fansub_lineEdit.setObjectName(u"fansub_lineEdit")

        self.fansub_horizontalLayout.addWidget(self.fansub_lineEdit)


        self.verticalLayout.addLayout(self.fansub_horizontalLayout)

        self.left_verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.left_verticalSpacer_2)

        self.left_line = QFrame(RenameDialog)
        self.left_line.setObjectName(u"left_line")
        self.left_line.setFrameShape(QFrame.Shape.HLine)
        self.left_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.left_line)

        self.country_horizontalLayout = QHBoxLayout()
        self.country_horizontalLayout.setObjectName(u"country_horizontalLayout")
        self.country_horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.country_label = QLabel(RenameDialog)
        self.country_label.setObjectName(u"country_label")

        self.country_horizontalLayout.addWidget(self.country_label)

        self.country_lineEdit = QLineEdit(RenameDialog)
        self.country_lineEdit.setObjectName(u"country_lineEdit")

        self.country_horizontalLayout.addWidget(self.country_lineEdit)


        self.verticalLayout.addLayout(self.country_horizontalLayout)

        self.score_horizontalLayout = QHBoxLayout()
        self.score_horizontalLayout.setObjectName(u"score_horizontalLayout")
        self.score_label = QLabel(RenameDialog)
        self.score_label.setObjectName(u"score_label")

        self.score_horizontalLayout.addWidget(self.score_label)

        self.score_lineEdit = QLineEdit(RenameDialog)
        self.score_lineEdit.setObjectName(u"score_lineEdit")

        self.score_horizontalLayout.addWidget(self.score_lineEdit)


        self.verticalLayout.addLayout(self.score_horizontalLayout)

        self.status_horizontalLayout = QHBoxLayout()
        self.status_horizontalLayout.setObjectName(u"status_horizontalLayout")
        self.status_label = QLabel(RenameDialog)
        self.status_label.setObjectName(u"status_label")

        self.status_horizontalLayout.addWidget(self.status_label)

        self.status_lineEdit = QLineEdit(RenameDialog)
        self.status_lineEdit.setObjectName(u"status_lineEdit")

        self.status_horizontalLayout.addWidget(self.status_lineEdit)


        self.verticalLayout.addLayout(self.status_horizontalLayout)

        self.left_verticalSpacer = QSpacerItem(20, 13, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.left_verticalSpacer)

        self.left_line_2 = QFrame(RenameDialog)
        self.left_line_2.setObjectName(u"left_line_2")
        self.left_line_2.setFrameShape(QFrame.Shape.HLine)
        self.left_line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.left_line_2)

        self.episodes_verticalLayout = QVBoxLayout()
        self.episodes_verticalLayout.setObjectName(u"episodes_verticalLayout")
        self.episodes_horizontalLayout = QHBoxLayout()
        self.episodes_horizontalLayout.setObjectName(u"episodes_horizontalLayout")
        self.episodes_horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.episodes_label = QLabel(RenameDialog)
        self.episodes_label.setObjectName(u"episodes_label")

        self.episodes_horizontalLayout.addWidget(self.episodes_label)

        self.episodes_lineEdit = QLineEdit(RenameDialog)
        self.episodes_lineEdit.setObjectName(u"episodes_lineEdit")

        self.episodes_horizontalLayout.addWidget(self.episodes_lineEdit)

        self.episodes_in_folder_label = QLabel(RenameDialog)
        self.episodes_in_folder_label.setObjectName(u"episodes_in_folder_label")

        self.episodes_horizontalLayout.addWidget(self.episodes_in_folder_label)

        self.episodes_horizontalLayout.setStretch(0, 1)
        self.episodes_horizontalLayout.setStretch(1, 2)
        self.episodes_horizontalLayout.setStretch(2, 2)

        self.episodes_verticalLayout.addLayout(self.episodes_horizontalLayout)

        self.start_from_horizontalLayout = QHBoxLayout()
        self.start_from_horizontalLayout.setObjectName(u"start_from_horizontalLayout")
        self.start_from_label = QLabel(RenameDialog)
        self.start_from_label.setObjectName(u"start_from_label")

        self.start_from_horizontalLayout.addWidget(self.start_from_label)

        self.start_from_lineEdit = QLineEdit(RenameDialog)
        self.start_from_lineEdit.setObjectName(u"start_from_lineEdit")

        self.start_from_horizontalLayout.addWidget(self.start_from_lineEdit)

        self.start_from_horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.start_from_horizontalLayout.addItem(self.start_from_horizontalSpacer)

        self.start_from_horizontalLayout.setStretch(0, 1)
        self.start_from_horizontalLayout.setStretch(1, 2)
        self.start_from_horizontalLayout.setStretch(2, 2)

        self.episodes_verticalLayout.addLayout(self.start_from_horizontalLayout)


        self.verticalLayout.addLayout(self.episodes_verticalLayout)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.main_line = QFrame(RenameDialog)
        self.main_line.setObjectName(u"main_line")
        self.main_line.setFrameShape(QFrame.Shape.VLine)
        self.main_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.main_line)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.path_lineEdit = QLineEdit(RenameDialog)
        self.path_lineEdit.setObjectName(u"path_lineEdit")
        self.path_lineEdit.setReadOnly(True)

        self.verticalLayout_5.addWidget(self.path_lineEdit)

        self.btn_frame = QFrame(RenameDialog)
        self.btn_frame.setObjectName(u"btn_frame")
        self.btn_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.btn_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.btn_frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.back_pushButton = QPushButton(self.btn_frame)
        self.back_pushButton.setObjectName(u"back_pushButton")
        self.back_pushButton.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.back_pushButton)

        self.forward_pushButton = QPushButton(self.btn_frame)
        self.forward_pushButton.setObjectName(u"forward_pushButton")
        self.forward_pushButton.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.forward_pushButton)

        self.refresh_pushButton = QPushButton(self.btn_frame)
        self.refresh_pushButton.setObjectName(u"refresh_pushButton")
        self.refresh_pushButton.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.refresh_pushButton)


        self.verticalLayout_5.addWidget(self.btn_frame)

        self.preview_treeWidget = QTreeWidget(RenameDialog)
        self.preview_treeWidget.setObjectName(u"preview_treeWidget")

        self.verticalLayout_5.addWidget(self.preview_treeWidget)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.preview_checkBox = QCheckBox(RenameDialog)
        self.preview_checkBox.setObjectName(u"preview_checkBox")

        self.horizontalLayout_4.addWidget(self.preview_checkBox)

        self.show_only_video_files_checkBox = QCheckBox(RenameDialog)
        self.show_only_video_files_checkBox.setObjectName(u"show_only_video_files_checkBox")

        self.horizontalLayout_4.addWidget(self.show_only_video_files_checkBox)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.verticalLayout_5.setStretch(2, 4)

        self.horizontalLayout.addLayout(self.verticalLayout_5)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(2, 4)

        self.verticalLayout_6.addLayout(self.horizontalLayout)


        self.horizontalLayout_3.addLayout(self.verticalLayout_6)

        self.line_2 = QFrame(RenameDialog)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_3.addWidget(self.line_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.poster_label = QLabel(RenameDialog)
        self.poster_label.setObjectName(u"poster_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.poster_label.sizePolicy().hasHeightForWidth())
        self.poster_label.setSizePolicy(sizePolicy1)
        self.poster_label.setMinimumSize(QSize(0, 0))
        self.poster_label.setMaximumSize(QSize(16777215, 16777215))
        self.poster_label.setFrameShape(QFrame.Shape.StyledPanel)
        self.poster_label.setScaledContents(False)
        self.poster_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.poster_label.setOpenExternalLinks(True)

        self.verticalLayout_4.addWidget(self.poster_label)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.rename_subs_checkBox = QCheckBox(RenameDialog)
        self.rename_subs_checkBox.setObjectName(u"rename_subs_checkBox")

        self.verticalLayout_2.addWidget(self.rename_subs_checkBox)

        self.rename_dubs_checkBox = QCheckBox(RenameDialog)
        self.rename_dubs_checkBox.setObjectName(u"rename_dubs_checkBox")

        self.verticalLayout_2.addWidget(self.rename_dubs_checkBox)

        self.rename_folder_checkBox = QCheckBox(RenameDialog)
        self.rename_folder_checkBox.setObjectName(u"rename_folder_checkBox")

        self.verticalLayout_2.addWidget(self.rename_folder_checkBox)

        self.rename_torrent_checkBox = QCheckBox(RenameDialog)
        self.rename_torrent_checkBox.setObjectName(u"rename_torrent_checkBox")

        self.verticalLayout_2.addWidget(self.rename_torrent_checkBox)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.save_poster_checkBox = QCheckBox(RenameDialog)
        self.save_poster_checkBox.setObjectName(u"save_poster_checkBox")
        self.save_poster_checkBox.setChecked(False)
        self.save_poster_checkBox.setTristate(False)

        self.verticalLayout_3.addWidget(self.save_poster_checkBox)

        self.save_poster_lineEdit = QLineEdit(RenameDialog)
        self.save_poster_lineEdit.setObjectName(u"save_poster_lineEdit")
        self.save_poster_lineEdit.setEnabled(False)

        self.verticalLayout_3.addWidget(self.save_poster_lineEdit)

        self.save_banner_checkBox = QCheckBox(RenameDialog)
        self.save_banner_checkBox.setObjectName(u"save_banner_checkBox")

        self.verticalLayout_3.addWidget(self.save_banner_checkBox)

        self.save_banner_lineEdit = QLineEdit(RenameDialog)
        self.save_banner_lineEdit.setObjectName(u"save_banner_lineEdit")
        self.save_banner_lineEdit.setEnabled(False)

        self.verticalLayout_3.addWidget(self.save_banner_lineEdit)


        self.verticalLayout_2.addLayout(self.verticalLayout_3)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 120, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.verticalLayout_4.setStretch(0, 4)

        self.horizontalLayout_3.addLayout(self.verticalLayout_4)

        self.horizontalLayout_3.setStretch(0, 4)
        self.horizontalLayout_3.setStretch(2, 1)

        self.verticalLayout_7.addLayout(self.horizontalLayout_3)

        self.bottom_line = QFrame(RenameDialog)
        self.bottom_line.setObjectName(u"bottom_line")
        self.bottom_line.setFrameShape(QFrame.Shape.HLine)
        self.bottom_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_7.addWidget(self.bottom_line)

        self.template_horizontalLayout = QHBoxLayout()
        self.template_horizontalLayout.setObjectName(u"template_horizontalLayout")
        self.template_label = QLabel(RenameDialog)
        self.template_label.setObjectName(u"template_label")

        self.template_horizontalLayout.addWidget(self.template_label)

        self.template_lineEdit = QLineEdit(RenameDialog)
        self.template_lineEdit.setObjectName(u"template_lineEdit")

        self.template_horizontalLayout.addWidget(self.template_lineEdit)

        self.template_pushButton = QPushButton(RenameDialog)
        self.template_pushButton.setObjectName(u"template_pushButton")
        self.template_pushButton.setMaximumSize(QSize(30, 30))

        self.template_horizontalLayout.addWidget(self.template_pushButton)

        self.folder_name_label = QLabel(RenameDialog)
        self.folder_name_label.setObjectName(u"folder_name_label")

        self.template_horizontalLayout.addWidget(self.folder_name_label)

        self.folder_name_lineEdit = QLineEdit(RenameDialog)
        self.folder_name_lineEdit.setObjectName(u"folder_name_lineEdit")
        self.folder_name_lineEdit.setEnabled(False)

        self.template_horizontalLayout.addWidget(self.folder_name_lineEdit)

        self.folder_name_pushButton = QPushButton(RenameDialog)
        self.folder_name_pushButton.setObjectName(u"folder_name_pushButton")
        self.folder_name_pushButton.setMaximumSize(QSize(30, 30))

        self.template_horizontalLayout.addWidget(self.folder_name_pushButton)

        self.template_horizontalLayout.setStretch(0, 1)
        self.template_horizontalLayout.setStretch(1, 5)
        self.template_horizontalLayout.setStretch(4, 5)

        self.verticalLayout_7.addLayout(self.template_horizontalLayout)

        self.buttonbox_horizontalLayout = QHBoxLayout()
        self.buttonbox_horizontalLayout.setObjectName(u"buttonbox_horizontalLayout")
        self.torrent_widget = QWidget(RenameDialog)
        self.torrent_widget.setObjectName(u"torrent_widget")
        self.torrent_widget.setMaximumSize(QSize(16777215, 26))
        self.horizontalLayout_5 = QHBoxLayout(self.torrent_widget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.torrent_name_label = QLabel(self.torrent_widget)
        self.torrent_name_label.setObjectName(u"torrent_name_label")
        self.torrent_name_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.torrent_name_label)

        self.torrent_name_lineEdit = QLineEdit(self.torrent_widget)
        self.torrent_name_lineEdit.setObjectName(u"torrent_name_lineEdit")
        self.torrent_name_lineEdit.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.torrent_name_lineEdit)

        self.torrent_name_arrow_label = QLabel(self.torrent_widget)
        self.torrent_name_arrow_label.setObjectName(u"torrent_name_arrow_label")
        self.torrent_name_arrow_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.torrent_name_arrow_label)

        self.torrent_name_preview_label = QLabel(self.torrent_widget)
        self.torrent_name_preview_label.setObjectName(u"torrent_name_preview_label")
        self.torrent_name_preview_label.setEnabled(True)
        self.torrent_name_preview_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.torrent_name_preview_label)

        self.torrent_name_pushButton = QPushButton(self.torrent_widget)
        self.torrent_name_pushButton.setObjectName(u"torrent_name_pushButton")
        self.torrent_name_pushButton.setMaximumSize(QSize(30, 30))

        self.horizontalLayout_5.addWidget(self.torrent_name_pushButton)

        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 5)
        self.horizontalLayout_5.setStretch(3, 5)

        self.buttonbox_horizontalLayout.addWidget(self.torrent_widget)

        self.buttonBox = QDialogButtonBox(RenameDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.buttonbox_horizontalLayout.addWidget(self.buttonBox)

        self.buttonbox_horizontalLayout.setStretch(0, 4)
        self.buttonbox_horizontalLayout.setStretch(1, 1)

        self.verticalLayout_7.addLayout(self.buttonbox_horizontalLayout)


        self.retranslateUi(RenameDialog)
        self.buttonBox.accepted.connect(RenameDialog.accept)
        self.buttonBox.rejected.connect(RenameDialog.reject)

        QMetaObject.connectSlotsByName(RenameDialog)
    # setupUi

    def retranslateUi(self, RenameDialog):
        RenameDialog.setWindowTitle(QCoreApplication.translate("RenameDialog", u"Rename", None))
        self.banner_label.setText("")
        self.title_label.setText(QCoreApplication.translate("RenameDialog", u"Title :", None))
        self.season_num_label.setText(QCoreApplication.translate("RenameDialog", u"Season number :", None))
        self.season_label.setText(QCoreApplication.translate("RenameDialog", u"Season :", None))
        self.season_year_label.setText(QCoreApplication.translate("RenameDialog", u"Year :", None))
        self.type_label.setText(QCoreApplication.translate("RenameDialog", u"Type :", None))
        self.studio_label.setText(QCoreApplication.translate("RenameDialog", u"Studio :", None))
        self.duration_label.setText(QCoreApplication.translate("RenameDialog", u"Duration :", None))
        self.source_label.setText(QCoreApplication.translate("RenameDialog", u"Source :", None))
        self.resolution_label.setText(QCoreApplication.translate("RenameDialog", u"Resolution :", None))
        self.fansub_label.setText(QCoreApplication.translate("RenameDialog", u"Fansub Group :", None))
        self.country_label.setText(QCoreApplication.translate("RenameDialog", u"Country : ", None))
        self.score_label.setText(QCoreApplication.translate("RenameDialog", u"Score :", None))
        self.status_label.setText(QCoreApplication.translate("RenameDialog", u"Status :", None))
        self.episodes_label.setText(QCoreApplication.translate("RenameDialog", u"Episodes :  ", None))
        self.episodes_in_folder_label.setText(QCoreApplication.translate("RenameDialog", u"(?? in folder)", None))
        self.start_from_label.setText(QCoreApplication.translate("RenameDialog", u"Start from :", None))
        self.path_lineEdit.setPlaceholderText(QCoreApplication.translate("RenameDialog", u"Path", None))
        self.back_pushButton.setText(QCoreApplication.translate("RenameDialog", u"\u2b60", None))
        self.forward_pushButton.setText(QCoreApplication.translate("RenameDialog", u"\u2b62", None))
        self.refresh_pushButton.setText(QCoreApplication.translate("RenameDialog", u"\u27f3", None))
        ___qtreewidgetitem = self.preview_treeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("RenameDialog", u"Folder", None))
        self.preview_checkBox.setText(QCoreApplication.translate("RenameDialog", u"Preview", None))
        self.show_only_video_files_checkBox.setText(QCoreApplication.translate("RenameDialog", u"Show only video files", None))
        self.poster_label.setText("")
        self.rename_subs_checkBox.setText(QCoreApplication.translate("RenameDialog", u"Rename subtitle files", None))
        self.rename_dubs_checkBox.setText(QCoreApplication.translate("RenameDialog", u"Rename audio files", None))
        self.rename_folder_checkBox.setText(QCoreApplication.translate("RenameDialog", u"Rename folder", None))
        self.rename_torrent_checkBox.setText(QCoreApplication.translate("RenameDialog", u"Rename torrent", None))
        self.save_poster_checkBox.setText(QCoreApplication.translate("RenameDialog", u"Save poster to folder", None))
        self.save_poster_lineEdit.setPlaceholderText(QCoreApplication.translate("RenameDialog", u"File name", None))
        self.save_banner_checkBox.setText(QCoreApplication.translate("RenameDialog", u"Save banner to folder", None))
        self.save_banner_lineEdit.setPlaceholderText(QCoreApplication.translate("RenameDialog", u"File name", None))
        self.template_label.setText(QCoreApplication.translate("RenameDialog", u"Template :", None))
        self.template_pushButton.setText(QCoreApplication.translate("RenameDialog", u"?", None))
        self.folder_name_label.setText(QCoreApplication.translate("RenameDialog", u"Folder name :", None))
        self.folder_name_pushButton.setText(QCoreApplication.translate("RenameDialog", u"?", None))
        self.torrent_name_label.setText(QCoreApplication.translate("RenameDialog", u"Torrent name :", None))
        self.torrent_name_arrow_label.setText(QCoreApplication.translate("RenameDialog", u"->", None))
        self.torrent_name_preview_label.setText("")
        self.torrent_name_pushButton.setText(QCoreApplication.translate("RenameDialog", u"?", None))
    # retranslateUi

