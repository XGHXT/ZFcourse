#coding:utf8
'''
 数据库迁移的文件
 flask-script让我们可以使用命令行去完成数据库迁移的操作
 输入python manage.py db init来初始化，这一步主要是建立数据库迁移相关的文件和文件夹，只是在第一次需要使用
 接着依次使用python manage.py db migrate和python manage.py db upgrade
'''
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from view import app, db
from models import Student, Subject, Score

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
