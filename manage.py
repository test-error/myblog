# -*- coding: utf-8 -*-

from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from models import cms_models
from exts import db
from sbbs import app
from models.cms_models import CMSUser,CMSRole
from models.front_models import FrontUser
from models.common_models import BoardModel,PostModel,HighlightPostModel


migrate = Migrate(app,db)
manager = Manager(app)

manager.add_command('db',MigrateCommand)

@manager.option('-e','--email',dest='email')
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
def create_cms_user(email,username,password):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        return u'该用户已存在'
    else:
        user = CMSUser(email=email,username=username,password=password)
        db.session.add(user)
        db.session.commit()
        print u'用户添加成功'

@manager.option('-n','--name',dest='name')
@manager.option('-d','--desc',dest='desc')
@manager.option('-p','--permissions',dest='permissions')
def create_cms_role(name,desc,permissions):
    role = CMSRole(name=name.decode('gbk').encode('utf-8'),desc=desc.decode('gbk').encode('utf-8'),permissions=permissions)
    db.session.add(role)
    db.session.commit()
    print u'角色添加成功'

@manager.option('-t','--telephone',dest='telephone')
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
def create_frontuser(telephone,username,password):
    front_user = FrontUser(telephone=telephone,username=username,password=password)
    db.session.add(front_user)
    db.session.commit()
    print u'前台用户已添加'


if __name__ == '__main__':
    manager.run()
