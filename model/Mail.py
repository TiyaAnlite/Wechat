# -*- coding: utf-8 -*-
# filename: Mail.py

import json
import smtplib
import threading

from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header

def input_mail(receivers, Mot, data):
    Mail = Mail_model(receivers, Mot, data)
    print("[Model]Mail:Model input")
    Mail.pack()
    print("[Model]Mail:Data packed")
    Mail.send()
    print("[Model]Mail:Data sent")
    
class Mail_model(object):
    def __init__(self, receivers, Mot, data):
        self.data = data
        fp = open("model/data/mail.json", "r")
        self.Appdata = json.loads(fp.read())
        fp.close()
        
        self.Mot = self.Appdata["MOT"][Mot]
        if receivers == "dev": #在此特别注明，收件人结构体是列表
            self.receivers = self.Appdata["Config"]["devmail"]
        else:
            self.receivers = receivers
            
    def pack(self): #除了［TO］部分，其他均在此完成包装
        Msg = self.Mot["Message"]
        #以下迭代值，次数等于输入的数据数目，注意range函数末尾需加一
        for i,x in zip(range(1, len(self.data) + 1), self.data):
            find = Msg.split("Value" + str(i))
            #使用split函数简介寻找键，若键不足则弹出
            if len(find) > 1:
                Msg = find.pop(0) #为了插入两个文本之间，先去头，顺带输出
                Msg = Msg + [x + u for u in find] #多位点插入（单个值插多处键），表达式实现
                
        self.SendMsg = MIMEText(Msg, 'plain', 'utf-8')
        self.SendMsg['Subject'] = Header(self.Mot["Subject"], 'utf-8')
        self.SendMsg['From'] = formataddr([self.Mot["From"], self.Appdata["Config"]["Sender"]])
        
    def send(self): #线程启动器
        thread = threading.Thread(target=self.send_thread)
        thread.start()
        
    def send_thread(self): #SMTP交互实际结构，内部迭代receivers
        config = self.Appdata["Config"]
        
        try:
            print("[Model]Mail(Thread):Connect & Login to SMTP server")
            smtpObj = smtplib.SMTP_SSL(config["Smtp_host"], config["Smtp_port_SSL"])
            # smtpObj.starttls() #SSL连接方式
            smtpObj.login(config["Mail_user"], config["Mail_pass"])
            print("[Model]Mail(Thread):Sending data to server")
            smtpObj.connect()
            for map_rec in self.receivers:
                map_SendMsg = self.SendMsg
                #给结构体加上最后一个TO头，迭代中发送
                map_SendMsg['To'] = formataddr([self.Mot["To"], map_rec])
                smtpObj.sendmail(config["Sender"], map_rec, map_SendMsg.as_string())
                smtpObj.quit()
                print("[Model]Mail(SMTP):a mail object has been sent")
        except Exception, Argment:
            print("[Model]Mail(SMTP): A mail has not been send")
            print(Argment)
            try:
                smtpObj.quit()
                print("[Model]Mail(SMTP):Closed a smtp connection")
            except:
                pass