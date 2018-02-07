# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import reply
import receive
import Controller

           
class Handle(object):
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
            global IOCallBack, IOList #重新强调下IOCallBack和IOList ，以免无法找到
            print "recMsg is ", recMsg
            print "[Debug]recMsg.MsgType is ", recMsg.MsgType
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text': #主要内容
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = recMsg.Content
                recontent = Controller.input(toUser, content, IOCallBack, IOList) #用户信息，内容送入控制器，同时将两个系统IO变量送回控制器
                replyMsg = reply.TextMsg(toUser, fromUser, recontent) 
                # replayMsg = "测试状态"
                return replyMsg.send()
            if isinstance(recMsg, receive.EventMsg) and recMsg.MsgType == 'event' and recMsg.Event == 'subscribe': #订阅部分事件推送
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = IOCallBack.Data[Main.subscribe] #这里唯一一次脱离控制器调用公共IO
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
