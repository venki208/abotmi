var allids = [];
var x = 0;
var max_fields = 5;
var wrapper = $("#awards_and_rewards_div");

// Intializing the country code to mobile number fields
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

// validating the add affilate form
function validate_form() {
    var missed_field = 0;
    var i = 0;
    var field_ids = ['iagree', 'document_e_brochure', 'point_of_contact_phone_number', 'point_of_contact_email_id',
        'point_of_contact_name', 'state', 'city', 'location', 'address_line_2', 'company_address', 'no_of_clients', 'no_of_employees', 'cin_no', 'company_description',
        'company_objective', 'company_url', 'company_tagline', 'company_name', 'document']
    var validation_messages = ['Please accept Terms and Conditions', 'Please upload company e-Brochure', 'Please enter mobile number', 'Please enter email ID', 'Please enter name', 'Please enter state', 'Please enter city', 'Please enter location', 'Please enter address line 2', 'Please enter address line 1', 'Please enter company description', 'Please enter company objective', 'Please enter company URL', 'Please enter company tagline', 'Please enter company name', 'Please upload company logo']
    for (i = 0; i <= field_ids.length; i++) {
        if (field_ids[i] == 'iagree') {
            if (document.getElementById(field_ids[i]).checked == false) {
                $('#' + field_ids[i]).addClass('not_valid');
                $('#' + field_ids[i]).focus();
                $('#help-text-' + field_ids[i]).html(validation_messages[i]);
                missed_field++;
            }
        }
        else if ($.trim($('#' + field_ids[i]).val()) == '' && $('#' + field_ids[i]).val() == '') {
            $('#' + field_ids[i]).addClass('not_valid');
            $('#' + field_ids[i]).focus();
            $('#help-text-' + field_ids[i]).html(validation_messages[i]);
            missed_field++;
        }
    }
    for (var j = 0; j < allids.length; j++) {
        var i = allids[j];
        if ($('#awards_and_rewards' + i).val() == "") {
            $("#awards_and_rewards" + i).addClass("not_valid");
            $("#help_awards_and_rewards" + i).html('Please Enter Awards And Rewards');
            document.getElementById('awards_and_rewards' + i).focus();
            missed_field++;
        } else {
            $("#awards_and_rewards" + i).removeClass('not_valid');
            document.getElementById('help_awards_and_rewards' + i).innerHTML = '';

        }
    }
    if (missed_field == 0) {
        $('#company_profile').modal('show');
        creating_institutions_json();
        if (validation_awards_rewards()) {
            $('#reia_contact_form').submit();
        }
    }
}

// generatings institutation json
function creating_institutions_json() {
    var value1 = '';
    var value2 = '';
    if (allids.length > 0) {
        for (var j = 0; j < allids.length; j++) {
            var i = allids[j];
            var awards_and_rewards = document.getElementById('awards_and_rewards' + i).value;
            if (i == allids[0]) {
                value1 = '[{"awards_and_rewards":"' + awards_and_rewards + '"}';

            } else {
                value2 = ',{"awards_and_rewards":"' + awards_and_rewards + '"}';
            }
            value1 = value1 + value2;
        }
        value3 = ']';
        value1 = value1 + value3;
    }
    document.getElementById("all_awards_and_rewards").value = value1;
}

// setting company email to email field
function set_email_value(id, domain_id) {
    var company_name_before_domain = $('#' + id).val();
    var company_domain_name = $("#" + domain_id).html();
    var total_company_email_id = company_name_before_domain + company_domain_name;
    $("#id_final_company_email").val(total_company_email_id);
    validate_input('id_final_company_email');
}

// Adding dynamic empty fields to awards and rewards
function add_awards_and_rewards() {
    if (validation_awards_rewards()) {
        if (allids.length < max_fields) {
            x++;
            allids.push(x);
            $(wrapper).append('<div class="row n-margin-0"><div class="col-md-11 col-xs-11 col-sm-11" id="awards_and_rewards_sub' + x + '" ><div class="col-md-8 col-xs-8 col-sm-8"><div class="control"><input type="text" class="form-control" name="awards_and_rewards' + x + '" id="awards_and_rewards' + x + '" placeholder="Awards and Rewards" ></input><span class="help-block" id="help_awards_and_rewards' + x + '"></span></div></div><div class="col-md-1 col-xs-1 col-sm-1"><a class = "remove_field btn additional_btn" id = "remove_field" onClick="remove_data(' + x + ');"><i class="fa fa-minus-circle" ></i></a></div></div>');
        }
    }
}

// removing awards and rewards fields row
function remove_data(id) {
    $('#awards_and_rewards_sub' + id).remove();
    var i = allids.indexOf(id);
    if (i != -1) {
        allids.splice(i, 1);
    }
}

// validating the awards and rewards
function validation_awards_rewards() {
    flag = true;
    for (var j = 0; j < allids.length; j++) {
        var i = allids[j];
        if ($('#awards_and_rewards' + i).val() == "") {
            $("#awards_and_rewards" + i).addClass("not_valid");
            $("#help_awards_and_rewards" + i).html('Please Enter Awards And Rewards');
            document.getElementById('awards_and_rewards' + i).focus();
            flag = false;
        } else {
            $("#awards_and_rewards" + i).removeClass('not_valid');
            document.getElementById('help_awards_and_rewards' + i).innerHTML = '';

        }

    }
    return flag;
}