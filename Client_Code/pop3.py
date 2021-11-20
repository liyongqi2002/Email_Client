from socket import *

class POP3():
    def connect(self,mailserver):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.mailserver=mailserver
        self.clientSocket.connect((self.mailserver, 110))
        self.connect_recv = self.clientSocket.recv(1024).decode()
        print(self.connect_recv)
    def auth(self,user_login,psw_login):

        self.user_login=str(user_login)
        self.psw_login=str(psw_login)

        self.clientSocket.sendall(('USER ' + self.user_login + '\r\n').encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)

        self.clientSocket.sendall(('PASS ' + self.psw_login + '\r\n').encode())
        self.auth_recv = self.clientSocket.recv(1024).decode()
        print(self.auth_recv)

        self.clientSocket.sendall(('LIST\r\n').encode())
        recv = self.clientSocket.recv(1024).decode()
        list = recv[4:-2].split('\r\n')[1:-1]
        self.MailList = []
        for _t in list:
                _d = {}
                _d['id'] = _t.split(' ')[0]
                _d['size'] = _t.split(' ')[1]
                self.MailList.append(_d)
        # print(list)
        # print(self.MailList)
    def getStat(self):
        self.clientSocket.sendall(('LIST\r\n').encode())
        recv = self.clientSocket.recv(1024).decode()
        list = recv[4:-2].split('\r\n')[1:-1]
        self.MailList = []
        for _t in list:
            _d = {}
            _d['id'] = _t.split(' ')[0]
            _d['size'] = _t.split(' ')[1]
            self.MailList.append(_d)
        self.clientSocket.sendall(('STAT\r\n').encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        self.len_mail_list=len(self.MailList)
        return len(self.MailList)
    def getAllMail(self):
        self.clientSocket.sendall(('LIST\r\n').encode())
        recv = self.clientSocket.recv(1024).decode()
        list = recv[4:-2].split('\r\n')[1:-1]
        self.MailList = []
        for _t in list:
            _d = {}
            _d['id'] = _t.split(' ')[0]
            _d['size'] = _t.split(' ')[1]
            self.MailList.append(_d)
        print('len_mail_list',len(self.MailList))
        self.mailList = []
        for _t in self.MailList:
            self.clientSocket.sendall(('RETR ' + _t['id'] + '\r\n').encode())
            _ = self.clientSocket.recv(1024).decode()
            if not '+OK' in _:
                return False
            _mail = ''
            _size = int(_t['size'])
            if('Received: from'in _):
                # print('里面有',_)
                b,start=_.split('octets\r\n', 1)
                _size -= len(start)
                _mail += start
            #     print('split',start)
            # print('第一次接收',_mail)
            while _size > 0:
                _ = self.clientSocket.recv(1024).decode()
                # print('第二次接收到',_)
                _size -= len(_)
                _mail = _mail + _
            # print('本轮共收到',_mail)
            # Format the mail
            # _mailobj = email.message_from_string(_mail)
            self.mailList.append(_mail)
            print("get all mails")
    def delete(self,index):
        print(self.len_mail_list,'删除第',index)
        self.clientSocket.sendall(('DELE ' + str(index+1) + '\r\n').encode())
        print('dele')
        _= self.clientSocket.recv(1024).decode()
        print(_,self.getStat())
    def newpop3(self):
        return self.mailserver,self.user_login,self.psw_login
    def quit(self):
        # if not self.loginSucc:
        #     self.logger.error('Please login first!')
        #     return False, '请先登录'

        self.clientSocket.sendall(('QUIT \r\n').encode())
        _ = self.clientSocket.recv(1024)
        print(_)


