// Validation only for Webinar
$(document).ready(function(){
    // validation for create_webinar_form
    var token = $("#id_csrf_token").val();
    $("#create_webinar_form").validate({
        rules: {
            name: {
                required: true,
                remote: {
                    url: "/webinar/check_room_name/",
                    beforeSend: function(request){
                        request.setRequestHeader("X-CSRFToken", token);
                    },
                    type: "POST",
                    data: {
                        name: function() {
                            return $("#id_name").val();
                        }
                    }
                }
            },
            lobby_description:{
                required: true
            },
            starts_at:{
                required: true
            },
            duration:{
                required: true,
                digits: true,
                min: 5,
                max: 180
            }
        },
        messages: {
            name:{
                required:"Please Enter Room Name",
                remote: "ROOM NAME already exists"
            },
            lobby_description: {
                required: "Please Enter lobby Description"
            },
            starts_at:{
                required:"Please Select Date and Time"
            },
            duration:{
                required: "Please Enter Duration",
                digits: "Please enter duration in minutes",
                min: "minimum duration is 5 minutes",
                max: "maximum duration allowed is 180 minutes"
            }
        },
        highlight: function(element) {
            $(element).closest('.control-group').removeClass('success').addClass('error');
        },
        unhighlight: function(element) {
            $(element).closest('.control-group').removeClass('error').addClass('success');
        },
        success: function(element) {
                //$(element).closest('.control-group').find('.fillimg').addClass('valid');
                // What is ".fillimg"?  That's not a real word.
        },
        errorPlacement: function (error, element) {
            $(element).closest('.control-group').find('.help-block').html(error.text());
        }
    });
});
