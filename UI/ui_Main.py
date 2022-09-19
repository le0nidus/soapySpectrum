# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainsWZSBM.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_SoapySpectrum(object):
    def setupUi(self, SoapySpectrum):
        if not SoapySpectrum.objectName():
            SoapySpectrum.setObjectName(u"SoapySpectrum")
        SoapySpectrum.resize(694, 392)
        self.centralwidget = QWidget(SoapySpectrum)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"QLabel{\n"
"	font: 12pt \"Calibri\";\n"
"}\n"
"QLineEdit{\n"
"	font: 14pt \"Calibri\";\n"
"}\n"
"QPushButton{\n"
"	font: 13pt \"Calibri\";\n"
"}\n"
"QComboBox{\n"
"	font: 13pt \"Calibri\";\n"
"}\n"
"QCheckBox {\n"
"	font: 12pt \"Calibri\";\n"
"}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_34 = QLabel(self.frame_3)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setMinimumSize(QSize(0, 30))
        self.label_34.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setFamily(u"Calibri")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_34.setFont(font)
        self.label_34.setStyleSheet(u"QLabel{\n"
"	border-radius: 7px;\n"
"	font: 16pt \"Calibri\";\n"
"}")
        self.label_34.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_2.addWidget(self.label_34)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setVerticalSpacing(6)
        self.formLayout.setContentsMargins(10, -1, 10, -1)
        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_3)

        self.rxFreq = QLineEdit(self.frame_3)
        self.rxFreq.setObjectName(u"rxFreq")
        self.rxFreq.setText("315")
        self.rxFreq.setMinimumSize(QSize(0, 24))
        self.rxFreq.setMaximumSize(QSize(16777215, 24))

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.rxFreq)

        self.label_9 = QLabel(self.frame_3)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_9)

        self.sampleRate = QLineEdit(self.frame_3)
        self.sampleRate.setObjectName(u"sampleRate")
        self.sampleRate.setText("5")
        self.sampleRate.setMinimumSize(QSize(0, 24))
        self.sampleRate.setMaximumSize(QSize(16777215, 24))

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.sampleRate)

        self.label_10 = QLabel(self.frame_3)
        self.label_10.setObjectName(u"label_10")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_10)

        self.gain = QLineEdit(self.frame_3)
        self.gain.setObjectName(u"gain")
        self.gain.setText("45")
        self.gain.setMinimumSize(QSize(0, 24))
        self.gain.setMaximumSize(QSize(16777215, 24))

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.gain)

        self.label_13 = QLabel(self.frame_3)
        self.label_13.setObjectName(u"label_13")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_13)

        self.bandwidthFilter = QComboBox(self.frame_3)
        self.bandwidthFilter.addItem("")
        self.bandwidthFilter.addItem("")
        self.bandwidthFilter.addItem("")
        self.bandwidthFilter.addItem("")
        self.bandwidthFilter.addItem("")
        self.bandwidthFilter.addItem("")
        self.bandwidthFilter.addItem("")
        self.bandwidthFilter.addItem("")
        self.bandwidthFilter.addItem("")
        self.bandwidthFilter.addItem("")
        self.bandwidthFilter.addItem("")
        self.bandwidthFilter.addItem("")
        self.bandwidthFilter.addItem("")
        self.bandwidthFilter.addItem("")
        self.bandwidthFilter.addItem("")
        self.bandwidthFilter.addItem("")
        self.bandwidthFilter.setObjectName(u"bandwidthFilter")
        self.bandwidthFilter.setMinimumSize(QSize(0, 25))
        self.bandwidthFilter.setMaximumSize(QSize(16777215, 25))
        self.bandwidthFilter.setStyleSheet(u"")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.bandwidthFilter)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.btnClear = QPushButton(self.frame_3)
        self.btnClear.setObjectName(u"btnClear")
        self.btnClear.setMinimumSize(QSize(0, 23))
        self.btnClear.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_2.addWidget(self.btnClear)

        self.btnStart = QPushButton(self.frame_3)
        self.btnStart.setObjectName(u"btnStart")
        self.btnStart.setMinimumSize(QSize(0, 23))
        self.btnStart.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_2.addWidget(self.btnStart)


        self.horizontalLayout.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, -1, -1, 0)
        self.label_35 = QLabel(self.frame_4)
        self.label_35.setObjectName(u"label_35")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_35.sizePolicy().hasHeightForWidth())
        self.label_35.setSizePolicy(sizePolicy)
        self.label_35.setMinimumSize(QSize(0, 30))
        self.label_35.setMaximumSize(QSize(16777215, 30))
        self.label_35.setFont(font)
        self.label_35.setStyleSheet(u"QLabel{\n"
"	border-radius: 7px;\n"
"	font: 16pt \"Calibri\";\n"
"}")
        self.label_35.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_3.addWidget(self.label_35)

        self.chkMax = QCheckBox(self.frame_4)
        self.chkMax.setObjectName(u"chkMax")
        sizePolicy1 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(4)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.chkMax.sizePolicy().hasHeightForWidth())
        self.chkMax.setSizePolicy(sizePolicy1)
        self.chkMax.setMinimumSize(QSize(100, 0))
        self.chkMax.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_3.addWidget(self.chkMax)

        self.chkAvg = QCheckBox(self.frame_4)
        self.chkAvg.setObjectName(u"chkAvg")
        sizePolicy1.setHeightForWidth(self.chkAvg.sizePolicy().hasHeightForWidth())
        self.chkAvg.setSizePolicy(sizePolicy1)
        self.chkAvg.setMinimumSize(QSize(100, 0))
        self.chkAvg.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_3.addWidget(self.chkAvg)

        self.chklog = QCheckBox(self.frame_4)
        self.chklog.setObjectName(u"chklog")
        sizePolicy1.setHeightForWidth(self.chklog.sizePolicy().hasHeightForWidth())
        self.chklog.setSizePolicy(sizePolicy1)
        self.chklog.setMinimumSize(QSize(100, 0))
        self.chklog.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_3.addWidget(self.chklog)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setVerticalSpacing(7)
        self.label_14 = QLabel(self.frame_4)
        self.label_14.setObjectName(u"label_14")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_14)

        self.avgRatio = QComboBox(self.frame_4)
        self.avgRatio.addItem("")
        self.avgRatio.addItem("")
        self.avgRatio.addItem("")
        self.avgRatio.addItem("")
        self.avgRatio.addItem("")
        self.avgRatio.addItem("")
        self.avgRatio.addItem("")
        self.avgRatio.addItem("")
        self.avgRatio.addItem("")
        self.avgRatio.addItem("")
        self.avgRatio.addItem("")
        self.avgRatio.addItem("")
        self.avgRatio.addItem("")
        self.avgRatio.addItem("")
        self.avgRatio.addItem("")
        self.avgRatio.setObjectName(u"avgRatio")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.avgRatio.sizePolicy().hasHeightForWidth())
        self.avgRatio.setSizePolicy(sizePolicy2)
        self.avgRatio.setMinimumSize(QSize(0, 25))
        self.avgRatio.setMaximumSize(QSize(16777215, 25))
        self.avgRatio.setStyleSheet(u"")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.avgRatio)

        self.label_16 = QLabel(self.frame_4)
        self.label_16.setObjectName(u"label_16")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_16)

        self.perRead = QComboBox(self.frame_4)
        self.perRead.addItem("")
        self.perRead.addItem("")
        self.perRead.addItem("")
        self.perRead.addItem("")
        self.perRead.addItem("")
        self.perRead.addItem("")
        self.perRead.setObjectName(u"perRead")
        sizePolicy2.setHeightForWidth(self.perRead.sizePolicy().hasHeightForWidth())
        self.perRead.setSizePolicy(sizePolicy2)
        self.perRead.setMinimumSize(QSize(0, 25))
        self.perRead.setMaximumSize(QSize(16777215, 25))
        self.perRead.setStyleSheet(u"")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.perRead)

        self.label_15 = QLabel(self.frame_4)
        self.label_15.setObjectName(u"label_15")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_15)

        self.perIteration = QComboBox(self.frame_4)
        self.perIteration.addItem("")
        self.perIteration.addItem("")
        self.perIteration.addItem("")
        self.perIteration.addItem("")
        self.perIteration.addItem("")
        self.perIteration.addItem("")
        self.perIteration.addItem("")
        self.perIteration.setObjectName(u"perIteration")
        sizePolicy2.setHeightForWidth(self.perIteration.sizePolicy().hasHeightForWidth())
        self.perIteration.setSizePolicy(sizePolicy2)
        self.perIteration.setMinimumSize(QSize(0, 25))
        self.perIteration.setMaximumSize(QSize(16777215, 25))
        self.perIteration.setStyleSheet(u"")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.perIteration)


        self.verticalLayout_3.addLayout(self.formLayout_2)


        self.horizontalLayout.addWidget(self.frame_4)


        self.verticalLayout.addWidget(self.frame)

        self.frmPlot = QGridLayout()
        self.frmPlot.setObjectName(u"frmPlot")

        self.verticalLayout.addLayout(self.frmPlot)

        SoapySpectrum.setCentralWidget(self.centralwidget)

        self.retranslateUi(SoapySpectrum)

        QMetaObject.connectSlotsByName(SoapySpectrum)
    # setupUi

    def retranslateUi(self, SoapySpectrum):
        SoapySpectrum.setWindowTitle(QCoreApplication.translate("SoapySpectrum", u"Soapy Spectrum", None))
        self.label_34.setText(QCoreApplication.translate("SoapySpectrum", u"SDR Settings :", None))
        self.label_3.setText(QCoreApplication.translate("SoapySpectrum", u"RX Frequency (MHz) :", None))
        self.label_9.setText(QCoreApplication.translate("SoapySpectrum", u"Sample Rate (MHz) :", None))
        self.label_10.setText(QCoreApplication.translate("SoapySpectrum", u"Gain :", None))
        self.label_13.setText(QCoreApplication.translate("SoapySpectrum", u"Bandwidth Filter (MHz) :", None))
        self.bandwidthFilter.setItemText(0, QCoreApplication.translate("SoapySpectrum", u"1.75", None))
        self.bandwidthFilter.setItemText(1, QCoreApplication.translate("SoapySpectrum", u"2.5", None))
        self.bandwidthFilter.setItemText(2, QCoreApplication.translate("SoapySpectrum", u"3.5", None))
        self.bandwidthFilter.setItemText(3, QCoreApplication.translate("SoapySpectrum", u"5", None))
        self.bandwidthFilter.setItemText(4, QCoreApplication.translate("SoapySpectrum", u"5.5", None))
        self.bandwidthFilter.setItemText(5, QCoreApplication.translate("SoapySpectrum", u"6", None))
        self.bandwidthFilter.setItemText(6, QCoreApplication.translate("SoapySpectrum", u"7", None))
        self.bandwidthFilter.setItemText(7, QCoreApplication.translate("SoapySpectrum", u"8", None))
        self.bandwidthFilter.setItemText(8, QCoreApplication.translate("SoapySpectrum", u"9", None))
        self.bandwidthFilter.setItemText(9, QCoreApplication.translate("SoapySpectrum", u"10", None))
        self.bandwidthFilter.setItemText(10, QCoreApplication.translate("SoapySpectrum", u"12", None))
        self.bandwidthFilter.setItemText(11, QCoreApplication.translate("SoapySpectrum", u"14", None))
        self.bandwidthFilter.setItemText(12, QCoreApplication.translate("SoapySpectrum", u"15", None))
        self.bandwidthFilter.setItemText(13, QCoreApplication.translate("SoapySpectrum", u"20", None))
        self.bandwidthFilter.setItemText(14, QCoreApplication.translate("SoapySpectrum", u"24", None))
        self.bandwidthFilter.setItemText(15, QCoreApplication.translate("SoapySpectrum", u"28", None))

        self.btnClear.setText(QCoreApplication.translate("SoapySpectrum", u"Clear Plot", None))
        self.btnStart.setText(QCoreApplication.translate("SoapySpectrum", u"Start/Update settings", None))
        self.label_35.setText(QCoreApplication.translate("SoapySpectrum", u"Spectrum Analyzer Settings :", None))
        self.chkMax.setText(QCoreApplication.translate("SoapySpectrum", u"Max hold", None))
        self.chkAvg.setText(QCoreApplication.translate("SoapySpectrum", u"Moving Average", None))
        self.chklog.setText(QCoreApplication.translate("SoapySpectrum", u"Log Scale Plot", None))
        self.label_14.setText(QCoreApplication.translate("SoapySpectrum", u"Moving average ratio :", None))
        self.avgRatio.setItemText(0, QCoreApplication.translate("SoapySpectrum", u"0.0625", None))
        self.avgRatio.setItemText(1, QCoreApplication.translate("SoapySpectrum", u"0.125", None))
        self.avgRatio.setItemText(2, QCoreApplication.translate("SoapySpectrum", u"0.1875", None))
        self.avgRatio.setItemText(3, QCoreApplication.translate("SoapySpectrum", u"0.25", None))
        self.avgRatio.setItemText(4, QCoreApplication.translate("SoapySpectrum", u"0.3125", None))
        self.avgRatio.setItemText(5, QCoreApplication.translate("SoapySpectrum", u"0.375", None))
        self.avgRatio.setItemText(6, QCoreApplication.translate("SoapySpectrum", u"0.4375", None))
        self.avgRatio.setItemText(7, QCoreApplication.translate("SoapySpectrum", u"0.5", None))
        self.avgRatio.setItemText(8, QCoreApplication.translate("SoapySpectrum", u"0.5625", None))
        self.avgRatio.setItemText(9, QCoreApplication.translate("SoapySpectrum", u"0.625", None))
        self.avgRatio.setItemText(10, QCoreApplication.translate("SoapySpectrum", u"0.6875", None))
        self.avgRatio.setItemText(11, QCoreApplication.translate("SoapySpectrum", u"0.75", None))
        self.avgRatio.setItemText(12, QCoreApplication.translate("SoapySpectrum", u"0.8125", None))
        self.avgRatio.setItemText(13, QCoreApplication.translate("SoapySpectrum", u"0.875", None))
        self.avgRatio.setItemText(14, QCoreApplication.translate("SoapySpectrum", u"0.9375", None))

        self.label_16.setText(QCoreApplication.translate("SoapySpectrum", u"Samples per read :", None))
        self.perRead.setItemText(0, QCoreApplication.translate("SoapySpectrum", u"32", None))
        self.perRead.setItemText(1, QCoreApplication.translate("SoapySpectrum", u"64", None))
        self.perRead.setItemText(2, QCoreApplication.translate("SoapySpectrum", u"128", None))
        self.perRead.setItemText(3, QCoreApplication.translate("SoapySpectrum", u"256", None))
        self.perRead.setItemText(4, QCoreApplication.translate("SoapySpectrum", u"512", None))
        self.perRead.setItemText(5, QCoreApplication.translate("SoapySpectrum", u"1024", None))

        self.label_15.setText(QCoreApplication.translate("SoapySpectrum", u"Samples per iteration :", None))
        self.perIteration.setItemText(0, QCoreApplication.translate("SoapySpectrum", u"2048", None))
        self.perIteration.setItemText(1, QCoreApplication.translate("SoapySpectrum", u"4096", None))
        self.perIteration.setItemText(2, QCoreApplication.translate("SoapySpectrum", u"8192", None))
        self.perIteration.setItemText(3, QCoreApplication.translate("SoapySpectrum", u"16384", None))
        self.perIteration.setItemText(4, QCoreApplication.translate("SoapySpectrum", u"32768", None))
        self.perIteration.setItemText(5, QCoreApplication.translate("SoapySpectrum", u"65536", None))
        self.perIteration.setItemText(6, QCoreApplication.translate("SoapySpectrum", u"131072", None))

    # retranslateUi

