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
        print "[UR]init"
        if os.path.isfile(self.file):
            print "[UR]Is User"
            re_UserData = open(self.file, "r")
            # json_string = json.dumps(re_UserData.read)
            self.Data = json.loads(re_UserData.read())
            self.Read = True
            re_UserData.close()
        else:
            print "[UR]Not User"
            self.Read = False

    def register(self, key=False): #用户注册[读/写结构]
        key_file_read = "reading"
        while key_file_read == "reading":
            try:
                key_file = open("config/apikey.json", "r")
                key_file_read = True
            except:
                time.sleep(0.1)
        api_key = json.loads(key_file.read())
        Name = False #为下面写入器打标记的
        NickName = None
        Status = "Main"
        Permission = {"AccountBook": False, "DevZone": False}
        if key:
            key_file.close()
            del key_file
            while True:
                try:
                    os.remove("config/apikey.json")
                    key_file = open("config/apikey.json", "w")
                    break
                except:
                    time.sleep(0.1)
            try:
                if key in api_key:
                    print "[Key]Check done"
                    if api_key[key]["isUsed"]: #key鉴权
                        keydata = json.dumps(api_key,sort_keys=True, indent=4, separators=(',', ': '))
                        key_file.write(keydata)
                        key_file.close()
                        raise MyException("This Api Key has been used: " + str(key))
                    print "[Key]Is key can benn use."
                    NickName = api_key[key]["NickName"]
                    Permission = api_key[key]["Permission"]
                    Data_AccountBook = self.AccountBook_Socket(Permission["AccountBook"])  #注意：传入的是要对应模块权限的布尔值
                    Name = self.User
                    api_key[key]["isUsed"] = True
                    print "Writing key data..."
                    keydata = json.dumps(api_key,sort_keys=True, indent=4, separators=(',', ': '))
                    key_file.write(keydata)
                    key_file.close()
                    callback = ["Content.keyok"]
                    print "Start to create user(key used)"
                else:
                    keydata = json.dumps(api_key,sort_keys=True, indent=4, separators=(',', ': '))
                    key_file.write(keydata)
                    key_file.close()
                    print "[Key]Worng key"
                    raise MyException("Worng key: " + str(key))
            except MyException as e:
                print "[Controller] UserRegister Callback: ", e

                callback = ["Content.illegalkey"]
        else:
            key_file.close()
            callback = ["Content.onkeyok"]
            Name = self.User
            print "Start to create user"

        if Name: #构造写入数据，写操作交给写结构，与存取数据合并
            writedata = {}
            waitfordatakey = ["Name", "NickName", "Status"] #这里存放的是除字典以外的元素数据
            waitfordata = [Name, NickName, Status]
            # 由于Python 2不支持在列表中存放字典元素，因此包含字典数据的要分开处理
            writedata["Permission"] = Permission
            if Data_AccountBook: #如果未授权是返回False，如果变量不存在会出错
                writedata["Data.AccountBook"] = Data_AccountBook

            for key, data in zip(waitfordatakey,waitfordata): #将数据的键与值打包，并对应赋予完成绑定
                writedata[key] = data

            self.Data = writedata
            self.Update()

               
        return callback


    def AccountBook_Socket(self, Permission):
        if Permission: #在此分支做模块功能鉴权
            data = {"Count":0, "TransferCount":0}
            return data
        else:
            return False

    def Update(self): #用户数据写入器[写结构]
        try:
            data = json.dumps(self.Data,sort_keys=True, indent=4, separators=(',', ': '))
            try:
                os.remove(self.file) #写入存在bug，用先删后写代替
            except:
                pass
            userfile = open(self.file,"w")
            userfile.write(data)
            userfile.close()
        
        except Exception as e:
           print "[Controller] Cannot write user data,try again/n", e
           time.sleep(0.1) #IO操作延时




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
        

    def zone(self): #区域分发器，决定应跳往哪个节点，也是通常消息处理器
        callback = []
        model = False
        if self.Content in self.IO[self.LastStatus]: #通常消息处理
            NextStatus = self.IO[self.LastStatus][self.Content]
            NextZone = NextStatus.split('.')
            NextZone = NextZone[0]
            if NextZone == "Model": #重定向模块接口检查
                model = True
                callback = NextStatus
            elif self.Userdata["Permission"][NextZone]: #内部区域鉴权
                self.Userdata["Status"] = NextStatus
                callback.append(NextStatus)
            else:
                callback.append(NextZone + ".illegal")
        else:
            if "custom" in self.IO[self.LastStatus]: #检查区域是否支持自定义消息，为了避免忘记直接改成检查是否存在键
                callback = self.IO[self.LastStatus]["custom"] #返回需要调用的模块，并打上标签
                model = True
            else:
                callback.append("Content.illegal")
                callback.append(self.LastZone)
         
        return callback, model
        
    def model_process(self, model): #模块分发中心，依据传入调用的模块，再转发用户输入和数据
        import model as ModelPackage #先从模块库导入模块
        print("[ModelProcess]inputModel:")
        print(model)
        inputModel = model.split('.')[1]
        print("[ModelProcess]import Model:")
        print(inputModel)
        inputZone = model.split('.')[2]
        print("[ModelProcess]input Zone")
        print(inputZone)
        modelImportStr = "ModelPackage." + inputModel
        print("[ModelProcess]Eval str")
        print(modelImportStr)
        ImportModel = eval(modelImportStr) #表达式化需调用的模块
        print("[ModelProcess]receve model")
        ModelCallback, self.Userdata = ImportModel.input(inputZone, self.Content, self.Userdata)
        return ModelCallback
    
    def process(self):
        model = False
        self.LastStatus = self.Userdata["Status"]
        self.LastZone = self.Userdata["Status"].split('.')
        self.LastZone = self.LastZone[0]
        if not self.LastZone == "Model": #第一次分发，普通消息处理方式
            ZoneCallback, model = self.zone()
        if model: #第二次分发，提供两种调用，模块处理方式（由菜单中调用）
            inferModel = ZoneCallback #调用模块在返回值
            ZoneCallback = self.model_process(inferModel)
        if self.LastZone == "Model": #（由状态码直接重定向）
            inferModel = self.LastStatus
            ZoneCallback = self.model_process(inferModel)
        else:
            return ZoneCallback


def input(User, Content, IOList): #流水线，注意由于没有IOCallback，返回的必须是键值
    print "[COM]Start to create user obj."
    User = UserReader(User)
    print "[COM]Created User object"
    if User.Read: #用户鉴权
        print "[COM]User checked"
        Content = str(Content)
        Reader = ContentReader(User.Data, Content, IOList) #先传入，初始化
        callback = Reader.process() #再处理，接受输出
        User.Data = Reader.Userdata #取出用户数据
        User.Update()
        return callback

    else: #非法用户区域
        print "[Com]Unreg"
        try:
            Content = int(Content)
        except:
            pass
        
        if isinstance(Content,int): #未注册用户输入的是数字？
            print "[Com]key"
            key = str(Content)
            if Content == "0": #无key注册模式
                print("[Reg]No key mode")
                return User.register()

            else: #key注册模式，内部鉴权
                print("[Reg]Key mode].")
                return User.register(key)

        else: #输入的不是数字
            print "[COM]illegal"
            return ["Content.illegal", "Main.subscribe"]


