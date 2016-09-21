#coding=utf-8
import shelve
from random import choice

'''
在服务器初始化
db = shelve.open('main/tools/ew.dat')
db['food'] = []
db.close()
'''

RESPONSE = [
    u'今天不如吃%s吧',
    u'就吃%s咯',
    u'我觉得今天应该吃%s',
    u'我听到猪仔的内心告诉我今天想吃%s'
]

def add_food(content):
    db = shelve.open('main/tools/ew.dat')
    content = content.strip()
    temp = db['food']
    temp.append(content)
    db['food'] = temp
    db.close()

def lookup_food():
    db = shelve.open('main/tools/ew.dat')
    try:
        temp = db['food']
        response = choice(RESPONSE) % choice(temp)
        return response
    finally:
        db.close()

