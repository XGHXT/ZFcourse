# -*- coding: UTF-8 -*-
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(use_native_unicode='utf8')



class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.BIGINT, primary_key=True) # 学号
    name = db.Column(db.String(20))             # 姓名
    sex = db.Column(db.String(10))              # 性别
    birthday = db.Column(db.String(20))         # 生日
    grade = db.Column(db.String(20))            # 年级
    collage = db.Column(db.String(20))          # 学院名称
    major = db.Column(db.String(20))            # 专业名称
    class_ = db.Column(db.String(20))           # 班级名称

    def __init__(self, id, name, sex, birthday, grade, collage, major, class_):
        self.id = id
        self.name = name
        self.sex = sex
        self.birthday = birthday
        self.grade = grade
        self.collage = collage
        self.major = major
        self.class_ = class_


class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.BIGINT, primary_key=True)
    school_year = db.Column(db.String(20))      # 学年
    school_term = db.Column(db.Integer)         # 学期
    class_name = db.Column(db.String(50))      # 课程名称
    class_code = db.Column(db.String(30))       # 课程代码kch_id
    credit = db.Column(db.Float)                # 学分
    class_category = db.Column(db.String(20))   # 课程性质
    test_category = db.Column(db.String(20))    # 考试性质
    cjsfzf = db.Column(db.String(10))           # 成绩是否作废
    score = db.Column(db.Float)                 # 成绩
    GPA = db.Column(db.Float)                   # 绩点
    class_mark = db.Column(db.String(10))       # 课程标记kcbj
    class_ownership = db.Column(db.String(100)) # 开课部门
    stu_id = db.Column(db.BIGINT)               # 学生学号

    def __init__(self, school_year, school_term, class_name, class_code, credit, class_category, test_category, cjsfzf,
                score, GPA, class_mark, class_ownership, stu_id):
        self.school_year = school_year
        self.school_term = school_term
        self.class_name = class_name
        self.class_code = class_code
        self.credit = credit
        self.class_category = class_category
        self.test_category = test_category
        self.cjsfzf = cjsfzf
        self.score = score
        self.GPA = GPA
        self.class_mark = class_mark
        self.class_ownership = class_ownership
        self.stu_id = stu_id


class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.BIGINT, primary_key=True)
    school_year = db.Column(db.String(20))      # 学年
    school_term = db.Column(db.Integer)         # 学期
    class_name = db.Column(db.String(100))      # 课程名称
    day = db.Column(db.String(10))              # 星期
    time = db.Column(db.String(10))             # 上课时间
    week = db.Column(db.String(20))             # 上课周
    classroom = db.Column(db.String(30))        # 上课地点
    teacher = db.Column(db.String(20))          # 任课老师
    department = db.Column(db.String(20))       # 本部
    stu_id = db.Column(db.BIGINT)               # 学生学号
    length = db.Column(db.INT)
    def __init__(self, school_year, school_term, class_name, day, time, week, classroom, teacher, department, stu_id, length):
        self.school_year = school_year
        self.school_term = school_term
        self.class_name = class_name
        self.day = day
        self.time = time
        self.week = week
        self.classroom = classroom
        self.teacher = teacher
        self.department = department
        self.stu_id = stu_id
        self.length = length


#db.drop_all()
#db.create_all()