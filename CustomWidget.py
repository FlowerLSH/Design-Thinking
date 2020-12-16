from PyQt5.QtWidgets import (QScrollArea, QVBoxLayout, QMessageBox, QWidget, QSizePolicy,QLabel, QPushButton, QHBoxLayout,QSpacerItem, QApplication)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import webbrowser
from PyQt5 import QtWidgets, uic
import clipboard
import lists, favorites, passs

infouifile = 'InfoUi.ui'
form, base = uic.loadUiType(infouifile)

edituifile = 'infoedit.ui'
form2, base2 = uic.loadUiType(edituifile)
spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)

taguifile = 'taglist.ui'
form3, base3 = uic.loadUiType(taguifile)

spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)

def clickable(widget):
    class Filter(QObject):
        clicked = pyqtSignal()

        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        return True
            return False
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked

class Tag(QWidget):
    def __init__(self,tag):
        super(Tag, self).__init__()
        self.tag = tag

        self.btn = QPushButton(self.tag)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.btn)
        self.setLayout(self.hbox)
        self.btn.clicked.connect(self.TagButtonClicked)
   
    def TagButtonClicked(self):
        self.taglist = TagList(self.tag)
        self.taglist.TagName.setText(self.tag)
        check = self.taglist.showModal()
    
class FavoritesWidget(QWidget):
    def __init__(self,name,link,user_id,user_password,tag = '',memo = ''):
        super(FavoritesWidget, self).__init__()
        self.name = name
        self.link = link
        self.id = user_id
        self.password = user_password
        self.tag = tag
        self.memo = memo
        self.text = name + ' (' + link + ')'

        self.lbl0 = QLabel(self.text)
        self.btn2 = QPushButton("Check")
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.lbl0)
        self.hbox.addWidget(self.btn2)
        self.setLayout(self.hbox)
        
        self.btn2.clicked.connect(self.OpenInfo)
        
        clickable(self.lbl0).connect(self.OpenWeb)

    def OpenInfo(self):
        if((passs.viewall())[1][1] == 'false'):
            self.info = InfoUi()
            self.info.NameLabel.setText(self.name)
            self.info.LinkLabel.setText(self.link)
            self.info.IDLabel.setText(self.id)
            self.info.PasswordLabel.setText(self.password)
            self.info.TagLabel.setText(self.tag)
            self.info.MemoLabel.setText(self.memo)

            check1 = favorites.search(self.name)
            if check1:
                self.info.FavoritesButton.setText("즐겨찾기 해제")
            else:
                self.info.FavoritesButton.setText("즐겨찾기 등록")
                
            check = self.info.showModal()
        else:
            QMessageBox.warning(self, "확인", "먼저 잠금을 해제해주세요.")

    def OpenWeb(self):
        url = self.link
        webbrowser.open_new_tab(url)
        
        
        
class AccountWidget(QWidget):
    def __init__(self,name,link,user_id,user_password,tag = '',memo = ''):
        super(AccountWidget, self).__init__()
        self.name = name
        self.link = link
        self.id = user_id
        self.password = user_password
        self.tag = tag
        self.memo = memo
        
        self.lbl0 = QLabel(self.name)
        self.lbl1 = QLabel(self.link)
        number1, number2 = len(self.id), len(self.password)
        num = int(number1*0.4)
        self.lbl3 = QLabel(self.id[0:num-1] + ('*' * (number1 - num + 1)))
        self.lbl4 = QLabel('*' * number2)
        self.btn = QPushButton("Check")
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.lbl0)
        self.hbox.addWidget(self.lbl1)
        self.hbox.addWidget(self.lbl3)
        self.hbox.addWidget(self.lbl4)
        self.hbox.addWidget(self.btn)
        self.setLayout(self.hbox)

        self.btn.clicked.connect(self.OpenInfo)
        
        clickable(self.lbl1).connect(self.OpenWeb)

    def OpenInfo(self):
        if((passs.viewall())[1][1] == "false"):
            self.info = InfoUi()
            self.info.IDLabel.setText(self.id)
            self.info.LinkLabel.setText(self.link)
            self.info.PasswordLabel.setText(self.password)
            self.info.TagLabel.setText(self.tag)
            self.info.MemoLabel.setText(self.memo)
            self.info.NameLabel.setText(self.name)

            check1 = favorites.search(self.name)
            if len(check1) != 0:
                self.info.FavoritesButton.setText("즐겨찾기 해제")
            else:
                self.info.FavoritesButton.setText("즐겨찾기 등록")
                
            check = self.info.showModal()
        else:
            QMessageBox.warning(self, "확인", "먼저 잠금을 해제해주세요.")

    def OpenWeb(self):
        url = self.link
        webbrowser.open_new_tab(url)
        
    def show(self):
        for i in [self, self.lbl0, self.lbl1, self.lbl3, self.lbl4, self.btn]:
            i.setVisible(True)
        

    def hide(self):
        for i in [self, self.lbl0, self.lbl1, self.lbl3, self.lbl4, self.btn]:
            i.setVisible(False)

accountlist = []
check2 = []
class TagList(base3, form3):
    def __init__(self, tag):
        super(base3, self).__init__()
        self.setupUi(self)
        
        check1 = lists.viewall()
        accountlist = []
        check2 = []
        for i in check1:
            a = []
            for j in i:
                if(isinstance(j, str)):
                    a.append(j)
            check2.append(a)

        for j in check2:
            if(j[4] == tag):
                accountlist.append(j)

        self.account = QWidget()
        self.accountLayout = QVBoxLayout()
        for i in reversed(range(self.accountLayout.count())):
            self.accountLayout.itemAt(i).widget().setParent(None)
        self.widgets = []
        for info in accountlist:
            item = FavoritesWidget(info[0], info[1], info[2], info[3], info[4], info[5])
            self.accountLayout.addWidget(item)
            self.widgets.append(item)
        self.account.setLayout(self.accountLayout)
        
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.account)
        
        container = self.tagList
        containerLayout = QVBoxLayout()
        containerLayout.addWidget(self.scroll)

        container.setLayout(containerLayout)

    def showModal(self):
        return super().exec_()
        

class EditUi(base2, form2):
    def __init__(self):
        print("init")
        super(base2, self).__init__()
        self.setupUi(self)
        self.CancelButton.clicked.connect(self.CancelButtonClicked)
        self.OKButton.clicked.connect(self.OKButtonClicked)
        

    def CancelButtonClicked(self):
        reply = QMessageBox.question(self, '확인', '저장하지 않고 편집을 취소합니다.', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if (reply == QMessageBox.Yes):
            print('yes')
            self.accept()
        else:
            print('no')

    def OKButtonClicked(self):
        reply = QMessageBox.question(self, '확인', '수정한 내용을 적용합니다.', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if (reply == QMessageBox.Yes):
            lists.update(self.hidden.text(), self.Nameedit.text(), self.LinkEdit.text(), self.idedit.text(), self.passwordedit.text(), self.tagedit.text(), self.memoedit.text())
            print(lists.viewall())
            print('yes')
            self.accept()
        else:
            print('no')

    def showModal(self):
        return super().exec_()
        
        
class InfoUi(base, form):
    def __init__(self):
        super(base, self).__init__()
        self.setupUi(self)
        self.OKButton.clicked.connect(self.OKButtonClicked)
        self.IDCopyButton.clicked.connect(self.IDCopy)
        self.PasswordCopyButton.clicked.connect(self.PasswordCopy)
        self.DeleteButton.clicked.connect(self.DeleteButtonClicked)
        self.EditButton.clicked.connect(self.EditButtonClicked)
        self.FavoritesButton.clicked.connect(self.FavoritesButtonClicked)

    def FavoritesButtonClicked(self):
        if(self.FavoritesButton.text() == "즐겨찾기 등록"):
            reply = QMessageBox.question(self, '즐겨찾기','즐겨찾기에 등록합니다.', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if (reply == QMessageBox.Yes):
                self.FavoritesButton.setText("즐겨찾기 해제")
                favorites.add(self.NameLabel.text(), self.LinkLabel.text(),self.IDLabel.text(), self.PasswordLabel.text(), self.TagLabel.text(), self.MemoLabel.text())
            else:
                print('no')
        else:
            reply = QMessageBox.question(self, '즐겨찾기', '즐겨찾기에서 해제합니다.', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if (reply == QMessageBox.Yes):
                self.FavoritesButton.setText("즐겨찾기 등록")
                favorites.delete(self.NameLabel.text())
            else:
                print('no')

    def EditButtonClicked(self):
        self.Edit = EditUi()
        self.Edit.LinkEdit.setText(self.LinkLabel.text())
        self.Edit.Nameedit.setText(self.NameLabel.text())
        self.Edit.idedit.setText(self.IDLabel.text())
        self.Edit.passwordedit.setText(self.PasswordLabel.text())
        self.Edit.tagedit.setText(self.TagLabel.text())
        self.Edit.memoedit.setText(self.MemoLabel.text())
        self.Edit.hidden.setText(self.NameLabel.text())
        check = self.Edit.showModal()

        if check:
            self.IDLabel.setText(self.Edit.idedit.text())
            self.LinkLabel.setText(self.Edit.LinkEdit.text())
            self.PasswordLabel.setText(self.Edit.passwordedit.text())
            self.TagLabel.setText(self.Edit.tagedit.text())
            self.MemoLabel.setText(self.Edit.memoedit.text())
            self.NameLabel.setText(self.Edit.Nameedit.text())

    def IDCopy(self):
        self.IDCopyButton.setText("Copied")
        clipboard.copy(self.IDLabel.text())

    def PasswordCopy(self):
        self.PasswordCopyButton.setText("Copied")
        clipboard.copy(self.PasswordLabel.text())

    def DeleteButtonClicked(self):
        reply = QMessageBox.question(self, '확인', '정말로 삭제하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if (reply == QMessageBox.Yes):
            favorites.delete(self.NameLabel.text())
            lists.delete(self.NameLabel.text())
            print('yes')
            self.accept()
        else:
            print('no')
        
        
    def OKButtonClicked(self):
        self.accept()

    def showModal(self):
        return super().exec_()


    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    #ex = InfoUi()
    #ex = AccountWidget('1','https://instagram.com','x','happyhands1029','lsh3576423','hello','momo')
    ex = FavoritesWidget('1','https://instagram.com','x','happyhands1029','lsh3576423','hello','momo')
    
    ex.show()
    sys.exit(app.exec_())
