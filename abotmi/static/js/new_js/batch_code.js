var csrf_token = $("#id_csrf_token").val();

var edit_batch_btn = $("#id_edit_batch_code_btn");
var input_batch_url = $("#basic_batch_url");
var input_batch_div = $("#id_batch_input_div");
var check_availability_btn = $("#id_batch_avail_btn");
var avail_btn_div = $("#avail_btn_div");
var help_batch_div = $("#help_batch_codes_div");

// Binding the events
edit_batch_btn.bind('click', [], edit_batch_code);
check_availability_btn.bind('click', [input_batch_url.val()], check_availability_batch);
// validating the filed
input_batch_url.on('keyup keydown change', function () {
    // var help_id = $('#' + this.id).closest(".form-group").find('.help-block')[0].id;
    var is_valid = validate_field_onkeypress(this.id, 'help_basic_batch_url', 'Profile Batch');
});

// function for Edit the batch code
function edit_batch_code(){
    $("#default_batch_code").addClass('hide');
    edit_batch_btn.addClass('hide');
    $("#basic-addon3").removeClass('hide');
    $("#html_batch").addClass('hide');
    input_batch_div.removeClass('hide');
    input_batch_url.focus();
    avail_btn_div.removeClass('hide');
}

// function for checking batch is exists or not
function check_availability_batch(){
    var is_valid = validate_field(
        'basic_batch_url', 'help_basic_batch_url', 'Profile Batch');
    if(is_valid){
        $.ajax({
            type: 'POST',
            url: '/my_identity/check_batch_availability/',
            beforeSend: setHeader,
            data: {
                batch_code: input_batch_url.val()
            },
            success: function(response){
                if(response == 'success'){
                    help_batch_div.html('');
                    check_availability_btn.html('Update');
                    check_availability_btn.unbind('click');
                    check_availability_btn.bind('click', [input_batch_url.val()], update_batch_code);
                }else if(response == 'failed'){
                    alert('Unable to check profile URL \n Please try again after some time');
                }else{
                    help_batch_div.html('<p>Here some of Batch codes are available.</p>');
                    for (i = 0; i < response.help_batch_codes.length; i++) {
                        help_batch_div.append('<p>' + response.help_batch_codes[i]+'</p>');
                    }
                }
            },
            error: function(reposne){
                alert('Unable to check profile URL \n Please try again after some time');
            }
        });
    }
}

// function for updating the batch
function update_batch_code(e){
    var batch_code = e.data[0];
    $.ajax({
        method: 'POST',
        url: '/my_identity/batch_code/',
        beforeSend: setHeader,
        data:{
            batch_code : batch_code
        },
        success:function(response){
            if(response == 'success'){
                $("#default_batch_code")
                    .removeClass('hide')
                    .html(batch_code);
                input_batch_url.val(batch_code);
                edit_batch_btn.removeClass('hide');
                input_batch_div.addClass('hide');
                avail_btn_div.addClass('hide');
                check_availability_btn.html('Check Availability');
                check_availability_btn.unbind('click');
                check_availability_btn.bind('click', [input_batch_url.val()], check_availability_batch);
                advisor_profile_url = default_server_url+'/profile/'+batch_code+'/';
                $("#profile_a_link").attr('href', advisor_profile_url);
                $("#html_batch")
                    .removeClass('hide')
                    .html(advisor_profile_url);
                $("#basic-addon3").addClass('hide');
                profile_link = '</br>To view the profile click <a href='+"'"+advisor_profile_url+"'"+'>here</a> <br/>';
            }else{
                alert('Unable to update the profile URl \n Please Try again after some time');
            }
        },
        error: function(response){
            alert('Unable to update the profile URl \n Please Try again after some time');
        }
    });
}
