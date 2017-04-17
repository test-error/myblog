/**
 * Created by Administrator on 2017/4/6.
 */


$(function(){
    $('#submit-btn').click(function(event){
        event.preventDefault();

        var content = window.editor.$txt.html();
        var post_id = $(this).attr('data-post-id');
        var comment_id = $('.origin-comment-group').attr('data-comment-id');

        bzajax.post({
            'url': '/add_comment/',
            'data': {
                'post_id': post_id,
                'content': content,
                'comment_id': comment_id,
            },
            'success': function(data){
                if(data['code'] == 200){
                    xtalert.alertSuccessToast('评论添加成功！');
                    setTimeout(function(){
                        window.location = '/post_detail/'+post_id+'/';
                    },800)
                }else {
                    xtalert.alertInfoToast(data['message']);
                }
            }
        });
    });
});