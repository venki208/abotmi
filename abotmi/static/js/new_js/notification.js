$(document).ready(function(e){
    $.ajax({
        type: 'GET',
        url: '/get_notification_count/',
        beforeSend: setHeader,
        success: function(response){
            if(response.nf_count > 0){
                $("#notf_count")
                    .html(response.nf_count)
                    .removeClass('hide');
            }else{
                $("#notf_count").addClass('hide');
            }
        },

    });
});


$(".notificationButton").on("show.bs.dropdown", function (event) {
    var show_notif = show_notifications();
    show_notif.success(function (response) {
        $('#notif_drop_down').html(response);
        $("#notf_count")
            .html(0)
            .addClass('hide');
        setTimeout(
            function(){
                var static_notif_ids = $('[static-notif="1"]').map(function (e) {
                    return this.id;
                }).get();
                if (static_notif_ids.length > 0){
                    update_notification(static_notif_ids);
                }
            }, 2500);
    });
});

function show_notifications(){
    return $.ajax({
        type: 'GET',
        url: '/get_notification/',
        beforeSend: setHeader,
    });
}

$("#notif_drop_down").on('click', "[name='action_btn']", function (e) {
    var parent_div = $(this).closest('.unread');
    var notif_id = $(parent_div).attr('id');
    update_notification([notif_id]);
});

function update_notification(notification_ids){
    $.ajax({
        type: 'POST',
        beforeSend: setHeader,
        url: '/update_notification_status/',
        data: {
            ids: notification_ids
        },
        success: function (response) {
            if (response == '200') {
                $.each(notification_ids, function (index, value) {
                    $("#" + value).removeClass('unread');
                });
            }
        }
    });
}