/**
 * Created by Administrator on 2017/3/29.
 */

$(function(){
    $('#graph-captcha-btn').click(function(event){
        event.preventDefault();
        $(this).css('cursor','pointer');
        var imgTag = $(this).children('img');
        var oldSrc = imgTag.attr('src');
        var href = xtparam.setParam(oldSrc,'xx',Math.random());
        imgTag.attr('src',href);
    });
});