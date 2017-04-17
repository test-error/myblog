/**
 * Created by Administrator on 2017/3/29.
 */


$(function(){
    $('#graph-captcha-btn').click(function(event){
        event.preventDefault();
        var imgTag = $(this).children('img');
        var oldSrc = imgTag.attr('src');
        var href = xtparam.setParam(oldSrc,'xx',Math.random());
        imgTag.attr('src',href);
    });
});

$(function(){
    $('#send-captcha-btn').click(function(event){
        event.preventDefault();
        var telephone = $('input[name=telephone]').val();
        var self = $(this);
        if(!telephone){
            xtalert.alertInfoToast('请输入手机号码！')
        }

        bzajax.get({
            'url': '/account/sms_captcha/',
            'data': {
                'telephone': telephone
            },
            'success': function(data){
                if(data['code'] == 200){
                    xtalert.alertSuccessToast('短信验证码发送成功！');
                    var timeCount = 60;
                    self.attr('disabled','disabled');
                    self.css('cursor','default');
                    var timer = setInterval(function(){
                        self.text(timeCount);
                        timeCount --;
                        if(timeCount <= 0){
                            self.text('发送验证码');
                            self.removeAttr('disabled');
                            clearInterval(timer);
                            self.css('cursor','pointer');
                        }
                    },1000);
                }else {
                    xtalert.alertInfoToast(data['message']);
                }
            }
        });

    });
});
