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

class CallBackReader(object): #返回码解析对象，服务初始化时调用
    pass

class ListReader(object): #菜单列表解析对象，服务初始化时调用
    pass

class ContentReader(object): #文本解析中心
    pass

# json.dumps(a,sort_keys=True, indent=4, separators=(',', ': '))

def input(User, Content, IOCallBack, IOList):
    User = UserReader(User)
    if User.UserRead: #用户鉴权
        pass