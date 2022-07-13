var csrf_token = $("#id_csrf_token").val();
var flag = false;
var dateArray;
var kyc_text = '';
var certificate_list;


$("#to_year, #from_year").bind('change', [], validate_education_year);
$("#certificate_from_year, #certificate_to_year").bind(
    'change', [], validate_certification_year);

// function to show the bootstrap modal
function show_bootstrap_modal(elem) {
    $(elem).modal({
        show: true,
        keyboard: false,
        backdrop: 'static'
    });
}

function show_success_modal() {
    $("#kyc_incomplete_block").addClass('hide').html('');
     $("#kyc_complete_block").removeClass('hide');
    $('#simple-modal').find("#ok_btn").attr('href', '/my_identity/');
    $("#simple-modal").modal({
        'show': true,
        'keyboard': false,
        'backdrop': 'static'
    });
}

$(".form-control, textarea").on('change paste keyup keydown', function (e) {
    var exclude_fields = ['to_year', 'certificate_to_year'];
    var field_id = $(this).attr('id');
    var help_id = $($(this).parent().find('.help-block')).attr('id');
    var label_name = $($(this).parent().find('label')).html().replace('*', '');
    if (exclude_fields.indexOf(field_id) < 0){
        validate_field_onkeypress(field_id, help_id, label_name);
    }
});

function validate_education_year(){
    if ($("#to_year").val() && $("#from_year").val()) {
        if ($("#to_year").val() < $("#from_year").val()) {
            $("#to_year").focus();
            $('#help-text-to-year').html('Please enter proper year of completion');
            return false;
        }else{
            $('#help-text-to-year').html('');
            return true;
        }
    }else{
        return true;
    }
}

function validate_certification_year(){
    if ($("#certificate_from_year").val() != '' || $("#certificate_to_year").val() != '') {
        var cert_from_year = $("#certificate_from_year").val();
        var cert_to_year = $("#certificate_to_year").val();
        if (cert_from_year){
            cert_from_year = parseInt(cert_from_year);
        }else{
            cert_from_year = 0;
        }
        if (cert_to_year){
            cert_to_year = parseInt(cert_to_year);
        }else{
            cert_to_year = 0;
        }
        if(cert_from_year == 0 && cert_to_year !=0){
            $("#help-text-from-year").html('Please select From Year');
            $("#certificate_from_year").focus();
            return false;
        }
        if (cert_from_year >= cert_to_year && (cert_from_year!=0 || cert_to_year !=0)) {
            $('#help_text_certificate_to_year').html('Please enter proper year of completion');
            return false;
        }else{
            $('#help_text_certificate_to_year').html('');
            return true;
        }
    }else{
        return true;
    }
}

// Validates and submit the form
function submit_forms() {
    var val_arr = [];
    // certification validating
    val_arr.push(validate_certification_form());
    // education validating
    if (!$('.fileinput-new').hasClass('hide')) {
        html_text = 'Please Upload The Document';
        help_field_id = 'help_text_document';
        $('#' + help_field_id).html(html_text);
        $('html, body').animate({
            scrollTop: $("#paper_clip0").offset().top - 90
        }, 0);
        $("#paper_clip0").find('span').addClass('add-shadow');
        val_arr.push(1);
    }
    if(!validate_education_year()){
        val_arr.push(1);
    }
    val_arr.push(validate_field_onkeypress('to_year', 'help-text-to-year', 'To Year'));
    val_arr.push(
        validate_field_onkeypress('from_year', 'help-text-from_year', 'From Year'));
    val_arr.push(validate_field_onkeypress('activities', 'help_text_activities', 'Activities'));
    val_arr.push(validate_field_onkeypress('field_of_study', 'help_text_field_of_study', 'Field of study'));
    val_arr.push(validate_field_onkeypress('qualification', 'help_text_qualification', 'Degree'));
    val_arr.push(validate_field_onkeypress('school', 'help_text_school', 'School'));
    
    if(val_arr.indexOf(1) < 0){
        return true;
    }
    else {
        return false;
    }
}

// Submit education and certification details
function submit_educational_qualification() {
    var educational_detail = "";
    var certification_detail_json = "";
    var certification_detail = get_certificate_json();
    educational_detail = '{"school":"' + $('#school').val() + '", "qualification":"' + $("#qualification").val() + '","field_of_study":"' + $('#field_of_study').val() + '","activities":"' + $('#activities').val() + '","from_year":"' + $('#from_year').val() + '","to_year":"' + $('#to_year').val() + '","grade":"' + $('#grade').val() + '"}';

    if (certification_detail){
        certification_detail_json = JSON.stringify(certification_detail);
    }
    else {
        certification_detail = "";
    }

    if (submit_forms()) {
        $.ajax({
            method: "POST",
            url: '/signup/educational_qualification/',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", token);
            },
            data: {
                'educational_details': educational_detail,
                'certification_details': certification_detail_json
            },
            complete: function (e, xhr, settings) {

                var status = e.status;
                if (status == 200) {
                    kyc = e.responseJSON.kyc_status;
                    if (kyc.kyc_step1 == 'completed' && 
                        kyc.kyc_step2 == 'completed' &&
                        kyc.kyc_step3 == 'completed' &&
                        kyc.kyc_step4 == 'completed' &&
                        kyc.kyc_step5 == 'completed'){
                            show_success_modal();
                    }else{
                        show_ekyc_incomplete_modal(kyc);
                    }
                } else {
                    alert("Unable to Process your request right now. \n Please try again after some time");
                }
            },
            error: function (response) {
                alert("Unable to Process your request right now. \n Please try again after some time");
            }
        });
    }
}


// function show_certification_div() {
//     flag = true;
//     $('#cerfication_div').removeClass('hide');
//     $('#add_btn_div').addClass('hide');
//     $('#remove_btn_div').removeClass('hide');
// }

// function remove_certification_div() {
//     flag = false;
//     $('#cerfication_div').addClass('hide');
//     $('#add_btn_div').removeClass('hide');
//     $('#remove_btn_div').addClass('hide');
// }

function show_ekyc_incomplete_modal(kyc){
    var kyc_arr = [];
    var redirection_link;
    var kyc_html_text;
    var kyc_text = '';
    if (kyc.kyc_step5 != 'completed'){
        kyc_arr.push('Step-5');
        redirection_link = '/signup/education/';
    }
    if (kyc.kyc_step4 != 'completed') {
        kyc_arr.push('Step-4');
        redirection_link = '/signup/business_information/';
    }
    if (kyc.kyc_step3 != 'completed') {
        kyc_arr.push('Step-3');
        redirection_link = '/signup/personal_information/';
    }
    if (kyc.kyc_step2 != 'completed') {
        kyc_arr.push('Step-2');
        redirection_link = '/signup/verification_process/';
    }
    if (kyc.kyc_step1 != 'completed') {
        kyc_arr.push('Step-1');
        redirection_link = '/signup/face_capture/';
    }
    kyc_arr = kyc_arr.reverse();
    for (var i=0; i<kyc_arr.length; i++){
        if(kyc_arr[i+1]){
            kyc_text += '<b>' + kyc_arr[i] + ', </b>';
        }else{
            kyc_text += '<b>'+kyc_arr[i]+' </b>';
        }
    }
    kyc_html_text = 'Please Complete ' + kyc_text + 'to become Register Advisor <br /> Click "OK" button to complete';
    $("#kyc_incomplete_block").removeClass('hide').html(kyc_html_text);
    $('#simple-modal').find("#ok_btn").attr('href', redirection_link);
    show_bootstrap_modal('#simple-modal');
}


