# -*- coding:utf-8 -*-

from flask import Blueprint,request,session,render_template,redirect,url_for,g,jsonify
from exts import db
from utils import bzjson
import constants
from qiniu import Auth
from decorators.front_decorators import login_required
from models.common_models import BoardModel,PostModel,CommentModel,StarPostModel,HighlightPostModel
from models.front_models import FrontUser
from forms.frontforms import AddPostForm,AddCommentForm,AddStarPostForm
from models.models_helpers import PostModelHelper
from datetime import datetime


bp = Blueprint('post',__name__)

@bp.route('/')
def index():
   return post_list(1,1,0)

@bp.route('/list/<int:page>/<int:sort_type>/<int:board_id>')
def post_list(page,sort_type,board_id):
    context = PostModelHelper.post_list(page,sort_type,board_id)
    return render_template('front/front_index.html',**context)

@bp.route('/add_comment/',methods=['POST','GET'])
def add_comment():
    if request.method == 'GET':
        post_id = request.args.get('post_id', type=int)
        comment_id = request.args.get('comment_id', type=int)
        post=PostModel.query.get(post_id)
        context = {
            'post': post
        }
        if comment_id:
            context['origin_comment'] = CommentModel.query.get(comment_id)
        return render_template('front/front_addcomment.html',**context)
    else:
        form = AddCommentForm(request.form)
        if form.validate():
            post_id = form.post_id.data
            comment_id = form.comment_id.data
            content = form.content.data

            comment_model = CommentModel(content=content)

            post_model = PostModel.query.get(post_id)
            comment_model.author = g.front_user
            comment_model.post = post_model
            # comment_model.create_time = datetime.now()
            if comment_id:
                origin_comment = CommentModel.query.get(comment_id)
                comment_model.origin_comment= origin_comment
            db.session.add(comment_model)
            db.session.commit()
            return bzjson.json_result()
        else:
            return bzjson.json_param_error(message=form.get_error())

@bp.route('/add_star/',methods=['POST'])
def add_star():
    form = AddStarPostForm(request.form)
    if form.validate():
        post_id = form.post_id.data
        is_addstar = form.is_addstar.data
        post_model = PostModel.query.get(post_id)
        star_model = StarPostModel.query.filter_by(author_id=g.front_user.id,post_id=post_id).first()
        # 添加点赞需要判断文章是否已经点赞
        if is_addstar:
            if star_model:
                return bzjson.json_param_error(message=u'该文章已经点赞！')
            star_model = StarPostModel()
            star_model.post = post_model
            star_model.author = g.front_user
            db.session.add(star_model)
            db.session.commit()
            return bzjson.json_result()
        # 取消点赞
        else:
            if star_model:
                db.session.delete(star_model)
                db.session.commit()
                return bzjson.json_result()
            else:
                return bzjson.json_param_error(message=u'该文章未点赞')
    return bzjson.json_param_error(message=form.get_error())


@bp.route('/post_detail/<int:post_id>/')
def post_detail(post_id):
    post_model = PostModel.query.get(post_id)
    post_model.read_count +=1
    db.session.commit()
    star_authors = [star.author.id for star in post_model.stars]
    context = {
        'post': post_model,
        'star_authors':star_authors,
    }
    return render_template('front/front_postdetail.html',**context)

@bp.route('/add_post/',methods=['POST','GET'])
def add_post():
    if request.method == 'GET':
        boards = BoardModel.query.all();
        return render_template('front/front_addpost.html',boards=boards)
    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            board_id = form.board_id.data
            content = form.content.data
            post_model = PostModel(title=title,content=content)
            board_model = BoardModel.query.filter_by(id=board_id).first()
            if not board_model:
                return bzjson.json_param_error(message=u'没有该板块')
            post_model.board = board_model
            post_model.author = g.front_user
            db.session.add(post_model)
            db.session.commit()
            return bzjson.json_result()
        else:
            return bzjson.json_param_error(message=form.get_error())

@bp.route('/qiniu_token/')
def qiniu_token():
    q = Auth(constants.access_key,constants.secret_key)
    bucket_name = 'test'
    token = q.upload_token(bucket_name)
    return jsonify({'uptoken': token})

@bp.errorhandler(401)
def post_auth_forbidden(error):
    if request.is_xhr:
        return bzjson.json_unauth_error()
    else:
        return redirect(url_for('account.login'))



@bp.route('/test/')
def test():
    author = FrontUser.query.first()
    board = BoardModel.query.first()
    for x in xrange(0,100):
        title = '帖子标题：%s' % x
        content = '帖子内容：%s' % x
        post_model = PostModel(title=title,content=content)
        post_model.author = author
        post_model.board = board
        db.session.add(post_model)
    db.session.commit()
    return 'success'
