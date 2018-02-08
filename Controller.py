# -*- coding: utf-8 -*-
# filename: Controller.py

import json
import os

class UserReader(object): #用户数据读写器
    def __init__(self, user):
        if os.path.isfile("users/" + key + ".json"):
            file = "users/" + str(user)
            re_UserData = open(file, "r+")
            self.Data = json.loads(re_UserData.read)
            self.Read = True
            re_UserData.close()
        else:
            self.UserRead = False

    def register(self, user, key=False): #用户注册
        key_file = open("config/apikey.json", "r+")
        api_key = json.loads(key_file.read())
        key_file.close()
        NickName = None
        Status = "Main"
        Permission = { "AccountBook": False, "DevZone": False}
        if key:
            try:
                 if api_key[key][isUsed]:
                     raise MyException("This Api Key has benn used: ",key)
                 NickName = api_key[key]["NickName"]
                 Permission = api_key[key]["Permission"]
                 if Permission[AccountBook]:
                     Permission[Data.AccountBook] = AccountBook_Socket()
                
            except expression as identifier:
                print "[Controller] UserRegister Callback: ", identifier
                return "Content.illegalkey"
        else:
            pass

    def AccountBook_Socket()
        data = {"Count":0, "TransferCount":0}
        return data



class CallBackReader(object): #返回码解析对象，服务初始化时调用
    def __init__(self):
        file = open("config/callback.json", "r")
        self.Data = json.loads(file.read())
        file.close()

class ListReader(object): #菜单列表解析对象，服务初始化时调用
    def __init__(self):
        file = open("config/list.json", "r")
        self.Data = json.loads(file.read())
        file.close()

class ContentReader(object): #文本解析中心
    pass

# json.dumps(a,sort_keys=True, indent=4, separators=(',', ': '))

def input(User, Content, IOCallBack, IOList):
    User = UserReader(User)
    if User.Read: #用户鉴权
        pass
    else:
        try:
            key = int(Content)
            if key == 0:
                
            else:
                pass
        except:
            pass
        finally:
            pass