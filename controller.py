# -*- coding: utf-8 -*-
# filename: controller.py

import json
import os
import time

class MyException(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message 
        
class UserReader(object): #用户数据读写器
    def __init__(self, user): #读取构造[读结构]
        self.User = user
        self.file = "users/" + str(self.User) + ".json"
        print "[UR]init"
        if os.path.isfile(self.file):
            print "[UR]Is User"
            re_UserData = open(self.file, "r+")
            json_string = json.dumps(re_UserData.read)
            self.Data = json.loads(json_string)
            self.Read = True
            re_UserData.close()
        else:
            print "[UR]Not User"
            self.Read = False

    def register(self, key=False): #用户注册[读/写结构]
        key_file = open("config/apikey.json", "r+")
        api_key = json.loads(key_file.read())
        key_file.close()
        Name = False #为下面写入器打标记的
        NickName = None
        Status = "Main"
        Permission = {"AccountBook": False, "DevZone": False}
        if key:
            try:
                if key in api_key:
                    print "[Key]Check done"
                    if api_key["key"]["isUsed"]: #key鉴权
                        raise MyException("This Api Key has been used: " + key)
                    NickName = api_key["key"]["NickName"]
                    Permission = api_key["key"]["Permission"]
                    Data_AccountBook = AccountBook_Socket(Permission["AccountBook"])  #注意：传入的是要对应模块权限的布尔值
                    Name = self.User
                    callback = ["Content.keyok"]
                else:
                    print "[Key]Worng key"
                    raise MyException("Worng key: " + key)
            except MyException, e:
                print "[Controller] UserRegister Callback: ", e
                callback = ["Content.illegalkey"]
        else:
            callback = ["Content.onkeyok"]
            Name = self.User

        if Name: #真正开始写入用户数据的部分
            while Name:
                try:
                    userfile = open(self.file,"w")
                    writedata = {}
                    waitfordatakey = ["Name", "NickName", "Status"] #这里存放的是除字典以外的元素数据
                    waitfordata = [Name, NickName, Status]
                    # 由于Python 2不支持在列表中存放字典元素，因此包含字典数据的要分开处理
                    writedata["Permission"] = Permission
                    if Data_AccountBook: #如果未授权是返回False，如果变量不存在会出错
                        writedata["Data.AccountBook"] = Data_AccountBook

                    for key, data in zip(waitfordatakey,waitfordata): #将数据的键与值打包，并对应赋予完成绑定
                        writedata[key] = data

                    userfile.write(writedata)
                    userfile.close()
                    Name = False #循环标记，以离开循环

                except:
                    print "[Controller] Cannot write user data,try again"
                    time.sleep(0.1) #IO操作延时

        return callback


    def AccountBook_Socket(self, Permission):
        if Permission: #在此分支做模块功能鉴权
            data = {"Count":0, "TransferCount":0}
            return data
        else:
            return False

    def Update(self): #用户数据写入器[写结构]
        data = json.dumps(self.Data,sort_keys=True, indent=4, separators=(',', ': '))
        userfile = open(self.file,"w")
        userfile.write(data)
        userfile.close()



class CallBackReader(object): #返回码解析对象，服务初始化时调用
    def __init__(self):
        dis_done = True
        while dis_done:
            try:
                file = open("config/callback.json", "r")
                # json_string = json.dumps(file.read())
                self.Data = json.loads(file.read())
                file.close()
                dis_done = False
            except:
                print "[IO] Cannot read system callback data,try again"
                time.sleep(0.1)
        
    

class ListReader(object): #菜单列表解析对象，服务初始化时调用
    def __init__(self):
        dis_done = True
        while dis_done:
            try:
                file = open("config/list.json", "r")
                # json_string = json.dumps(file.read())
                self.Data = json.loads(file.read())
                file.close()
                dis_done = False
            except:
                print "[IO] Cannot read system list data,try again"
                time.sleep(0.1)
            

class ContentReader(object): #文本解析中心
    def __init__(self, user, content, io): #文本解析中心接受用户数据，请求内容和系统IO，初始化当前状态和数据接口
        self.Userdata = user
        self.Content = content
        self.IO = io
        

    def zone(self): #区域分发器，决定应跳往哪个节点
        callback = []
        model = False
        if self.Content in self.IO[self.LastStatus]: #通常消息处理
            NextStatus = self.IO[self.LastStatus][self.Content]
            NextZone = NextStatus.split('.')
            NextZone = NextZone[0]
            if self.Userdata["Permission"][NextStatus]: #内部区域鉴权
                self.Userdata["Status"] = NextStatus
                callback.append(NextZone)
            else:
                callback.append(NextZone + ".illegal")
        else:
            if "custom" in self.IO[self.LastStatus]: #检查区域是否支持自定义消息，为了避免忘记直接改成检查是否存在键
                callback.append("开发还尚未完成")
            else:
                callback.append("Content.illegal")
                callback.append(self.LastZone)
         
        return callback, model
    def process(self):
        self.LastStatus = self.Userdata["Status"]
        self.LastZone = self.Userdata["Status"].split('.')
        self.LastZone = self.LastZone[0]
        ZoneCallback, model = zone()
        if model:
            pass
        else:
            return self.Userdata, callback


def input(User, Content, IOList): #流水线，注意由于没有IOCallback，返回的必须是键值
    print "[COM]Start to create user obj."
    User = UserReader(User)
    print "[COM]Created User object"
    if User.Read: #用户鉴权
        print "[COM]User check"
        Reader = ContentReader(User.Data, Content, IOList) #先传入，初始化
        User.Data, callback = ContentReader.process() #再处理，接受输出
        User(update)
        return callback

    else: #非法用户区域
        print "[Com]Unreg"
        try:
            Content = int(Content)
        except:
            pass
        
        if isinstance(Content,int): #未注册用户输入的是数字？
            print "[Com]key"
            key = Content
            if Content == 0: #无key注册模式
                return User.register()

            else: #key注册模式，内部鉴权
                return User.register(key)

        else: #输入的不是数字
            print "[COM]illegal"
            return ["Content.illegal"]


