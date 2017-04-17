/**
 * Created by Administrator on 2017/3/27.
 */


$(function(){
    $('#add-board-btn').click(function(event){
        event.preventDefault();

        xtalert.alertOneInput({
            'title': '请输入板块名称',
            'placeholder': '板块名称',
            'confirmCallback': function(inputValue){
                bzajax.post({
                    'url': '/add_board/',
                    'data': {
                        'name': inputValue,
                    },
                    'success': function(data){
                        if(data['code'] == 200){
                            xtalert.alertSuccessToast('板块添加成功！');
                            setTimeout(function(){
                                window.location.reload();
                            },800)
                        }else{
                            xtalert.alertInfoToast(data['message']);
                        }
                    }
                });
            },
        });
    });
});

$(function(){
    $('#edit_board').click(function(event){
        event.preventDefault();

        var id = $(this).attr('board-id');
        xtalert.alertOneInput({
            'title': '请输入板块名称',
            'placeholder': '板块名称',
            'confirmCallback': function(inputValue){
                bzajax.post({
                    'url': '/edit_board/',
                    'data': {
                        'id': id,
                        'name': inputValue,
                    },
                    'success': function(data){
                        if(data['code'] == 200){
                            xtalert.alertSuccessToast('板块修改成功！');
                            setTimeout(function(){
                                window.location.reload();
                            },800);
                        }else {
                            xtalert.alertInfoToast(data['message']);
                        }
                    }
                });
            }
        });
    });

    $('#delete_board').click(function(event){
        event.preventDefault();

        var id = $(this).attr('board-id');
        xtalert.alertConfirm({
            'msg': '您确定要删除本板块吗？',
            'confirmCallback': function(){
                bzajax.post({
                    'url': '/delete_board/',
                    'data': {
                        'id': id,
                    },
                    'success': function(data){
                        if(data['code'] == 200){
                            xtalert.alertSuccessToast('板块删除成功！');
                            setTimeout(function(){
                                window.location.reload();
                            },800);
                        }
                    }
                });
            }
        });
    });
});