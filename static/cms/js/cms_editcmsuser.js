/**
 * Created by Administrator on 2017/3/22.
 */


$(function(){
    $('#edit').click(function(event){
        event.preventDefault();

        var checkboxInput = $(':checkbox:checked');
        var roles = [];

        checkboxInput.each(function(){
            var role_id = $(this).val();
            roles.push(role_id);
        });
        var user_id = $(this).attr("data-user-id");

        bzajax.post({
            'url': '/edit_cmsuser/',
            'data': {
                'user_id': user_id,
                'roles': roles,
            },
            'success': function(data){
                if(data['code'] == 200){
                    xtalert.alertSuccessToast('修改成功！')
                }else{
                    xtalert.alertInfo(data['message'])
                }
            }
        });
    });
});

$(function(){
    $('#black').click(function(event){
        event.preventDefault();

        var user_id = $(this).attr("data-user_id");
        var is_active = parseInt($(this).attr("data-active"));
        //is_active传入"1"加入黑名单
        //is_active传入"0"移出黑名单

        bzajax.post({
            'url': '/change_active/',
            'data': {
                'user_id': user_id,
                'is_active': is_active,
            },
            'success': function(data){
                if(data['code'] == 200){
                    if(is_active == 1){
                        xtalert.alertSuccessToast('用户加入黑名单');
                    }else{
                        xtalert.alertSuccessToast('用户移出黑名单');
                    }
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