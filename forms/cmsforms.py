# -*- coding: utf-8 -*-

from baseforms import BaseForm
from wtforms import StringField,BooleanField,IntegerField
from wtforms.validators import InputRequired,Length,Email,EqualTo,ValidationError
from utils import bzcache
from models.common_models import BoardModel

class CMSLoginForm(BaseForm):
    email = StringField(validators=[InputRequired(message=u'必须输入邮箱名'),Email(message=u'邮箱格式不正确')])
    password = StringField(validators=[InputRequired(u'没有输入密码'),Length(6,20,message=u'密码长度必须在6-20位')])
    remember = BooleanField()

class CMSResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[InputRequired(message=u'必须输入密码'),Length(6,20,message=u'密码长度必须在6-20位')])
    newpwd = StringField(validators=[InputRequired(message=u'必须输入密码'),Length(6,20,message=u'密码长度必须在6-20位')])
    newpwd_repeat = StringField(validators=[EqualTo('newpwd',message=u'两次输入密码必须一致')])

class CMSResetmailForm(BaseForm):
    email = StringField(validators=[InputRequired(message=u'必须输入邮箱名'),Email(message=u'邮箱格式不正确')])
    captcha = StringField(validators=[InputRequired(message=u'没有输入验证码')])

    def validate_captcha(self,field):
        email = self.email.data
        captcha = field.data
        captcha_cache = bzcache.get(email)
        if not captcha_cache or captcha_cache.lower() != captcha:
            raise ValidationError(message=u'验证码错误')
        return True

class CMSAdduserForm(BaseForm):
    email = StringField(validators=[InputRequired(message=u'必须输入邮箱'),Email(message=u'邮箱格式不正确')])
    username = StringField(validators=[InputRequired(message=u'必须输入用户名')])
    password = StringField(validators=[InputRequired(message=u'必须输入密码'),Length(6,20,message=u'密码长度必须在6-20位')])


class CMSBlackListForm(BaseForm):
    user_id = IntegerField(validators=[InputRequired(message=u'必须传入id！')])
    is_active = IntegerField(validators=[InputRequired(message=u'必须指定是否加入黑名单！')])

class CMSEditFrontUserForm(BaseForm):
    user_id = StringField(validators=[InputRequired(message=u'需要传入id')])
    is_active = IntegerField(validators=[InputRequired(message=u'没有指定是否加入黑名单')])

class CMSEditBoard(BaseForm):
    id = IntegerField(validators=[InputRequired(message=u'没有输入板块id')])
    name = StringField(validators=[InputRequired(message=u'没有输入板块名称')])

    def validate_id(self,field):
        id = field.data
        board = BoardModel.query.get(id)
        if not board:
            raise ValidationError(message=u'该板块id不存在')
        return True

    def validate_name(self, field):
        name = field.data
        board = BoardModel.query.filter_by(name = name).first()
        if board:
            raise ValidationError(message=u'该板块名称已存在!')
        return True

class CMSHighlightPostForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(message=u'没有传入帖子id')])
    is_hightlight = BooleanField(validators=[InputRequired(message=u'没有操作行为')])
