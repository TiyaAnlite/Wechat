# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import reply
import receive
import controller

           
class Handle(object):
    def reReadIO(self): #读取系统配置
        print "[Load]IOCallBack"
        IOCallBack = controller.CallBackReader()
        print "[Load]IOList"
        IOList = controller.ListReader()
        return IOCallBack.Data, IOList.Data

    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "872855454" #请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "Handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument

    def POST(self):
        try:
            webData = web.data()
            print "Handle/POST: webdata is ", webData
   #后台打日志
            recMsg = receive.parse_xml(webData)
            print "recMsg is ", recMsg
            print "[Debug]recMsg.MsgType is ", recMsg.MsgType
            
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text': #主要内容
                IOCallBack, IOList = self.reReadIO() #IO操作在分支下独立操作，避免无效消息消耗IO
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = recMsg.Content
                recontent = controller.input(toUser, content, IOList) #用户信息，内容送入控制器，同时将其中一个系统IO变量送回控制器，同时为了适应多行输出，输出内容已改为列表数据
                e = 0
                print "[Conver]IOMsg"
                for i in recontent: #支持多行输出，后面是为了计数，注意它是从0开始计数的
                    if e > 0:
                        IOrecontent = IOrecontent + '\n'
                    e = e + 1
                    if i in IOCallBack: #部分消息是自定义的，为了识别，先会和库的配置先匹配
                        IOrecontent = IOCallBack[recontent].encode("utf-8") #中文信息必须要先被UTF-8编码，IOCallback不再送入控制器
                    else:
                        IOrecontent = i
                replyMsg = reply.TextMsg(toUser, fromUser, IOrecontent) 
                # replayMsg = "测试状态"
                return replyMsg.send()
            if isinstance(recMsg, receive.EventMsg) and recMsg.MsgType == 'event' and recMsg.Event == 'subscribe': #订阅部分事件推送
                IOCallBack, IOList = self.reReadIO()
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = IOCallBack["Main.subscribe"].encode("utf-8") #这里唯一一次脱离控制器调用公共IO
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                replytext = replyMsg.send()
                print "Callback Data is ", replytext
                return replytext
            else:
                print "[Msg PASS]"
                return "success"
        except Exception, Argment:
            print "except: ", Argment
            return Argment
