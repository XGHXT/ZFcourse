# coding:utf8
import json
import re
import shutil
import time

import requests
from bs4 import BeautifulSoup
from flask import (Flask, flash, g, jsonify, redirect, render_template,
                   request, session, url_for)

import config
from exts import draw, exts, sub_query, getTimeTable
from matplot import chart
from models import Score, Student, Subject, db
from sendemail import sendemail, parsermail, wechatInfo
from spider import getScore, spiderLogin, timeTable

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

with app.test_request_context():
    #db.drop_all()
    db.create_all()


# 上下文管理器，保存登陆用户
@app.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
        return {'login_user': g.user}
    return {}


# 钩子函数，每次响应执行前运行
@app.before_request
def my_before_request():
    id = session.get('id')
    name = session.get('name')
    if id:
        g.user = name


@app.route('/')
def login():
    return render_template('login.html', user=1)


# 登出
@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))


# 学生用户登陆
@app.route('/studentlogin', methods=['GET', 'POST'])
def studentlogin():
    if request.method == 'GET':
        return render_template('login.html', user=1)
    else:
        try:
            id = request.form.get('id')
            password = str(request.form.get('password'))
            username = getScore(id, password)
            session['id'] = id
            session['passwd'] = password
            session['name'] = username
            session['user'] = 'student'
            return redirect(url_for('student'))
        except:
            flash('', 'error')
            return render_template('login.html', user=1)


# 学生主界面
@app.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'GET':
        id = session.get('id')
        credit_list, time_list = draw(id)
        credit = []
        for c in credit_list:
            credit.append(c[2])
        chart(credit, time_list)
        return render_template('student.html')
    else:
        return render_template('student.html')


# 成绩查询
@app.route('/score', methods=['GET', 'POST'])
def score():
    if request.method == 'GET':
        id = session.get('id')
        stu = Score.query.filter(Score.stu_id == id).all()
        credit = exts(stu)
        credit.append('all')
        credit.append('all')
        return render_template("score.html", classes=stu, credit=credit)
    else:
        id = session.get('id')
        year = request.form.get('year')
        term = request.form.get('term')
        if year == 'all' and term == 'all':
            return redirect(url_for('score'))
        else:
            credit, cla = sub_query(id, year, term)
        credit.append(year)
        credit.append(term)
        return render_template("score.html", classes=cla, credit=credit)


# 课程查询
@app.route('/timetable', methods=['GET', 'POST'])
def timetable():
    week = ['星期一','星期二','星期三','星期四','星期五','星期六','星期日']
    id = session.get('id')
    passwd = session.get('passwd')
    if request.method == 'GET':
        timeTable(id, passwd, '2018', '1')
        time_table = getTimeTable(id, '2018', '1')
        return render_template("timetable.html",len=len, week=week,  time_table=time_table, year='2017', term='1')
    else:
        year = request.form.get('year')
        term = request.form.get('term')
        timeTable(id, passwd, year, term)
        time_table = getTimeTable(id, year, term)
        return render_template("timetable.html",len=len, week=week, time_table=time_table, year=year, term=term)


# 邮箱推送
@app.route('/email', methods=['GET', 'POST'])
def email():
    if request.method == 'GET':
        return render_template('sendemail.html')
    else:
        receive = request.form.get('email')
        id = session.get('id')
        name = session.get('name')
        if sendemail(id, receive, name):
            flash('', 'OK')
            return render_template('sendemail.html')
        else:
            flash('', 'error')
            return render_template('sendemail.html')


def xml_parser(text):
    dic = {}
    soup = BeautifulSoup(text, 'html.parser')
    div = soup.find(name='error')
    for item in div.find_all(recursive=False):
        dic[item.name] = item.text
    return dic








if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4000,debug=True)
