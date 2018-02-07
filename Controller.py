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

class CallBackReader(object): #返回码解析对象
    pass

class ContentReader(object): #文本解析中心
    pass

# json.dumps(a,sort_keys=True, indent=4, separators=(',', ': '))

def input(User, Content):
    User = UserReader(User)
    if User.UserRead: #用户鉴权
        pass