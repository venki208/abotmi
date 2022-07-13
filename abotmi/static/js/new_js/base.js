/**
 * Global CSRF token 
 * @use: sending with headers in ajax requests
 *     -> call any where this variable to pass csrf token
 */
var csrf_token = $("#id_csrf_token").val();

/**
 * Common Validatation function
 * @param(1): field id of html attr
 * @param(2): help block id to display the validation message
 * @param(3): Field name of html attr
 */
function validate_field_onkeypress(field_id, help_id, field_name){
    var is_max_length = $("#"+field_id).attr("max-length");
    var is_min_length = $("#"+field_id).attr("min-length");
    var is_required = $("#"+field_id).attr("required");
    var is_email = $("#"+field_id).attr("is-email");
    var is_password = $("#"+field_id).attr("pwd-check");
    var is_number = $("#"+field_id).attr("is-num");
    var is_mobile = $("#"+field_id).attr("is-mobile");
    var is_url = $("#"+field_id).attr("is-url");
    var is_batch = $("#"+field_id).attr("is-batch");
    var is_select = $("#" + field_id).attr("is-select");
    var is_text = $("#" + field_id).attr("is-text");
    var field_val = $("#"+field_id).val();
    var missed_field = 0;
    var v_m = '';

    if(missed_field == 0){
        $("#"+field_id).removeClass('not_valid');
        $("#"+help_id).html('');
        missed_field = 0;
    }
    if(is_max_length){
        if (is_max_length < $("#"+field_id).val().length){
            if(is_number){
                v_m = ' numbers';
            }else{
                v_m = ' characters';
            }
            $("#"+help_id).html('Please enter less than '+is_max_length+v_m);
            $("#"+field_id).addClass("not_valid");
            $("#"+field_id).focus();
            missed_field = 1;
        }
    }
    if(is_min_length){
        if(is_min_length > $("#"+field_id).val().length
            && $("#"+field_id).val() != ''){
            if(is_number){
                v_m = ' numbers';
            }else{
                v_m = ' characters';
            }
            $("#"+help_id).html('Please enter minimum '+is_min_length+v_m);
            $("#"+field_id).addClass("not_valid");
            $("#"+field_id).focus();
            missed_field = 1;
        }
    }
    if(is_number){
        var re = /^[0-9]*$/;
        if(!re.test($("#"+field_id).val())){
            $("#"+help_id).html('Please Enter Only Numbers');
            $("#"+field_id).addClass("not_valid");
            $("#"+field_id).focus();
            missed_field = 1;
        }
    }
    if(is_url){
        var re = /^(http[s]?:\/\/){0,1}(www\.){0,1}[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,5}[\.]{0,1}/;
        if($("#"+field_id).val()){
            if(!re.test($("#"+field_id).val())){
                $("#"+help_id).html('Please Enter Vaild URL');
                $("#"+field_id).addClass("not_valid");
                $("#"+field_id).focus();
                missed_field = 1;
            }
        }else{
            $("#"+help_id).html('');
            $("#"+field_id).removeClass("not_valid");
        }
    }
    if(is_required){
        var fld_val = $("#" + field_id).val();
        if (fld_val == '' || fld_val == 'select' || !fld_val) {
            var field_type;
            if (is_select) {
                field_type = 'Select';
            } else {
                field_type = 'Please enter';
            }
            $("#" + help_id).html(field_type + ' ' + field_name);
            $("#" + field_id).addClass("not_valid");
            $("#" + field_id).focus();
            missed_field = 1;
        }
    }
    if (is_email && field_val != ''){
        var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
        if(!re.test($.trim($("#"+field_id).val()))){
            $("#"+help_id).html('Please Enter Valid Email ID');
            $("#"+field_id).addClass("not_valid");
            $("#"+field_id).focus();
            missed_field = 1;
        }
    }
    if(is_password){
        var re  = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$/;
        if(!re.test($("#"+field_id).val())){
            $("#"+help_id).html('Please make sure you follow the instructions');
            $("#"+field_id).addClass("not_valid");
            $("#"+field_id).focus();
            missed_field = 1;
        }
    }
    if(is_mobile&& field_val != ''){
        var isValidNumber = $('#'+field_id).intlTelInput("isValidNumber");
        if (!isValidNumber) {
            $("#"+help_id).html('Please Enter Valid Mobile Number');
            $("#"+field_id).addClass("not_valid");
            $("#"+field_id).focus();
            missed_field = 1;
        }
    }
    if (is_text) {
        var text_re = /^[a-zA-Z ]+$/;
        if (!text_re.test($("#" + field_id).val()) && $.trim($("#" + field_id).val()) != '') {
            $("#" + help_id).html('Please enter only characters');
            $("#" + field_id).addClass("not_valid");
            $("#" + field_id).focus();
            missed_field = 1;
        }
    }
    if(is_batch){
        // allows only a-z A-z 0-9 _ -
        var bth_re = /^[A-Za-z0-9_-]*$/;
        if (!bth_re.test($("#"+field_id).val())){
            $("#" + help_id).html('Please Enter Valid Batch Code');
            $("#" + field_id).addClass("not_valid");
            $("#" + field_id).focus();
            missed_field = 1;
        }
    }
    return missed_field;
}

/**
 * @use: Commomn function for validating Recaptcha
 * @param(1): widget id to check Recaptcha completed or not
 * @param(2): help block id to display the validation message
*/
function validate_recptcha(widget_id, help_id) {
    var is_recaptcha = grecaptcha.getResponse(widget_id);
    if (is_recaptcha){
        $("#"+help_id).html('');
        $("#"+help_id).removeClass('recaptcha-help-block');
        return true;
    }else{
        $("#"+help_id).addClass('recaptcha-help-block');
        $("#"+help_id).html('Please Complete the Recaptcha');
        return false;
    }
}

/**
 * @use: ajax function for Checkgin Email is exists or not in database
 * @param(1): Users Email
 * @returns Response with callback functions
*/
// checking requested email is exists or not
function check_email(email_id) {
    var token = csrf_token;
    return $.ajax({
        type: "POST",
        url: "/signup/check_email/",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        data:{'username': email_id}
    });
}

function check_user_exist(email_id) {
    var token = csrf_token;
    return $.ajax({
        type: "POST",
        url: "/signup/check_user_exist/",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        data:{'username': email_id}
    });
}

// applying blur when modal will trigger
$('.modal').on('show.bs.modal', function () {
    $('.container').addClass('blur');
});
// removing blur when modal will close
$('.modal').on('hide.bs.modal', function () {
    $('.container').removeClass('blur');
});

/** 
 * @use: Function for Getting Mobile number with country code
 * @param {HTMLElementAttribute} (widget)
 *      @ex: get_mobile_no('#id') or get_mobile_no('[name="name"]')
*/
function get_mobile_no(widget){
    var mobile = $(widget).intlTelInput("getNumber").trim().replace(/\s+/g, "");
    return mobile;
}

/**
 * @use: Setting mobile number with country code
 * @param {HTMLElementAttribute} (widget)
 *      need to pass '#id' or '[name="name"]' etc..
 * @param {String} (value)
 *      mobile number as string format
*/
function set_mobile_no(widget, value){
    $(widget).intlTelInput("setNumber", value);
}

/**
 * @use: Getting address by replacing <br /> tag into '\n'
 * @param {HTMLElementAttribute} (widget)
 *      need to pass '#id' or '[name="name"]' etc...
*/
function get_address(widget) {
    var address = $(widget).val().replace(new RegExp('\n','g'), '<br />');
    return address;
}

/**
 * @use: Setting address into HTMLElement by replacing '\n' into <br />
 * @param {HTMLEelementAttribute} (widget)
 *      need to pass '#id' or '[name="name"]' etc...
 * @param {String} (value)
 *      need to pass value
*/
function set_address(widget, value) {
    final_val = value.replace(new RegExp('&lt;br /&gt;','g'), '\n');
    $(widget).val(final_val);
}

/**
 * @use: Removing value from array and returns final array
 * @param {array} (array) -> need to pass array
 * @param (value) -> need to pass removed value from the array
 */
// function for removing value from array and return the array
function remove_value_from_array(array, removed_value){
    array = jQuery.grep(array, function (value) {
        return value != removed_value;
    });
    return array;
}

// setting csrf token to request headers
function setHeader(xhr) {
    xhr.setRequestHeader("X-CSRFToken", csrf_token);
}

/**
 * @use: To load the Get Advise Modal
*/
function get_advice(id, name, email){
    if (email && email != 'None' && email != ''){
        if(id!=undefined && name!=undefined && email!=undefined){
            url = "/member/advice_form/?adv_id="+id+"&adv_name="+name+"&advisor_email="+email;
        }else{
            url = "/member/advice_form/";
        }
        $.ajax({
            type: "GET",
            url: url,
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", token);
            },
            success: function(response){
                $('#common_base_modal').html('');
                $('#common_base_modal').html(response);
                $('#get-advice-modal').modal({
                    show:true,
                    keyboard:false,
                    backdrop:'static'
                });
            }
        });
    }else{
        show_alert(
            'warning',
            '',
            "<p>Selected Advisor's Email is not available.</p>"
        );
    }
}

/**
 * header menu responsive
 */

var slide_wrp 		= ".side-menu-wrapper"; //Menu Wrapper
var open_button 	= ".menu-open"; //Menu Open Button
var close_button 	= ".menu-close"; //Menu Close Button
var overlay 		= ".menu-overlay"; //Overlay

//Initial menu position
$(slide_wrp).hide().css( {"right": -$(slide_wrp).outerWidth()+'px'}).delay(50).queue(function(){$(slide_wrp).show()}); 

$(open_button).click(function(e){ //On menu open button click
  e.preventDefault();
  $(slide_wrp).css( {"right": "0px"}); //move menu right position to 0
  setTimeout(function(){
    $(slide_wrp).addClass('active'); //add active class
  },50);
  $(overlay).css({"opacity":"1", "width":"100%"});
});

$(close_button).click(function(e){ //on menu close button click
  e.preventDefault();
  $(slide_wrp).css( {"right": -$(slide_wrp).outerWidth()+'px'}); //hide menu by setting right position 
  setTimeout(function(){
    $(slide_wrp).removeClass('active'); // remove active class
  },50);
  $(overlay).css({"opacity":"0", "width":"0"});
});

$(document).on('click', function(e) { //Hide menu when clicked outside menu area
  if (!e.target.closest(slide_wrp) && $(slide_wrp).hasClass("active")){ // check menu condition
    $(slide_wrp).css( {"right": -$(slide_wrp).outerWidth()+'px'}).removeClass('active');
    $(overlay).css({"opacity":"0", "width":"0"});
  }
});

$(document).on('show.bs.modal', '.modal', function (event) {
    var zIndex = 1040 + (10 * $('.modal:visible').length);
    $(this).css('z-index', zIndex);
    setTimeout(function () {
        $('.modal-backdrop').not('.modal-stack').css('z-index', zIndex - 1).addClass('modal-stack');
    }, 0);
});
$(document).on('hidden.bs.modal', '.modal', function () {
    $('.modal:visible').length && $(document.body).addClass('modal-open');
});