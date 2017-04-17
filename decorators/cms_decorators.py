# -*- coding:utf-8 -*-

from flask import session,redirect,url_for
from functools import wraps
import constants
from flask import g,abort,request
from utils import bzjson
from models.cms_models import CMSPermission

def login_required(func):

    @wraps(func)
    def wrapper(*args,**kwargs):
        id = session.get(constants.CMS_SESSION_ID)
        if id:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('cms.login'))

    return wrapper

def permission_required(permission):

    def check_permission(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            if g.cms_user.has_permissions(permission):
                return func(*args,**kwargs);
            else:
                if request.is_xhr:
                    return bzjson.json_unauth_error(message=u'用户没有权限！')
                else:
                    abort(401)
        return wrapper
    return check_permission

def superadin_required(func):
    return permission_required(CMSPermission.ADMINISTRATOR)(func)




