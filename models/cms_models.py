# -*- coding: utf-8 -*-

from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class CMSPermission:
        ADMINISTRATOR = 255
        OPERATOR = 1
        PERMISSION_MAP = {
            ADMINISTRATOR: (u'超级管理员',u'拥有最高权限'),
            OPERATOR: (u'普通管理员',u'操作前台帖子权限')
        }

cms_user_role = db.Table('cms_user_role',
    db.Column('role_id',db.Integer,db.ForeignKey('cms_role.id'),primary_key=True),
    db.Column('user_id',db.Integer,db.ForeignKey('cms_user.id'),primary_key=True)
)

class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    desc = db.Column(db.String(100),nullable=True)
    create_time = db.Column(db.DateTime,default=datetime.now)
    permissions = db.Column(db.Integer,default=CMSPermission.OPERATOR,nullable=False)


class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    join_time = db.Column(db.DateTime,default=datetime.now)
    is_active = db.Column(db.Boolean,default=True)
    last_login_time = db.Column(db.DateTime,nullable=True)
    roles = db.relationship('CMSRole',secondary=cms_user_role,backref='users')

    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email


    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw_pwd):
        self._password = generate_password_hash(raw_pwd)

    def check_password(self,raw_pwd):
        return check_password_hash(self._password,raw_pwd)

    @property
    def is_administartor(self):
        return self.has_permissions(CMSPermission.ADMINISTRATOR)

    def has_permissions(self,permission):
        if not self.roles:
            return False
        all_pemissions = 0
        for role in self.roles:
            all_pemissions |= role.permissions
        return all_pemissions & permission == permission

    @property
    def permissions(self):
        if not self.roles:
            return None

        all_permissions = 0
        for role in self.roles:
            all_permissions |= role.permissions

        permission_dicts = []
        for permission,permission_info in CMSPermission.PERMISSION_MAP.items():
            if permission & all_permissions == permission:
                permission_dicts.append({permission:permission_info})

        return permission_dicts
