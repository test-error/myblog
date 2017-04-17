# -*- coding: utf-8 -*-

import random
import string

from flask import Blueprint,session, redirect,url_for,g,abort
from flask import render_template,request
from flask.views import  MethodView

import constants
from decorators.cms_decorators import login_required,superadin_required
from exts import db
from forms.cmsforms import CMSLoginForm,CMSResetpwdForm,CMSResetmailForm,CMSAdduserForm,CMSBlackListForm, \
    CMSEditFrontUserForm,CMSEditBoard,CMSHighlightPostForm
from models.cms_models import CMSUser,CMSRole
from models.common_models import BoardModel,PostModel,HighlightPostModel
from models.front_models import FrontUser
from tasks import sendmail
from utils import bzjson,bzcache

# bp = Blueprint('cms',__name__,url_prefix='/cms/')
bp = Blueprint('cms',__name__,subdomain='cms')


@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')

class CMSLoginView(MethodView):

    def get(self,message=None):
        return render_template('cms/login.html',message=message)

    def post(self):
        form = CMSLoginForm(request.form)

        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[constants.CMS_SESSION_ID] = user.id
                if remember:
                    session.permanent = True
                else:
                    session.permanent = False
                return redirect(url_for('cms.index'))
            else:
                return self.get(message=u'密码或邮箱错误')
        else:
            return self.get(message=form.get_error())

bp.add_url_rule('/login/',view_func=CMSLoginView.as_view('login'))

@bp.route('/logout')
@login_required
def logout():
    session.pop(constants.CMS_SESSION_ID)
    return redirect(url_for('cms.login'))

@bp.context_processor
def cms_context_processor():
    id = session.get(constants.CMS_SESSION_ID)
    if id:
        user = CMSUser.query.get(id)
        return {'cms_user': user}
    else:
        return {}

@bp.before_request
def cms_before_request():
    id = session.get(constants.CMS_SESSION_ID)
    if id:
        user = CMSUser.query.get(id)
        g.cms_user = user


@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_user_profile.html')

@bp.route('/resetpwd/', methods=['GET','POST'])
@login_required
def resetpwd():
    if request.method == 'GET':
        return render_template('cms/cms_resetpwd.html')
    else:
        form = CMSResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            if g.cms_user.check_password(oldpwd):
                g.cms_user.password = newpwd
                db.session.commit()
                return bzjson.json_result()
            else:
                return bzjson.json_param_error(message=u'密码错误')
        else:
            return bzjson.json_param_error(message=form.get_error())

@bp.route('/captcha/')
@login_required
def captcha():
    email = request.args.get('email')
    if bzcache.get(email):
        return bzjson.json_param_error(message=u'改邮箱已经发送过验证码！')

    source = list(string.letters)
    for x in xrange(0,10):
        source.append(str(x))

    captcha_list = random.sample(source,4)
    captcha = ''.join(captcha_list)
    print '------',captcha
    # bzcache.set(email,captcha)
    # return bzjson.json_result()
    # if bzemail.send_mail(subject=u'测试验证码',receivers=email,body=u'验证码是:'+captcha):
    sendmail.delay(subject=u'测试验证码',receivers=email,body=u'验证码是:'+captcha)
    bzcache.set(email,captcha)
    return bzjson.json_result()
    # else:
    #     return bzjson.json_param_error(message=u'验证码发送错误！')



@bp.route('/resetmail/',methods=['GET','POST'])
@login_required
def resetmail():
    if request.method == 'GET':
        return render_template('cms/cms_resetmail.html')
    else:
        form = CMSResetmailForm(request.form)
        if form.validate():
            email = form.email.data
            # captcha = form.captcha.data
            if g.cms_user.email == email:
                return bzjson.json_param_error(message=u'新邮箱与老邮箱一致，无需修改')
            g.cms_user.email = email
            db.session.commit()
            return bzjson.json_result()
        else:
            return bzjson.json_param_error(message=form.get_error())

@bp.route('/cmsusers/')
@login_required
def cmsusers():
    users = CMSUser.query.all()
    context= {
        'users': users
    }
    return render_template('cms/cms_cmsusers.html',**context)

@bp.route('/add_cmsuser/',methods=['GET','POST'])
@login_required
def add_cmsuser():
    if request.method == 'GET':
        roles = CMSRole.query.all()
        return render_template('cms/cms_addcmsuser.html',roles=roles)
    else:
        form = CMSAdduserForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            roles = request.form.getlist('roles[]')
            if not roles:
                return bzjson.json_param_error(message=u'必须添加一个分组')
            user = CMSUser(email=email,username=username,password=password)
            for role_id in roles:
                role = CMSRole.query.get(role_id)
                role.users.append(user)
            db.session.commit()
            return bzjson.json_result()
        else:
            return bzjson.json_param_error(message=form.get_error())

@bp.route('/edit_cmsuser/',methods=['GET','POST'])
@login_required
@superadin_required
def edit_cmsuser():
    if request.method == 'GET':
        user_id = request.args.get('user_id')
        if not user_id:
            abort(404)
        user = CMSUser.query.get(user_id)
        roles = CMSRole.query.all()
        current_roles = [role.id for role in user.roles]
        context = {
            'user': user,
            'roles': roles,
            'current_roles': current_roles
        }
        return render_template('cms/cms_editcmsuser.html',**context)
    else:
        user_id = request.form.get('user_id')
        roles = request.form.getlist('roles[]')

        if not user_id:
            return bzjson.json_param_error(message=u'没有制定用户！')
        if not roles:
            return bzjson.json_param_error(message=u'没有指定用户分组！')

        user = CMSUser.query.get(user_id)
        user.roles[:] = []
        for role_id in roles:
            role_model = CMSRole.query.get(role_id)
            user.roles.append(role_model)
        db.session.commit()
        return bzjson.json_result()

@bp.route('/change_active/',methods=['POST'])
@login_required
def change_active():
    form = CMSBlackListForm(request.form)
    if form.validate():
        user_id = form.user_id.data
        is_active = form.is_active.data
        if g.cms_user.id == user_id:
            return bzjson.json_param_error(message=u'不能拉黑自己！')
        user = CMSUser.query.get(user_id)
        user.is_active = False if is_active ==1 else True
        db.session.commit()
        return bzjson.json_result()
    else:
        return bzjson.json_param_error(message=form.get_error())

@bp.route('/front_users/')
@login_required
def front_users():
    sort = request.args.get('sort')
    # 1:  按加入时间排序
    # 2： 按发表帖子数量排序
    # 3： 按评论数量排序
    if not sort or sort == '1':
        front_users = FrontUser.query.order_by(FrontUser.join_time.desc()).all()
    else:
        front_users = FrontUser.query.all()
    context = {
        'front_users': front_users,
        'current_sort': sort,
    }
    return render_template('cms/cms_frontusers.html',**context)

@bp.route('/edit_frontuser/')
@login_required
def edit_frontuser():
    user_id = request.args.get('id')
    if not user_id:
        abort(404)

    user = FrontUser.query.get(user_id)
    if not user:
        abort(404)

    return render_template('cms/cms_editfrontuser.html',current_user=user)

@bp.route('/front_black_list/',methods=["POST"])
@login_required
def front_black_list():
    form = CMSEditFrontUserForm(request.form)
    if form.validate():
        user_id = form.user_id.data
        is_actvie = form.is_active.data
        user = FrontUser.query.get(user_id)
        if not user:
            return bzjson.json_param_error(message=u'该用户不存在！')
        user.is_active = not is_actvie
        db.session.commit()
        return bzjson.json_result()
    else:
        return bzjson.json_param_error(message=form.get_error())

@bp.route('/cms_board/')
@login_required
def cms_board():
    boards = BoardModel.query.all()
    return render_template('cms/cms_boards.html',boards=boards)

@bp.route('/add_board/',methods=['POST'])
@login_required
def add_board():
    board_name = request.form.get('name')
    board = BoardModel(name=board_name)
    board.author = g.cms_user
    db.session.add(board)
    db.session.commit()
    return bzjson.json_result()

@bp.route('/edit_board/',methods=['POST'])
@login_required
def edit_board():
    form = CMSEditBoard(request.form)
    if form.validate():
        id = form.id.data
        name = form.name.data
        board = BoardModel.query.get(id)
        board.name = name
        db.session.commit()
        return bzjson.json_result()
    else:
        return bzjson.json_param_error(message=form.get_error())

@bp.route('/delete_board/',methods=['POST'])
@login_required
def delete_board():
    id = request.form.get('id')
    if not id:
        abort(404)
    board = BoardModel.query.get(id)
    db.session.delete(board)
    db.session.commit()
    return bzjson.json_result()

@bp.route('/posts/')
@login_required
def posts():
    sort_type = request.args.get('sort',1,type=int)
    board_id = request.args.get('board_id',0,type=int)
    page = request.args.get('page',1,type=int)
    # sort_type:1 -代表按时间排序
    #sort_type:2 -代表按加精排序
    #sort_type:3 -代表按评论量排序

    start = constants.PAGE_NUM * (page - 1)
    end = start + constants.PAGE_NUM
    posts = None
    if sort_type == 1:
        posts = PostModel.query.filter(PostModel.is_removed==False).order_by(PostModel.create_time.desc())
    elif sort_type == 2:
        # 多表查询
        # posts = db.session.query(PostModel,HighlightPostModel).filter(PostModel.is_removed==False).order_by(HighlightPostModel.create_time.desc()).all()
        posts = db.session.query(PostModel).outerjoin(HighlightPostModel).filter(PostModel.is_removed==False).order_by(HighlightPostModel.create_time.desc(),PostModel.create_time.desc())
    else:
        posts = PostModel.query.filter(PostModel.is_removed==False)

    if board_id != 0:
        posts = posts.filter(PostModel.board_id == board_id)

    total_posts_count = posts.count()
    total_page_count = total_posts_count / constants.PAGE_NUM
    if total_posts_count % constants.PAGE_NUM > 0:
        total_page_count += 1

    page_int = divmod(page,5)[0] if divmod(page,5)[1] != 0 else divmod(page,5)[0] - 1
    pages = [i+1 for i in range(page_int*5,(page_int+1)*5) if i < total_page_count]


    context = {
        'posts': posts.slice(start,end),
        'boards': BoardModel.query.all(),
        'c_sort': sort_type,
        'c_board': board_id,
        'c_page': page,
        't_page': total_page_count,
        'pages': pages
    }
    return render_template('cms/cms_posts.html', **context)

@bp.route('/highlight/', methods=['POST'])
def highlight():
    form = CMSHighlightPostForm(request.form)
    if form.validate():
        post_id = form.post_id.data
        is_hightlight = form.is_hightlight.data
        post_model = PostModel.query.get(post_id)
        if is_hightlight:
            if post_model.highlight:
                return bzjson.json_param_error(message=u'该帖子已经加精')
            highlight_model = HighlightPostModel()
            post_model.highlight = highlight_model
            db.session.add(highlight_model)
            db.session.commit()
            return bzjson.json_result()
        else:
            if not post_model.highlight:
                return bzjson.json_param_error(message=u'该帖子没有加精')
            db.session.delete(post_model.highlight)
            db.session.commit()
            return bzjson.json_result()
    else:
        return bzjson.json_param_error(message=form.get_error())

@bp.route('/remove_post/',methods=['POST'])
def remove_post():
    post_id = request.form.get('post_id')
    if not post_id:
        return bzjson.json_param_error(message=u'请输入帖子id')
    post_model = PostModel.query.get(post_id)
    post_model.is_removed = True
    db.session.commit()
    return bzjson.json_result()

@bp.errorhandler(404)
def cms_not_found(error):
    return render_template('cms/cms_404.html'),404

@bp.errorhandler(401)
def cms_unauth(err0r):
    return render_template('cms/cms_401.html'),401