/**
 * Created by Administrator on 2017/3/27.
 */

$(function(){
    $('#back-list-btn').click(function(event){
        event.preventDefault();

        var user_id = $(this).attr('data-user-id');
        var is_active = $(this).attr('data-is-active');

        bzajax.post({
            'url': '/front_black_list/',
            'data': {
                'user_id': user_id,
                'is_active': is_active,
            },
            'success': function(data){
                if(data['code'] == 200){
                    if(is_active == '1'){
                        xtalert.alertSuccessToast('用户加入黑名单!');
                    }else {
                        xtalert.alertSuccessToast('用户移出黑名单!');
                    }
                    setTimeout(function(){
                        window.location.reload();
                    },800)
                }
            }
        });
    });
});