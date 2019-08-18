#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 使用QQ的SMTP服务器代理发送邮件

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

from models import Score

def sendemail(id, my_user, user_name):
    my_sender='wsyuacm@foxmail.com'    # 发件人邮箱账号
    my_pass = 'xsivmanwcvrebffb'              # 发件人邮箱授权码
    ret=True
    try:
        n = parsermail(id)
        msg=MIMEText(n,'html','utf-8')
        msg['From']=formataddr(["教务系统",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']=formataddr([user_name,my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']="你的成绩单"                # 邮件的主题，也可以说是标题

        server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret=False
        
    if ret:
        return True
    else:
        return False

def parsermail(id):
    html = '''<table border="1" cellspacing="0" cellpadding="0">\n
    <tr>
    <td>学年</td>
    <td>学期</td>
    <td>课程名称</td>
    <td>考试性质</td>
    <td>成绩</td>
    </tr>'''
    sco = Score.query.filter(Score.stu_id == id).all()
    for s in sco:
        html = html + '<tr><td>\n'
        html = html + str(s.school_year.encode('utf8')) + '</td>\n<td>'
        html = html + str(s.school_term) + '</td>\n<td>'
        html = html + str(s.class_name.encode('utf8')) + '</td>\n<td>'
        html = html + str(s.test_category.encode('utf8')) + '</td>\n<td>'
        html = html + str(s.score) + '</td>\n<tr>'

    html = html + '</table>'
    return html


def wechatInfo(id, year, term):
    html = ""
    if year == 'all':
        if term == 'all':
            sco = Score.query.filter(Score.stu_id == id).all()
        else:
            sco = Score.query.filter(Score.stu_id == id).filter(Score.school_term == term).all()
    else:
        if term == 'all':
            sco = Score.query.filter(Score.stu_id == id).filter(Score.school_year == year).all()
        else:
            sco = Score.query.filter(Score.stu_id == id).filter(Score.school_year == year).filter(Score.school_term == term).all()
    if sco:
        for s in sco:
            html = html + str(s.class_name.encode('utf8')) + " "
            html = html + str(s.test_category.encode('utf8')) + " "
            html = html + str(s.score) + '\n'
            html = html + '\n'
    else:
        html = "暂无{}学年{}学期的成绩信息!".format(year, term)

    return html
