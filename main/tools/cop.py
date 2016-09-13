#coding=utf-8

import MySQLdb

def cop(date=None):
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123321', db='cop', charset='utf8')
    cursor = conn.cursor()
    sql = "SELECT FROM_UNIXTIME(regtime,'%Y%m%d') days,COUNT(*) COUNT FROM tp_user GROUP BY days"
    returns = cursor.execute(sql)
    content = '  日期  |注册人数\n'
    for row in cursor.fetchall():
        content += '%s|%s\n' %(str(row[0]), str(row[1]))

    return content

# conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123321', db='cop', charset='utf8')
# cursor = conn.cursor()
# sql = "SELECT FROM_UNIXTIME(regtime,'%Y%m%d') days,COUNT(*) COUNT FROM tp_user GROUP BY days"
# returns = cursor.execute(sql)
# content = '日期 注册人数\n'
# for row in cursor.fetchall():
#     content += '%s %s\n' %(str(row[0]), str(row[1]))
# print len(content)