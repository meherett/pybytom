# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/tmp/btmhdwzk3024.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!
from btmhdw import BTMHDW, BytomHDWallet, BTMHDW_HARDEN, PATH, INDEXES
from PyQt5 import QtCore, QtGui, QtWidgets
import qdarkstyle


class Ui_btmhdw(object):

    def __init__(self):
        self.language = "english"
        self.net = "mainnet"

    def setupUi(self, btmhdw):
        btmhdw.setObjectName("btmhdw")
        btmhdw.resize(731, 642)
        btmhdw.setMinimumSize(QtCore.QSize(731, 642))
        btmhdw.setMaximumSize(QtCore.QSize(731, 642))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/btmhdw-logo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        btmhdw.setWindowIcon(icon)
        self.widgetMain = QtWidgets.QWidget(btmhdw)
        self.widgetMain.setGeometry(QtCore.QRect(10, 130, 711, 201))
        self.widgetMain.setObjectName("widgetMain")
        self.lineEditBtmhdw = QtWidgets.QLineEdit(self.widgetMain)
        self.lineEditBtmhdw.setGeometry(QtCore.QRect(0, 0, 711, 41))
        self.lineEditBtmhdw.setStyleSheet("padding: 0 10px;")
        self.lineEditBtmhdw.setObjectName("lineEditBtmhdw")
        self.pushButtonGenerateHDWallet = QtWidgets.QPushButton(self.widgetMain)
        self.pushButtonGenerateHDWallet.setGeometry(QtCore.QRect(180, 50, 241, 41))
        self.pushButtonGenerateHDWallet.setObjectName("pushButtonGenerateHDWallet")
        self.pushButtonGetAddressFromXPublicKey_2 = QtWidgets.QPushButton(self.widgetMain)
        self.pushButtonGetAddressFromXPublicKey_2.setGeometry(QtCore.QRect(430, 100, 281, 41))
        self.pushButtonGetAddressFromXPublicKey_2.setObjectName("pushButtonGetAddressFromXPublicKey_2")
        self.pushButtonGenerateMnemonic = QtWidgets.QPushButton(self.widgetMain)
        self.pushButtonGenerateMnemonic.setGeometry(QtCore.QRect(0, 100, 171, 41))
        self.pushButtonGenerateMnemonic.setObjectName("pushButtonGenerateMnemonic")
        self.pushButtonGenerateEnteropy = QtWidgets.QPushButton(self.widgetMain)
        self.pushButtonGenerateEnteropy.setGeometry(QtCore.QRect(0, 150, 171, 41))
        self.pushButtonGenerateEnteropy.setObjectName("pushButtonGenerateEnteropy")
        self.radioButtonEnglish = QtWidgets.QRadioButton(self.widgetMain)
        self.radioButtonEnglish.setGeometry(QtCore.QRect(0, 50, 81, 41))
        self.radioButtonEnglish.setStyleSheet("QRadioButton::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"   image: url(/home/meheret/PycharmProjects/btmhdw/ui/icons/radio_checked.svg);\n"
"}\n"
"QRadioButton::indicator:unchecked {\n"
"    image: url(/home/meheret/PycharmProjects/btmhdw/ui/icons/radio_unchecked.svg);\n"
"}")
        self.radioButtonEnglish.setObjectName("radioButtonEnglish")
        self.radioButtonJapanese = QtWidgets.QRadioButton(self.widgetMain)
        self.radioButtonJapanese.setGeometry(QtCore.QRect(80, 50, 91, 41))
        self.radioButtonJapanese.setStyleSheet("QRadioButton::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"   image: url(/home/meheret/PycharmProjects/btmhdw/ui/icons/radio_checked.svg);\n"
"}\n"
"QRadioButton::indicator:unchecked {\n"
"    image: url(/home/meheret/PycharmProjects/btmhdw/ui/icons/radio_unchecked.svg);\n"
"}")
        self.radioButtonJapanese.setObjectName("radioButtonJapanese")
        self.pushButtonGetInformationFromXPrivateKey_2 = QtWidgets.QPushButton(self.widgetMain)
        self.pushButtonGetInformationFromXPrivateKey_2.setGeometry(QtCore.QRect(180, 100, 241, 41))
        self.pushButtonGetInformationFromXPrivateKey_2.setObjectName("pushButtonGetInformationFromXPrivateKey_2")
        self.pushButtonGetAddressFromXPublicKey = QtWidgets.QPushButton(self.widgetMain)
        self.pushButtonGetAddressFromXPublicKey.setGeometry(QtCore.QRect(180, 150, 241, 41))
        self.pushButtonGetAddressFromXPublicKey.setObjectName("pushButtonGetAddressFromXPublicKey")
        self.checkBoxPath = QtWidgets.QCheckBox(self.widgetMain)
        self.checkBoxPath.setGeometry(QtCore.QRect(430, 150, 71, 41))
        self.checkBoxPath.setStyleSheet("QCheckBox::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    image: url(/home/meheret/PycharmProjects/btmhdw/ui/icons/checkbox_checked.svg);\n"
"}\n"
"QCheckBox::indicator:unchecked {\n"
"    image: url(/home/meheret/PycharmProjects/btmhdw/ui/icons/checkbox_unchecked.svg);\n"
"}")
        self.checkBoxPath.setObjectName("checkBoxPath")
        self.lineEditPath = QtWidgets.QLineEdit(self.widgetMain)
        self.lineEditPath.setEnabled(False)
        self.lineEditPath.setGeometry(QtCore.QRect(500, 150, 211, 41))
        self.lineEditPath.setObjectName("lineEditPath")
        self.pushButtonGetInformationFromXPrivateKey = QtWidgets.QPushButton(self.widgetMain)
        self.pushButtonGetInformationFromXPrivateKey.setGeometry(QtCore.QRect(430, 50, 281, 41))
        self.pushButtonGetInformationFromXPrivateKey.setObjectName("pushButtonGetInformationFromXPrivateKey")
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
"   image: url(/home/meheret/PycharmProjects/btmhdw/ui/icons/radio_checked.svg);\n"
"}\n"
"QRadioButton::indicator:unchecked {\n"
"    image: url(/home/meheret/PycharmProjects/btmhdw/ui/icons/radio_unchecked.svg);\n"
"}")
        self.radioButtonSolonet.setObjectName("radioButtonSolonet")
        self.radioButtonMainnet = QtWidgets.QRadioButton(self.widgetNet)
        self.radioButtonMainnet.setGeometry(QtCore.QRect(0, 0, 81, 31))
        self.radioButtonMainnet.setStyleSheet("QRadioButton::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"   image: url(/home/meheret/PycharmProjects/btmhdw/ui/icons/radio_checked.svg);\n"
"}\n"
"QRadioButton::indicator:unchecked {\n"
"    image: url(/home/meheret/PycharmProjects/btmhdw/ui/icons/radio_unchecked.svg);\n"
"}")
        self.radioButtonMainnet.setObjectName("radioButtonMainnet")
        self.radioButtonTestnet = QtWidgets.QRadioButton(self.widgetNet)
        self.radioButtonTestnet.setGeometry(QtCore.QRect(0, 40, 81, 31))
        self.radioButtonTestnet.setStyleSheet("QRadioButton::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"   image: url(/home/meheret/PycharmProjects/btmhdw/ui/icons/radio_checked.svg);\n"
"}\n"
"QRadioButton::indicator:unchecked {\n"
"    image: url(/home/meheret/PycharmProjects/btmhdw/ui/icons/radio_unchecked.svg);\n"
"}")
        self.radioButtonTestnet.setObjectName("radioButtonTestnet")
        self.widgetFooter = QtWidgets.QWidget(btmhdw)
        self.widgetFooter.setGeometry(QtCore.QRect(510, 600, 211, 31))
        self.widgetFooter.setObjectName("widgetFooter")
        self.pushButtonExit = QtWidgets.QPushButton(self.widgetFooter)
        self.pushButtonExit.setGeometry(QtCore.QRect(110, 0, 99, 31))
        self.pushButtonExit.setObjectName("pushButtonExit")
        self.pushButtonSave = QtWidgets.QPushButton(self.widgetFooter)
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
        self.spinBoxPathAccount.setObjectName("spinBoxPathAccount")
        self.labelPathAccount = QtWidgets.QLabel(self.widgetPaths)
        self.labelPathAccount.setGeometry(QtCore.QRect(0, 0, 71, 31))
        self.labelPathAccount.setObjectName("labelPathAccount")
        self.spinBoxPathChange = QtWidgets.QSpinBox(self.widgetPaths)
        self.spinBoxPathChange.setEnabled(False)
        self.spinBoxPathChange.setGeometry(QtCore.QRect(71, 40, 51, 31))
        self.spinBoxPathChange.setObjectName("spinBoxPathChange")
        self.spinBoxPathAddress = QtWidgets.QSpinBox(self.widgetPaths)
        self.spinBoxPathAddress.setEnabled(True)
        self.spinBoxPathAddress.setGeometry(QtCore.QRect(71, 80, 51, 31))
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
        self.checkBoxConsole = QtWidgets.QCheckBox(btmhdw)
        self.checkBoxConsole.setGeometry(QtCore.QRect(10, 600, 121, 31))
        self.checkBoxConsole.setStyleSheet("QCheckBox::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    image: url(/home/meheret/PycharmProjects/btmhdw/ui/icons/checkbox_checked.svg);\n"
"}\n"
"QCheckBox::indicator:unchecked {\n"
"    image: url(/home/meheret/PycharmProjects/btmhdw/ui/icons/checkbox_unchecked.svg);\n"
"}")
        self.checkBoxConsole.setTristate(False)
        self.checkBoxConsole.setObjectName("checkBoxConsole")
        self.checkBoxNightMode = QtWidgets.QCheckBox(btmhdw)
        self.checkBoxNightMode.setGeometry(QtCore.QRect(140, 600, 111, 31))
        self.checkBoxNightMode.setStyleSheet("QCheckBox::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    image: url(/home/meheret/PycharmProjects/btmhdw/ui/icons/checkbox_checked.svg);\n"
"}\n"
"QCheckBox::indicator:unchecked {\n"
"    image: url(/home/meheret/PycharmProjects/btmhdw/ui/icons/checkbox_unchecked.svg);\n"
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
        self.labelCopyright.setGeometry(QtCore.QRect(280, 600, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.labelCopyright.setFont(font)
        self.labelCopyright.setStyleSheet("color: rgb(121, 121, 121);")
        self.labelCopyright.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCopyright.setObjectName("labelCopyright")
        self.widgetHDWallet = QtWidgets.QWidget(btmhdw)
        self.widgetHDWallet.setEnabled(True)
        self.widgetHDWallet.setGeometry(QtCore.QRect(10, 330, 711, 271))
        self.widgetHDWallet.setObjectName("widgetHDWallet")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.widgetHDWallet)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 711, 281))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutHDWallet = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayoutHDWallet.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayoutHDWallet.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutHDWallet.setSpacing(0)
        self.verticalLayoutHDWallet.setObjectName("verticalLayoutHDWallet")
        self.widgetMnemonic = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.widgetMnemonic.setObjectName("widgetMnemonic")
        self.textEditMnemonicLabel = QtWidgets.QTextEdit(self.widgetMnemonic)
        self.textEditMnemonicLabel.setGeometry(QtCore.QRect(0, 0, 91, 61))
        self.textEditMnemonicLabel.setAutoFillBackground(False)
        self.textEditMnemonicLabel.setStyleSheet("background: transparent;\n"
"border: none;")
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
        self.textEditMnemonic.setReadOnly(True)
        self.textEditMnemonic.setObjectName("textEditMnemonic")
        self.verticalLayoutHDWallet.addWidget(self.widgetMnemonic)
        self.widgetAddress = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.widgetAddress.setEnabled(True)
        self.widgetAddress.setObjectName("widgetAddress")
        self.textEditAddressLabel = QtWidgets.QTextEdit(self.widgetAddress)
        self.textEditAddressLabel.setGeometry(QtCore.QRect(0, 0, 71, 41))
        self.textEditAddressLabel.setAutoFillBackground(False)
        self.textEditAddressLabel.setStyleSheet("background: transparent;\n"
"border: none;\n"
"margin: 6 0;")
        self.textEditAddressLabel.setReadOnly(True)
        self.textEditAddressLabel.setObjectName("textEditAddressLabel")
        self.textEditAddress = QtWidgets.QTextEdit(self.widgetAddress)
        self.textEditAddress.setGeometry(QtCore.QRect(70, 0, 641, 41))
        self.textEditAddress.setStyleSheet("background: transparent;\n"
"border: none;\n"
"margin: 6 0;")
        self.textEditAddress.setReadOnly(True)
        self.textEditAddress.setObjectName("textEditAddress")
        self.verticalLayoutHDWallet.addWidget(self.widgetAddress)
        self.widgetSeed = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.widgetSeed.setObjectName("widgetSeed")
        self.textEditSeedLabel = QtWidgets.QTextEdit(self.widgetSeed)
        self.textEditSeedLabel.setGeometry(QtCore.QRect(0, 0, 51, 51))
        self.textEditSeedLabel.setAutoFillBackground(False)
        self.textEditSeedLabel.setStyleSheet("background: transparent;\n"
"border: none;")
        self.textEditSeedLabel.setReadOnly(True)
        self.textEditSeedLabel.setObjectName("textEditSeedLabel")
        self.textEditSeed = QtWidgets.QTextEdit(self.widgetSeed)
        self.textEditSeed.setGeometry(QtCore.QRect(50, 0, 661, 51))
        self.textEditSeed.setStyleSheet("background: transparent;\n"
"border: none;")
        self.textEditSeed.setReadOnly(True)
        self.textEditSeed.setObjectName("textEditSeed")
        self.verticalLayoutHDWallet.addWidget(self.widgetSeed)
        self.widgetXPublicKey = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.widgetXPublicKey.setObjectName("widgetXPublicKey")
        self.textEditXPublicKeyLabel = QtWidgets.QTextEdit(self.widgetXPublicKey)
        self.textEditXPublicKeyLabel.setGeometry(QtCore.QRect(0, 0, 111, 51))
        self.textEditXPublicKeyLabel.setAutoFillBackground(False)
        self.textEditXPublicKeyLabel.setStyleSheet("background: transparent;\n"
"border: none;")
        self.textEditXPublicKeyLabel.setReadOnly(True)
        self.textEditXPublicKeyLabel.setObjectName("textEditXPublicKeyLabel")
        self.textEditXPublicKey = QtWidgets.QTextEdit(self.widgetXPublicKey)
        self.textEditXPublicKey.setGeometry(QtCore.QRect(90, 0, 621, 51))
        self.textEditXPublicKey.setStyleSheet("background: transparent;\n"
"border: none;")
        self.textEditXPublicKey.setReadOnly(True)
        self.textEditXPublicKey.setObjectName("textEditXPublicKey")
        self.verticalLayoutHDWallet.addWidget(self.widgetXPublicKey)
        self.widgetXPrivateKey = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.widgetXPrivateKey.setObjectName("widgetXPrivateKey")
        self.textEditXPrivateKeyLabel = QtWidgets.QTextEdit(self.widgetXPrivateKey)
        self.textEditXPrivateKeyLabel.setGeometry(QtCore.QRect(0, 0, 111, 51))
        self.textEditXPrivateKeyLabel.setAutoFillBackground(False)
        self.textEditXPrivateKeyLabel.setStyleSheet("background: transparent;\n"
"border: none;")
        self.textEditXPrivateKeyLabel.setReadOnly(True)
        self.textEditXPrivateKeyLabel.setObjectName("textEditXPrivateKeyLabel")
        self.textEditXPrivateKey = QtWidgets.QTextEdit(self.widgetXPrivateKey)
        self.textEditXPrivateKey.setGeometry(QtCore.QRect(100, 0, 611, 51))
        self.textEditXPrivateKey.setStyleSheet("background: transparent;\n"
"border: none;")
        self.textEditXPrivateKey.setReadOnly(True)
        self.textEditXPrivateKey.setObjectName("textEditXPrivateKey")
        self.verticalLayoutHDWallet.addWidget(self.widgetXPrivateKey)
        self.widgetContractProgram = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.widgetContractProgram.setObjectName("widgetContractProgram")
        self.textEditContractProgramLabel = QtWidgets.QTextEdit(self.widgetContractProgram)
        self.textEditContractProgramLabel.setGeometry(QtCore.QRect(0, 0, 151, 41))
        self.textEditContractProgramLabel.setAutoFillBackground(False)
        self.textEditContractProgramLabel.setStyleSheet("background: transparent;\n"
"border: none;\n"
"margin: 6 0;")
        self.textEditContractProgramLabel.setReadOnly(True)
        self.textEditContractProgramLabel.setObjectName("textEditContractProgramLabel")
        self.textEditContractProgram = QtWidgets.QTextEdit(self.widgetContractProgram)
        self.textEditContractProgram.setEnabled(True)
        self.textEditContractProgram.setGeometry(QtCore.QRect(140, 0, 571, 41))
        self.textEditContractProgram.setStyleSheet("background: transparent;\n"
"border: none;\n"
"margin: 6 0;")
        self.textEditContractProgram.setReadOnly(True)
        self.textEditContractProgram.setObjectName("textEditContractProgram")
        self.verticalLayoutHDWallet.addWidget(self.widgetContractProgram)
        self.widgetPath = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.widgetPath.setObjectName("widgetPath")
        self.textEditPathLabel = QtWidgets.QTextEdit(self.widgetPath)
        self.textEditPathLabel.setGeometry(QtCore.QRect(0, 0, 71, 41))
        self.textEditPathLabel.setAutoFillBackground(False)
        self.textEditPathLabel.setStyleSheet("background: transparent;\n"
"border: none;")
        self.textEditPathLabel.setReadOnly(True)
        self.textEditPathLabel.setObjectName("textEditPathLabel")
        self.textEditPath = QtWidgets.QTextEdit(self.widgetPath)
        self.textEditPath.setGeometry(QtCore.QRect(50, 0, 661, 41))
        self.textEditPath.setStyleSheet("background: transparent;\n"
"border: none;")
        self.textEditPath.setReadOnly(True)
        self.textEditPath.setObjectName("textEditPath")
        self.verticalLayoutHDWallet.addWidget(self.widgetPath)
        self.widgetConsole = QtWidgets.QWidget(btmhdw)
        self.widgetConsole.setGeometry(QtCore.QRect(10, 330, 711, 261))
        self.widgetConsole.setObjectName("widgetConsole")
        self.textEditConsole = QtWidgets.QTextEdit(self.widgetConsole)
        self.textEditConsole.setGeometry(QtCore.QRect(0, 20, 711, 241))
        self.textEditConsole.setStyleSheet("background: transparent;\n"
"border: none;")
        self.textEditConsole.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditConsole.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditConsole.setObjectName("textEditConsole")
        self.textEditConsoleLabel = QtWidgets.QTextEdit(self.widgetConsole)
        self.textEditConsoleLabel.setGeometry(QtCore.QRect(0, 0, 711, 31))
        self.textEditConsoleLabel.setStyleSheet("background: transparent;\n"
"border: none;")
        self.textEditConsoleLabel.setObjectName("textEditConsoleLabel")

        self.retranslateUi(btmhdw)
        QtCore.QMetaObject.connectSlotsByName(btmhdw)

    def retranslateUi(self, btmhdw):
        _translate = QtCore.QCoreApplication.translate
        btmhdw.setWindowTitle(_translate("btmhdw", "BTMHDW"))
        self.lineEditBtmhdw.setPlaceholderText(_translate("btmhdw", "Mnemonic/Enteropy/XPrivate Key/XPublic Key/Contract Program"))
        self.pushButtonGenerateHDWallet.setText(_translate("btmhdw", "Get HDWallet from Mnemonic"))
        self.pushButtonGetAddressFromXPublicKey_2.setText(_translate("btmhdw", "Get Address form Contract Program"))
        self.pushButtonGenerateMnemonic.setText(_translate("btmhdw", "Generate Mnemonic"))
        self.pushButtonGenerateEnteropy.setText(_translate("btmhdw", "Generate Enteropy"))
        self.radioButtonEnglish.setText(_translate("btmhdw", "English"))
        self.radioButtonJapanese.setText(_translate("btmhdw", "Japanese"))
        self.pushButtonGetInformationFromXPrivateKey_2.setText(_translate("btmhdw", "Get HDWallet form Enteropy"))
        self.pushButtonGetAddressFromXPublicKey.setText(_translate("btmhdw", "Get Address form XPublic Key"))
        self.checkBoxPath.setText(_translate("btmhdw", "Path"))
        self.lineEditPath.setPlaceholderText(_translate("btmhdw", "m/44/153/1/0/1"))
        self.pushButtonGetInformationFromXPrivateKey.setText(_translate("btmhdw", "Get HDWallet form XPrivate Key"))
        self.radioButtonSolonet.setText(_translate("btmhdw", "Solonet"))
        self.radioButtonMainnet.setText(_translate("btmhdw", "Mainnet"))
        self.radioButtonTestnet.setText(_translate("btmhdw", "Testnet"))
        self.pushButtonExit.setText(_translate("btmhdw", "Exit"))
        self.pushButtonSave.setText(_translate("btmhdw", "Save"))
        self.labelPathAddress.setText(_translate("btmhdw", "Address"))
        self.labelPathChange.setText(_translate("btmhdw", "Change"))
        self.labelPathAccount.setText(_translate("btmhdw", "Account"))
        self.checkBoxConsole.setText(_translate("btmhdw", "View Console"))
        self.checkBoxNightMode.setText(_translate("btmhdw", "Night Mode"))
        self.textEditHome.setHtml(_translate("btmhdw", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:26pt; font-weight:600; color:#878787;\">btmhdw</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#747474;\">Version 0.1.1</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#747474;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-style:italic; color:#747474;\">The implementation of Hierarchical Deterministic (HD) wallets generator for Bytom blockchain.</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-style:italic; color:#747474;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic; color:#747474;\">With btmhdw you can generate mnemonic(English or Japanese language 12 words)/enteropy for new HDWallet, you can get HDWallet from XPrivate key, you can drive your own path(Index) and you can get HDWallet address from contract program/XPublic key.</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-style:italic; color:#747474;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic; color:#747474;\">Github </span><span style=\" color:#747474;\">https://github.com/meherett/btmhdw</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; text-decoration: underline; color:#747474;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic; color:#747474;\">Auther </span><span style=\" color:#747474;\">Meheret Tesfaye</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic; color:#747474;\">Email meherett@zoho.com</span></p></body></html>"))
        self.labelCopyright.setText(_translate("btmhdw", "Copyright © 2019 BTMHDW"))
        self.verticalLayoutWidget.setStyleSheet(_translate("btmhdw", "background: transparent;\n"
"border: none;\n"
"display: flex;\n"
"align-item: center;\n"
"margin: 0;"))
        self.textEditMnemonicLabel.setHtml(_translate("btmhdw", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Mnemonic</span></p></body></html>"))
        self.textEditMnemonic.setHtml(_translate("btmhdw", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">とおるãげこうãへいおんãにげるãはけんãいどうãふあんãよそくãひんこんãついかãはったつãしゃいん</span></p></body></html>"))
        self.textEditAddressLabel.setHtml(_translate("btmhdw", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Address</span></p></body></html>"))
        self.textEditAddress.setHtml(_translate("btmhdw", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">bm1qq5nzpwr2d40qwvga2qval73cvnxv3f4au5vrht</p></body></html>"))
        self.textEditSeedLabel.setHtml(_translate("btmhdw", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Seed</span></p></body></html>"))
        self.textEditSeed.setHtml(_translate("btmhdw", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">d47ece6097f93b5d19259886d210dab017f5b37520b4dad8160712fd5b1065e7189b8b295cc023e0b2c78f79725f859ac512afdfebc0b94cfd83faa59e42d82e</p></body></html>"))
        self.textEditXPublicKeyLabel.setHtml(_translate("btmhdw", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">XPublic Key</span></p></body></html>"))
        self.textEditXPublicKey.setHtml(_translate("btmhdw", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">d47ece6097f93b5d19259886d210dab017f5b37520b4dad8160712fd5b1065e7189b8b295cc023e0b2c78f79725f859ac512afdfebc0b94cfd83faa59e42d82e</p></body></html>"))
        self.textEditXPrivateKeyLabel.setHtml(_translate("btmhdw", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">XPrivate Key</span></p></body></html>"))
        self.textEditXPrivateKey.setHtml(_translate("btmhdw", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">d47ece6097f93b5d19259886d210dab017f5b37520b4dad8160712fd5b1065e7189b8b295cc023e0b2c78f79725f859ac512afdfebc0b94cfd83faa59e42d82e</p></body></html>"))
        self.textEditContractProgramLabel.setHtml(_translate("btmhdw", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Contract Program</span></p></body></html>"))
        self.textEditContractProgram.setHtml(_translate("btmhdw", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">001478c3aa31753389fcde04d33d0779bdc2840f0ad4</p></body></html>"))
        self.textEditPathLabel.setHtml(_translate("btmhdw", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Path</span></p></body></html>"))
        self.textEditPath.setHtml(_translate("btmhdw", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">m/44/153/1/0/1</p></body></html>"))
        self.textEditConsole.setHtml(_translate("btmhdw", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ff0000;\">[ERROR]</span>: <span style=\" color:#999999;\">Get HDWallet from Mnemonic</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">                   Please insert mnemonic, It\'s Empty!</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">                   Exit done!</p></body></html>"))
        self.textEditConsoleLabel.setHtml(_translate("btmhdw", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#909090;\">BTMHDW Console</span></p></body></html>"))

        # Button
        self.pushButtonGenerateMnemonic.clicked.connect(self.generateMnemonic)
        self.pushButtonGenerateEnteropy.clicked.connect(self.generateEntropy)
        # CheckBox Button
        self.checkBoxNightMode.clicked.connect(lambda: self.nightMode(btmhdw))
        # Radio Button
        self.radioButtonEnglish.setChecked(True)
        self.radioButtonEnglish.toggled.connect(lambda: self.checkLanguage(self.radioButtonEnglish))
        self.radioButtonJapanese.toggled.connect(lambda: self.checkLanguage(self.radioButtonJapanese))

        # self.widgetHome.setHidden(True)
        self.widgetConsole.setHidden(True)
        self.widgetHDWallet.setHidden(True)

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

    def nightMode(self, btmhdw):
        if self.checkBoxNightMode.isChecked():
            btmhdw.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        else:
            btmhdw.setStyleSheet(str())

    def generateMnemonic(self):
        self.lineEditBtmhdw.setText(str(BTMHDW().generateMnemonic(language=self.language)))

    def generateEntropy(self):
        self.lineEditBtmhdw.setText(str(BTMHDW().generateEntropy().hex()))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_btmhdw()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

