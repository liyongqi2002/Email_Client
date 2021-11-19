# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\60307\Desktop\test.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import base64
import sys, threading
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime

from png_163 import png_163
from pop3 import POP3
from smtp import SMTP
from PyQt5.QtWidgets import QMainWindow, QPushButton,QTableWidgetItem, QMessageBox
from flanker import mime

pop3 = POP3()
smtp = SMTP()
mutex = threading.Lock()
t = []
usr=''
psw=''
class ui_163_login(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:\\Users\\60307\\Desktop\\计网实验大作业\\version-2.0\\163.ico"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setGeometry(700, 300, 500, 500)
        self.setWindowTitle('网易163邮箱📫客户端')

        self.username_input = QtWidgets.QLineEdit(self)
        self.username_input.setGeometry(QtCore.QRect(80, 170, 331, 41))
        self.username_input.setObjectName("username_input")

        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setGeometry(QtCore.QRect(80, 250, 331, 41))
        self.password_input.setObjectName("password_input")

        self.username_label = QtWidgets.QLabel("用户名", self)
        self.username_label.setGeometry(QtCore.QRect(10, 180, 51, 21))
        self.username_label.setObjectName("username_label")
        self.password_label = QtWidgets.QLabel("授权码", self)
        self.password_label.setGeometry(QtCore.QRect(10, 260, 51, 21))
        self.password_label.setObjectName("password_label")

        self.login_button = QtWidgets.QPushButton("登陆", self)
        self.login_button.setGeometry(QtCore.QRect(100, 320, 111, 41))
        self.login_button.setObjectName("login_button")

        self.exit_button = QtWidgets.QPushButton("取消", self)
        self.exit_button.setGeometry(QtCore.QRect(270, 320, 101, 41))
        self.exit_button.setObjectName("exit_button")
        self.exit_button.clicked.connect(self.close)

        self.login_button.clicked.connect(self.login)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(60, 50, 341, 71))
        self.label.setText("")
        icon = QtGui.QPixmap()
        icon.loadFromData(png_163)
        self.label.setPixmap(icon)
        self.label.setScaledContents(False)
        self.label.setObjectName("label")
        self.show()

    def login(self):
        t = threading.Thread(target=self.loginRun)
        t.start()
        time.sleep(2)
        self.close()

    def loginRun(self):
        mutex.acquire()
        usr=self.username_input.text()
        psw=self.password_input.text()
        pop3.connect('pop.163.com')
        smtp.connect('smtp.163.com')
        for index in range(50):
            t[index].usr=usr
            t[index].psw=psw
        pop3.auth(usr, psw)
        smtp.auth(usr, psw)

        pop3.getAllMail()
        mutex.release()


class Ui_send(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:\\Users\\60307\\Desktop\\计网实验大作业\\version-2.0\\163.ico"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setGeometry(600, 300, 290, 150)
        self.setWindowTitle('发邮件')
        self.resize(700, 600)

        self.topic_input = QtWidgets.QPlainTextEdit(self)
        self.topic_input.setGeometry(QtCore.QRect(100, 100, 541, 51))
        self.topic_input.setObjectName("topic_input")

        self.content_input = QtWidgets.QPlainTextEdit(self)
        self.content_input.setGeometry(QtCore.QRect(100, 170, 541, 271))
        self.content_input.setObjectName("content_input")

        self.topic_label = QtWidgets.QLabel("主题", self)
        self.topic_label.setGeometry(QtCore.QRect(30, 110, 41, 31))
        self.topic_label.setObjectName("topic_label")

        self.content_label = QtWidgets.QLabel("邮件内容", self)
        self.content_label.setGeometry(QtCore.QRect(20, 280, 72, 15))
        self.content_label.setObjectName("content_label")

        self.toaddress_input = QtWidgets.QLineEdit(self)
        self.toaddress_input.setGeometry(QtCore.QRect(100, 30, 541, 40))
        self.toaddress_input.setObjectName("toaddress_input")

        self.toaddress_label = QtWidgets.QLabel("收件人", self)
        self.toaddress_label.setGeometry(QtCore.QRect(20, 50, 72, 15))
        self.toaddress_label.setObjectName("toaddress")

        self.send_button = QtWidgets.QPushButton("发送", self)
        self.send_button.setGeometry(QtCore.QRect(100, 470, 541, 41))
        self.send_button.setObjectName("send_button")

        self.warning_send=Ui_send_warning()
        self.warning_send.pushButton_yes.clicked.connect(self.send)

        self.send_button.clicked.connect(self.warning_send.show)

    def send(self):
        t = threading.Thread(target=self.sendRun, args=())
        t.start()
        self.warning_send.close()

    def sendRun(self):
        mutex.acquire()
        smtp.send_to(self.toaddress_input.text())
        topic = self.topic_input.toPlainText()
        content = self.content_input.toPlainText()
        _=smtp.send_content(topic, "text/plain", content)
        self.mailserver,self.usr,self.psw=smtp.newsmtp()
        print(self.mailserver,self.usr,self.psw)
        try:
            smtp.quit()
        except ConnectionAbortedError:
            smtp.connect(self.mailserver)
            smtp.auth(self.usr,self.psw)
        smtp.connect(self.mailserver)
        smtp.auth(self.usr, self.psw)
        print(_)
        if('OK' in _):
            print('成功发送')
            self.close()
            self.infor(0)
            self.topic_input.clear()
            self.content_input.clear()
            self.toaddress_input.clear()
        else:
            print('请检查收件地址是否正确')
            self.close()
            self.infor(1)
            self.topic_input.clear()
            self.content_input.clear()
            self.toaddress_input.clear()
        mutex.release()
    def infor(self,m):
        t = threading.Thread(target=self.inforRun, args=(m,))
        t.start()

    def inforRun(self,m):
        mutex.acquire()
        msgBox=QMessageBox()
        if (m == 0):
            msgBox.setText("成功！邮件已经发送成功！")
            msgBox.addButton(QMessageBox.Ok)
            msgBox.button(QMessageBox.Ok).hide()
            msgBox.exec()

        elif (m == 1):
            msgBox.setText("错误,发送失败！请检查收件地址是否正确！")
            msgBox.addButton(QMessageBox.Ok)
            msgBox.button(QMessageBox.Ok).hide()
            msgBox.exec()

        mutex.release()


class Ui_pop3(QMainWindow):
    def __init__(self):
        super().__init__()
        self.readBtns = []
        for i in range(50):
            readBtn = QPushButton("查看")  # 新建一个按钮
            self.readBtns.append(readBtn)

        self.setupUi()
        self.num=0
    def setupUi(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:\\Users\\60307\\Desktop\\计网实验大作业\\version-2.0\\163.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setObjectName("self")
        self.resize(770, 600)
        self.setWindowTitle('网易163邮箱📫')
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_send = QtWidgets.QPushButton('发件', self.centralwidget)
        self.pushButton_send.setGeometry(QtCore.QRect(370, 10, 91, 51))
        self.pushButton_send.setObjectName("pushButton_send")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 331, 91))
        self.label.setText("")
        icon=QtGui.QPixmap()
        icon.loadFromData(png_163)
        self.label.setPixmap(icon)
        self.label.setObjectName("label")

        self.pushButton_refresh = QtWidgets.QPushButton('刷新', self.centralwidget)
        self.pushButton_refresh.setGeometry(QtCore.QRect(500, 10, 91, 51))
        self.pushButton_refresh.setObjectName("pushButton_refresh")

        self.pushButton_loginout = QtWidgets.QPushButton('登出', self.centralwidget)
        self.pushButton_loginout.setGeometry(QtCore.QRect(630, 10, 91, 51))
        self.pushButton_loginout.setObjectName("pushButton_loginout")

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(370, 70, 351, 47))
        self.textBrowser.setObjectName("textBrowser")
        self.datetimenow=datetime.now()
        self.textBrowser.setText("登录时间："+str(self.datetimenow))


        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget.setColumnCount(4)

        self.headers = ['主题', '发件人', '时间', '操作']
        self.tableWidget.setHorizontalHeaderLabels(self.headers)
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 300)
        self.tableWidget.setColumnWidth(2, 240)
        self.tableWidget.setColumnWidth(3, 50)

        self.tableWidget.setGeometry(QtCore.QRect(20, 140, 711, 411))
        self.tableWidget.setObjectName("tableWidget")

        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.pushButton_refresh.clicked.connect(self.refresh)

    def loginout(self):
        t = threading.Thread(target=self.loginoutRun, args=())
        t.start()
        self.close()
    def loginoutRun(self):
        smtp.quit()
        pop3.quit()

    def show_refresh(self):
        time.sleep(0.5)
        self.refresh()
        self.show()
    def add_button(self,num):

        for index in range(num):
            t[index].index = index
            self.readBtns[index].setDown(True)
            self.readBtns[index].setStyleSheet("QPushButton{margin:3px};")
            self.tableWidget.setCellWidget(index, 3, self.readBtns[index])  # 添加按钮到列表（0，2）
    def refresh(self):
        self.mailserver,self.usr,self.psw=pop3.newpop3()
        pop3.quit()
        pop3.connect(self.mailserver)
        pop3.auth(self.usr,self.psw)
        pop3.getAllMail()
        print(pop3.getStat())
        t = threading.Thread(target=self.refreshRun)
        t.start()
        len_mail_list=pop3.getStat()
        print(len_mail_list,'当前数量')
        time.sleep(1)
        self.datetimenow=datetime.now()
        t,_=str(self.datetimenow).split('.')
        self.textBrowser.setText("上次刷新时间：" + t)
        self.textBrowser.append("欢迎访问网易163邮箱📫！")
        self.add_button(len_mail_list)


    def refreshRun(self):
        mutex.acquire()
        time.sleep(1)
        mail_list = pop3.mailList
        print('login后的初始值',mail_list)
        mail_list_mime = []

        for item in mail_list:
            m = mime.from_string(item)
            mail_list_mime.append(m)
        mail_list_headers = []
        for item in mail_list_mime:
            headers = item.headers.items()
            mail_list_headers.append(headers)
        print(mail_list_headers)
        num_mails = len(mail_list)  # 设置总信件数
        self.old_num=num_mails
        self.tableWidget.setRowCount(num_mails)
        print(num_mails)
        for index in range(len(mail_list_headers)):
            t = mail_list_headers[index]
            for item in t:
                if (item[0] == "Date"):
                    sendtime = item[1]  # 时间
                elif (item[0] == "From"):
                    sendfrom = item[1]  # 发件人
                elif (item[0] == "Subject"):
                    subject = item[1]  # 发件人
                elif (item[0] == "To"):
                    self.usr = item[1]  # 收件人
            self.tableWidget.setItem(index, 0, QTableWidgetItem(subject))  # 主题
            self.tableWidget.setItem(index, 1, QTableWidgetItem(sendfrom))  # 发件人
            self.tableWidget.setItem(index, 2, QTableWidgetItem(sendtime))  # 时间
        mutex.release()


class Ui_content(QMainWindow):
    def __init__(self):
        super().__init__()
        self.usr=''
        self.psw=''
        self.index=0

    def show_this(self):
        self.setupUi()
        self.show()
    def setupUi(self):
        self.setWindowTitle('邮件内容 📧')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:\\Users\\60307\\Desktop\\计网实验大作业\\version-2.0\\163.ico"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        pop3.connect("pop.163.com")
        pop3.auth(self.usr,self.psw)
        print(self.index,'第几封信')
        pop3.getAllMail()
        self.mail=pop3.mailList[self.index]
        self.mail_mime=mime.from_string(self.mail)
        self.headers=self.mail_mime.headers.items()
        for item in self.headers:
            print(item[0])
            if(item[0]=="Date"):
                self.sendtime = item[1]  # 时间
            elif(item[0]=="From"):
                self.sendfrom = item[1]  # 发件人
            elif (item[0] == "Subject"):
                self.subject = item[1]  # 发件人
        print(self.sendfrom,self.sendtime)
        self.setObjectName("MainWindow")
        self.resize(1007, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_delete = QtWidgets.QPushButton('删除邮件',self.centralwidget)
        self.pushButton_delete.setGeometry(QtCore.QRect(760, 20, 93, 41))
        self.pushButton_delete.setObjectName("pushButton_delete")

        self.warning_del=Ui_del()
        self.pushButton_delete.clicked.connect(self.warning_del.show)
        self.warning_del.pushButton_yes.clicked.connect(self.dele)

        self.pushButton_close = QtWidgets.QPushButton('退出阅读',self.centralwidget)
        self.pushButton_close.setGeometry(QtCore.QRect(870, 20, 93, 41))
        self.pushButton_close.setObjectName("pushButton_close")
        self.pushButton_close.clicked.connect(self.close)

        self.textBrowser_content = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_content.setGeometry(QtCore.QRect(30, 80, 941, 471))
        self.textBrowser_content.setObjectName("textBrowser_content")
        if(self.mail_mime.content_type.is_multipart()):
            contents=''
            for part in self.mail_mime.parts:
                contents += part.body
            self.textBrowser_content.setText("<h1>主题：" + self.subject + "</h1>")
            self.textBrowser_content.append("内容："+contents)
        elif(self.mail_mime.content_type.is_singlepart()):
            self.textBrowser_content.setText("<h1>主题："+self.subject+"</h1>")
            self.textBrowser_content.append("内容："+self.mail_mime.body)

        self.textBrowser_from = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_from.setGeometry(QtCore.QRect(100, 20, 251, 50))
        self.textBrowser_from.setObjectName("textBrowser_from")
        self.textBrowser_from.setText(self.sendfrom)

        self.label_from = QtWidgets.QLabel('邮件来自',self.centralwidget)
        self.label_from.setGeometry(QtCore.QRect(20, 40, 72, 15))
        self.label_from.setObjectName("label_from")

        self.label_time = QtWidgets.QLabel('发送时间',self.centralwidget)
        self.label_time.setGeometry(QtCore.QRect(380, 40, 72, 15))
        self.label_time.setObjectName("label_time")

        self.textBrowser_time = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_time.setGeometry(QtCore.QRect(450, 20, 251, 50))
        self.textBrowser_time.setObjectName("textBrowser_time")
        self.textBrowser_time.setText(self.sendtime)

        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
    def dele(self):
        t = threading.Thread(target=self.deleRun)
        t.start()
        self.warning_del.close()
        self.close()
    def deleRun(self):
        mutex.acquire()
        print(self.index,'删除第几个')
        pop3.delete(self.index)
        time.sleep(1)
        mutex.release()

class Ui_del(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
    def setupUi(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:\\Users\\60307\\Desktop\\计网实验大作业\\version-2.0\\163.ico"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setObjectName("self")
        self.resize(328, 157)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel('确定要删除该邮件？',self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 30, 131, 31))
        self.label.setObjectName("label")
        self.pushButton_yes = QtWidgets.QPushButton('确定',self.centralwidget)
        self.pushButton_yes.setGeometry(QtCore.QRect(30, 80, 71, 41))
        self.pushButton_yes.setObjectName("pushButton_yes")

        self.pushButton_no = QtWidgets.QPushButton('取消',self.centralwidget)
        self.pushButton_no.setGeometry(QtCore.QRect(210, 80, 71, 41))
        self.pushButton_no.setObjectName("pushButton_no")
        self.pushButton_no.clicked.connect(self.close)
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

class Ui_send_warning(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
    def setupUi(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:\\Users\\60307\\Desktop\\计网实验大作业\\version-2.0\\163.ico"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setObjectName("self")
        self.resize(328, 157)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel('确定要发送该邮件？',self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 30, 131, 31))
        self.label.setObjectName("label")
        self.pushButton_yes = QtWidgets.QPushButton('确定',self.centralwidget)
        self.pushButton_yes.setGeometry(QtCore.QRect(30, 80, 71, 41))
        self.pushButton_yes.setObjectName("pushButton_yes")

        self.pushButton_no = QtWidgets.QPushButton('取消',self.centralwidget)
        self.pushButton_no.setGeometry(QtCore.QRect(210, 80, 71, 41))
        self.pushButton_no.setObjectName("pushButton_no")
        self.pushButton_no.clicked.connect(self.close)
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

if __name__ == "__main__":
    png_163 = base64.b64decode(png_163)
    app = QtWidgets.QApplication(sys.argv)
    for index in range(50):
        t.append(Ui_content())
    window_163_login = ui_163_login()
    window_163_login.show()
    send_window = Ui_send()
    pop3_window = Ui_pop3()
    window_163_login.login_button.clicked.connect(pop3_window.show_refresh)
    pop3_window.pushButton_send.clicked.connect(send_window.show)
    pop3_window.pushButton_loginout.clicked.connect(pop3_window.loginout)
    for index in range(50):
        pop3_window.readBtns[index].clicked.connect(t[index].show_this)
    sys.exit(app.exec_())