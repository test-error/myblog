/**
 * Created by Administrator on 2017/4/6.
 */


$(function(){
    $('#star-btn').click(function(event){
        event.preventDefault();

        var post_id = $(this).attr('data-post-id');
        var is_addstar = parseInt($(this).attr('is-addstar'));

        bzajax.post({
            'url': '/add_star/',
            'data': {
                'post_id': post_id,
                'is_addstar': !is_addstar,
            },
            'success': function(data){
                if(data['code'] == 200){
                    if(!is_addstar){
                        xtalert.alertSuccessToast('点赞成功！');
                        setTimeout(function(){
                            window.location.reload();
                        },800);
                    }else {
                        xtalert.alertSuccessToast('取消点赞！');
                        setTimeout(function(){
                            window.location.reload();
                        },800);
                    }
                }else {
                    xtalert.alertInfoToast(data['message']);
                }
            }
        });
    });
});