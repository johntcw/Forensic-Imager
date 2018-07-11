# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(320, 240)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(320, 240))
        MainWindow.setMaximumSize(QtCore.QSize(320, 240))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.srcBox = QtWidgets.QComboBox(self.centralwidget)
        self.srcBox.setGeometry(QtCore.QRect(70, 10, 211, 26))
        self.srcBox.setObjectName("srcBox")
        self.destBox = QtWidgets.QComboBox(self.centralwidget)
        self.destBox.setGeometry(QtCore.QRect(70, 50, 211, 26))
        self.destBox.setObjectName("destBox")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 51, 26))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 51, 26))
        self.label_2.setObjectName("label_2")
        self.imagingBtn = QtWidgets.QPushButton(self.centralwidget)
        self.imagingBtn.setGeometry(QtCore.QRect(190, 80, 113, 32))
        self.imagingBtn.setObjectName("imagingBtn")
        self.refreshBtn = QtWidgets.QPushButton(self.centralwidget)
        self.refreshBtn.setGeometry(QtCore.QRect(290, 10, 21, 21))
        self.refreshBtn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtGui.QImageReader("./reload_24.png").read()), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refreshBtn.setIcon(icon)
        self.refreshBtn.setObjectName("refreshBtn")
        self.hashSrcBtn = QtWidgets.QPushButton(self.centralwidget)
        self.hashSrcBtn.setGeometry(QtCore.QRect(70, 80, 114, 32))
        self.hashSrcBtn.setObjectName("hashSrcBtn")
        self.logView = QtWidgets.QTextEdit(self.centralwidget)
        self.logView.setGeometry(QtCore.QRect(10, 120, 301, 71))
        self.logView.setObjectName("logView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 320, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Forensic Imager"))
        self.srcBox.setToolTip(_translate("MainWindow", "Evidence source disk"))
        self.destBox.setToolTip(_translate("MainWindow", "Image destination"))
        self.label.setText(_translate("MainWindow", "Source"))
        self.label_2.setText(_translate("MainWindow", "Target"))
        self.imagingBtn.setText(_translate("MainWindow", "Start imaging"))
        self.refreshBtn.setToolTip(_translate("MainWindow", "Refresh disk list"))
        self.hashSrcBtn.setText(_translate("MainWindow", "Hash Source"))

