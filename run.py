from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtWidgets import (QMessageBox, qApp, QStyle, QAction, QSystemTrayIcon, QMenu, QCompleter, QWidget, QLineEdit, QLabel, QPushButton, QScrollArea, QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy )
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPainter, QFont, QColor, QPen
from CustomWidget import AccountWidget, FavoritesWidget, Tag
import lists
import favorites
import threading, time
import passs


uifile_1 = 'mainwindow.ui'
form_1, base_1 = uic.loadUiType(uifile_1)


SaveUifile = 'SaveUi.ui'
form_2, base_2 = uic.loadUiType(SaveUifile)

helpUi = 'HelpUi.ui'
form_3, base_3 = uic.loadUiType(helpUi)

unlockUi = 'VerifyPIN.ui'
form4, base4 = uic.loadUiType(unlockUi)

changeUi = 'ChangePIN.ui'
form5, base5 = uic.loadUiType(changeUi)

widget_list = [['insta','https://instagram.com','happyhands1029','lsh3576423','hello','momo']]
favorites_list = [['insta','https://instagram.com','happyhands1029','lsh3576423','hello','momo']]
spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
lock = True
password = "000000"
site_names = []
tag_list = []

class MainWindow(base_1, form_1):
    def __init__(self):
        print("__init__")
        lists.create()
        favorites.create()

        widget_list = []
        favorites_list = []
        self.lock = passs.update("false", "true")
        check1 = lists.viewall()
        check2 = favorites.viewall()
        password = (passs.viewall())[0][1]
        for i in check1:
            a = []
            for j in i:
                if(isinstance(j, str)):
                    a.append(j)
            widget_list.append(a)

        for i in check2:
            a = []
            for j in i:
                if(isinstance(j, str)):
                    a.append(j)
            favorites_list.append(a)

        for i in widget_list:
            if(i[4] not in tag_list):
                tag_list.append(i[4])
            
                
        super(base_1,self).__init__()
        self.setupUi(self)
        self.account = QWidget()
        self.accountLayout = QVBoxLayout()
        for i in reversed(range(self.accountLayout.count())):
            self.accountLayout.itemAt(i).widget().setParent(None)
        self.widgets = []
        for info in widget_list:
            item = AccountWidget(info[0], info[1], info[2], info[3], info[4], info[5])
            self.accountLayout.addWidget(item)
            self.widgets.append(item)
        self.account.setLayout(self.accountLayout)
        
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.account)
        
        self.scroll2 = QScrollArea()
        self.scroll2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll2.setWidgetResizable(True)

        self.scroll3 = QScrollArea()
        self.scroll3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll3.setWidgetResizable(True)
        
        self.searchbar = self.SearchLine
        self.searchbar.textChanged.connect(self.update)

        container = self.SearchReturn
        containerLayout = QVBoxLayout()
        containerLayout.addWidget(self.scroll)

        container.setLayout(containerLayout)
        site_names = []
        for i in widget_list:
            site_names.append(i[0])


        self.completer = QCompleter(site_names)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchbar.setCompleter(self.completer)

        self.AddButton.clicked.connect(self.AddButtonClicked)
        self.favorites = QWidget()
        self.favoritesLayout = QVBoxLayout()
        for i in reversed(range(self.favoritesLayout.count())):
            self.favoritesLayout.itemAt(i).widget().setParent(None)
        self.favorites_widget = []
        for info in favorites_list:
            item = FavoritesWidget(info[0], info[1], info[2], info[3], info[4], info[5])
            self.favoritesLayout.addWidget(item)
            self.favorites_widget.append(item)

        self.favorites.setLayout(self.favoritesLayout)
        self.scroll2.setWidget(self.favorites)
        container2 = self.Favorites
        container2Layout = QVBoxLayout()
        container2Layout.addWidget(self.scroll2)

        container2.setLayout(container2Layout)

        self.HelpButton.clicked.connect(self.HelpButtonClicked)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.tray_icon.activated.connect(self.showing)
 
        '''
            Define and add steps to work with the system tray icon
            show - show window
            hide - hide window
            exit - exit from application
        '''
        show_action = QAction("창 보이기", self)
        quit_action = QAction("프로그램 종료", self)
        hide_action = QAction("창 숨기기", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self.quiting)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.resetButton.clicked.connect(self.reset)

        self.tags = QWidget()
        self.tagsLayout = QVBoxLayout()
        for i in reversed(range(self.tagsLayout.count())):
            self.tagsLayout.itemAt(i).widget().setParent(None)
        self.tags_widget = []
        for info in tag_list:
            item = Tag(info)
            self.tagsLayout.addWidget(item)
            self.tags_widget.append(item)
        self.tags.setLayout(self.tagsLayout)
        self.scroll3.setWidget(self.tags)
        container3 = self.TagWidget
        container3Layout = QVBoxLayout()
        container3Layout.addWidget(self.scroll3)

        container3.setLayout(container3Layout)

        self.lockButton.clicked.connect(self.LockButtonClicked)
        self.changePassword.clicked.connect(self.ChangeButtonClicked)
        self.setFixedSize(1000, 650)

    def ChangeButtonClicked(self):
        self.change = ChangeUi()

        check = self.change.showModal()
        

    def LockButtonClicked(self):
        self.lock = (passs.viewall())[1][1]
        print(self.lock)
        if self.lock == "true":
            self.test = VerifyUi()

            check = self.test.showModal()

            if check:
                self.lockButton.setText("잠금 설정")
                self.StatusLabel.setText("잠금 해제 상태입니다.")
                passs.update("true", "false")
                
        else:
            reply = QMessageBox.question(self, '확인', '잠금을 적용합니다.', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if (reply == QMessageBox.Yes):
                self.lockButton.setText("잠금 해제")
                self.StatusLabel.setText("잠금 상태입니다.")
                QMessageBox.about(self, "확인", "잠금이 적용되었습니다.")
                passs.update("false", "true")

    def ChangePassword(self):
        ori = "000000"
        new = "000000"
        passs.update(ori, new)
        print(passs.viewall())
        
    def clearLayout(self,layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
    def reset(self):
        self.clearLayout(self.accountLayout)
        self.clearLayout(self.favoritesLayout)
        self.clearLayout(self.tagsLayout)

        print("reset")
        lists.create()
        favorites.create()

        widget_list = []
        favorites_list = []
        tag_list = []
        
        check1 = lists.viewall()
        check2 = favorites.viewall()

        for i in check1:
            a = []
            for j in i:
                if(isinstance(j, str)):
                    a.append(j)
            widget_list.append(a)

        for i in check2:
            a = []
            for j in i:
                if(isinstance(j, str)):
                    a.append(j)
            favorites_list.append(a)

        for i in widget_list:
            if(i[4] not in tag_list):
                tag_list.append(i[4])
            
            
        self.widgets = []
        for info in widget_list:
            item = AccountWidget(info[0], info[1], info[2], info[3], info[4], info[5])
            self.accountLayout.addWidget(item)
            self.widgets.append(item)
        
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        
        self.scroll2 = QScrollArea()
        self.scroll2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll2.setWidgetResizable(True)

        self.scroll3 = QScrollArea()
        self.scroll3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll3.setWidgetResizable(True)
        
        self.searchbar = self.SearchLine
        self.searchbar.textChanged.connect(self.update)

        site_names = []
        for i in widget_list:
            site_names.append(i[0])
        self.completer = QCompleter(site_names)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchbar.setCompleter(self.completer)

        
        self.favorites_widget = []
        for info in favorites_list:
            item = FavoritesWidget(info[0], info[1], info[2], info[3], info[4], info[5])
            self.favoritesLayout.addWidget(item)
            self.favorites_widget.append(item)

        for info in tag_list:
            item = Tag(info)
            self.tagsLayout.addWidget(item)
            self.tags_widget.append(item)


    def quiting(self):
        self.tray_icon.hide()
        self.close()
        qApp.quit()
            
    def printing(self):
        self.HelpButtonClicked(self)
        
    def HelpButtonClicked(self):
        self.help = HelpUi()
        self.help.setWindowModality(Qt.ApplicationModal)
        self.help.show()

    def showing(self, reason):
        if(reason == QSystemTrayIcon.DoubleClick):
            self.show()

    def update(self,text):
        #self.__init__()
        for widget in self.widgets:
            if text.lower() in widget.name.lower() or text.lower() in widget.link.lower():
                widget.show()
            else:
                widget.hide()

    def AddButtonClicked(self):
        self.AddDialog = SaveUi()
        check = self.AddDialog.showModal()

        if check:
            item = AccountWidget(self.AddDialog.SaveName.text(), self.AddDialog.SiteLink.text(), self.AddDialog.ID.text(), self.AddDialog.Password.text(),self.AddDialog.Tag.text(),self.AddDialog.Memo.text())
            self.accountLayout.addWidget(item, -2)
            self.widgets.append(item)
            widget_list.append([self.AddDialog.SaveName.text(), self.AddDialog.SiteLink.text(), self.AddDialog.ID.text(), self.AddDialog.Password.text(),self.AddDialog.Tag.text(),self.AddDialog.Memo.text()])
            site_names.append(widget_list[-1][0])
            self.completer = QCompleter(site_names)
            self.searchbar.setCompleter(self.completer)
            self.account.setLayout(self.accountLayout)
            lists.add(self.AddDialog.SaveName.text(), self.AddDialog.SiteLink.text(), self.AddDialog.ID.text(), self.AddDialog.Password.text(),self.AddDialog.Tag.text(),self.AddDialog.Memo.text())
            check2 = self.AddDialog.FavoriteCheck.isChecked()

            if check2:
                print("check2")
                item = FavoritesWidget(self.AddDialog.SaveName.text(), self.AddDialog.SiteLink.text(), self.AddDialog.ID.text(), self.AddDialog.Password.text(),self.AddDialog.Tag.text(),self.AddDialog.Memo.text())
                self.favoritesLayout.addWidget(item, -2)
                favorites_list.append([self.AddDialog.SaveName.text(), self.AddDialog.SiteLink.text(), self.AddDialog.ID.text(), self.AddDialog.Password.text(),self.AddDialog.Tag.text(),self.AddDialog.Memo.text()])
                self.favorites.setLayout(self.favoritesLayout)
                favorites.add(self.AddDialog.SaveName.text(), self.AddDialog.SiteLink.text(), self.AddDialog.ID.text(), self.AddDialog.Password.text(),self.AddDialog.Tag.text(),self.AddDialog.Memo.text())

class ChangeUi(base5, form5):
    def __init__(self):
        super(base5, self).__init__()
        self.setupUi(self)
        self.ConfirmButton.clicked.connect(self.Confirm)
        self.setFixedSize(450, 350)

    def Confirm(self):
        password = (passs.viewall())[0][1]
        if self.CurrentPINedit.text() == password:
            if len(self.NewPINedit.text()) == 6:
                if ((self.NewPINedit.text()) == (self.confirmNewPINEdit.text())):
                    self.accept()
                    passs.update(password, self.NewPINedit.text())
                    QMessageBox.about(self, "확인", "비밀번호가 변경되었습니다.")
                else:
                    QMessageBox.warning(self, "확인", "비밀번호와 비밀번호 확인이 일치하지 않습니다.")
            else:
                QMessageBox.warning(self, "확인", "새로운 비밀번호로 6자리를 입력해주세요.")
        else:
            QMessageBox.warning(self, "확인", "기존 비밀번호가 일치하지 않습니다.")

    def showModal(self):
        return super().exec_()
                    
class VerifyUi(base4, form4):
    def __init__(self):
        super(base4, self).__init__()
        self.setupUi(self)
        print("hi")
        self.verifyButton.clicked.connect(self.verify)
        self.setFixedSize(450, 350)

    def verify(self):
        password = (passs.viewall())[0][1]
        if self.VerifyPINedit.text() == password:
            self.accept()
            QMessageBox.about(self, "확인", "잠금이 해제되었습니다.")

        else:
            QMessageBox.about(self, "확인", "PIN이 잘못되었습니다. 다시 입력해주세요.")

    def showModal(self):
        return super().exec_()

class SaveUi(base_2, form_2):
    def __init__(self):
        super(base_2, self).__init__()
        self.setupUi(self)
        self.SaveButton.clicked.connect(self.SaveButtonClicked)
        self.setFixedSize(800, 500)

    def SaveButtonClicked(self):
        if(self.SaveName.text() != '' and self.SiteLink.text() != '' and self.ID.text() != '' and self.Password.text() != ''):
            self.accept()
            
    def showModal(self):
        return super().exec_()

class HelpUi(base_3, form_3):
    def __init__(self):
        super(base_3,self).__init__()
        self.setupUi(self)
        self.setFixedSize(1000, 550)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setQuitOnLastWindowClosed(False)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
