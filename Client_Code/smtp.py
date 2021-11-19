import time
from socket import *
import base64

class SMTP():
    def __init__(self):
        super().__init__()
    def connect(self,mailserver):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.mailserver=mailserver
        self.clientSocket.connect((self.mailserver, 25))
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        heloCommand = 'HELO Alice\r\n'
        self.clientSocket.send(heloCommand.encode())
        recv1 = self.clientSocket.recv(1024).decode()
        print(recv1)
    
    def auth(self,user_login,psw_login):
        self.clientSocket.sendall('AUTH LOGIN\r\n'.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        self.user_login=user_login
        self.psw_login=psw_login
        username = base64.b64encode(user_login.encode()).decode()
        password = base64.b64encode(psw_login.encode()).decode()
        #分别发username和password(授权码)
        self.clientSocket.sendall((username + '\r\n').encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        self.clientSocket.sendall((password + '\r\n').encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
    
    def send_to(self,toaddress):
        self.clientSocket.sendall(('MAIL FROM: <' + self.user_login + '>\r\n').encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        self.toaddress=toaddress
        self.clientSocket.sendall(('RCPT TO: <' + self.toaddress + '>\r\n').encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        self.clientSocket.send('DATA\r\n'.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
    def send_content(self,subject,contenttype,content):
        message = 'from:' + self.user_login + '\r\n'
        message += 'to:' + self.toaddress + '\r\n'
        message += 'subject:' + subject + '\r\n'
        message += 'Content-Type:' + contenttype + '\t\n'
        message += '\r\n' + content
        self.clientSocket.sendall(message.encode())
        endmsg = "\r\n.\r\n"
        # Message ends with a single period.
        self.clientSocket.sendall(endmsg.encode())
        recv = self.clientSocket.recv(1024).decode()
        time.sleep(1)
        return recv
    def newsmtp(self):
        return self.mailserver,self.user_login,self.psw_login


    def quit(self):
        self.clientSocket.sendall('QUIT\r\n'.encode())
        _ = self.clientSocket.recv(1024)
        print(_,'quit成功')

# s=SMTP()
# s.connect_helo(mailserver = "smtp.163.com")
# s.auth(user_login="lee_yongqi@163.com",psw_login="VOAEJXSKAYMZVIDY")
# s.send_to(toaddress="lee_yongqi@163.com")
# s.send_content(subject="ceshi",contenttype="text/plain",content="eqwe")

