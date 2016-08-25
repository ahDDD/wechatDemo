#coding=utf-8
from main import app

from main.utils import init_wechat_instance
from main.response import handle_response
from flask import request, make_response, redirect


@app.route('/', methods = ['GET', 'POST'])
def wechat_auth():

    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')

    wechat = init_wechat_instance()
    if not wechat.check_signature(
        signature=signature, timestamp=timestamp, nonce=nonce):
        if request.method == 'POST':
            return "signature failed"
        else:
            return redirect(app.config['MAIN_URL'])

    if request.method == 'POST':
        return handle_response(request.data)
    else:
        # 微信接入验证
        return make_response(request.args.get('echostr', ''))

if __name__ == '__main__':
    app.debug = app.config['DEBUG']
    app.run(port=8000)
