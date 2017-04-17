/**
 * Created by Administrator on 2017/4/7.
 */


$(function(){
    bzqiniu.setUp({
        'browse_btn': 'avatar-img',
        'success': function(up,file,info){
            var imgTag = $('#avatar-img');
            imgTag.attr('src',file.name);
        }
    });
});

$(function(){
    $('#submit-btn').click(function(event){
        event.preventDefault();

        var username = $('input[name=username]').val();
        var realname = $('input[name=realname]').val();
        var qq = $('input[name=qq]').val();
        var avatar = $('#avatar-img').attr('src');
        var signature = $('#signature-area').val();

        bzajax.post({
            'url': '/account/settings/',
            'data': {
                'username': username,
                'realname': realname,
                'qq': qq,
                'avatar': avatar,
                'signature': signature,
            },
            'success': function(data){
                if(data['code'] == 200){
                    xtalert.alertSuccessToast('修改成功！');
                }else {
                    xtalert.alertInfoToast(data['message']);
                }
            }
        });

    });
})