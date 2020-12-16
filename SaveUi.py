from PyQt5 import QtWidgets, uic
import sys
import lists
from PyQt5.QtWidgets import *

namelist = []
uifile = 'SaveUi.ui'
form_2, base_2 = uic.loadUiType(uifile)
k = []

class SaveUi(base_2, form_2):
    def __init__(self):
        super(base_2, self).__init__()
        self.setupUi(self)
        self.SaveButton.clicked.connect(self.SaveButtonClicked)
        print("asdf")
        lists.create()
        namelist = []
        k = []
        check1 = lists.viewall()

        for i in check1:
            a = []
            for j in i:
                if(isinstance(j, str)):
                    a.append(j)
            k.append(a)
            
        for i in k:
            namelist.append(i[0])
    def Message(self, text):
        box = QtWidgets.QMessageBox()
        box.setText(text)
        box.setWindowTitle("주의")
        box.setEscapeButton(QtWidgets.QMessageBox.Close)
        box.exec_()

    def SaveButtonClicked(self):
        print("hi")
        print(self.SaveName.text(), self.SiteLink.text(), self.ID.text(), self.Password.text())
        if(self.SaveName.text() not in namelist):
            if(self.SaveName.text() != '' and self.SiteLink.text() != '' and self.ID.text() != '' and self.Password.text() != ''):
                print("1")
                self.close()
            else:
                print("2")
                self.warnLabel.setText("이름, 주소, ID, 비밀번호에는 최소 한 글자 이상 입력해주세요.")
        else:
            print("3")
            self.Message("이미 있는 이름입니다. 다른 이름을 입력해주세요.")
            

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SaveUi()
    ex.show()
    sys.exit(app.exec_())

    
    
