import sys
import wordChangeFunc as wCF
from PyQt5.QtWidgets import *


class ChangeFileName(QMainWindow):
    oldOption = True
    newOption = False

    def __init__(self):
        super().__init__()
        self.oldStr = QLineEdit(self)
        self.newStr = QLineEdit(self)
        self.oldButtons = [QRadioButton('old 폴더에 보관하기'), QRadioButton('삭제하기\n(휴지통에 보관되지 않습니다.)')]
        self.blankCheckbox = QCheckBox('다음 패턴을 포함\nex) ver_1, ver1')
        self.newButtons = [QRadioButton('new 폴더에 보관하기'), QRadioButton('현재 폴더에 보관하기')]
        self.dirBtn = QPushButton("폴더 선택", self)
        self.execBtn = QPushButton("실행", self)
        self.initUI()

    def initUI(self):
        widget = QWidget(self)
        totalBox = QVBoxLayout()
        groupboxesLayout = QHBoxLayout()
        oldGroupLayout = QVBoxLayout()
        newGroupLayout = QVBoxLayout()

        oldGroupbox = QGroupBox('원본 파일')
        newGroupbox = QGroupBox('수정 파일')

        self.oldStr.textChanged.connect(self.checkFilled)
        self.newStr.textChanged.connect(self.checkFilled)

        self.oldButtons[0].setChecked(True)
        self.blankCheckbox.setChecked(False)
        self.newButtons[1].setChecked(True)

        self.dirBtn.clicked.connect(self.selectDirPath)
        self.execBtn.clicked.connect(self.executeChange)
        self.execBtn.setEnabled(False)

        # 원본 파일 레이아웃
        oldGroupLayout.addWidget(self.oldStr)
        for i in range(len(self.oldButtons)):
            oldGroupLayout.addWidget(self.oldButtons[i])
            self.oldButtons[i].clicked.connect(self.oldRadioButtonClicked)
        oldGroupLayout.addWidget(self.blankCheckbox)
        oldGroupbox.setLayout(oldGroupLayout)

        # 수정 파일 레이아웃
        newGroupLayout.addWidget(self.newStr)
        for i in range(len(self.newButtons)):
            newGroupLayout.addWidget(self.newButtons[i])
            self.newButtons[i].clicked.connect(self.newRadioButtonClicked)
        newGroupbox.setLayout(newGroupLayout)

        # 그룹박스 레이아웃
        groupboxesLayout.addWidget(oldGroupbox)
        groupboxesLayout.addWidget(newGroupbox)

        # 전체 레이아웃
        totalBox.addLayout(groupboxesLayout)
        totalBox.addWidget(self.dirBtn)
        totalBox.addWidget(self.execBtn)

        widget.setLayout(totalBox)
        self.setCentralWidget(widget)

        self.setWindowTitle('Change File Name')
        self.setGeometry(300, 300, 600, 300)
        self.show()

    def oldRadioButtonClicked(self):
        if self.oldButtons[0].isChecked():
            self.oldOption = True
        elif self.oldButtons[1].isChecked():
            self.oldOption = False

    def newRadioButtonClicked(self):
        if self.newButtons[0].isChecked():
            self.newOption = True
        else:
            self.newOption = False

    def selectDirPath(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder:
            self.dirBtn.setText(folder)
        else:
            self.dirBtn.setText("폴더 선택")
        self.checkFilled()

    def checkFilled(self):
        if (not self.oldStr.text()) or (not self.newStr.text()) or (self.dirBtn.text() == "폴더 선택"):
            self.execBtn.setEnabled(False)
        else:
            self.execBtn.setEnabled(True)

    def executeChange(self):
        wCF.execute(self, self.dirBtn.text().replace("/", "\\"), self.oldStr.text(), self.newStr.text(),
                    self.oldOption, self.newOption, self.blankCheckbox.isChecked())

    def alertMessageDiaglog(self, title, content):
        reply = QMessageBox.question(self, title, content, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            return True
        else:
            return False

    def alertInformationDiaglog(self, title, content):
        QMessageBox.information(self, title, content, QMessageBox.Yes, QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChangeFileName()
    sys.exit(app.exec_())
