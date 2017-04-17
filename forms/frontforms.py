# -*- coding:utf-8 -*-

from wtforms import StringField,IntegerField,BooleanField,ValidationError
from wtforms.validators import InputRequired,Email,EqualTo,Length,URL
from baseforms import BaseForm
from utils import bzcache

class GraphCaptchaForm(BaseForm):
    graph_captcha = StringField(validators=[InputRequired(message=u'请输入验证码')])

    def validate_graph_captcha(self,field):
        graph_captcha = field.data
        captcha_cache = bzcache.get(graph_captcha.lower())
        if not captcha_cache or captcha_cache.lower() != graph_captcha.lower():
            raise ValidationError(message=u'验证码错误')


class FrontRegistForm(BaseForm):
    telephone = StringField(validators=[InputRequired(message='请输入手机号码！'),Length(11,11,message=u'手机格式不正确')])
    sms_captcha = StringField(validators=[InputRequired(message=u'请输入短信验证码')])
    username = StringField(validators=[InputRequired(message=u'请输入用户名')])
    password = StringField(validators=[InputRequired(message=u'请输入密码'),Length(6,20,message=u'密码长度6位到20位')])
    password_repeat = StringField(validators=[EqualTo('password')])
    graph_captcha = StringField(validators=[InputRequired(message=u'请输入验证码')])

    def validate_sms_captcha(self,field):
        sms_captcha = field.data
        telephone = self.telephone.data
        captcha_cache = bzcache.get(telephone)
        if not captcha_cache or sms_captcha.lower() != captcha_cache.lower():
            raise ValidationError(message=u'短信验证码错误')

    def validate_graph_captcha(self,field):
        graph_captcha = field.data
        captcha_cache = bzcache.get(graph_captcha.lower())
        if not captcha_cache or captcha_cache.lower() != graph_captcha.lower():
            raise ValidationError(message=u'验证码错误')

class FrontLoginForm(GraphCaptchaForm):
    telephone = StringField(InputRequired(message=u'请输入手机号码'))
    password = StringField(InputRequired(message=u'请输入密码'))
    remember = IntegerField()

class AddPostForm(GraphCaptchaForm):
    title = StringField(InputRequired(message=u'请输入标题'))
    board_id = IntegerField(InputRequired(message=u'请选择板块'))
    content = StringField(InputRequired(message=u'请输入帖子内容'))

class AddCommentForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(message=u'请输入帖子id')])
    comment_id = IntegerField()
    content = StringField(validators=[InputRequired(message=u'请输入帖子内容')])

class AddStarPostForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(message=u'请输入帖子id')])
    is_addstar = BooleanField(validators=[InputRequired(message=u'要有点赞行为')])

class FrontUserSettingsForm(BaseForm):
    username = StringField(validators=[InputRequired(message=u'请输入用户名')])
    realname = StringField()
    qq = StringField()
    avatar = StringField(validators=[URL(message=u'头像url格式不正确')])
    signature = StringField()



