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
        file = open("model/data/accountbook.json","r")
        self.Appdata = json.loads(file.read())
        file.close()
        
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
                Mail.input("dev", "AccountBook.transfer", maildata)
            else:
                self.FuctionTag = "transfer.error"
    
    def callback(self):
        pass