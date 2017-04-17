#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask,session,g
from exts import db
import config
import constants
from models.front_models import FrontUser
from views.cms_views import cms_views
from views.front_views import account_views,post_views
from flask_wtf import CsrfProtect
from datetime import datetime

app = Flask(__name__)
app.config.from_object(config)
CsrfProtect(app)
db.init_app(app)
# email.init_app(app)

app.register_blueprint(cms_views.bp)
app.register_blueprint(account_views.bp)
app.register_blueprint(post_views.bp)


@app.before_request
def post_before_request():
    id = session.get(constants.FRONTUSER_SESSION_ID)
    if id:
        front_user = FrontUser.query.get(id)
        g.front_user = front_user

@app.context_processor
def post_context_processor():
    if hasattr(g,'front_user'):
        return {'front_user':g.front_user}
    return {}

# 自定义过滤器
@app.template_filter('passtime')
def show_passtime(time):
    if not isinstance(time,datetime):
        return
    if (datetime.now() - time).total_seconds() < 10 * 60:
        return u'刚刚发布'
    elif (datetime.now() - time).total_seconds() < 60 * 60:
        return u'1个小时前发布'
    elif (datetime.now() - time).total_seconds() < 24 * 60 * 60:
        return u'1天前发布'
    elif (datetime.now() - time).total_seconds() < 7 * 24 * 60 * 60:
        return u'1周前发布'
    elif (datetime.now() - time).total_seconds() < 30 * 24 * 60 * 60:
        return u'1个月前发布'




if __name__ == '__main__':
    app.run()
