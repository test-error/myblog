/**
 * Created by Administrator on 2017/3/20.
 */

$(function(){
    $('#get-captcha').click(function(event){
        event.preventDefault();

        var email = $('input[name=email]').val();

        bzajax.get({
            'url': '/captcha/',
            'data': {
                'email': email,
            },
            'success': function(data){
              if(data['code'] == 200){
                  xtalert.alertInfoToast('验证码发送成功!');
              }else{
                  xtalert.alertError(data['message']);
              }
            },
        });
    });
});

$(function(){
    $('#submit').click(function(event){
        event.preventDefault();

        var emailInput = $('input[name=email]');
        var captchaInput = $('input[name=captcha]');

        var email = emailInput.val();
        var captcha = captchaInput.val();

        bzajax.post({
            'url': '/resetmail/',
            'data': {
                'email': email,
                'captcha': captcha,
            },
            'success': function(data){
                if(data['code'] == 200){
                    emailInput.val('');
                    captchaInput.val('');
                    xtalert.alertSuccessToast('邮箱修改成功!');
                }else{
                    xtalert.alertError(data['message']);
                }
            },
        });

    });
});