# encoding: utf-8
import os
import shutil
import sys
import time

import requests
from pyecharts import Line

reload(sys)
sys.setdefaultencoding('utf-8')


def chart(credit_list, time_list):
    bar = Line("学生成绩平均绩点折线图\n")
    bar.add("平均绩点GPA", time_list, credit_list, is_more_utils=True)
    bar.show_config()
    bar.render()
    shutil.move(os.path.abspath('render.html'), os.path.abspath('templates/student.html'))

    file = ""
    with open(os.path.abspath('templates/student.html'), 'r') as f:
        hello = f.read()
        file = hello
        f.close()

    head = '''
    {% extends 'base.html' %}
    {% block page_name %}你好,{{login_user}}{% endblock %}
    {% block body_part3 %}
    <a href="{{ url_for('student') }}" class="nav-link active">
    {% endblock %}
    {% block body_part1 %}
    <span class="glyphicon glyphicon-stats"></span>&ensp;你好,{{login_user}}
    {% endblock %}
    {% block body_part2 %}
    '''
    with open(os.path.abspath('templates/student.html'), 'w') as f1:
        f1.write(head)
        f1.write(file)
        f1.write('\n')
        f1.write("{% endblock %}")
