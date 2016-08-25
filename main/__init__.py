#coding=utf-8
from flask import Flask
from redis import Redis
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__, instance_relative_config=True)

app.config.from_pyfile('config.py')

redis = Redis(host='127.0.0.1', port=5280)

# 记录日志
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
handler.setLevel(logging.WARNING)
app.logger.addHandler(handler)