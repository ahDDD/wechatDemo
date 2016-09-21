#coding=utf-8

from . import redis
from .utils import init_wechat_instance
from .model import User, Message
from flask import make_response
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage, EventMessage
from .tools.convert_dt import *
from .tools.cop import *
from .tools.eat_what import *
from sqlalchemy.exc import IntegrityError, InvalidRequestError

def handle_response(data):
    wechat = init_wechat_instance()
    try:
        wechat.parse_data(data=data)
    except ParseError:
        return 'Invalid XML Data', 400

    message = wechat.message
    openid = message.source

    # 防止openid已存在写不进数据库
    user = User.query.filter_by(openid=openid).first()
    if not isinstance(user, User):
        user = User(openid=openid)
        user.save()

    if isinstance(message, EventMessage):
        if wechat.message.type == 'subscribe':
            dt = timestamp_datetime(message.time)
            message_instance = Message(openid=openid, message_type='subscribe', dt=dt)
            message_instance.save()
            user.subscribe_dt = dt
            user.update()
            content = "欢迎关注调试使用~\n回复 '我' 查看目前唯一的功能"
            reply = wechat.response_text(content=content)
            response = make_response(reply)
            response.content_type = 'application/xml'
            return response


    if isinstance(message, TextMessage):
        dt = timestamp_datetime(message.time)

        user.last_dialog_dt = dt
        user.update()

        content = message.content

        message_instance = Message(openid=openid, message_type='TextMessage', dt=dt, message_content=content)
        message_instance.save()

        if content == u'我':
            reply_text = me(user)

        elif content[:2] == u'cop':
            reply_text = cop()
            # if len(content) > 3:
            #     reply_text = cop(content[4:])

        elif content[:4] == u'我知道 ':
            add_food(content[4:])
            reply_text = u'好'

        elif content[:5] == u'今天吃什么':

            reply_text = lookup_food()

        else:
            reply_text = content

        reply = wechat.response_text(content=reply_text)
        response = make_response(reply)
        response.content_type = 'application/xml'
        return response

def me(user):
    content = \
        '''
目前还没法知道你叫什么\n
你关注的时间为%s\n
你和我的对话记录一共有%d条\n
最后一条的记录为 %s\n
发送于%s
        '''
    subscribe_dt = str(user.subscribe_dt)
    messages_count = int(Message.query.filter_by(openid=user.openid).count())
    last_message = Message.query.filter_by(openid=user.openid).order_by(Message.dt.desc()).first()
    last_message_content = str(last_message.message_content.encode('utf-8'))
    last_message_dt = last_message.dt.strftime('%Y-%m-%d %H:%M:%S')
    reply_text = content % (subscribe_dt, messages_count, last_message_content, last_message_dt)
    return reply_text