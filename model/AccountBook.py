# -*- coding: utf-8 -*-
# filename: AccountBook.py

import model.Mail as Mail
import json
import time

def input(Call, Content, Userdata):
    Account = AccountBook(Content, Userdata)
    exp = "Account." + Call + "()"
    eval(exp)
    callback, data = Account.callback()
    return callback, data
    
class AccountBook(object):
    def __init__(self, Content, Data):
        self.Content = Content
        self.Data = Data
        self.FuctionTag = False
        self.UserAccount = str(self.Data["Data.AccountBook"]["Count"])
        self.Transfer = str(self.Data["Data.AccountBook"]["TransferCount"])
        self.UserName = self.Data["NickName"]
        fp = open("model/data/accountbook.json","r")
        self.Appdata = json.loads(fp.read())
        fp.close()
        
    def checkout(self):
        self.FuctionTag = "checkout"
        
    def transfer(self):
        UserAccount = int(self.UserAccount)
        try:
            Request = int(self.Content) #预防用户输入值非法
        except:
            pass
        else:
            if UserAccount >= Request:
                self.Transfer = str(int(self.Transfer) + Request)
                self.UserAccount = str(UserAccount - Request)
                self.FuctionTag = "transfer.successed"
                y, m, d, h, mi, s, null, null, null = time.localtime(time.time())
                order_id = "T0297" + str(y) + str(m) + str(d) + str(h) + str(mi) + str(s)
                maildata = [order_id, time.asctime(time.localtime(time.time)), self.UserName, str(Request), self.Transfer, self.UserAccount]
                #构建消息体：订单号，创建时间，连接用户，请求金额，总请求金额，用户余额
                #调用Mail模块
                Mail.input("dev", "AccountBook.transfer", maildata)
            else:
                self.FuctionTag = "transfer.error"
    
    
    def callback(self): #读取，链接，模块解析器
        key = self.FuctionTag.split('.')
        list = self.Appdata["MSG_model"]
        [list = list[i] for i in key] #迭代递进到对应功能目录
        msg = [] 
        for x in list: #逐行读取列表
            head = x.split('_')
            
            if head[0] == "M" #Message键"
                msg.append(self.Appdata["Message"][head[1]]
            
            if head[0] == "V" #Variable键
                msg.append(eval("self." + head[1]))
                
        #写回IO，注意时刻与readIO()保持反向
        self.Data["Data.AccountBook"]["Count"] = int(self.UserAccount)
        self.Data["Data.AccountBook"]["TransferCount"] = int(self.Transfer)
        
        return msg, self.Data