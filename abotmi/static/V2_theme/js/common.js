// function for setting success/error/alert information to common modal is showing
/**
 * @type_msg -> need to pass "sucess|warning|error",
 * @old_modal_id {optional} -> pass id of existing open modal to close before this modal loads
 * @data {optional} -> Body text
 * @btn_type -> if btn_type -> btn will show otherwise it will hide
 *      options:
 *          "click: <action>"
 *          "hide: true"
 *          "href: <link>"
 *          "reload: true"
 * @static -> need to pass "true|false"
 */
// function for setting success/error/alert information to common modal is showing
function show_alert(type_msg, old_modal_id, data, btn_type, static) {
    var msg = '';
    var modal_show_data;
    if (old_modal_id != "common_modal" && old_modal_id) {
        $("#" + old_modal_id).modal('hide');
    }
    switch (type_msg) {
        case "success":
            msg = "<i class='fa fa-check success'></i>";
            break;
        case "warning":
            msg = "<i class='fa fa-exclamation-circle warning'></i>";
            break;
        case "error":
            msg = "<i class='fa fa-times-circle error'></i>";
            break;
    }
    $("#common_modal").find("#msg_type").html(msg);
    $("#common_modal").find(".sub-div").empty();
    $("#common_modal").find(".sub-div").append(data);
    // removing the old attr except type and class attr
    if (btn_type) {
        $("#common_btn").css('display', 'inline-block');
        $("#common_cancel_btn").css('display', 'none');
        try{
            var old_attr = $("#common_btn")[0].getAttributeNames();
        }catch(e){
            var old_attr = [];
            var old_btn_attr_map = $("#common_btn")[0].attributes;
            $.each(old_btn_attr_map, function(e){
                old_attr.push(old_btn_attr_map[e].name);
            });
        }
        $.each(old_attr, function (e) {
            if (old_attr[e] != 'type' && old_attr[e] != 'class' && old_attr[e] != 'id') {
                $("#common_btn").removeAttr(old_attr[e]);
            }
        });
        var type_fun = btn_type.split(':');
        switch (type_fun[0]) {
            case 'click':
                $('#common_btn').attr('onclick', type_fun[1]);
                if(type_fun[2]!=''){
                    $('#common_btn').text(type_fun[2]);
                }
                break;
            case 'hide':
                $("#common_btn")
                    .attr('data-dismiss', "modal")
                    .attr('aria-hidden', "true");
                break;
            case 'href':
                $("#common_btn").attr('href', type_fun[1]);
                break;
            case 'reload':
                $("#common_btn").attr('onclick', 'return window.location.reload();');
                break;
            case 'confirmation':
                $("#common_cancel_btn").css('display', 'inline-block');
                $("#common_btn").attr('onclick', type_fun[1]);
                $("#common_cancel_btn")
                    .attr('data-dismiss', "modal")
                    .attr('aria-hidden', "true");
                break;
        }
        //showing close button according to button element present
        if(type_fun[0]){
            $("#common_modal").find('.close').hide();
        }else{
            $("#common_modal").find('.close').show();
        }
    } else {
        $("#common_cancel_btn").css('display', 'none');
        $("#common_btn").css('display', 'none');
    }
    //show model with more functionality accourding static variable 
    if(static == true){
        modal_show_data = {
            show: true,
            backdrop: 'static',
            keyboard: false
        }
    }else{
        modal_show_data = {
            show: true,
            keyboard: false
        }
    }
    $("#common_modal").modal(modal_show_data);
}

function avoid_double_click(btn_id){
    var default_btn = $('#'+btn_id);
    default_btn.prop('disabled', true);
    setTimeout(function(){
        default_btn.prop('disabled', false);
    }, 1000);
}