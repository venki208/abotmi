var csrf_token = $("#id_csrf_token").val();
var digital_links_list_length = digital_links_list_length;
// Saving the digital foot print
function save_digital_link(id, help_id, str) {
    var url_link = $("#" + id).val();
    var token = csrf_token;
    if (!validate_field_onkeypress('id_send_link_url', 'help_send_link_url', 'URL')) {
        $.ajax({
            method: "POST",
            url: '/signup/save_foot_print_verification/',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", token);
            },
            data: {
                'digital_links': url_link
            },
            success: function (response) {
                digital_links_list_length = parseInt(digital_links_list_length) + 1;
                $("#add_url").append(
                    '<div class="main-alert row" role="alert">' +
                    '<div class="col-md-4 col-xs-12 alert_link_box">' +
                    '<span id="link_' + digital_links_list_length + '">' + url_link + '</span>' +
                    '<button type="button" class="close" data-dismiss="alert" aria-label="Close" id="' + digital_links_list_length + '"><i class="fa fa-times-thin fa-2x"></i></button></div></div>');
                $("#" + digital_links_list_length)
                    .attr('onclick', "delete_digital_link('" + url_link + "');");
                $("#" + id).val('');
            },
            error: function (response) {
                    alert("Unable to Process your request right now. \n Please try again after some time'");
                }
        });
    }
}

// Deleting the foot print record in databas
function delete_digital_link(id) {
    var token = csrf_token;
    $.ajax({
        method: "POST",
        url: '/signup/delete_foot_print_verification/',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        data: {
            'digital_links': id
        },
        error: function (response) {
                alert("Unable to Process your request right now. \n Please try again after some time'");
            }
    }); 
}
