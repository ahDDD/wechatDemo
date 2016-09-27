#coding=utf-8
import requests
import re


def check_720p() :
    '''
    检查电影是否有720版本
    '''
    headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'}
    html = requests.get('http://www.dysfz.net/movie13325.html', headers=headers)
    html.encoding = 'utf-8'
    if re.search('720p', html.text):
        return u'有高清啦!!'
    else:
        return u'还是没有高清额,我们再等等~'

