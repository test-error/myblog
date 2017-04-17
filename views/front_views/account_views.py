# -*- coding:utf-8 -*-

from flask import Blueprint,request,session,g,render_template,views,make_response,redirect,url_for
import top.api
import constants
from utils import bzcache
from utils import bzjson
from utils.captcha.xtcaptcha import Captcha
from models.front_models import FrontUser
from forms.frontforms import FrontRegistForm,FrontLoginForm,FrontUserSettingsForm
from exts import db
from StringIO import StringIO
from datetime import datetime

bp = Blueprint('account',__name__,url_prefix='/account')

@bp.route('/')
def index():
    return 'this is index page'


class RegistView(views.MethodView):

    def get(self,message=None):
        return render_template('front/front_regist.html',message=message)

    def post(self):
        form = FrontRegistForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password.data
            frontuser = FrontUser(telephone=telephone,username=username,password=password)
            db.session.add(frontuser)
            db.session.commit()
            return 'ok'
        else:
            return self.get(form.get_error())

bp.add_url_rule('/regist/',view_func=RegistView.as_view('regist'))

class LoginView(views.MethodView):

    def get(self,message=None):
        return render_template('front/front_login.html',message=message)

    def post(self):
        form = FrontLoginForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            front_user = FrontUser.query.filter_by(telephone=telephone).first()
            if front_user and front_user.check_password(password):
                front_user.last_login_time = datetime.now()
                if not front_user.last_login_time or front_user.last_login_time.day < datetime.now().day:
                    front_user.points += constants.DAYUPPOINT
                db.session.commit()
                session[constants.FRONTUSER_SESSION_ID] = front_user.id
                if remember:
                    session.permanent = True
                return redirect(url_for('post.index'))
            else:
                return self.get(message=u'手机号码或密码错误')
        else:
            return self.get(message=form.get_error())

bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))

@bp.route('/logout/')
def logout():
    session.pop(constants.FRONTUSER_SESSION_ID)
    return redirect(url_for('account.login'))

@bp.route('/settings/',methods=['POST','GET'])
def settings():
    if request.method == 'GET':
        return render_template('front/front_settings.html')
    else:
        form = FrontUserSettingsForm(request.form)
        if form.validate():
            username = form.username.data
            realname = form.realname.data
            qq = form.qq.data
            avatar = form.avatar.data
            signature = form.signature.data
            user_model = g.front_user
            user_model.realname = realname if realname else ''
            user_model.qq = qq if qq else ''
            user_model.avatar = avatar if avatar else ''
            user_model.signature = signature if signature else ''
            db.session.commit()
            return bzjson.json_result()
        else:
            return bzjson.json_param_error(message=form.get_error())


@bp.route('/graph_captcha/')
def graph_captcha():
    text,img = Captcha.gene_code();
    out = StringIO()
    img.save(out,'png')
    out.seek(0)
    response = make_response(out.read())
    response.content_type = 'img/png'
    bzcache.set(text.lower(),text.lower())
    return response

@bp.route('/sms_captcha/')
def sms_captcha():
    telephone = request.args.get('telephone')
    if not telephone:
        return bzjson.json_param_error(message=u'没有输入手机号码')

    if bzcache.get(telephone):
        return bzjson.json_param_error(message=u'验证码已经发送')

    app_key = constants.ALIDAYU_APP_KEY
    app_secret = constants.ALIDAYU_APP_SECRET
    req = top.setDefaultAppInfo(app_key,app_secret)
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.extend = ""
    req.sms_type = 'normal'
    req.sms_free_sign_name = constants.ALIDAYU_SIGN_NAME
    captcha = Captcha.gene_text()
    req.sms_param = "{captcha:%s}" % captcha
    req.rec_num = telephone.decode('utf-8').encode('ascii')
    req.sms_template_code = constants.ALIDAYU_TEMPLATE_CODE
    try:
        resp = req.getResponse()
        bzcache.set(telephone,captcha)
        return bzjson.json_result()
    except Exception, e:
        print e
        return bzjson.json_servererror_error()

