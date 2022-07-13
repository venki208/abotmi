// CSRF token initializing
var csrf_token = $("#id_csrf_token").val();

// setting suffix/title value to regstration form
if (suffix == 0 || suffix == '') {
    $('#suffix').val('0');
} else {
    $("#suffix").val(suffix);
}

// setting country value to registration form
if (country) {
    $("#country").val(country);
}
// setting nationality
$("#nationality").val(nationality_value);

// setting gender value
if (gender == 'M') {
    document.getElementById("gender_male").checked = true;
    document.getElementById("gender_female").checked = false;
    document.getElementById("gender_others").checked = false;
}
if (gender == 'F') {
    document.getElementById("gender_male").checked = false;
    document.getElementById("gender_female").checked = true;
    document.getElementById("gender_others").checked = false;
}
if (gender == 'O') {
    document.getElementById("gender_male").checked = false;
    document.getElementById("gender_female").checked = false;
    document.getElementById("gender_others").checked = true;
}

// Setting communication type
if (communication_email == 'primary') {
    document.getElementById('communication_email_primary').checked = true;
}
if (communication_email == 'secondary') {
    document.getElementById('communication_email_secondary').checked = true;
}

$("#mobile_no").intlTelInput({
    nationalMode: false,
    initialCountry: user_agent_country,
    separateDialCode: true,
    autoPlaceholder: "off",
    hiddenInput: "mobile",
    utilsScript: "/static/js/plugins/intl-tel-input-js/js/utils.js",
});

// attaching jquery ui date picker
$(document).ready(function () {
    var altFormat = $("#birthdate").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "mm-dd-yy",
        yearRange: "-100Y:Date()",
        maxDate: '-18Y',
        defaultDate: '-27y'
    });
});
$('#birthdate').on('keypress', function (e) {
    e.preventDefault(); // Don't allow direct editing
});
$('.date_class').on('keypress', function (e) {
    e.preventDefault(); // Don't allow direct editing
});
$('.datepicker').on('keypress', function (e) {
    e.preventDefault(); // Don't allow direct editing
});

// function to show the bootstrap modal
function show_bootstrap_modal(elem) {
    $(elem).modal({
        show: true,
        keyboard: false,
        backdrop: 'static'
    });
}

// function to scroll to the div
function scroll_to(elem){
    $('html,body').animate({
        scrollTop: $(elem).offset().top-100
    }, 'slow');
}

function validateAlpha(str, help_id) {
    var name = document.getElementById(str);
    if (name.value != '') {
        var alpha = /^[a-zA-Z()\s]+$/.test(name.value);
        if (alpha) {
            return true;
        } else {
            $('#' + str).css('border', '1px solid #C32F2F');
            document.getElementById(str).value = "";
            $('#' + help_id).html('Enter Valid Input');
            return false;
        }
    }
}

function check_and_save_secondary_email(name, id) {
    document.getElementById('help-text-secondary_email').innerHTML = ''
    var email = $("#" + id).val();
    var primary = $("#username").val();
    if (email != '') {
        document.getElementById(id).style.border = '1px #bfbfbf solid';
        var token = "{{ csrf_token }}";
        var re = /\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/;
        if (!re.test(email)) {
            document.getElementById('help-text-secondary_email').innerHTML = 'Please enter valid Email'
            $("#secondary_email").val('');
            $("#secondary_email").css('border', '1px solid #C32F2F')
            $("#secondary_email").focus();
        } else if (primary == email) {
            document.getElementById('help-text-secondary_email').innerHTML = 'Second Email ID should be different from Primary Email ID'
            $("#secondary_email").val('');
            $("#secondary_email").css('border', '1px solid #C32F2F')
            $("#secondary_email").focus();
        } else {
            $.ajax({
                url: "/signup/check_and_save_secondary_email/",
                method: "POST",
                beforeSend: function (request) {
                    request.setRequestHeader("X-CSRFToken", token);
                },
                data: {
                    username: '{{user.username}}',
                    value: email,
                    name: name
                },
                success: function (response) {
                    if (response == 0 || response == 'old_secondary_email') {
                        save_onchange('secondary_email', 'secondary_email');
                        document.getElementById('help-text-secondary_email').innerHTML = '';
                    } else {
                        document.getElementById('help-text-secondary_email').innerHTML = 'Email Already Exists'
                        $("#secondary_email").val('');
                        $("#secondary_email").css('border', '1px solid #C32F2F')
                        $("#secondary_email").focus();
                    }
                },
                error: function (response) {},
            });
        }
    }
}

//  Action : Auto Save Form
function save_onchange(name, id, help_text_ids) {
    var value = $("#" + id).val();
    if (value != '' || value != '--Select--') {
        $("#" + help_text_ids).html('');
        document.getElementById(id).style.border = '1px #bfbfbf solid';
    }
    if (id == 'gender_male' || id == 'gender_female' || id == 'gender_others') {
        document.getElementById(help_text_ids).innerHTML = '';
        $("#validate-gender-male").append('<style>input[type=radio]+#validate-gender-male::before{border-color: #adb8c0;}</style>');
        $("#validate-gender-female").append('<style>input[type=radio]+#validate-gender-female::before{border-color: #adb8c0;}</style>');
        $("#validate-gender-others").append('<style>input[type=radio]+#validate-gender-others::before{border-color: #adb8c0;}</style>');
        document.getElementById('help-text-gender').innerHTML = '';
    }
    if (id == 'communication_email_primary') {
        value = 'primary';
    }
    if (id == 'communication_email_secondary') {
        value = 'secondary';
    }
    $.ajax({
        url: "/signup/onchange_save_field/",
        method: "POST",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", csrf_token);
        },
        data: {
            username: username,
            value: value,
            name: name
        },
        success: function (response) {},
        error: function (response) {},
    });
}

// validating form
function validate_form(is_validate) {
    var missed_field = 0;
    if ($('#my_belief').val() == '') {
        if (is_validate) {
            $("#help_text_my_belief").html('Please Enter My Belief');
            $('#my_belief').css('border', '1px solid #C32F2F');
            $("#my_belief").focus();
        }
        missed_field = 1;
    } else {
        $("#help_text_my_belief").html('');
        $('#my_belief').css('border', '');
    }
    if ($('#my_promise').val() == '') {
        if (is_validate) {
            $("#help_text_my_promise").html('Please Enter My Promise');
            $('#my_promise').css('border', '1px solid #C32F2F');
            $("#my_promise").focus();
        }
        missed_field = 1;
    } else {
        $("#help_text_my_promise").html('');
        $('#my_promise').css('border', '');
    }
    var isValidNumber = $('#mobile_no').intlTelInput("isValidNumber");
    var country = $("#country").val();
    if (country == '' || country == 'Select') {
        if (is_validate) {
            document.getElementById('country').style.border = '1px solid #C32F2F';
            document.getElementById('help-text-country').innerHTML = 'Please Enter Country';
            $("#country").focus();
        }
        missed_field = 1;
    }
    var state = $.trim($("#state").val());
    if (state == '') {
        if (is_validate) {
            document.getElementById('state').style.border = '1px solid #C32F2F';
            document.getElementById('help-text-state').innerHTML = 'Please Enter State';
            $("#state").val('').focus();
        }
        missed_field = 1;
    }
    var pincode = $.trim($("#pincode").val());
    if (pincode == '') {
        if (is_validate) {
            document.getElementById('pincode').style.border = '1px solid #C32F2F';
            document.getElementById('help-text-pincode').innerHTML = 'Please Enter Code';
            $("#pincode").val('').focus();
        }
        missed_field = 1;
    }
    var city = $.trim($("#city").val());
    var reg = /^([\s.]?[a-zA-Z]+)+$/;
    if (!reg.test(city)) {
        if (is_validate) {
            document.getElementById('city').style.border = '1px solid #C32F2F';
            document.getElementById('help-text-city').innerHTML = 'Please Enter City';
            $("#city").val('').focus();
        }
        missed_field = 1;
    } 
    var address = $.trim($("#address").val());
    if (address == '') {
        if (is_validate) {
            document.getElementById('address').style.border = '1px solid #C32F2F';
            document.getElementById('help-text-address').innerHTML = 'Please Enter Address Line 1';
            $("#address").val('').focus();
        }
        missed_field = 1;
    }
    if (isValidNumber == false) {
        if (is_validate) {
            $("#help_text_mobile").html('Enter Valid Mobile number');
            $('#mobile_no').css('border', '1px solid #C32F2F');
            $("#mobile_no").focus();
        }
        missed_field = 1;
    } else {
        $("#help_text_mobile").html('');
        $('#mobile_no').css('border', '');
    }
    var communication_email = document.getElementById('communication_email_secondary');
    if (communication_email.checked == true) {
        var primary = $("#username").val();
        if ($("#secondary_email").val() == '') {
            if (is_validate) {
                $('#help-text-secondary_email').html('Please Enter Second Email');
                $('#secondary_email').css('border', '1px solid #C32F2F');
                $("#secondary_email").focus();
            }
            missed_field = 1;
        } else {
            var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
            var email = $("#secondary_email").val()
            if (!re.test(email)) {
                if (is_validate) {
                    $('#help-text-secondary_email').html('Please Enter Second Email');
                    $('#secondary_email').css('border', '1px solid #C32F2F');
                    $("#secondary_email").focus();
                }
                missed_field = 1;
            } else if (primary == email) {
                if (is_validate) {
                    document.getElementById('help-text-secondary_email').innerHTML = 'Second Email ID should be different from Primary Email ID'
                    $("#secondary_email").val('');
                    $("#secondary_email").css('border', '1px solid #C32F2F')
                    $("#secondary_email").focus();
                }
                missed_field = 1;
            } else {

                $('#help-text-secondary_email').html('');
                $('#secondary_email').css('border', '');
            }
        }
    }
    if ($("#nationality").val() == '' ) {
        if (is_validate) {
            document.getElementById('nationality').style.border = '1px solid #C32F2F';
            document.getElementById('help-text-nationality').innerHTML = 'Please Enter Nationality';
            $("#nationality").focus();
        }
        missed_field++;
    }
    if ($("#birthdate").val() == '') {
        if (is_validate) {
            $('#help_text_birthdate').html('Please Enter Birthdate');
            $('#birthdate').css('border', '1px solid #C32F2F');
            $("#birthdate").focus();
            $("#birthdate").datepicker("hide");
        }
        missed_field = 1;
    }
    if ($('input[name="gender"]:checked').length < 1) {
        if (is_validate) {
            $("#validate-gender-male").append('<style>input[type=radio]+#validate-gender-male::before{border-color: #8C0606;}</style>');
            $("#validate-gender-female").append('<style>input[type=radio]+#validate-gender-female::before{border-color: #8C0606;}</style>');
            $("#validate-gender-others").append('<style>input[type=radio]+#validate-gender-others::before{border-color: #8C0606;}</style>');
            document.getElementById('help-text-gender').innerHTML = 'Please Select Gender';
            $("#gender_male").focus();
        }
        missed_field = 1;
    }
    if ($.trim($("#last_name").val()) == '') {
        if (is_validate) {
            $('#help_text_last_name').html('Please Enter Last Name');
            $('#last_name').css('border', '1px solid #C32F2F');
            $("#last_name").focus();
            missed_field = 1;
        }
        missed_field = 1;
    } else if ($("#last_name").val() != '') {
        var alpha = /^[a-zA-Z()\s]+$/.test($("#last_name").val());
        if (alpha) {
            if ($("#last_name").val().length >= 30) {
                $('#help_text_last_name').html('Please Enter Less than 30 Characters');
                $('#last_name').css('border', '1px solid #C32F2F');
                $("#last_name").focus();
                missed_field = 1;
            }
        } else {
            if (is_validate) {
                $('#help_text_last_name').html('Please Enter only Characters in Last Name');
                $('#last_name').css('border', '1px solid #C32F2F');
                $('#last_name').focus();
            }
            missed_field = 1;
        }
    }
    if ($('#middle_name').val() != '' && $('#middle_name').val().length >= 30) {
        $('#help_text_middle_name').html('Please Enter Less than 30 Characters');
        $('#middle_name').css('border', '1px solid #C32F2F');
        $("#middle_name").focus();
        missed_field = 1;
    }
    if ($.trim($("#first_name").val()) == '') {
        if (is_validate) {
            $('#help_text_first_name').html('Please Enter First Name');
            $('#first_name').css('border', '1px solid #C32F2F');
            $("#first_name").focus();
            // this code is for scroll top
            scroll(0, 0);
        }
        missed_field = 1;
    }
    if ($("#first_name").val() != '') {
        var alpha = /^[a-zA-Z()\s]+$/.test($("#first_name").val());
        if (alpha) {
            if ($("#first_name").val().length >= 30) {
                $('#help_text_first_name').html('Please Enter Less than 30 Characters');
                $('#first_name').css('border', '1px solid #C32F2F');
                $("#first_name").focus();
            }
        } else {
            if (is_validate) {
                $('#help_text_first_name').html('Please Enter only Characters in First Name');
                $('#first_name').css('border', '1px solid #C32F2F');
                $('#first_name').focus();
            }
            missed_field = 1;
        }
    }
    // comment temporarily as per client requirements 
    // if ($("#suffix").val() == 'Select' || $("#suffix").val() == '') {
    //     if (is_validate) {
    //         $('#help_text_suffix').html('Please Select Title');
    //         $('#suffix').css('border', '1px solid #C32F2F');
    //         $("#suffix").focus();
    //     }
    //     missed_field = 1;
    // }
    return missed_field 
}

function submit_creditbility_form() {
    var missed_field = validate_form(true);
    if (missed_field == 0) {
        $("input[name='filled_form_status']").val('true');
        $('#signup_form').submit();
    }
}
