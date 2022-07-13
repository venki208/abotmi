// attaching country code to mobile number field
$("#mobile_number").intlTelInput({
    geoIpLookup: function (callback) {
        $.getJSON('http://ipinfo.io', function (resp) {
            var countryCode = (resp && resp.country) ? resp.country : "";
            callback(countryCode);
        });
    },
    nationalMode: false,
    initialCountry: "in"
});


// fetching the not approved advisors list
function fetch_not_approved_advisors_list(id) {
    $.ajax({
        type: 'POST',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        url: '/company/get_not_approved_advsors_list/',
        data: {
            'username': username
        },
        success: function (response) {
            console.log(response);
            $('#not_approved_advisors_tab').html('');
            $('#not_approved_advisors_tab').html(response);
        },
        error: function (response) {
        }
    });
}

// fetching not approved advisor list
$(document).ready(function () {
    fetch_not_approved_advisors_list('fetch_not_approved_advisors_list');
});

// Viewing the details of advisor
function view_details_of_advisor(id) {
    if (id != '') {
        $.ajax({
            type: 'POST',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", token);
            },
            url: "/company/fetch_advisor_details/",
            data: { id: id, domain: domain },
            success: function (response) {
                if (response.status == 'details_found') {
                    $('#id_advisor_details_modal_body').html('');
                    $('#id_company_email' + id).html(response.advisor_company_email);
                    $('#id_registration' + id).html(response.advisor_company_registration);
                    $("#id_picture" + id).html("<img src='" + response.profile_pic + "'>");
                    $('#id_advisor_details_modal_body').html($('#other_details_of_advisor' + id).html());
                    $('#id_advisor_details_modal').modal('show');
                }
            },
            error: function (response) {
            }
        });
    }
}

// Loading the feedback modal
function call_feedback_modal(id, status) {
    var placeholder;
    $("#id_feedback_button").attr(
        'onclick', 
        "validate_feedback('id_feed_back'," + "'" + status + "'" + "," + "'" + id + "');"
    );
    if (status == 'approved') {
        placeholder = 'Please provide reason for Disowning the advisor. The remarks given here will be kept confidential and will not be shared with the Advisor';
    }
    else if (status == 'dis_own') {
        placeholder = 'Please provide reason for Re-Own the advisor. The remarks given here will be kept confidential and will not be shared with the Advisor';
    }
    $("#id_feed_back").attr('placeholder', placeholder);
    $("#id_feedback_modal").modal('show');
}

// validating the feedback form and submittin the feedback
function validate_feedback(id, status, user_id) {
    if ($.trim($("#" + id).val()) == '') {
        $('#help_text_' + id).html('Please enter feedback');
        return false;
    } else {
        var feedback = $('#' + id).html();
        update_affiliate_company_status(user_id, status, 'id_feed_back');
    }
}

// updating the affiliate company status by submitting the feedback
function update_affiliate_company_status(id, status, feedback) {
    $.ajax({
        type: 'POST',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        url: "/company/update_affiliate_company_status/",
        data: {
            id: id,
            status: status,
            feedback: $("#" + feedback).val()
        },
        success: function (response) {
            if (response == 'success') {
                $("#" + feedback).val('');
                window.location.reload();
            } else {
                alert('Some thing went wrong!');
            }
        },
        error: function (response) {
        }
    });
}

// Fetching approved advisors list
function fetch_approved_advisors_list(id) {
    $.ajax({
        type: 'POST',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        url: '/company/get_approved_advisor_list/',
        data: {
            'username': username
        },
        success: function (response) {
            $('#approved_advisors_tab').html('');
            $('#approved_advisors_tab').html(response);
        },
        error: function (response) {
        }
    });
}

// Fetching disown advisors list
function fetch_disown_advisor_details(id) {
    $.ajax({
        type: 'POST',
        beforeSend: function (request) {
            request.setRequestHeader('X-CSRFToken', token)
        },
        url: '/company/get_disown_advisors_list/',
        data: {
            'username': username
        },
        success: function (response) {
            $("#disown_advisors_tab").html('');
            $("#disown_advisors_tab").html(response);
        }
    })
}