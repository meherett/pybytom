# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/tmp/btmhdwzk3024.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!
from btmhdw import BTMHDW, BytomHDWallet, BTMHDW_HARDEN, PATH, INDEXES
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import os


class Ui_btmhdw(object):

    def __init__(self):
        self.language = "english"
        self.network = "mainnet"
        self.consoleMessage = str()
        self.path = "m/44/153/1/0/1"
        self.hideHome = False
        self.saveHDWallet = None
        self.currentPath = os.getcwd()

    def setupUi(self, btmhdw):
        self.window = btmhdw
        btmhdw.setObjectName("btmhdw")
        btmhdw.resize(731, 642)
        btmhdw.setMinimumSize(QtCore.QSize(731, 642))
        btmhdw.setMaximumSize(QtCore.QSize(731, 642))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.currentPath + "icons/btmhdw-logo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        btmhdw.setWindowIcon(icon)
        self.widgetMain = QtWidgets.QWidget(btmhdw)
        self.widgetMain.setGeometry(QtCore.QRect(10, 130, 711, 201))
        self.widgetMain.setObjectName("widgetMain")
        self.lineEditBtmhdw = QtWidgets.QLineEdit(self.widgetMain)
        self.lineEditBtmhdw.setGeometry(QtCore.QRect(0, 0, 711, 41))
        self.lineEditBtmhdw.setStyleSheet("padding: 0 10px;")
        self.lineEditBtmhdw.setObjectName("lineEditBtmhdw")
        self.pushButtonGetHDWalletFromMnemonic = QtWidgets.QPushButton(self.widgetMain)
        self.pushButtonGetHDWalletFromMnemonic.setGeometry(QtCore.QRect(180, 50, 241, 41))
        self.pushButtonGetHDWalletFromMnemonic.setObjectName("pushButtonGetHDWalletFromMnemonic")
        self.pushButtonGenerateMnemonic = QtWidgets.QPushButton(self.widgetMain)
        self.pushButtonGenerateMnemonic.setGeometry(QtCore.QRect(0, 100, 171, 41))
        self.pushButtonGenerateMnemonic.setObjectName("pushButtonGenerateMnemonic")
        self.pushButtonGenerateEntropy = QtWidgets.QPushButton(self.widgetMain)
        self.pushButtonGenerateEntropy.setGeometry(QtCore.QRect(0, 150, 171, 41))
        self.pushButtonGenerateEntropy.setObjectName("pushButtonGenerateEntropy")
        self.radioButtonEnglish = QtWidgets.QRadioButton(self.widgetMain)
        self.radioButtonEnglish.setGeometry(QtCore.QRect(0, 50, 81, 41))
        self.radioButtonEnglish.setStyleSheet("QRadioButton::indicator {\n"
                                              "    width: 16px;\n"
                                              "    height: 16px;\n"
                                              "}\n"
                                              "QRadioButton::indicator:checked {\n"
                                              "   image: url(" + self.currentPath + "/icons/radio_checked.svg);\n"
                                              "}\n"
                                              "QRadioButton::indicator:unchecked {\n"
                                              "    image: url(" + self.currentPath + "/icons/radio_unchecked.svg);\n"
                                              "}")
        self.radioButtonEnglish.setChecked(True)
        self.radioButtonEnglish.setObjectName("radioButtonEnglish")
        self.radioButtonJapanese = QtWidgets.QRadioButton(self.widgetMain)
        self.radioButtonJapanese.setGeometry(QtCore.QRect(80, 50, 91, 41))
        self.radioButtonJapanese.setStyleSheet("QRadioButton::indicator {\n"
                                               "    width: 16px;\n"
                                               "    height: 16px;\n"
                                               "}\n"
                                               "QRadioButton::indicator:checked {\n"
                                               "   image: url(" + self.currentPath + "/icons/radio_checked.svg);\n"
                                               "}\n"
                                               "QRadioButton::indicator:unchecked {\n"
                                               "    image: url(" + self.currentPath + "/icons/radio_unchecked.svg);\n"
                                               "}")
        self.radioButtonJapanese.setObjectName("radioButtonJapanese")
        self.pushButtonGetHDWalletFromEntropy = QtWidgets.QPushButton(self.widgetMain)
        self.pushButtonGetHDWalletFromEntropy.setGeometry(QtCore.QRect(180, 100, 241, 41))
        self.pushButtonGetHDWalletFromEntropy.setObjectName("pushButtonGetHDWalletFromEntropy")
        self.pushButtonGetContractProgramFromXPublicKey = QtWidgets.QPushButton(self.widgetMain)
        self.pushButtonGetContractProgramFromXPublicKey.setGeometry(QtCore.QRect(430, 100, 281, 41))
        self.pushButtonGetContractProgramFromXPublicKey.setObjectName("pushButtonGetContractProgramFromXPublicKey")
        self.checkBoxPath = QtWidgets.QCheckBox(self.widgetMain)
        self.checkBoxPath.setGeometry(QtCore.QRect(430, 150, 71, 41))
        self.checkBoxPath.setStyleSheet("QCheckBox::indicator {\n"
                                        "    width: 16px;\n"
                                        "    height: 16px;\n"
                                        "}\n"
                                        "QCheckBox::indicator:checked {\n"
                                        "    image: url(" + self.currentPath + "/icons/checkbox_checked.svg);\n"
                                        "}\n"
                                        "QCheckBox::indicator:unchecked {\n"
                                        "    image: url(" + self.currentPath + "/icons/checkbox_unchecked.svg);\n"
                                        "}")
        self.checkBoxPath.setObjectName("checkBoxPath")
        self.lineEditPath = QtWidgets.QLineEdit(self.widgetMain)
        self.lineEditPath.setEnabled(False)
        self.lineEditPath.setGeometry(QtCore.QRect(500, 150, 211, 41))
        self.lineEditPath.setStyleSheet("padding: 0 10px;")
        self.lineEditPath.setObjectName("lineEditPath")
        self.pushButtonGetHDWalletFromXPrivateKey = QtWidgets.QPushButton(self.widgetMain)
        self.pushButtonGetHDWalletFromXPrivateKey.setGeometry(QtCore.QRect(180, 150, 241, 41))
        self.pushButtonGetHDWalletFromXPrivateKey.setObjectName("pushButtonGetHDWalletFromXPrivateKey")
        self.lineEditPassword = QtWidgets.QLineEdit(self.widgetMain)
        self.lineEditPassword.setGeometry(QtCore.QRect(430, 50, 281, 41))
        self.lineEditPassword.setStyleSheet("padding: 0 10px;")
        self.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEditPassword.setObjectName("lineEditPassword")
        self.widgetNet = QtWidgets.QWidget(btmhdw)
        self.widgetNet.setGeometry(QtCore.QRect(490, 10, 81, 111))
        self.widgetNet.setObjectName("widgetNet")
        self.radioButtonSolonet = QtWidgets.QRadioButton(self.widgetNet)
        self.radioButtonSolonet.setGeometry(QtCore.QRect(0, 80, 81, 31))
        self.radioButtonSolonet.setStyleSheet("QRadioButton::indicator {\n"
                                              "    width: 16px;\n"
                                              "    height: 16px;\n"
                                              "}\n"
                                              "QRadioButton::indicator:checked {\n"
                                              "   image: url(" + self.currentPath + "/icons/radio_checked.svg);\n"
                                              "}\n"
                                              "QRadioButton::indicator:unchecked {\n"
                                              "    image: url(" + self.currentPath + "/icons/radio_unchecked.svg);\n"
                                              "}")
        self.radioButtonSolonet.setObjectName("radioButtonSolonet")
        self.radioButtonMainnet = QtWidgets.QRadioButton(self.widgetNet)
        self.radioButtonMainnet.setGeometry(QtCore.QRect(0, 0, 81, 31))
        self.radioButtonMainnet.setStyleSheet("QRadioButton::indicator {\n"
                                              "    width: 16px;\n"
                                              "    height: 16px;\n"
                                              "}\n"
                                              "QRadioButton::indicator:checked {\n"
                                              "   image: url(" + self.currentPath + "/icons/radio_checked.svg);\n"
                                              "}\n"
                                              "QRadioButton::indicator:unchecked {\n"
                                              "    image: url(" + self.currentPath + "/icons/radio_unchecked.svg);\n"
                                              "}")
        self.radioButtonMainnet.setChecked(True)
        self.radioButtonMainnet.setObjectName("radioButtonMainnet")
        self.radioButtonTestnet = QtWidgets.QRadioButton(self.widgetNet)
        self.radioButtonTestnet.setGeometry(QtCore.QRect(0, 40, 81, 31))
        self.radioButtonTestnet.setStyleSheet("QRadioButton::indicator {\n"
                                              "    width: 16px;\n"
                                              "    height: 16px;\n"
                                              "}\n"
                                              "QRadioButton::indicator:checked {\n"
                                              "   image: url(" + self.currentPath + "/icons/radio_checked.svg);\n"
                                              "}\n"
                                              "QRadioButton::indicator:unchecked {\n"
                                              "    image: url(" + self.currentPath + "/icons/radio_unchecked.svg);\n"
                                              "}")
        self.radioButtonTestnet.setObjectName("radioButtonTestnet")
        self.widgetFooter = QtWidgets.QWidget(btmhdw)
        self.widgetFooter.setGeometry(QtCore.QRect(510, 600, 211, 31))
        self.widgetFooter.setObjectName("widgetFooter")
        self.pushButtonExit = QtWidgets.QPushButton(self.widgetFooter)
        self.pushButtonExit.setGeometry(QtCore.QRect(110, 0, 99, 31))
        self.pushButtonExit.setObjectName("pushButtonExit")
        self.pushButtonSave = QtWidgets.QPushButton(self.widgetFooter)
        self.pushButtonSave.setEnabled(False)
        self.pushButtonSave.setGeometry(QtCore.QRect(0, 0, 99, 31))
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.widgetPaths = QtWidgets.QWidget(btmhdw)
        self.widgetPaths.setGeometry(QtCore.QRect(590, 10, 131, 111))
        self.widgetPaths.setObjectName("widgetPaths")
        self.labelPathAddress = QtWidgets.QLabel(self.widgetPaths)
        self.labelPathAddress.setGeometry(QtCore.QRect(0, 80, 71, 31))
        self.labelPathAddress.setObjectName("labelPathAddress")
        self.labelPathChange = QtWidgets.QLabel(self.widgetPaths)
        self.labelPathChange.setGeometry(QtCore.QRect(0, 40, 61, 31))
        self.labelPathChange.setObjectName("labelPathChange")
        self.spinBoxPathAccount = QtWidgets.QSpinBox(self.widgetPaths)
        self.spinBoxPathAccount.setGeometry(QtCore.QRect(71, 0, 51, 31))
        self.spinBoxPathAccount.setProperty("value", 1)
        self.spinBoxPathAccount.setObjectName("spinBoxPathAccount")
        self.labelPathAccount = QtWidgets.QLabel(self.widgetPaths)
        self.labelPathAccount.setGeometry(QtCore.QRect(0, 0, 71, 31))
        self.labelPathAccount.setObjectName("labelPathAccount")
        self.spinBoxPathChange = QtWidgets.QSpinBox(self.widgetPaths)
        self.spinBoxPathChange.setEnabled(True)
        self.spinBoxPathChange.setGeometry(QtCore.QRect(71, 40, 51, 31))
        self.spinBoxPathChange.setMaximum(1)
        self.spinBoxPathChange.setObjectName("spinBoxPathChange")
        self.spinBoxPathAddress = QtWidgets.QSpinBox(self.widgetPaths)
        self.spinBoxPathAddress.setEnabled(True)
        self.spinBoxPathAddress.setGeometry(QtCore.QRect(71, 80, 51, 31))
        self.spinBoxPathAddress.setProperty("value", 1)
        self.spinBoxPathAddress.setObjectName("spinBoxPathAddress")
        self.labelBtmhdwLogo = QtWidgets.QLabel(btmhdw)
        self.labelBtmhdwLogo.setGeometry(QtCore.QRect(10, 10, 471, 111))
        self.labelBtmhdwLogo.setText("")
        self.labelBtmhdwLogo.setPixmap(QtGui.QPixmap("btmhdw.png"))
        self.labelBtmhdwLogo.setObjectName("labelBtmhdwLogo")
        self.textEditLine = QtWidgets.QTextEdit(btmhdw)
        self.textEditLine.setEnabled(False)
        self.textEditLine.setGeometry(QtCore.QRect(579, 21, 2, 89))
        self.textEditLine.setStyleSheet("background: rgb(161, 161, 176);")
        self.textEditLine.setObjectName("textEditLine")
        self.checkBoxLog = QtWidgets.QCheckBox(btmhdw)
        self.checkBoxLog.setGeometry(QtCore.QRect(10, 600, 111, 31))
        self.checkBoxLog.setStyleSheet("QCheckBox::indicator {\n"
                                       "    width: 16px;\n"
                                       "    height: 16px;\n"
                                       "}\n"
                                       "QCheckBox::indicator:checked {\n"
                                       "    image: url(" + self.currentPath + "/icons/checkbox_checked.svg);\n"
                                       "}\n"
                                       "QCheckBox::indicator:unchecked {\n"
                                       "    image: url(" + self.currentPath + "/icons/checkbox_unchecked.svg);\n"
                                       "}")
        self.checkBoxLog.setTristate(False)
        self.checkBoxLog.setObjectName("checkBoxLog")
        self.checkBoxNightMode = QtWidgets.QCheckBox(btmhdw)
        self.checkBoxNightMode.setGeometry(QtCore.QRect(110, 600, 111, 31))
        self.checkBoxNightMode.setStyleSheet("QCheckBox::indicator {\n"
                                             "    width: 16px;\n"
                                             "    height: 16px;\n"
                                             "}\n"
                                             "QCheckBox::indicator:checked {\n"
                                             "    image: url(" + self.currentPath + "/icons/checkbox_checked.svg);\n"
                                             "}\n"
                                             "QCheckBox::indicator:unchecked {\n"
                                             "    image: url(" + self.currentPath + "/icons/checkbox_unchecked.svg);\n"
                                             "}")
        self.checkBoxNightMode.setCheckable(True)
        self.checkBoxNightMode.setObjectName("checkBoxNightMode")
        self.widgetHome = QtWidgets.QWidget(btmhdw)
        self.widgetHome.setGeometry(QtCore.QRect(10, 330, 711, 261))
        self.widgetHome.setObjectName("widgetHome")
        self.textEditHome = QtWidgets.QTextEdit(self.widgetHome)
        self.textEditHome.setGeometry(QtCore.QRect(0, 0, 711, 261))
        self.textEditHome.setStyleSheet("background: transparent;\n"
                                        "border: none;")
        self.textEditHome.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditHome.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditHome.setReadOnly(True)
        self.textEditHome.setObjectName("textEditHome")
        self.labelCopyright = QtWidgets.QLabel(btmhdw)
        self.labelCopyright.setGeometry(QtCore.QRect(230, 600, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.labelCopyright.setFont(font)
        self.labelCopyright.setStyleSheet("color: rgb(121, 121, 121);")
        self.labelCopyright.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCopyright.setObjectName("labelCopyright")
        self.widgetLog = QtWidgets.QWidget(btmhdw)
        self.widgetLog.setGeometry(QtCore.QRect(10, 330, 711, 261))
        self.widgetLog.setObjectName("widgetLog")
        self.textEditLog = QtWidgets.QTextEdit(self.widgetLog)
        self.textEditLog.setGeometry(QtCore.QRect(0, 25, 711, 231))
        self.textEditLog.setStyleSheet("background: transparent;\n"
                                       "border: none;")
        self.textEditLog.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditLog.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditLog.setReadOnly(True)
        self.textEditLog.setObjectName("textEditLog")
        self.textEditLogLabel = QtWidgets.QTextEdit(self.widgetLog)
        self.textEditLogLabel.setGeometry(QtCore.QRect(0, 0, 611, 31))
        self.textEditLogLabel.setStyleSheet("background: transparent;\n"
                                            "border: none;")
        self.textEditLogLabel.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditLogLabel.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditLogLabel.setReadOnly(True)
        self.textEditLogLabel.setObjectName("textEditLogLabel")
        self.pushButtonLog = QtWidgets.QPushButton(self.widgetLog)
        self.pushButtonLog.setGeometry(QtCore.QRect(622, 0, 88, 31))
        self.pushButtonLog.setObjectName("pushButtonLog")
        self.textEditStatus = QtWidgets.QTextEdit(btmhdw)
        self.textEditStatus.setGeometry(QtCore.QRect(112, 100, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Droid Sans Fallback")
        font.setBold(True)
        font.setWeight(75)
        self.textEditStatus.setFont(font)
        self.textEditStatus.setStyleSheet("background: transparent;\n"
                                          "border: none;")
        self.textEditStatus.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditStatus.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditStatus.setReadOnly(True)
        self.textEditStatus.setObjectName("textEditStatus")
        self.widgetHDWallet = QtWidgets.QWidget(btmhdw)
        self.widgetHDWallet.setGeometry(QtCore.QRect(10, 330, 711, 268))
        self.widgetHDWallet.setObjectName("widgetHDWallet")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.widgetHDWallet)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 711, 281))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutHDWallet = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayoutHDWallet.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutHDWallet.setSpacing(0)
        self.verticalLayoutHDWallet.setObjectName("verticalLayoutHDWallet")
        self.widgetMnemonic = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.widgetMnemonic.setObjectName("widgetMnemonic")
        self.textEditMnemonicLabel = QtWidgets.QTextEdit(self.widgetMnemonic)
        self.textEditMnemonicLabel.setGeometry(QtCore.QRect(0, 0, 311, 61))
        self.textEditMnemonicLabel.setAutoFillBackground(False)
        self.textEditMnemonicLabel.setStyleSheet("background: transparent;\n"
                                                 "border: none;")
        self.textEditMnemonicLabel.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditMnemonicLabel.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditMnemonicLabel.setReadOnly(True)
        self.textEditMnemonicLabel.setObjectName("textEditMnemonicLabel")
        self.textEditMnemonic = QtWidgets.QTextEdit(self.widgetMnemonic)
        self.textEditMnemonic.setGeometry(QtCore.QRect(90, 0, 621, 61))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textEditMnemonic.setFont(font)
        self.textEditMnemonic.setAutoFillBackground(False)
        self.textEditMnemonic.setStyleSheet("background: transparent;\n"
                                            "border: none;")
        self.textEditMnemonic.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditMnemonic.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditMnemonic.setReadOnly(True)
        self.textEditMnemonic.setObjectName("textEditMnemonic")
        self.verticalLayoutHDWallet.addWidget(self.widgetMnemonic)
        self.widgetAddress = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.widgetAddress.setEnabled(True)
        self.widgetAddress.setObjectName("widgetAddress")
        self.textEditAddressLabel = QtWidgets.QTextEdit(self.widgetAddress)
        self.textEditAddressLabel.setGeometry(QtCore.QRect(0, 0, 281, 51))
        self.textEditAddressLabel.setAutoFillBackground(False)
        self.textEditAddressLabel.setStyleSheet("background: transparent;\n"
                                                "border: none;\n"
                                                "margin: 6 0;")
        self.textEditAddressLabel.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditAddressLabel.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditAddressLabel.setReadOnly(True)
        self.textEditAddressLabel.setObjectName("textEditAddressLabel")
        self.textEditAddress = QtWidgets.QTextEdit(self.widgetAddress)
        self.textEditAddress.setGeometry(QtCore.QRect(76, 0, 631, 41))
        self.textEditAddress.setStyleSheet("background: transparent;\n"
                                           "border: none;\n"
                                           "margin: 6 0;")
        self.textEditAddress.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditAddress.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditAddress.setReadOnly(True)
        self.textEditAddress.setObjectName("textEditAddress")
        self.verticalLayoutHDWallet.addWidget(self.widgetAddress)
        self.widgetSeed = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.widgetSeed.setObjectName("widgetSeed")
        self.textEditSeedLabel = QtWidgets.QTextEdit(self.widgetSeed)
        self.textEditSeedLabel.setGeometry(QtCore.QRect(0, -3, 261, 51))
        self.textEditSeedLabel.setAutoFillBackground(False)
        self.textEditSeedLabel.setStyleSheet("background: transparent;\n"
                                             "border: none;")
        self.textEditSeedLabel.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditSeedLabel.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditSeedLabel.setReadOnly(True)
        self.textEditSeedLabel.setObjectName("textEditSeedLabel")
        self.textEditSeed = QtWidgets.QTextEdit(self.widgetSeed)
        self.textEditSeed.setGeometry(QtCore.QRect(51, -3, 657, 51))
        self.textEditSeed.setStyleSheet("background: transparent;\n"
                                        "border: none;")
        self.textEditSeed.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditSeed.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditSeed.setReadOnly(True)
        self.textEditSeed.setObjectName("textEditSeed")
        self.verticalLayoutHDWallet.addWidget(self.widgetSeed)
        self.widgetXPublicKey = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.widgetXPublicKey.setObjectName("widgetXPublicKey")
        self.textEditXPublicKeyLabel = QtWidgets.QTextEdit(self.widgetXPublicKey)
        self.textEditXPublicKeyLabel.setGeometry(QtCore.QRect(0, 0, 321, 51))
        self.textEditXPublicKeyLabel.setAutoFillBackground(False)
        self.textEditXPublicKeyLabel.setStyleSheet("background: transparent;\n"
                                                   "border: none;")
        self.textEditXPublicKeyLabel.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditXPublicKeyLabel.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditXPublicKeyLabel.setReadOnly(True)
        self.textEditXPublicKeyLabel.setObjectName("textEditXPublicKeyLabel")
        self.textEditXPublicKey = QtWidgets.QTextEdit(self.widgetXPublicKey)
        self.textEditXPublicKey.setGeometry(QtCore.QRect(105, 0, 601, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textEditXPublicKey.setFont(font)
        self.textEditXPublicKey.setStyleSheet("background: transparent;\n"
                                              "border: none;")
        self.textEditXPublicKey.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditXPublicKey.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditXPublicKey.setReadOnly(True)
        self.textEditXPublicKey.setObjectName("textEditXPublicKey")
        self.verticalLayoutHDWallet.addWidget(self.widgetXPublicKey)
        self.widgetXPrivateKey = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.widgetXPrivateKey.setObjectName("widgetXPrivateKey")
        self.textEditXPrivateKeyLabel = QtWidgets.QTextEdit(self.widgetXPrivateKey)
        self.textEditXPrivateKeyLabel.setGeometry(QtCore.QRect(0, 3, 321, 51))
        self.textEditXPrivateKeyLabel.setAutoFillBackground(False)
        self.textEditXPrivateKeyLabel.setStyleSheet("background: transparent;\n"
                                                    "border: none;")
        self.textEditXPrivateKeyLabel.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditXPrivateKeyLabel.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditXPrivateKeyLabel.setReadOnly(True)
        self.textEditXPrivateKeyLabel.setObjectName("textEditXPrivateKeyLabel")
        self.textEditXPrivateKey = QtWidgets.QTextEdit(self.widgetXPrivateKey)
        self.textEditXPrivateKey.setGeometry(QtCore.QRect(116, 3, 591, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textEditXPrivateKey.setFont(font)
        self.textEditXPrivateKey.setStyleSheet("background: transparent;\n"
                                               "border: none;")
        self.textEditXPrivateKey.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditXPrivateKey.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditXPrivateKey.setReadOnly(True)
        self.textEditXPrivateKey.setObjectName("textEditXPrivateKey")
        self.verticalLayoutHDWallet.addWidget(self.widgetXPrivateKey)
        self.widgetContractProgram = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.widgetContractProgram.setObjectName("widgetContractProgram")
        self.textEditContractProgramLabel = QtWidgets.QTextEdit(self.widgetContractProgram)
        self.textEditContractProgramLabel.setGeometry(QtCore.QRect(0, 0, 301, 41))
        self.textEditContractProgramLabel.setAutoFillBackground(False)
        self.textEditContractProgramLabel.setStyleSheet("background: transparent;\n"
                                                        "border: none;\n"
                                                        "margin: 6 0;")
        self.textEditContractProgramLabel.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditContractProgramLabel.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditContractProgramLabel.setReadOnly(True)
        self.textEditContractProgramLabel.setObjectName("textEditContractProgramLabel")
        self.textEditContractProgram = QtWidgets.QTextEdit(self.widgetContractProgram)
        self.textEditContractProgram.setEnabled(True)
        self.textEditContractProgram.setGeometry(QtCore.QRect(153, 0, 551, 51))
        self.textEditContractProgram.setStyleSheet("background: transparent;\n"
                                                   "border: none;\n"
                                                   "margin: 6 0;")
        self.textEditContractProgram.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditContractProgram.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditContractProgram.setReadOnly(True)
        self.textEditContractProgram.setObjectName("textEditContractProgram")
        self.verticalLayoutHDWallet.addWidget(self.widgetContractProgram)
        self.widgetPath = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.widgetPath.setObjectName("widgetPath")
        self.textEditPathLabel = QtWidgets.QTextEdit(self.widgetPath)
        self.textEditPathLabel.setGeometry(QtCore.QRect(0, 0, 101, 41))
        self.textEditPathLabel.setAutoFillBackground(False)
        self.textEditPathLabel.setStyleSheet("background: transparent;\n"
                                             "border: none;")
        self.textEditPathLabel.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditPathLabel.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditPathLabel.setReadOnly(True)
        self.textEditPathLabel.setObjectName("textEditPathLabel")
        self.textEditPath = QtWidgets.QTextEdit(self.widgetPath)
        self.textEditPath.setGeometry(QtCore.QRect(49, 0, 661, 41))
        self.textEditPath.setStyleSheet("background: transparent;\n"
                                        "border: none;")
        self.textEditPath.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditPath.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditPath.setReadOnly(True)
        self.textEditPath.setObjectName("textEditPath")
        self.verticalLayoutHDWallet.addWidget(self.widgetPath)

        self.retranslateUi(btmhdw)
        QtCore.QMetaObject.connectSlotsByName(btmhdw)

    def retranslateUi(self, btmhdw):
        _translate = QtCore.QCoreApplication.translate
        btmhdw.setWindowTitle(_translate("btmhdw", "BTMHDW"))
        self.lineEditBtmhdw.setPlaceholderText(
            _translate("btmhdw", "Mnemonic/Entropy/XPrivate Key/XPublic Key/Contract Program"))
        self.pushButtonGetHDWalletFromMnemonic.setText(_translate("btmhdw", "Get HDWallet from Mnemonic"))
        self.pushButtonGenerateMnemonic.setText(_translate("btmhdw", "Generate Mnemonic"))
        self.pushButtonGenerateEntropy.setText(_translate("btmhdw", "Generate Entropy"))
        self.radioButtonEnglish.setText(_translate("btmhdw", "English"))
        self.radioButtonJapanese.setText(_translate("btmhdw", "Japanese"))
        self.pushButtonGetHDWalletFromEntropy.setText(_translate("btmhdw", "Get HDWallet form Entropy"))
        self.pushButtonGetContractProgramFromXPublicKey.setText(
            _translate("btmhdw", "Get Contract Program form XPublic Key"))
        self.checkBoxPath.setText(_translate("btmhdw", "Path"))
        self.lineEditPath.setPlaceholderText(_translate("btmhdw", self.path))
        self.pushButtonGetHDWalletFromXPrivateKey.setText(_translate("btmhdw", "Get HDWallet form XPrivate Key"))
        self.lineEditPassword.setPlaceholderText(_translate("btmhdw", "Password"))
        self.radioButtonSolonet.setText(_translate("btmhdw", "Solonet"))
        self.radioButtonMainnet.setText(_translate("btmhdw", "Mainnet"))
        self.radioButtonTestnet.setText(_translate("btmhdw", "Testnet"))
        self.pushButtonExit.setText(_translate("btmhdw", "Exit"))
        self.pushButtonSave.setText(_translate("btmhdw", "Save"))
        self.labelPathAddress.setText(_translate("btmhdw", "Address"))
        self.labelPathChange.setText(_translate("btmhdw", "Change"))
        self.labelPathAccount.setText(_translate("btmhdw", "Account"))
        self.checkBoxLog.setText(_translate("btmhdw", "View Log"))
        self.checkBoxNightMode.setText(_translate("btmhdw", "Night Mode"))
        self.textEditHome.setHtml(_translate("btmhdw",
                                             "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                             "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                             "p, li { white-space: pre-wrap; }\n"
                                             "</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                             "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:26pt; font-weight:600; color:#878787;\">btmhdw</span></p>\n"
                                             "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10pt; color:#747474;\">Version 0.1.1</span></p>\n"
                                             "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; color:#747474;\"><br /></p>\n"
                                             "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-style:italic; color:#747474;\">The implementation of Hierarchical Deterministic (HD) wallets generator for Bytom blockchain.</span></p>\n"
                                             "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-style:italic; color:#747474;\"><br /></p>\n"
                                             "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10pt; font-style:italic; color:#747474;\">With btmhdw you can generate mnemonic(English or Japanese language 12 words)/enteropy for new HDWallet, you can get HDWallet from XPrivate key, you can drive your own path(Index) and you can get HDWallet address from contract program/XPublic key.</span></p>\n"
                                             "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-size:10pt; font-style:italic; color:#747474;\"><br /></p>\n"
                                             "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10pt; font-style:italic; color:#747474;\">Github </span><span style=\" font-family:\'Ubuntu\'; font-size:10pt; color:#747474;\">https://github.com/meherett/btmhdw</span></p>\n"
                                             "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10pt; font-style:italic; color:#747474;\">Auther </span><span style=\" font-family:\'Ubuntu\'; font-size:10pt; color:#747474;\">Meheret Tesfaye</span></p>\n"
                                             "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10pt; font-style:italic; color:#747474;\">Email meherett@zoho.com</span></p></body></html>"))
        self.labelCopyright.setText(_translate("btmhdw", "Copyright © 2019 BTMHDW"))
        self.textEditLog.setHtml(_translate("btmhdw",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textEditLogLabel.setHtml(_translate("btmhdw",
                                                 "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                 "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                 "p, li { white-space: pre-wrap; }\n"
                                                 "</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                                 "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:12pt; font-weight:600; color:#909090;\">BTMHDW Log</span></p></body></html>"))
        self.pushButtonLog.setText(_translate("btmhdw", "Clear Log"))
        self.textEditStatus.setHtml(_translate("btmhdw",
                                               "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                               "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                               "p, li { white-space: pre-wrap; }\n"
                                               "</style></head><body style=\" font-family:\'Droid Sans Fallback\'; font-size:11pt; font-weight:600; font-style:normal;\">\n"
                                               "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#555555;\">STATUS</span></p></body></html>"))
        self.textEditMnemonicLabel.setHtml(_translate("btmhdw",
                                                      "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                      "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                      "p, li { white-space: pre-wrap; }\n"
                                                      "</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                                      "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10.5pt; font-weight:600;\">Mnemonic</span></p></body></html>"))
        self.textEditMnemonic.setHtml(_translate("btmhdw",
                                                 "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                 "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                 "p, li { white-space: pre-wrap; }\n"
                                                 "</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                                 "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10.5pt;\">とおるãげこうãへいおんãにげるãはけんãいどうãふあんãよそくãひんこんãついかãはったつãしゃいん</span></p></body></html>"))
        self.textEditAddressLabel.setHtml(_translate("btmhdw",
                                                     "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                     "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                     "p, li { white-space: pre-wrap; }\n"
                                                     "</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10.5pt; font-weight:600;\">Address</span></p></body></html>"))
        self.textEditAddress.setHtml(_translate("btmhdw",
                                                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                "p, li { white-space: pre-wrap; }\n"
                                                "</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10.5pt;\">bm1qq5nzpwr2d40qwvga2qval73cvnxv3f4au5vrht</span></p></body></html>"))
        self.textEditSeedLabel.setHtml(_translate("btmhdw",
                                                  "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                  "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                  "p, li { white-space: pre-wrap; }\n"
                                                  "</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10.5pt; font-weight:600;\">Seed</span></p></body></html>"))
        self.textEditSeed.setHtml(_translate("btmhdw",
                                             "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                             "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                             "p, li { white-space: pre-wrap; }\n"
                                             "</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                             "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10.5pt;\">d47ece6097f93b5d19259886d210dab017f5b37520b4dad8160712fd5b1065e7189b8b295cc023e0b2c78f79725f859ac512afdfebc0b94cfd83faa59e42d82e</span></p></body></html>"))
        self.textEditXPublicKeyLabel.setHtml(_translate("btmhdw",
                                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                        "p, li { white-space: pre-wrap; }\n"
                                                        "</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10.5pt; font-weight:600;\">XPublic Key</span></p></body></html>"))
        self.textEditXPublicKey.setHtml(_translate("btmhdw",
                                                   "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                   "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                   "p, li { white-space: pre-wrap; }\n"
                                                   "</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                                   "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10.5pt;\">d47ece6097f93b5d19259886d210dab017f5b37520b4dad8160712fd5b1065e7189b8b295cc023e0b2c78f79725f859ac512afdfebc0b94cfd83faa59e42d82e</span></p></body></html>"))
        self.textEditXPrivateKeyLabel.setHtml(_translate("btmhdw",
                                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                         "p, li { white-space: pre-wrap; }\n"
                                                         "</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10.5pt; font-weight:600;\">XPrivate Key</span></p></body></html>"))
        self.textEditXPrivateKey.setHtml(_translate("btmhdw",
                                                    "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                    "p, li { white-space: pre-wrap; }\n"
                                                    "</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                                    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10.5pt;\">d47ece6097f93b5d19259886d210dab017f5b37520b4dad8160712fd5b1065e7189b8b295cc023e0b2c78f79725f859ac512afdfebc0b94cfd83faa59e42d82e</span></p></body></html>"))
        self.textEditContractProgramLabel.setHtml(_translate("btmhdw",
                                                             "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                             "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                             "p, li { white-space: pre-wrap; }\n"
                                                             "</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                                             "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10.5pt; font-weight:600;\">Contract Program</span></p></body></html>"))
        self.textEditContractProgram.setHtml(_translate("btmhdw",
                                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                        "p, li { white-space: pre-wrap; }\n"
                                                        "</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10.5pt;\">001478c3aa31753389fcde04d33d0779bdc2840f0ad4</span></p></body></html>"))
        self.textEditPathLabel.setHtml(_translate("btmhdw",
                                                  "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                  "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                  "p, li { white-space: pre-wrap; }\n"
                                                  "</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10.5pt; font-weight:600;\">Path</span></p></body></html>"))
        self.textEditPath.setHtml(_translate("btmhdw",
                                             "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                             "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                             "p, li { white-space: pre-wrap; }\n"
                                             "</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                             "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10.5pt;\">m/44/153/1/0/1</span></p></body></html>"))

        # Button
        self.pushButtonGenerateMnemonic.clicked.connect(self.generateMnemonic)
        self.pushButtonGenerateEntropy.clicked.connect(self.generateEntropy)
        self.pushButtonGetHDWalletFromMnemonic.clicked.connect(self.getHDWalletFromMnemonic)
        self.pushButtonGetHDWalletFromEntropy.clicked.connect(self.getHDWalletFromEntropy)
        self.pushButtonGetHDWalletFromXPrivateKey.clicked.connect(self.getHDWalletFromXPrivateKey)
        self.pushButtonGetContractProgramFromXPublicKey.clicked.connect(self.getContractProgramFromXPublicKey)
        self.pushButtonLog.clicked.connect(self.clearLog)
        self.pushButtonSave.clicked.connect(self.saveFileDialog)
        self.pushButtonExit.clicked.connect(self.exitBtmhdw)
        # CheckBox Button
        self.checkBoxLog.clicked.connect(self.viewLog)
        self.checkBoxNightMode.clicked.connect(lambda: self.nightMode(btmhdw))
        self.checkBoxPath.clicked.connect(self.onPath)
        # Radio Button
        self.radioButtonEnglish.toggled.connect(lambda: self.checkLanguage(self.radioButtonEnglish))
        self.radioButtonJapanese.toggled.connect(lambda: self.checkLanguage(self.radioButtonJapanese))
        self.radioButtonMainnet.toggled.connect(lambda: self.checkNetwork(self.radioButtonMainnet))
        self.radioButtonTestnet.toggled.connect(lambda: self.checkNetwork(self.radioButtonTestnet))
        self.radioButtonSolonet.toggled.connect(lambda: self.checkNetwork(self.radioButtonSolonet))
        # SpinBox Button
        self.spinBoxPathAccount.valueChanged.connect(self.getPath)
        self.spinBoxPathChange.valueChanged.connect(self.getPath)
        self.spinBoxPathAddress.valueChanged.connect(self.getPath)

        # self.widgetHome.setHidden(True)
        self.widgetLog.setHidden(True)
        self.widgetHDWallet.setHidden(True)

    def onPath(self):
        if self.checkBoxPath.isChecked():
            self.lineEditPath.setEnabled(True)
            self.spinBoxPathAccount.setEnabled(False)
            self.spinBoxPathChange.setEnabled(False)
            self.spinBoxPathAddress.setEnabled(False)
        else:
            self.lineEditPath.setEnabled(False)
            self.spinBoxPathAccount.setEnabled(True)
            self.spinBoxPathChange.setEnabled(True)
            self.spinBoxPathAddress.setEnabled(True)

    def getPath(self):
        _translate = QtCore.QCoreApplication.translate
        if self.checkBoxPath.isChecked():
            if str(self.lineEditPath.text())[0:2] != 'm/':
                self.hideHome = False
                self.setStatus("WARNING")
                self.widgetHome.setHidden(True)
                self.widgetLog.setHidden(False)
                self.widgetHDWallet.setHidden(True)
                self.console("WARNING", "Path", "Bad path, please insert like this type of path \"m/0'/0\"! ")
                return True
            else:
                self.path = self.lineEditPath.text()
                self.lineEditPath.setPlaceholderText(_translate("btmhdw", self.path))
                return False
        else:
            self.path = str("m/44/153/%s/%s/%s" % (
                str(self.spinBoxPathAccount.value()),
                str(self.spinBoxPathChange.value()),
                str(self.spinBoxPathAddress.value())
            ))
            self.lineEditPath.setPlaceholderText(_translate("btmhdw", self.path))
            return False

    def setStatus(self, status):
        _translate = QtCore.QCoreApplication.translate
        if status == "SUCCESS":
            self.textEditStatus.setHtml(_translate("btmhdw",
                                                   "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                   "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                   "p, li { white-space: pre-wrap; }\n"
                                                   "</style></head><body style=\" font-family:\'Droid Sans Fallback\'; font-size:11pt; font-weight:600; font-style:normal;\">\n"
                                                   "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color: green;\">SUCCESS</span></p></body></html>"))

        elif status == "WARNING":
            self.textEditStatus.setHtml(_translate("btmhdw",
                                                   "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                   "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                   "p, li { white-space: pre-wrap; }\n"
                                                   "</style></head><body style=\" font-family:\'Droid Sans Fallback\'; font-size:11pt; font-weight:600; font-style:normal;\">\n"
                                                   "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color: rgb(237, 212, 0);\">WARNING</span></p></body></html>"))
        elif status == "ERROR":
            self.textEditStatus.setHtml(_translate("btmhdw",
                                                   "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                   "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                   "p, li { white-space: pre-wrap; }\n"
                                                   "</style></head><body style=\" font-family:\'Droid Sans Fallback\'; font-size:11pt; font-weight:600; font-style:normal;\">\n"
                                                   "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color: red;\">ERROR</span></p></body></html>"))

    def consConsole(self):
        return str(
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n" + self.consoleMessage + "</body></html>")

    def console(self, _type, title, text):
        _translate = QtCore.QCoreApplication.translate
        if _type == "SUCCESS":
            newMessage = str(
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10pt; color: green; font-weight:600;\">[" + _type + "]</span><span style=\" font-family:\'Ubuntu\'; font-size:10pt;\">: </span><span style=\" font-family:\'Ubuntu\'; font-size:10pt; color:#999999;\">" + title + "</span></p>\n"
                                                                                                                                                                                                                                                                                                                                                                                                              "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10pt;\">                     " + text + "</span></p>\n")
        elif _type == "ERROR":
            newMessage = str(
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10pt; color: red; font-weight:600;\">[" + _type + "]</span><span style=\" font-family:\'Ubuntu\'; font-size:10pt;\">: </span><span style=\" font-family:\'Ubuntu\'; font-size:10pt; color:#999999;\">" + title + "</span></p>\n"
                                                                                                                                                                                                                                                                                                                                                                                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10pt;\">                 " + text + "</span></p>\n")
        elif _type == "WARNING":
            newMessage = str(
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10pt; color: rgb(237, 212, 0); font-weight:600;\">[" + _type + "]</span><span style=\" font-family:\'Ubuntu\'; font-size:10pt;\">: </span><span style=\" font-family:\'Ubuntu\'; font-size:10pt; color:#999999;\">" + title + "</span></p>\n"
                                                                                                                                                                                                                                                                                                                                                                                                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:10pt;\">                      " + text + "</span></p>\n")
        self.consoleMessage = self.consoleMessage + newMessage
        self.textEditLog.setHtml(_translate("btmhdw", self.consConsole()))
        self.textEditLog.verticalScrollBar().setValue(self.textEditLog.verticalScrollBar().maximum())

    def checkLanguage(self, language):
        if language.text() == "English":
            if language.isChecked():
                self.language = "english"
            else:
                self.language = "japanese"
        if language.text() == "Japanese":
            if language.isChecked():
                self.language = "japanese"
            else:
                self.language = "english"

    def checkNetwork(self, network):
        if network.text() == "Mainnet":
            if network.isChecked():
                self.network = "mainnet"
        if network.text() == "Testnet":
            if network.isChecked():
                self.network = "testnet"
        if network.text() == "Solonet":
            if network.isChecked():
                self.network = "solonet"

    def nightMode(self, btmhdw):
        if self.checkBoxNightMode.isChecked():
            import qdarkstyle
            btmhdw.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
            self.textEditXPrivateKey.setGeometry(QtCore.QRect(116, 1.5, 591, 51))
        else:
            btmhdw.setStyleSheet(str())

    def viewLog(self):
        if self.checkBoxLog.isChecked():
            self.widgetHome.setHidden(True)
            self.widgetLog.setHidden(False)
            self.widgetHDWallet.setHidden(True)
        else:
            if self.hideHome:
                self.widgetHome.setHidden(True)
                self.widgetLog.setHidden(True)
                self.widgetHDWallet.setHidden(False)
            else:
                self.widgetHome.setHidden(False)
                self.widgetLog.setHidden(True)
                self.widgetHDWallet.setHidden(True)

    def clearLog(self):
        self.consoleMessage = str()
        self.textEditLog.setHtml(self.consoleMessage)

    def exitBtmhdw(self):
        import sys
        sys.exit()

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self.window, "BTMHDW Save", "",
                                                  "Json Files (*.json)",
                                                  options=options)
        if fileName and self.saveHDWallet:
            import json
            with open(fileName, 'w', encoding='utf-8') as f:
                json.dump(self.saveHDWallet, f, ensure_ascii=False, indent=4)

    def generateMnemonic(self):
        self.lineEditBtmhdw.setText(str(BTMHDW().generateMnemonic(language=self.language)))

    def generateEntropy(self):
        self.lineEditBtmhdw.setText(str(BTMHDW().generateEntropy().hex()))

    def getHDWalletFromMnemonic(self):
        lineEditBtmhdw = self.lineEditBtmhdw.text()
        lineEditPassword = self.lineEditPassword.text()
        if not lineEditPassword:
            lineEditPassword = str()
        if BytomHDWallet().checkMnemonic(lineEditBtmhdw, language=self.language):
            if not self.getPath():
                self.hideHome = True
                newHDWalletFromMnemonic = BTMHDW().createWallet(mnemonic=lineEditBtmhdw,
                                                                network=self.network,
                                                                passphrase=lineEditPassword,
                                                                path=self.path)
                self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 711, 281))
                self.saveHDWallet = newHDWalletFromMnemonic
                self.pushButtonSave.setEnabled(True)
                self.widgetMnemonic.setHidden(False)
                self.textEditMnemonic.setText(newHDWalletFromMnemonic['mnemonic'])
                self.widgetAddress.setHidden(False)
                self.textEditAddress.setText(newHDWalletFromMnemonic['address'])
                self.widgetSeed.setHidden(False)
                self.textEditSeed.setText(newHDWalletFromMnemonic['seed'])
                self.textEditXPublicKey.setText(newHDWalletFromMnemonic['xpublic'])
                self.widgetXPrivateKey.setHidden(False)
                self.textEditXPrivateKey.setText(newHDWalletFromMnemonic['xprivate'])
                self.textEditContractProgram.setText(newHDWalletFromMnemonic['program'])
                self.textEditPath.setText(newHDWalletFromMnemonic['path'])
                self.setStatus('SUCCESS')
                self.console('SUCCESS', 'GetHDWalletFromMnemonic',
                             'Successfully generated new HDWallet from Mnemonic!')
                self.widgetHome.setHidden(True)
                self.widgetLog.setHidden(True)
                self.checkBoxLog.setChecked(False)
                self.widgetHDWallet.setHidden(False)
        else:
            self.hideHome = False
            self.setStatus('ERROR')
            self.console('ERROR', 'GetHDWalletFromMnemonic',
                         'Please check you mnemonic, insert mnemonic!')
            self.saveHDWallet = None
            self.pushButtonSave.setEnabled(False)
            self.widgetHome.setHidden(True)
            self.widgetLog.setHidden(False)
            self.checkBoxLog.setChecked(True)
            self.widgetHDWallet.setHidden(True)

    def getHDWalletFromEntropy(self):
        lineEditBtmhdw = self.lineEditBtmhdw.text()
        lineEditPassword = self.lineEditPassword.text()
        if not lineEditPassword:
            lineEditPassword = str()
        if lineEditBtmhdw and len(str(lineEditBtmhdw)) == 32:
            if not self.getPath():
                self.hideHome = True
                newHDWalletFromEntropy = BTMHDW().createWallet(entropy=lineEditBtmhdw.encode(),
                                                               network=self.network,
                                                               passphrase=lineEditPassword,
                                                               path=self.path)
                self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 711, 281))
                self.saveHDWallet = newHDWalletFromEntropy
                self.pushButtonSave.setEnabled(True)
                self.widgetMnemonic.setHidden(False)
                self.textEditMnemonic.setText(newHDWalletFromEntropy['mnemonic'])
                self.widgetAddress.setHidden(False)
                self.textEditAddress.setText(newHDWalletFromEntropy['address'])
                self.widgetSeed.setHidden(False)
                self.textEditSeed.setText(newHDWalletFromEntropy['seed'])
                self.textEditXPublicKey.setText(newHDWalletFromEntropy['xpublic'])
                self.widgetXPrivateKey.setHidden(False)
                self.textEditXPrivateKey.setText(newHDWalletFromEntropy['xprivate'])
                self.textEditContractProgram.setText(newHDWalletFromEntropy['program'])
                self.textEditPath.setText(newHDWalletFromEntropy['path'])
                self.setStatus('SUCCESS')
                self.console('SUCCESS', 'GetHDWalletFromEntropy',
                             'Successfully generated new HDWallet from Entropy!')
                self.widgetHome.setHidden(True)
                self.widgetLog.setHidden(True)
                self.checkBoxLog.setChecked(False)
                self.widgetHDWallet.setHidden(False)
        else:
            self.hideHome = False
            self.setStatus('ERROR')
            self.console('ERROR', 'GetHDWalletFromEntropy',
                         'Please check you entropy, length must be 32, insert entropy!')
            self.saveHDWallet = None
            self.pushButtonSave.setEnabled(False)
            self.widgetHome.setHidden(True)
            self.widgetLog.setHidden(False)
            self.checkBoxLog.setChecked(True)
            self.widgetHDWallet.setHidden(True)

    def getHDWalletFromXPrivateKey(self):
        lineEditBtmhdw = self.lineEditBtmhdw.text()
        lineEditPassword = self.lineEditPassword.text()
        if lineEditPassword:
            self.setStatus('WARNING')
            self.console('WARNING', 'GetHDWalletFromXPrivateKey',
                         'Please remove password, XPrivate key is not used password!')
        if lineEditBtmhdw and len(str(lineEditBtmhdw)) == 128:
            if not self.getPath():
                self.hideHome = True
                newHDWalletFromXPrivateKey = BTMHDW().walletFromXPrivate(xprivate=lineEditBtmhdw,
                                                                         network=self.network,
                                                                         path=self.path)
                self.saveHDWallet = newHDWalletFromXPrivateKey
                self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 711, 200))
                self.pushButtonSave.setEnabled(True)
                self.widgetMnemonic.setHidden(True)
                self.widgetAddress.setHidden(False)
                self.textEditAddress.setText(newHDWalletFromXPrivateKey['address'])
                self.widgetSeed.setHidden(True)
                self.textEditXPublicKey.setText(newHDWalletFromXPrivateKey['xpublic'])
                self.widgetXPrivateKey.setHidden(False)
                self.textEditXPrivateKey.setText(newHDWalletFromXPrivateKey['xprivate'])
                self.textEditContractProgram.setText(newHDWalletFromXPrivateKey['program'])
                self.textEditPath.setText(newHDWalletFromXPrivateKey['path'])
                self.setStatus('SUCCESS')
                self.console('SUCCESS', 'GetHDWalletFromXPrivateKey',
                             'Successfully get HDWallet information from XPrivate key!')
                self.widgetHome.setHidden(True)
                self.widgetLog.setHidden(True)
                self.checkBoxLog.setChecked(False)
                self.widgetHDWallet.setHidden(False)
        else:
            self.hideHome = False
            self.setStatus('ERROR')
            self.console('ERROR', 'GetHDWalletFromXPrivateKey',
                         'Please check you xprivate key, length must be 128, insert xprivate key!')
            self.saveHDWallet = None
            self.pushButtonSave.setEnabled(False)
            self.widgetHome.setHidden(True)
            self.widgetLog.setHidden(False)
            self.checkBoxLog.setChecked(True)
            self.widgetHDWallet.setHidden(True)

    def getContractProgramFromXPublicKey(self):
        lineEditBtmhdw = self.lineEditBtmhdw.text()
        lineEditPassword = self.lineEditPassword.text()
        if lineEditPassword:
            self.setStatus('WARNING')
            self.console('WARNING', 'GetHDWalletFromXPublicKey',
                         'Please remove password, XPublic key is not used password!')
        if lineEditBtmhdw and len(str(lineEditBtmhdw)) == 128:
            if not self.getPath():
                self.hideHome = True
                program = BytomHDWallet().program(xpublic=lineEditBtmhdw, path=self.path)
                newContractProgramFromXPublicKey = dict(xpublic=lineEditBtmhdw,
                                                        path=self.path,
                                                        program=program)
                self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 711, 120))
                self.saveHDWallet = newContractProgramFromXPublicKey
                self.pushButtonSave.setEnabled(True)
                self.widgetMnemonic.setHidden(True)
                self.widgetAddress.setHidden(True)
                self.widgetSeed.setHidden(True)
                self.textEditXPublicKey.setText(newContractProgramFromXPublicKey['xpublic'])
                self.widgetXPrivateKey.setHidden(True)
                self.textEditContractProgram.setText(newContractProgramFromXPublicKey['program'])
                self.textEditPath.setText(newContractProgramFromXPublicKey['path'])
                self.setStatus('SUCCESS')
                self.console('SUCCESS', 'GetContractProgramFromXPublicKey',
                             'Successfully get HDWallet contract program from XPublic key!')
                self.widgetHome.setHidden(True)
                self.widgetLog.setHidden(True)
                self.checkBoxLog.setChecked(False)
                self.widgetHDWallet.setHidden(False)
        else:
            self.hideHome = False
            self.setStatus('ERROR')
            self.console('ERROR', 'GetContractProgramFromXPublicKey',
                         'Please check you xpublic key, length must be 128, insert xpublic key!')
            self.saveHDWallet = None
            self.pushButtonSave.setEnabled(False)
            self.widgetHome.setHidden(True)
            self.widgetLog.setHidden(False)
            self.checkBoxLog.setChecked(True)
            self.widgetHDWallet.setHidden(True)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_btmhdw()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
