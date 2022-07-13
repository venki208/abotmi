var token = csrf_token;

$("#company_country").val(company_country_value);
if (primary_communication == 'home') {
    document.getElementById("home").checked = true;
    document.getElementById("office").checked = false;
}
if (primary_communication == 'office') {
    document.getElementById("home").checked = false;
    document.getElementById("office").checked = true;
}

/**
 * @use -> used upload the documents and attaching docs
 * @param {HTMLFormId} form_id -> need to pass HTML form attribute id
 * @param {HTMLAttrID} uploaded_div 
 * @param {HTMLAttrID} paper_clip 
 */
function upload_govt_doc(form_id, uploaded_div, paper_clip){
    var max_uploads = 3;
    if(max_uploads > $('.attach_class').length){
        var upload_res = upload_document(form_id);
        upload_res.success(function(response){
            remove_icon = "&nbsp;&nbsp" +
                    "<i class='glyphicon glyphicon-trash download_link_color'></i>";
            attach_document('renewal_document_div', response, paper_clip, false, '');
        });
        $('#help-text-govt_no').hide();
        upload_res.error(function(response){
            alert('unable to upload the document \n Please try again.');
        });
    }else{
        alert('Maximum 3 Files can be uploaded');
    }
}

function validateCurrency(str) {
    if ($("#" + str).val() == 0) {
        document.getElementById(str).value = "";
        $("#help-text-annual").html('Please Enter Valid Annual Income');
    }
}

function CheckIsValidDomain(str) {
    var domain = document.getElementById(str).value;
    var re = new RegExp('^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9](?:\.[a-zA-Z]{2,})+$');
    if (!domain.match(re)) {
        document.getElementById(str).value = '';
        $("#help-text-company-website").html('Please Enter Valid website (example: www.xyz.net)');
        return false;
    }
}

function validate_alpha(str, save) {
    var name = document.getElementById(str).value;
    var alpha = /^[a-zA-Z ]+(([\'\,\.\- ][a-zA-Z ])?[a-zA-Z ]*)*$/;
    var m_alpha = /^[a-zA-Z()\s]+$/;
    var hq_alpha = /[a-zA-Z ]+(([\.\,])*[a-zA-Z ]*)*$/;
    var l_alpha = /^(?!.*?([A-Z][a-z]).*?\1)[A-Z, a-z](?:,[A-Z, a-z])*$/;
    if (str == "language_known") {
        if (document.getElementById(str).value.trim().length == 0) {
            document.getElementById('language_known').style.border = '1px solid #C32F2F';
            document.getElementById('help-text-language_known').innerHTML = 'Please Enter Languages known to Speak';
            $('#' + str).focus();
            return false;
        } else if (name.match(alpha)) {
            if (save) {
                save_onchange('language_known', str, 'help-text-language_known');
            }
            document.getElementById('language_known').style.border = '';
            document.getElementById('help-text-language_known').innerHTML = '';
            return true;
        } else {
            $('#' + str).focus();
            document.getElementById('language_known').style.border = '1px solid #C32F2F';
            document.getElementById('help-text-language_known').innerHTML = 'Please Enter Only Characters';
            return false;
        }
    }
    if (str == "languages_known_read_write") {
        if (document.getElementById(str).value.trim().length == 0) {
            document.getElementById('languages_known_read_write').style.border = '1px solid #C32F2F';
            document.getElementById('help-text-languages_known_read_write').innerHTML = 'Please Enter Languages known to Read and Write';
            $('#' + str).focus();
            return false;
        } else if (name.match(alpha)) {
            if (save) {
                save_onchange("languages_known_read_write", str, 'help-text-languages_known_read_write');
            }
            document.getElementById('languages_known_read_write').style.border = '';
            document.getElementById('help-text-languages_known_read_write').innerHTML = '';
            return true;
        } else {
            $('#' + str).focus();
            document.getElementById('languages_known_read_write').style.border = '1px solid #C32F2F';
            document.getElementById('help-text-languages_known_read_write').innerHTML = 'Please Enter Only Characters';
            return false;
        }
    }
    if (str == "mother_tongue") {
        if (document.getElementById(str).value.trim().length == 0) {
            document.getElementById('mother_tongue').style.border = '1px solid #C32F2F';
            if (user_agent_country == "IN") {
                document.getElementById('help-text-language_mother_tongue').innerHTML = 'Please Enter Mother Tongue';
            } else {
                document.getElementById('help-text-language_mother_tongue').innerHTML = 'Please Enter Primary Language Spoken';

            }
            $('#' + str).focus();
            return false;
        } else if (name.match(m_alpha)) {
            if (save) {
                save_onchange("mother_tongue", str, 'help-text-language_mother_tongue');
            }
            document.getElementById('mother_tongue').style.border = '';
            document.getElementById('help-text-language_mother_tongue').innerHTML = '';
            return true;
        } else {
            $("#" + str).focus();
            document.getElementById('mother_tongue').style.border = '1px solid #C32F2F';
            document.getElementById('help-text-language_mother_tongue').innerHTML = 'Please Enter Only Characters';
            return false;
        }
    }
}

function save_onchange(name, id, error_message_block_id) {
    var value = $("#" + id).val();
    if (value != '') {
        document.getElementById(error_message_block_id).innerHTML = '';
    }
    document.getElementById(id).style.border = '1px #bfbfbf solid';
    if (id == 'home' || id == 'office') {
        $("#primary_communication_address_validate_home").append('<style>input[type=radio]+#primary_communication_address_validate_home::before{border-color: #adb8c0;}</style>');
        $("#primary_communication_address_validate_office").append('<style>input[type=radio]+#primary_communication_address_validate_office::before{border-color: #adb8c0;}</style>');
        document.getElementById(error_message_block_id).innerHTML = '';
    }
    if (id == 'home') {
        var communication_address = document.getElementById('home').checked;
        if (communication_address == true) {
            document.getElementById('company_address1').style.border = '';
            document.getElementById('help-text-company-address1').innerHTML = '';
            document.getElementById('company_address2').style.border = '';
            document.getElementById('help-text-company-address2').innerHTML = '';
            document.getElementById('company_city').style.border = '';
            document.getElementById('help-text-company-city').innerHTML = '';
            document.getElementById('company_pincode').style.border = '';
            document.getElementById('help-text-company_pincode').innerHTML = '';
            document.getElementById('company_country').style.border = '';
            document.getElementById('help-text-company-country').innerHTML = '';
        }
    }
    $.ajax({
        url: "/signup/onchange_save_field/",
        method: "POST",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        data: {
            username: user_name,
            value: value,
            name: name
        },
        success: function (response) {
            onchange_visit(id);
        },
        error: function (response) {},
    });
}

function onchange_visit(id) {
    var visit = validating_personal_information_page(false);
    $.ajax({
        url: "/signup/onchange_save_field/",
        method: "POST",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        data: {
            username: user_name,
            value: visit,
            name: 'is_submitted_all'
        },
        success: function (response) {},
        error: function (response) {},
    });
}

function validating_personal_information_page(is_validate) {
    var missed_filed_count = 0;
    var pan_validate = /^([a-zA-Z]{3})([pPcC]{1})([a-zA-Z]{1})(\d{4})([a-zA-Z]{1})$/;
    var pan_no = $("#pan_no").val();
    if (user_agent_country == "IN") {
        if (!$('.fileinput-new').hasClass('hide')) {
            if (is_validate) {
                html_text = 'Please Upload The PAN Document';
                help_field_id = 'help-pan-no';
                $('#' + help_field_id).html(html_text);
                $('#pan_card').addClass('add-shadow');
            }
            missed_filed_count++;
        }
    }
    if (user_agent_country == "IN") {
        if (!pan_no.match(pan_validate)) {
            if (is_validate) {
                $("#pan_no").css('border', '1px solid #C32F2F');
                $('#help-pan-no').html('Please Enter Valid PAN Number');
                $("#pan_no").val('');
                $("#pan_no").focus();
            }
            missed_filed_count++;
        }
    }
    var mother_tongue = $("#mother_tongue").val();
    if (mother_tongue.trim().length == 0) {
        if (is_validate) {
            document.getElementById('mother_tongue').style.border = '1px solid #C32F2F';
            if (user_agent_country == "IN") {
                document.getElementById('help-text-language_mother_tongue').innerHTML = 'Please Enter Mother Tongue';
            } else {
                document.getElementById('help-text-language_mother_tongue').innerHTML = 'Please Enter Primary Language spoken';
            }
            $("#mother_tongue").focus();
        }
        missed_filed_count++;
    } else {
        if(is_validate){
            if (!validate_alpha('mother_tongue')) {
                missed_filed_count++;
            }
        }

    }
    var languages_known_read_write = $("#languages_known_read_write").val();
    if (languages_known_read_write.trim().length == 0) {
        if (is_validate) {
            document.getElementById('languages_known_read_write').style.border = '1px solid #C32F2F';
            document.getElementById('help-text-languages_known_read_write').innerHTML = 'Please Enter Languages known to Read & Write';
            $("#languages_known_read_write").focus();
        }
        missed_filed_count++;
    } else {
        if(is_validate){
            if (!validate_alpha('languages_known_read_write')) {
                missed_filed_count++;
            }
        }
    }
    var language_known = $("#language_known").val();
    if (language_known.trim().length == 0) {
        if (is_validate) {
            document.getElementById('language_known').style.border = '1px solid #C32F2F';
            document.getElementById('help-text-language_known').innerHTML = 'Please Enter Languages known to Speak';
            $("#language_known").focus();
        }
        missed_filed_count++;
    } else {
        if(is_validate){
            if (!validate_alpha('language_known')) {
                missed_filed_count++;
            }
        }
    }
    var primary = $('input[name="primary_communication_address"]:checked').val();
    if (primary == 'office') {
        var company_country = $("#company_country").val();
        if (company_country == '' || company_country == 'Select') {
            if (is_validate) {
                document.getElementById('company_country').style.border = '1px solid #C32F2F';
                document.getElementById('help-text-company-country').innerHTML = 'Please Enter Country';
                $("#company_country").focus();
            }
            missed_filed_count++;
        }
        var pincode = $("#company_pincode").val();
        if (pincode == '') {
            if (is_validate) {
                document.getElementById('company_pincode').style.border = '1px solid #C32F2F';
                document.getElementById('help-text-company_pincode').innerHTML = 'Please Enter zipcode';
                $("#company_pincode").focus();
            }
            missed_filed_count++;
        }
        var city = $("#company_city").val();
        if (city == '') {
            if (is_validate) {
                document.getElementById('company_city').style.border = '1px solid #C32F2F';
                document.getElementById('help-text-company-city').innerHTML = 'Please Enter City';
                $("#company_city").focus();
            }
            missed_filed_count++;
        }
        var address = $("#company_address2").val();
        if (address == '') {
            if (is_validate) {
                document.getElementById('company_address2').style.border = '1px solid #C32F2F';
                document.getElementById('help-text-company-address2').innerHTML = 'Please Enter Address Line2';
                $("#company_address2").focus();
            }
            missed_filed_count++;
        }
        var street_name = $('#company_address1').val();
        if (street_name == '') {
            if (is_validate) {
                document.getElementById('company_address1').style.border = '1px solid #C32F2F';
                document.getElementById('help-text-company-address1').innerHTML = 'Please Enter Address Line1';
                $("#company_address1").focus();
            }
            missed_filed_count++;
        }
    } else {
        document.getElementById('company_address1').style.border = '';
        document.getElementById('help-text-company-address1').innerHTML = '';
        document.getElementById('company_address2').style.border = '';
        document.getElementById('help-text-company-address2').innerHTML = '';
        document.getElementById('company_city').style.border = '';
        document.getElementById('help-text-company-city').innerHTML = '';
        document.getElementById('company_pincode').style.border = '';
        document.getElementById('help-text-company_pincode').innerHTML = '';
        document.getElementById('company_country').style.border = '';
        document.getElementById('help-text-company-country').innerHTML = '';
    }
    if(!validate_website_url('company_website')){
        missed_filed_count++;
    }
    var designation = $("#designation").val();
    if (designation == '') {
        if (is_validate) {
            document.getElementById('designation').style.border = '1px solid #C32F2F';
            document.getElementById('help-text-designation').innerHTML = 'Please Enter Position';
            $("#designation").focus();
        }
        missed_filed_count++;
    }
    var company_name = $("#company_name").val();
    if (company_name == '') {
        if (is_validate) {
            document.getElementById('company_name').style.border = '1px solid #C32F2F';
            document.getElementById('help-text-company-name').innerHTML = 'Please Enter Company';
            $("#company_name").focus();
        }
        missed_filed_count++;
    }
    if (x == 0) {
        x = 1;
    }
    if (z == 0) {
        z = 1;
    }

    if (is_validate) {
        var missed_practice_country = validate_pracrtice_country(true)
        if (missed_practice_country == 1) {
            missed_field = 1;
        }
    } else {
        if (missed_practice_country == 1) {
            missed_field = 1;
        }
        validate_pracrtice_country(false)
    }
    
    var practice_value1 = '';
    var practice_value2 = '';
    for (var j = 0; j < allidsp.length; j++) {
        var i = allidsp[j];
        var practice_country = document.getElementById('practice_country' + i).value;
        var practice_city = document.getElementById('practice_city' + i).value;
        if (user_agent_country == default_country) {
            var practice_location = document.getElementById('practice_location' + i).value;
        } else {
            var practice_location = '';
        }
        var practice_pincode = document.getElementById('practice_pincode' + i).value;
        if (j == 0) {
            practice_value1 = '[{"practice_country":"' + practice_country + '","practice_city":"' + practice_city + '","practice_location":"' + practice_location + '","practice_pincode":"' + practice_pincode + '"}';

        } else if (i == z) {
            practice_value2 = ',{"practice_country":"' + practice_country + '","practice_city":"' + practice_city + '","practice_location":"' + practice_location + '","practice_pincode":"' + practice_pincode + '"}';

        } else {
            practice_value2 = ',{"practice_country":"' + practice_country + '","practice_city":"' + practice_city + '","practice_location":"' + practice_location + '","practice_pincode":"' + practice_pincode + '"}';
        }
        practice_value1 = practice_value1 + practice_value2;

    }
    practice_value3 = ']';
    if (practice_value1 != '') {
        practice_value1 = practice_value1 + practice_value3;
    }
    document.getElementById("hidden_practice_details_input").value = practice_value1;
    if (missed_filed_count < 1) {
        return true;
    } else {
        return false;
    }
}

function validate_pan(id) {
    var pan_validate = /^([a-zA-Z]{3})([pPcC]{1})([a-zA-Z]{1})(\d{4})([a-zA-Z]{1})$/;
    var pan_no = document.getElementById(id).value;
    if (!pan_no.match(pan_validate)) {
        $("#pan_no").css('border', '1px solid #C32F2F');
        $('#help-pan-no').html('Please Enter Valid PAN Number');
        $("#pan_no").focus();
        document.getElementById(id).value = '';
    } else {
        $('#help-pan-no').html('');
        $("#pan_no").css('border', '1px #bfbfbf solid');
    }
}

function user_profile_autosave() {
    var validation_result = validating_personal_information_page(true);
    var question_result = validate_business_information_form();
    var practice_validation_result = validate_pracrtice_country(true);
    if (validation_result && question_result && practice_validation_result) {
        $('#submit1').prop('disabled', true);
        $.ajax({
            url: "/signup/user_profile_basicdetails/",
            method: "POST",
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", token);
            },
            data: {
                designation: $("#designation").val(),
                annual_income: $("#annual_income").val(),
                company_website: $("#company_website").val(),
                company_address1: $("#company_address1").val(),
                company_address2: $("#company_address2").val(),
                company_city: $("#company_city").val(),
                company_pincode: $("#company_pincode").val(),
                company_name: $("#company_name").val(),
                company_state: $("#company_state").val(),
                company_country: $("#company_country").val(),
                language_known: $("#language_known").val(),
                languages_known_read_write: $("#languages_known_read_write").val(),
                pan_no: $("#pan_no").val(),
                hidden_practice_details_input : $("#hidden_practice_details_input").val(),
                is_submitted_all: true
            },
            success: function (response) {
                advisorQuestionAnwserSave();
            },
            error: function (response) {}
        });

    }
}


function validate_website_url(id){
    var token = csrf_token;
    var domain = document.getElementById(id).value;
    var re = new RegExp(
        /^(http[s]?:\/\/){0,1}(www\.){0,1}[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,5}[\.]{0,1}/);
    if(domain){
        if (domain.match(re)){
            modify_web_url(id);
            return true;
        }else{
            $("#"+id).focus();
            $("#help-text-"+id).html('Please Enter valid domain URL');
            return false;
        }   
    }else{
        $("#help-text-"+id).html('');
        return true;
    }
}