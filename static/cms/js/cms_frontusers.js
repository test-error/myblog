/**
 * Created by Administrator on 2017/3/27.
 */

$(function(){
    $('.sort-select').change(function(event){
        event.preventDefault();

        var sort_id = $(this).val();
        console.log(sort_id);
        var newHref = xtparam.setParam(window.location.href,'sort',sort_id);
        window.location = newHref;
    });
});