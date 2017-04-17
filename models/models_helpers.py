# -*- coding:utf-8 -*-

from common_models import PostModel,HighlightPostModel,StarPostModel,CommentModel,BoardModel
from exts import db
import constants

class PostModelHelper(object):
        CREATE_TIME = 1
        HIGHLIGH_TIME = 2
        COMMENT_COUNT = 3
        STAR_COUNT = 4

        @classmethod
        def post_list(cls,page,sort_type,board_id,):
            # sort_type：1 - 代表是按时间排序
            # sort_type：2 - 代表是按加精排序
            # sort_type：3 - 代表是按评论量排序
            # sort_type：4 - 代表是按点赞量排序

            if sort_type == cls.CREATE_TIME:
                posts = PostModel.query.order_by(PostModel.create_time.desc())
            elif sort_type == cls.HIGHLIGH_TIME:
                posts = db.session.query(PostModel).outerjoin(HighlightPostModel).order_by(HighlightPostModel.create_time.desc(),PostModel.create_time.desc())
            elif sort_type == cls.COMMENT_COUNT:
                posts = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(db.func.count(CommentModel.id).desc(),PostModel.create_time.desc())
            elif sort_type== cls.STAR_COUNT:
                posts = db.session.query(PostModel).outerjoin(StarPostModel).group_by(PostModel.id).order_by(db.func.count(StarPostModel.id).desc(),PostModel.create_time.desc())

            #过滤板块
            if board_id:
                posts = posts.filter(PostModel.board_id == board_id)

            #过滤被删除的帖子
            posts = posts.filter(PostModel.is_removed==False)

            total_post_count = posts.count()
            total_page = total_post_count / constants.PAGE_NUM
            if total_post_count % constants.PAGE_NUM > 0:
                total_page += 1
            page_int = divmod(page,5)[0] if divmod(page,5)[1] !=0 else divmod(page,5)[0] - 1
            pages = [i+1 for i in range(page_int*5,(page_int+1)*5) if i < total_page]
            start = (page-1) * constants.PAGE_NUM
            end = start + constants.PAGE_NUM

            context = {
                'posts': posts.slice(start,end),
                'boards': BoardModel.query.all(),
                'pages': pages,
                'c_page': page,
                't_page': total_page,
                'c_sort': sort_type,
                'c_board': board_id,
            }

            return context

