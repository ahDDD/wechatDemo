#coding=utf-8from . import app, redisfrom wechat_sdk import WechatConf, WechatBasicdef init_wechat_instance():    """初始化微信实例"""    access_token = redis.get('wechat:access_token')    token_expires_at = redis.get('wechat:access_token_expires_at')    if access_token and token_expires_at:        wechat = WechatBasic(            appid=app.config['APP_ID'],            appsecret=app.config['APP_SECRET'],            token=app.config['TOKEN'],            #encrypt_mode=app.config['ENCRYPT_MODE'],            access_token=access_token,            access_token_expires_at=int(token_expires_at)        )        # wechat = WechatBasic(conf=conf)    else:        wechat = WechatBasic(            appid=app.config['APP_ID'],            appsecret=app.config['APP_SECRET'],            token=app.config['TOKEN'],            #encrypt_mode=app.config['ENCRYPT_MODE']        )        # wechat = WechatBasic(conf=conf)        access_token = wechat.get_access_token()        redis.set('wechat:access_token', access_token['access_token'], 7000)        redis.set('wechat:access_token_expires_at', access_token['access_token_expires_at'], 7000)    return wechat