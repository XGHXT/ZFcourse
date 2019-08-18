# -*-coding:utf-8 -*-
import json
import sys
import time
import re

import requests
from bs4 import BeautifulSoup

from crypto_rsa.base64 import Base64 as pB64
from crypto_rsa.RSAJS import RSAKey
from models import Score, Student, Subject, db

reload(sys)
sys.setdefaultencoding("utf-8")

# 时间戳
ctime = int(time.time() * 1000)
post_url = 'http://syjw.wsyu.edu.cn/xtgl/login_slogin.html?time={0}'.format(
    ctime)
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Length': '471',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'syjw.wsyu.edu.cn',
    'Origin': 'http://syjw.wsyu.edu.cn',
    'Pragma': 'no-cache',
    'Referer': 'http://syjw.wsyu.edu.cn/xtgl/login_slogin.html?language=zh_CN&_t={0}'.format(ctime),
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

header1 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'syjw.wsyu.edu.cn',
    'Referer': 'http://syjw.wsyu.edu.cn/xtgl/login_slogin.html?language=zh_CN&_t={0}'.format(ctime),
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}


# 密码加密
def getEnPassword(string, exponent, modulus):
    b64 = pB64()
    exponent = b64.b64_to_hex(exponent)
    modulus = b64.b64_to_hex(modulus)
    rsa = RSAKey()
    rsa.setPublic(modulus, exponent)
    crypto_t = rsa.encrypt(string)
    return b64.hex_to_b64(crypto_t)


# 模拟登陆
def spiderLogin(yhm, passwd):
    s = requests.Session()
    r = s.get(post_url, headers=header1)
    r.encoding = 'utf-8'
    doc = r.text
    soup = BeautifulSoup(doc, 'html.parser')
    # 解析获取csrftoken值
    csrftoken = str(soup.find('input', id="csrftoken")['value'])
    publicKeyUrl = "http://syjw.wsyu.edu.cn/xtgl/login_getPublicKey.html?time={}&_={}".format(
        ctime, ctime-10)
    modExp = s.get(publicKeyUrl).json()
    get_mm = getEnPassword(passwd, modExp["exponent"], modExp["modulus"])
    postdata = [
        ('csrftoken', csrftoken),
        ('yhm', yhm),
        ('mm', get_mm),
        ('mm', get_mm)
    ]
    s.post(post_url, data=postdata, headers=header)
    score_url = 'http://syjw.wsyu.edu.cn/xsxxxggl/xsgrxxwh_cxXsgrxx.html?gnmkdm=N100801&layout=default&su={}'.format(
        yhm)
    r = s.get(score_url)
    r.encoding = 'utf8'
    doc = r.content
    soup = BeautifulSoup(doc, 'html.parser')
    info = soup.find_all('p', class_='form-control-static')
    # 存储学生信息
    lists = []
    for text in info:
        text = text.getText().strip()
        lists.append(text)
    # 查询是否已存在该用户, 若存在则更新数据，不存在则写入
    user = Student.query.filter(Student.id == yhm).first()
    if user:
        user.grade = lists[21]
        user.collage = lists[22]
        user.major = lists[24]
        user.class_ = lists[26]
        db.session.commit()
    else:
        stu = Student(lists[0], lists[1], lists[6], lists[8],
                      lists[21], lists[22], lists[24], lists[26])
        db.session.add(stu)
        db.session.commit()
    return lists[1], s


# 将成绩存入数据库
def addScoreDB(key):
    if key.has_key('jd') == False:
        key['jd'] = None
    school_year = str(key['xnmmc'])
    school_term = int(key['xqmmc'])
    class_name = str(key['kcmc'])
    class_code = str(key['kch_id'])
    if len(class_code) > 10:
        class_code = class_code[0:8]
    credit = float(key['xf'])
    class_category = str(key['kcxzmc'])
    test_category = str(key['ksxz'])
    cjsfzf = str(key['cjsfzf'])
    score = str(key['cj'])
    if score =="中等":
        score = "75"
    if score =="合格":
        score = "65"
    if score =="良好":
        score = "85"
    if score =="优秀":
        score = "95"  
          
 
    if score >= "90":
        GPA=4.0
    elif score >= "80":
        GPA=3.0
    elif score >= "70":
        GPA=2.0
    elif score >= "60":
        GPA=1.0
    else:
        GPA=0.0
            
    class_mark = str(key['kcbj'])
    if key.has_key('kkbmmc') == False:
        key['kkbmmc'] = None
    class_ownership = str(key['kkbmmc'])
    stu_id = str(key['xh'])
    sco = Score.query.filter(Score.school_year == school_year).filter(Score.school_term == school_term).filter(
        Score.class_name == class_name).filter(Score.test_category == test_category).filter(Score.stu_id == stu_id).first()
    if sco:
        sco.credit = credit
        sco.class_category = class_category
        sco.test_category = test_category
        sco.cjsfzf = cjsfzf
        sco.score = score
        sco.GPA = GPA
        sco.class_mark = class_mark
        sco.class_ownership = class_ownership
        db.session.commit()
    else:
        sco = Score(school_year, school_term, class_name, class_code, credit, class_category,
                    test_category, cjsfzf, score, GPA, class_mark, class_ownership, stu_id)
        db.session.add(sco)
        db.session.commit()


# 获取成绩
def getScore(yhm, passwd):
    name, s = spiderLogin(yhm, passwd)
    formdata = {
        'xnm': '',
        'xqm': '',
        '_search': 'false',
        'nd': ctime,
        'queryModel.showCount': '100',
        'queryModel.currentPage': '1',
        'queryModel.sortName': '',
        'queryModel.sortOrder': 'asc',
        'time': '0',
    }
    score_url = 'http://syjw.wsyu.edu.cn/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005'
    r = s.post(score_url, data=formdata)
    r.encoding = 'utf8'
    doc = r.content
    # 将字符串转为字典
    doc = json.loads(doc)
    for key in doc['items']:
        addScoreDB(key)
    return name

# 将课程表添加进数据库
def addTimetableDB(key, yhm, xnm, xqm):
    class_name = key['kcmc']
    day = key['xqjmc']
    time = key['jc']
    week = key['zcd']
    classroom = key['cdmc']
    teacher = key['xm']
    department = key['xqmc']
    length = re.findall(r"\d+\.?\d*", time)
    l = int(length[1]) - int(length[0]) + 1
    sub = Subject.query.filter(Subject.school_year == xnm).filter(Subject.school_term == xqm).filter(
    Subject.day == day).filter(
        Subject.class_name == class_name).filter(Subject.stu_id == yhm).first()
    if sub:
        sub.time = time
        sub.week = week
        sub.classroom = classroom
        sub.teacher = teacher
        sub.department = department
        sub.length = l
        db.session.commit()
    else:
        sub = Subject(xnm, xqm, class_name, day, time, week,
                      classroom, teacher, department, yhm, l)
        db.session.add(sub)
        db.session.commit()


# 获取课程表
def timeTable(yhm, passwd, xnm, xqm):
    name,s = spiderLogin(yhm, passwd)
    if xqm == "1":
        xq = "3"
    elif xqm == "2":
        xq = "12"
    table_url = "http://syjw.wsyu.edu.cn/kbcx/xskbcx_cxXsKb.html?gnmkdm=N253508"
    formdata = {
        'xnm': xnm,
        'xqm': xq
    }
    tables = s.post(table_url, data=formdata)
    tables.encoding = 'utf8'
    doc = tables.content
    table = json.loads(doc)
    for key in table['kbList']:
        addTimetableDB(key, yhm, xnm, xqm)
