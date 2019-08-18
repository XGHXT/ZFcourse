# coding:utf8
from models import Student, Subject, Score
import re


# 计算平均学分
def exts(cla):
    # 所有课程的学分
    allcredit = 0
    # 未获得的学分
    gotcredit = 0
    # 平均绩点
    GPA = 0
    #平均分
    apoint = 0
    
    for c in cla:
        if c.test_category.encode('utf-8') == '正常考试':
            allcredit = allcredit + c.credit
            GPA = GPA + c.GPA * c.credit
            apoint = apoint+c.credit*c.score
        else:
            if c.score < 60:
                gotcredit = gotcredit + c.credit
    if allcredit == 0:
        GPA = 0
    else:
        GPA = GPA/allcredit
        apoint = apoint/allcredit
    GPA = round(GPA, 2)
    apoint = round(apoint, 2)
    credit = [allcredit, gotcredit, GPA, apoint]
    return credit


def sub_query(id, year, term):
    lists = []
    stu = Score.query.filter(Score.stu_id == id).all()
    if year == 'all':
        for cla in stu:
            if cla.school_term == int(term):
                lists.append(cla)
    elif term == 'all':
        for cla in stu:
            if cla.school_year == year:
                lists.append(cla)
    else:
        for cla in stu:
            if cla.school_term == int(term) and cla.school_year == year:
                lists.append(cla)
    if lists:
        credit = exts(lists)
    else:
        credit = [0, 0, 0]

    return credit, lists


def draw(id):
    year_list = []
    term_list = []
    score_list = []
    credit_list = []
    time_list = []
    sco = Score.query.filter(Score.stu_id == id).all()
    for s in sco:
        if s.school_year in year_list:
            pass
        else:
            year_list.append(s.school_year)
        if s.school_term in term_list:
            pass
        else:
            term_list.append(s.school_term)
    for year in year_list:
        for term in term_list:
            for s in sco:
                if s.school_year == year and s.school_term == term:
                    score_list.append(s)
            time = str(year) + '(' + str(term) + ')'
            print time
            time_list.append(time)
            credit = exts(score_list)
            credit_list.append(credit)
            score_list = []
            print credit
    return credit_list, time_list


def getTimeTable(id, year, term):
    time_table = {
        '星期一': [[], [], [], [], [], [], [], [], [], [], []],
        '星期二': [[], [], [], [], [], [], [], [], [], [], []],
        '星期三': [[], [], [], [], [], [], [], [], [], [], []],
        '星期四': [[], [], [], [], [], [], [], [], [], [], []],
        '星期五': [[], [], [], [], [], [], [], [], [], [], []],
        '星期六': [[], [], [], [], [], [], [], [], [], [], []],
        '星期日': [[], [], [], [], [], [], [], [], [], [], []],
    }
    lists = ''
    for day in time_table.keys():
        sco = Subject.query.filter(Subject.stu_id == id).filter(Subject.school_year == year).filter(
            Subject.school_term == term).filter(Subject.day == day).all()
        for s in sco:
            time = re.findall(r"\d+\.?\d*", s.time)
            time_table[day][int(time[0])-1].append(s)
            for i in range(int(time[0])-1, int(time[1])):
                time_table[day][i-1].append(0)
    return time_table
