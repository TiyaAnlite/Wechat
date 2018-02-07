# -*- coding: utf-8 -*-
# filename: Controller.py

import json

class UserReader(object): #用户数据读写器
    def __init__(self, user):
        try:
            file = "users/" + str(user)
            re_UserData = open(file, "r+")
            self.UserData = json.loads(re_UserData.read)
            self.UserRead = True
        except expression as identifier:
            self.UserRead = False
            print "[Controller] UserReader Callback: ", identifier #将抛出的错误输出到控制台

    def register(self, user, key=False): #用户注册
        file = open("config/apikey.json", "r+")
        api_key = json.loads(file.read())
        NickName = None
        Permission = { "AccountBook": False, "DevZone": False}
        if key:
            try:
                 if api_key[key][isUsed]:
                     raise MyException("This Api Key has benn used: ",key)
                 NickName = api_key[key][]
            except expression as identifier:
                print "[Controller] UserRegister Callback: ", identifier



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
    if User.UserRead: #用户鉴权
        pass
    else:
        pass