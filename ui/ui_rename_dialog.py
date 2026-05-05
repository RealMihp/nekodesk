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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFrame, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_RenameDialog(object):
    def setupUi(self, RenameDialog):
        if not RenameDialog.objectName():
            RenameDialog.setObjectName(u"RenameDialog")
        RenameDialog.resize(800, 600)
        RenameDialog.setSizeGripEnabled(True)
        self.verticalLayout_3 = QVBoxLayout(RenameDialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.title_horizontalLayout = QHBoxLayout()
        self.title_horizontalLayout.setObjectName(u"title_horizontalLayout")
        self.title_label = QLabel(RenameDialog)
        self.title_label.setObjectName(u"title_label")

        self.title_horizontalLayout.addWidget(self.title_label)

        self.title_lineEdit = QLineEdit(RenameDialog)
        self.title_lineEdit.setObjectName(u"title_lineEdit")

        self.title_horizontalLayout.addWidget(self.title_lineEdit)


        self.verticalLayout_3.addLayout(self.title_horizontalLayout)

        self.main_horizontalLayout = QHBoxLayout()
        self.main_horizontalLayout.setObjectName(u"main_horizontalLayout")
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

        self.quality_horizontalLayout = QHBoxLayout()
        self.quality_horizontalLayout.setObjectName(u"quality_horizontalLayout")
        self.quality_label = QLabel(RenameDialog)
        self.quality_label.setObjectName(u"quality_label")

        self.quality_horizontalLayout.addWidget(self.quality_label)

        self.quality_lineEdit = QLineEdit(RenameDialog)
        self.quality_lineEdit.setObjectName(u"quality_lineEdit")

        self.quality_horizontalLayout.addWidget(self.quality_lineEdit)


        self.verticalLayout.addLayout(self.quality_horizontalLayout)

        self.translation_studio_horizontalLayout = QHBoxLayout()
        self.translation_studio_horizontalLayout.setObjectName(u"translation_studio_horizontalLayout")
        self.translation_studio_label = QLabel(RenameDialog)
        self.translation_studio_label.setObjectName(u"translation_studio_label")

        self.translation_studio_horizontalLayout.addWidget(self.translation_studio_label)

        self.translation_studio_lineEdit = QLineEdit(RenameDialog)
        self.translation_studio_lineEdit.setObjectName(u"translation_studio_lineEdit")

        self.translation_studio_horizontalLayout.addWidget(self.translation_studio_lineEdit)


        self.verticalLayout.addLayout(self.translation_studio_horizontalLayout)

        self.left_verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.left_verticalSpacer_2)

        self.left_line = QFrame(RenameDialog)
        self.left_line.setObjectName(u"left_line")
        self.left_line.setFrameShape(QFrame.Shape.HLine)
        self.left_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.left_line)

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


        self.main_horizontalLayout.addLayout(self.verticalLayout)

        self.main_line = QFrame(RenameDialog)
        self.main_line.setObjectName(u"main_line")
        self.main_line.setFrameShape(QFrame.Shape.VLine)
        self.main_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.main_horizontalLayout.addWidget(self.main_line)

        self.preview_verticalLayout = QVBoxLayout()
        self.preview_verticalLayout.setObjectName(u"preview_verticalLayout")
        self.preview_label = QLabel(RenameDialog)
        self.preview_label.setObjectName(u"preview_label")

        self.preview_verticalLayout.addWidget(self.preview_label)

        self.preview_treeWidget = QTreeWidget(RenameDialog)
        self.preview_treeWidget.setObjectName(u"preview_treeWidget")

        self.preview_verticalLayout.addWidget(self.preview_treeWidget)


        self.main_horizontalLayout.addLayout(self.preview_verticalLayout)

        self.main_horizontalLayout.setStretch(0, 1)
        self.main_horizontalLayout.setStretch(2, 2)

        self.verticalLayout_3.addLayout(self.main_horizontalLayout)

        self.bottom_line = QFrame(RenameDialog)
        self.bottom_line.setObjectName(u"bottom_line")
        self.bottom_line.setFrameShape(QFrame.Shape.HLine)
        self.bottom_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.bottom_line)

        self.botoom_verticalLayout = QVBoxLayout()
        self.botoom_verticalLayout.setObjectName(u"botoom_verticalLayout")
        self.template_horizontalLayout = QHBoxLayout()
        self.template_horizontalLayout.setObjectName(u"template_horizontalLayout")
        self.template_label = QLabel(RenameDialog)
        self.template_label.setObjectName(u"template_label")

        self.template_horizontalLayout.addWidget(self.template_label)

        self.template_pushButton = QPushButton(RenameDialog)
        self.template_pushButton.setObjectName(u"template_pushButton")
        self.template_pushButton.setMaximumSize(QSize(30, 30))

        self.template_horizontalLayout.addWidget(self.template_pushButton)

        self.template_horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.template_horizontalLayout.addItem(self.template_horizontalSpacer)


        self.botoom_verticalLayout.addLayout(self.template_horizontalLayout)

        self.buttonbox_horizontalLayout = QHBoxLayout()
        self.buttonbox_horizontalLayout.setObjectName(u"buttonbox_horizontalLayout")
        self.template_lineEdit = QLineEdit(RenameDialog)
        self.template_lineEdit.setObjectName(u"template_lineEdit")

        self.buttonbox_horizontalLayout.addWidget(self.template_lineEdit)

        self.buttonBox = QDialogButtonBox(RenameDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.buttonbox_horizontalLayout.addWidget(self.buttonBox)

        self.buttonbox_horizontalLayout.setStretch(0, 2)
        self.buttonbox_horizontalLayout.setStretch(1, 1)

        self.botoom_verticalLayout.addLayout(self.buttonbox_horizontalLayout)


        self.verticalLayout_3.addLayout(self.botoom_verticalLayout)


        self.retranslateUi(RenameDialog)
        self.buttonBox.accepted.connect(RenameDialog.accept)
        self.buttonBox.rejected.connect(RenameDialog.reject)

        QMetaObject.connectSlotsByName(RenameDialog)
    # setupUi

    def retranslateUi(self, RenameDialog):
        RenameDialog.setWindowTitle(QCoreApplication.translate("RenameDialog", u"Rename", None))
        self.title_label.setText(QCoreApplication.translate("RenameDialog", u"Title :", None))
        self.season_num_label.setText(QCoreApplication.translate("RenameDialog", u"Season number :", None))
        self.season_label.setText(QCoreApplication.translate("RenameDialog", u"Season :", None))
        self.season_year_label.setText(QCoreApplication.translate("RenameDialog", u"Year :", None))
        self.type_label.setText(QCoreApplication.translate("RenameDialog", u"Type :", None))
        self.studio_label.setText(QCoreApplication.translate("RenameDialog", u"Studio :", None))
        self.duration_label.setText(QCoreApplication.translate("RenameDialog", u"Duration :", None))
        self.source_label.setText(QCoreApplication.translate("RenameDialog", u"Source :", None))
        self.quality_label.setText(QCoreApplication.translate("RenameDialog", u"Quality :", None))
        self.translation_studio_label.setText(QCoreApplication.translate("RenameDialog", u"Translation studio :", None))
        self.score_label.setText(QCoreApplication.translate("RenameDialog", u"Score :", None))
        self.status_label.setText(QCoreApplication.translate("RenameDialog", u"Status :", None))
        self.episodes_label.setText(QCoreApplication.translate("RenameDialog", u"Episodes :  ", None))
        self.episodes_in_folder_label.setText(QCoreApplication.translate("RenameDialog", u"(?? in folder)", None))
        self.start_from_label.setText(QCoreApplication.translate("RenameDialog", u"Start from :", None))
        self.preview_label.setText(QCoreApplication.translate("RenameDialog", u"Preview", None))
        ___qtreewidgetitem = self.preview_treeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("RenameDialog", u"Folder", None))
        self.template_label.setText(QCoreApplication.translate("RenameDialog", u"Template :", None))
        self.template_pushButton.setText(QCoreApplication.translate("RenameDialog", u"?", None))
    # retranslateUi

