var allidsp = [];
var max_fields = 6;
var z = 0;
$(document).ready(function () {
    z = document.getElementById('practice_count').value;
    for (i = 1; i <= z; i++) {
        allidsp.push(i);
    }
});

var wrapper_practice = $(".input_practice_fields_wrap");
var add_practice_button = $(".add_practice_field");
$(add_practice_button).click(function (e) {
    document.getElementById('help-text-practice_details').innerHTML = '';
    var is_valid_practice_country = validate_pracrtice_country(true);
    e.preventDefault();
    if (is_valid_practice_country) {
        if (allidsp.length < max_fields) { //max input box allowed
            z++; //text box increment
            allidsp.push(z);
            if (user_agent_country == default_country) {
                $(wrapper_practice).append(
                    '<div class="row row_financial" id="practice' + z + '">' +
                    '<div  class="col-sm-4 col-md-4 col-lg-4 selection-btn left-no-padding">' +
                    '<select class="form-group form-control" name="practice_country' + z + '" id = "practice_country' + z + '" onchange="check_country_selected(id);"></select>' +
                    '<span class="help-block" id="help_text_practice_country' + z + '">' +
                    '</div>' +
                    '<div class="col-sm-4 col-md-4 col-lg-4 selection-btn">' +
                    '<input type="text" class="form-group form-control" name="practice_city' + z + '" id="practice_city' + z + '" onChange="validateCity(id,'+"'"+'help_text_practice_city' + z +"'"+');" >' +
                    '<span class="help-block" id="help_text_practice_city' + z + '">' +
                    '</div>' +
                    '<div class="col-sm-4 col-md-4 col-lg-4 selection-btn">' +
                    '<input type="text" class="form-group form-control" name="practice_location' + z + '" id="practice_location' + z + '" onChange="validateAlpha(id,'+"'"+'help_text_practice_location' + z +"'"+');" >' +
                    '<span class="help-block" id="help_text_practice_location' + z + '">' +
                    '</div>' +
                    '<div class="col-sm-3 col-md-3 col-lg-3 selection-btn">' +
                    '<input type="text" class="form-group form-control" name="practice_pincode' + z + '" id="practice_pincode' + z + '" onChange="validate_pincode(id);" >' +
                    '<span class="help-block" id="help-text-practice_pincode' + z + '">' +
                    '</div>' +
                    '<div class="col-sm-1 col-lg-1 col-md-1 mob-address-col">' +
                    '<div class="">' +
                    '<a class = "remove_field" id = "remove_field' + z + '" onClick="remove_practice_data(' + z + ');">' +
                    '<img style="margin-top: -2px; width: 30px;"src="/static/new_images/delete-icon.png">' +
                    '</a>' +
                    '</div>' +
                    '</div>' +
                    '</div>');
            } else {
                $(wrapper_practice).append(
                    '<div class="row row_financial" id="practice' + z + '">' +
                    '<div  class="col-sm-4 col-md-4 col-lg-4 selection-btn left-no-padding">' +
                    '<select class="form-group form-control" name="practice_country' + z + '" id = "practice_country' + z + '" onchange="check_country_selected(id);"></select>' +
                    '<span class="help-block" id="help_text_practice_country' + z + '">' +
                    '</div>' +
                    '<div class="col-sm-4 col-md-4 col-lg-4 selection-btn">' +
                    '<input type="text" class="form-group form-control" name="practice_city' + z + '" id="practice_city' + z + '" onChange="validateCity(id,'+"'"+'help_text_practice_city' + z +"'"+');" >' +
                    '<span class="help-block" id="help_text_practice_city' + z + '">' +
                    '</div>' +
                    '<div class="col-sm-3 col-md-3 col-lg-3 selection-btn">' +
                    '<input type="text" class="form-group form-control" name="practice_pincode' + z + '" id="practice_pincode' + z + '" onChange="validate_pincode(id);">' +
                    '<span class="help-block" id="help-text-practice_pincode' + z + '">' +
                    '</div>' +
                    '<div class="col-sm-1 col-lg-1 col-md-1 mob-address-col">' +
                    '<div class="">' +
                    '<a class = "remove_field" id = "remove_field' + z + '" onClick="remove_practice_data(' + z + ');">' +
                    '<img style="margin-top: -2px; width: 30px;"src="/static/new_images/delete-icon.png">' +
                    '</a>' +
                    '</div>' +
                    '</div>' +
                    '</div>');
            }
            $('#practice_country' + z).html(''); //Clear
            y = z - 1;
            $('#practice_countries option').clone().appendTo('#practice_country' + z);
        }
    }
});

// It removes the practice data
function remove_practice_data(id) {
    var e = document.getElementById("practice_country" + id);
    var strUser = e.options[e.selectedIndex].value;
    // add_options(strUser);
    $('#practice' + id).remove();
    var i = allidsp.indexOf(id);
    if (i != -1) {
        allidsp.splice(i, 1);
    }
}

// Function validates and returns pratice country details
function validate_pracrtice_country(is_validate) {
    missed_field_add = 0;
    for (var j = 0; j < allidsp.length; j++) {
        var i = allidsp[j];
        // var re = /^[a-zA-Z\. ]*$/;
        var val_practice_city = document.getElementById('practice_city' + i);
        var re = /^[a-zA-Z\. ]*$/;

        var re_pincode;
        if (user_agent_country == 'IN') {
            re_pincode = /^[0-9][0-9]{5}$/;
        } else {  
           re_pincode = /^([^ -](?=.*[0-9])(?=.*[a-zA-Z])([a-zA-Z0-9- ]{1,5}[^-!@#$%^*~` :_])|[^- ][0-9 -]{2,4}[^ -!@#$%^&*:_])$/;
        }
        var validexperience = document.getElementById('practice_pincode' + i);
        if (!validexperience.value.match(re_pincode)) {
            if (is_validate) {
                $("#practice_pincode" + i).addClass('not_valid');
                $("#help-text-practice_pincode" + i).html('Please enter Zip Code');
                $("#practice_pincode" + i).focus();
            }
            missed_field_add = 1;
        } else {
            $("#help_text_practice_pincode" + i).html('');
        }

        var val = $("#practice_city" + i).val();
        if (!val_practice_city.value.match(re) || !val_practice_city.value) {
            if (is_validate) {
                $("#practice_city" + i).addClass('not_valid');
                $("#help_text_practice_city" + i).html('Please enter practice city');
                $("#practice_city" + i).focus();
            }
            missed_field_add = 1;
        } else {
            $("#help_text_practice_city" + i).html('');
        }
        if (user_agent_country == default_country) {
            var val_practice_location = document.getElementById('practice_location' + i);
            if (!val_practice_location.value.match(re)) {
                if (is_validate) {
                    $("#practice_location" + i).addClass('not_valid');
                    $("#help_text_practice_location" + i).html('Please enter practice location');
                    $("#practice_location" + i).focus();
                }
                missed_field_add = 1;
            } else {
                $("#help_text_practice_location" + i).html(' ');
                document.getElementById('practice_location' + i).style.border = '';
            }
        }
        

        validinstruments = "";
        var val = $("#practice_country" + i).val();
        if (val == 'Select' || val == 'select') {
            if (is_validate) {
                $("#practice_country" + i).addClass('not_valid');
                $("#help_text_practice_country" + i).html('Please select practice country');
                $("#practice_country" + i).focus();
            }
            missed_field_add = 1;
        } else {
            $("#help_text_practice_country" + i).html('');
        }
    }
    if(missed_field_add){
        return false;
    }else{
        return true;
    }
    // return missed_field_add;
}

$(".input_practice_fields_wrap").find('select, input').on('change', function(e){
    validate_pracrtice_country(true);
});