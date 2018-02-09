# -*- coding: utf-8 -*-
# filename: main.py
import web
from handle import Handle
from controller import CallBackReader, ListReader

def reReadIO(): #系统初始化时预读系统配置，减少并发IO负担与冲突
    IOCallBack = CallBackReader()
    IOList = ListReader()
    return IOCallBack, IOList

urls = (
    '/wx', 'Handle',
)

if __name__ == '__main__':
    IOCallBack, IOList = reReadIO()
    app = web.application(urls, globals())
    app.run()
