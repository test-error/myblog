/**
 * Created by Administrator on 2017/4/5.
 */


$(function(){
    $('.hightlight-btn').click(function(event){
        event.preventDefault();
        var post_id = $(this).attr('data-post-id');
        var is_hightlight = parseInt($(this).attr('data-is-highlight'));

        bzajax.post({
            'url': '/highlight/',
            'data': {
                'post_id': post_id,
                'is_hightlight': !is_hightlight,
            },
            'success': function(data){
                if(data['code'] == 200){
                    if(is_hightlight){
                        xtalert.alertSuccessToast('精华取消成功！');
                    }else {
                        xtalert.alertSuccessToast('精华添加成功！');
                    }
                    setTimeout(function(){
                        window.location.reload();
                    },800);
                }else {
                    xtalert.alertInfoToast(data['message']);
                }
            }
        });
    });
});

$(function(){
    $('.remove-btn').click(function(event){
        event.preventDefault();

        var post_id = $(this).attr('data-post-id');
        console.log('-----------');
        bzajax.post({
            'url': '/remove_post/',
            'data': {
                'post_id': post_id,
            },
            'success': function(data){
                if(data['code'] ==200){
                    xtalert.alertSuccessToast('文章删除成功！');
                    setTimeout(function(){
                        window.location.reload();
                    },500);
                }else{
                    xtalert.alertInfoToast(data['message']);
                }
            }
        });
    });
});

$(function(){
    $('#top-select').change(function(event){
        event.preventDefault();

        var value = $(this).val();
        var newHref = xtparam.setParam(window.location.href,'sort',value);
        window.location = newHref;
    });
});

$(function(){
    $('#board-filter-select').change(function(event){
        event.preventDefault();
        var value = $(this).val();
        var newHref = xtparam.setParam(window.location.href,'board_id',value);
        window.location = newHref;
    });
});