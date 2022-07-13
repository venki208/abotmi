// It validates the pincode format with a regx
function validate_pincode(str){
    if (user_agent_country == 'IN'){
        var re = /^[0-9][0-9]{5}$/;
    }
    else{
        var re = /^([^ -](?=.*[0-9])(?=.*[a-zA-Z])([a-zA-Z0-9- ]{1,5}[^-!@#$%^*~` :_])|[^- ][0-9 -]{2,4}[^ -!@#$%^&*:_])$/;
    }
    var inputvalue = $("#"+str).val();
    if(inputvalue.match(re)){
        document.getElementById(str).style.border='';
        document.getElementById('help-text-'+str).innerHTML='';
    }else{
        var a=document.getElementById(str).value = "";
        document.getElementById(str).style.border='1px solid #C32F2F';
        document.getElementById('help-text-'+str).innerHTML='Please enter valid Zip Code';
        $("#"+str).focus();
    }
}

// Validate if input 0 in step-3
function validate_if_zero(str){
    var re = /^[0-9\b]+$/;
    var inputvalue = $("#"+str).val();
    if(inputvalue.match(re) && inputvalue > 0){
        document.getElementById(str).style.border='';
        if (str=='y-o-b' || str=='no_institutions') {
            document.getElementById('help-'+str).innerHTML='';
        }
        else{
            document.getElementById('help_text_'+str).innerHTML='';
        }
        if(str == 'total_client_served' || str == 'advisor_is_connected_with'){
            onchange_savequestions(str);
        }
    }else{
        var a=document.getElementById(str).value = "";
        document.getElementById(str).style.border='1px solid #C32F2F';
        if (str=='y-o-b' || str=='no_institutions') {
            document.getElementById('help-'+str).innerHTML='Enter Valid Input';
        }
        else{
            document.getElementById('help_text_'+str).innerHTML='Enter Valid Input';
        }
        $("#"+str).focus();
    }
}

// It validates the mobile phone with inTel plugin  
function validateMobile(id, help_id) {
    var isValidNumber = $('#mobile').intlTelInput("isValidNumber");
    if(isValidNumber == false){
        document.getElementById(id).value = "";
        $('#'+help_id).html('Enter Valid Mobile number');
        $('#mobile').focus();
    }else{
        $('#'+help_id).html('');
    }
}

// Function takes only alphabets
function validateAlpha(str,help_id) {
    var name = document.getElementById(str);
    if(name.value != ''){
        var alpha = /^[a-zA-Z()\s]+$/.test(name.value);
        if(alpha){
            return true;
        }
        else {
            $('#'+str).css('border', '1px solid #C32F2F');
            document.getElementById(str).value = "";
            $('#'+help_id).html('Enter Valid Input');
            return false;
        }
    }
}

// Function takes only alphabets and . for mother's name field only
function validateAlpha_mother_name(str,help_id) {
    var name = document.getElementById(str);
    if(name.value != ''){
        var alpha = /^[a-zA-Z()\s.]+$/.test(name.value);
        if(alpha){
            return true;
        }
        else {
            $('#'+str).css('border', '1px solid #C32F2F');
            document.getElementById(str).value = "";
            $('#'+help_id).html('Enter Valid Input');
            return false;
        }
    }
}




// Validates the names- first name, last name and middle name
$("#first_name").keypress(function(e){
    var inputValue = e.charCode;
    if(!(inputValue >= 65 && inputValue <= 122) && (inputValue != 32 && inputValue != 0)){
    $("#help_text_first_name").html("Name can have only characters and spaces");
    event.preventDefault();
    }
});
$("#last_name").keypress(function(e){
    var inputValue = e.charCode;
    if(!(inputValue >= 65 && inputValue <= 122) && (inputValue != 32 && inputValue != 0)){
    $("#help_text_last_name").html("Name can have only characters and spaces");
    event.preventDefault();
    }
});
$("#middle_name").keypress(function(e){
    var inputValue = e.charCode;
    if(!(inputValue >= 65 && inputValue <= 122) && (inputValue != 32 && inputValue != 0)){
    $("#help_text_middle_name").html("Name can have only characters and spaces").show().fadeOut(4000);
    event.preventDefault();
    }
});


$("#news_type").keypress(function(e){
    var inputValue = e.charCode;
    if(!(inputValue >= 65 && inputValue <= 122) && (inputValue != 32 && inputValue != 0)){
    $("#help_text_news_type").html("This field can have only characters and spaces").show().fadeOut(4000);
    event.preventDefault();
    }
});

$("#notice_date").keypress(function(e){
    var inputValue = e.charCode;
    if(!(inputValue >= 65 && inputValue <= 122) && (inputValue != 32 && inputValue != 0)){
    $("#help_text_notice_date").html("This field can have only Date format").show().fadeOut(4000);
    event.preventDefault();
    }
});

$("#headline").keypress(function(e){
    var inputValue = e.charCode;
    if(!(inputValue >= 65 && inputValue <= 122) && (inputValue != 32 && inputValue != 0)){
    $("#help_text_headline").html("This field can have only characters and spaces").show().fadeOut(4000);
    event.preventDefault();
    }
});


// Descrption: Cheking Communication email is checked or not and saving.
function check_communication_email(id,id2,id3){
    if(document.getElementById(id).checked == true){
        document.getElementById(id2).checked=false;
        $('#'+id2).parent().removeClass("selected");
        if(id == 'communication_email_primary'){
            var email_value = $("#primary_email").val();
        }else {
            var email_value = $("#secondary_email").val();
        }
        if(email_value != ''){
            save_onchange('communication_email_id',id,'help-text-secondary_email');
        }
        if(id2 == 'communication_email_secondary'){
            document.getElementById('secondary_email').style.border='1px #bfbfbf solid';
            document.getElementById(id3).innerHTML = '';
        }
    }
}


function validateAlphaNumeric(field, str) {
    var field_value = $('#' + field).val();
    if (field != '') {
        var alphanumeric = /^([0-9a-zA-Z]){1,15}$/.test(field_value);
        if (!alphanumeric) {
            alert('Please Enter Valid' + str);
            $('#' + field).focus();
            return false;
        } else
            return true;
    }
}

function validateCity(str, help_id) {
    var name = document.getElementById(str);
    if (name.value != '') {
        var alpha = /^[a-zA-Z\. ]*$/.test(name.value);
        if (alpha) {
            $('#' + help_id).html('');
            return true;
        } else {
            $('#' + str).css('border', '1px solid #C32F2F');
            document.getElementById(str).value = "";
            $('#' + help_id).html('Enter Valid Input');
            return false;
        }
    }
}

function check_country_selected(id){
    var c_v = $("#"+id).val();
    if(c_v !='Select' && c_v != ''){
        $("#help_text_"+id).html('');
    }else{
        $("#help_text_"+id).html('Please select practice country');
    }
}