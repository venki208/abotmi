var profile_pic = $("#id_profile_pic");

// setting Gender value
var gender_sel_id;
if(gender == 'M'){
    gender_sel_id = 'inv_gender_male';
}else if(gender == 'F'){
    gender_sel_id = 'inv_gender_female';
}else{
    gender_sel_id = 'inv_gender';
}
$("#"+gender_sel_id).prop('checked', true);

// It validates the pincode format with a regx
function validate_pincode_investor(str){
    if (user_agent_country == 'IN'){
        var re = /^[0-9][0-9]{5}$/;
    }
    else{
        var re = /^[0-9][0-9]{2,5}$/;
    }
    var inputvalue = $("#"+str).val();
    if(inputvalue.match(re) && inputvalue > 0){
        document.getElementById(str).style.border='';
        document.getElementById('inv_error_zipcode').innerHTML='';
    }else{
        document.getElementById('inv_error_zipcode').innerHTML='Enter Valid Input';
        document.getElementById(str).style.border='1px solid #C32F2F';
        $("#"+str).focus();
    }
}

// It validates the mobile phone with inTel plugin  
function validateMobile(id, help_id) {
    var isValidNumber = $('#inv_mobile').intlTelInput("isValidNumber");
    if(isValidNumber == false){
        document.getElementById(id).value = "";
        $('#'+help_id).html('Enter Valid Mobile number');
        $('#inv_mobile').focus();
    }else{
        $('#'+help_id).html('');
    }
}

// Show bootstrap Modal function(pass id or name)
function show_bootstrap_modal(elem) {
    $(elem).modal({
        show:true,
        keyboard:false,
        backdrop:'static'
    });
}

// setting response data into common div
function load_data(response) {
    $("#my_identity_modal").html('');
    $("#my_identity_modal").html(response);
}

// Caldener loading function
$(document).ready(function () {
    var altFormat = $("#inv_birthdate_invester").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "M,d,yy",
        yearRange: "-100Y:Date()",
        maxDate: '-21Y',
        defaultDate: '-27y'
    });
    $("#inv_mobile").intlTelInput({
        nationalMode: false,
        initialCountry: user_agent_country,
        separateDialCode: true,
        autoPlaceholder: "off",
    });
});

$('#inv_birthdate_invester').on('keypress', function (e) {
    e.preventDefault(); // Don't allow direct editing
});

// hiding and showing the div
function showediteditform(){
    $("#view_user_profile_div").addClass('hide');
    $("#edit_user_profile_div").removeClass('hide');
}

// submit form function
function submit_investor_edit_profile(){
    if (validate_edit_investor_form()) {
        var first_name = $("#inv_first_name").val();
        var last_name = $("#inv_last_name").val();
        var email = $("#inv_email").val();
        var mobile = get_mobile_no("#inv_mobile");
        var city = $("#inv_city").val();
        var gender = $("input[name='inv_gender']:checked").val();
        var birthdate = $("#inv_birthdate_invester").val();
        var pincode = $("#inv_pincode").val();
        var token = $("#id_csrf_token").val();
        $.ajax({
            type: 'POST',
            url: '/signup/investor_identity/',
            beforeSend: function(request){
                request.setRequestHeader("X-CSRFToken", token);
            },
            data: {
                first_name: first_name,
                last_name: last_name,
                email: email,
                mobile: mobile,
                city: city,
                gender: gender,
                birthdate: birthdate,
                pincode: pincode
            },
            success:function(response){ 
                $("#edit_user_profile_div").addClass('hide');
                $("#view_user_profile_div").removeClass('hide');
                document.getElementById("view_email").innerHTML = email;
                if (mobile.length){
                    document.getElementById("view_mobile").innerHTML = mobile;
                }else{
                    document.getElementById("view_mobile").innerHTML = "Nil";
                }
                if(city.length>0){
                    document.getElementById("view_city").innerHTML = city;
                }else{
                    document.getElementById("view_city").innerHTML = "Nil";
                }
                if(pincode.length>0){
                    document.getElementById("view_pincode").innerHTML = pincode;
                }else{
                    document.getElementById("view_pincode").innerHTML = "Nil";
                }
                if(birthdate.length>0){
                    $("#view_birthdate").html(birthdate);
                }else{
                    $("#view_birthdate").html("Nil");
                }
                var gender_val;
                if(gender == 'M'){
                    $("#gender_block").removeClass('hide');
                    gender_val =  'Male';
                }else if(gender == 'F'){
                    $("#gender_block").removeClass('hide');
                    gender_val = 'Female';
                }else{
                    $("#gender_block").addClass('hide');
                    gender_val = '';
                }
                $("#view_gender").html(gender_val);
                document.body.scrollTop = 0;
                document.documentElement.scrollTop = 0;
            }
        });
    }
}

// validation function for inverstor form submit
function validate_edit_investor_form(){
    var is_last_name = validate_field_onkeypress('inv_last_name', 'inv_error_last_name', 'Last Name');
    var is_first_name = validate_field_onkeypress('inv_first_name', 'inv_error_first_name', 'First Name');
    var is_mobile = validate_field_onkeypress('inv_mobile', 'inv_error_mobile', 'Mobile Number');
    var is_email = validate_field_onkeypress('inv_email', 'inv_error_email', 'Email');
    var is_city = validate_field_onkeypress('inv_city', 'inv_error_city', 'City');
    var is_zipcode = validate_field_onkeypress('inv_pincode', 'inv_error_zipcode', 'Zip Code');
    var missed_field = 0;
    if ($('input[name="inv_gender"]:checked').length < 1) {
        $("#inv_gender_male").append('<style>input[type=radio]+#inv_gender_male::before{border-color: #8C0606;}</style>');
        $("#inv_gender_female").append('<style>input[type=radio]+#inv_gender_female::before{border-color: #8C0606;}</style>');
        $("#inv_gender").append('<style>input[type=radio]+#inv_gender::before{border-color: #8C0606;}</style>');
        document.getElementById('inv_error_gender').innerHTML = 'Please Select Gender';
        $("#inv_gender_male").focus();
        missed_field = 1;
    }else{
        document.getElementById('inv_error_gender').innerHTML = '';
    }
    // Commented temporarily 
    // if ($("#inv_birthdate_invester").val() == '') {
    //     $('#inv_error_birthday').html('Please Enter Birthdate');
    //     $('#inv_birthdate_invester').css('border', '1px solid #C32F2F');
    //     $("#inv_birthdate_invester").focus();
    //     $("#inv_birthdate_invester").datepicker("hide");
    //     missed_field = 1;
    // }
    if(is_last_name !=0 || is_first_name != 0 || is_mobile != 0 || is_email != 0 || is_city != 0 ||  is_zipcode != 0 || missed_field == 1 ){
        return false;
    }else{
        return true;
    }
}

// Edit/View Image modal
profile_pic.on('click', function(){
    $.ajax({
        method:'GET',
        url: '/my_identity/edit_or_view_image/',
        beforeSend: function(request){
            request.setRequestHeader('X-CSRFToken', token);
        },
        data:{},
        success: function(response){
            load_data(response);
            show_bootstrap_modal('#imageModal');
        },
        error: function(response){
            alert("Unable to Process your request right now. \n Please try again after some time'");
        }
    });
});