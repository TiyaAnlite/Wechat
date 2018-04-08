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
    Mail.pack()
    Mail.send()
    
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
        self.SendMsg['From'] = formataddr(self.Mot["From"], self.Appdata["Config"]["Sender"])
        
    def send(self): #线程启动器
        thread = threading.Thread(target=send_thread)
        thread.start()
        
    def send_thread(self): #SMTP交互实际结构，内部迭代receivers
        config = self.Appdata["Config"]
        smtpObj = smtplib.SMTP()
        try:
            smtpObj.connect(config["Smtp_host"], config["Smtp_port"])
            smtpObj.login(config["Mail_user"], config["Mail_pass"])
            for map_rec in self.receivers:
                map_SendMsg = self.SendMsg
                #给结构体加上最后一个TO头，迭代中发送
                map_SendMsg['To'] = formataddr(self.Mot["To"], map_rec)
                smtpObj.sendmail(config["Sender"], map_rec, map_SendMsg.as_string())
                smtpObj.quit()
        except:
            print("[Model]Mail: A mail has not been send")