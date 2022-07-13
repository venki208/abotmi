// CSRF token initializing
var csrf_token = $("#id_csrf_token").val();

// return date input tag
function return_date_input_tag(id_rera){
    return '<div class="input-group date">'+
            '<input type="text" class="form-control datetimepicker" id="rera_expire_date'+id_rera+'" name="rera_expire_date'+id_rera+'" placeholder="Valid up to" value="" onchange="check_rera_or_dsa_field(id,'+"'"+"'"+','+"'"+'rera'+"'"+');">'+
            '<span class="input-group-addon" style="top: auto;">'+
                '<i class="fa fa-calendar" onClick="show_date_for_rera('+id_rera+');" aria-hidden="true"></i>'+
            '</span>'+
            '<span class="help-block register_with" id="help_rera_expire_date'+id_rera+'"></span>'+
        '</div> '
}

// Initialzing the values to the respective fields
if (dsa_details == 'None'){
    dsa_details = '';
}
if((sebi_no != '') || (sebi_expired != '')){
    if((sebi_no != 'None' && sebi_no != '')||(sebi_expired != 'None' && sebi_expired != '')
        ||(sebi_start != 'None' && sebi_start != '')){
        document.getElementById('certification_sebi').checked = true;
        display_certification_details('certification_sebi',"unclicked");
        $('#id_sebi_document').show();
    }else{
        $('#id_sebi_document').hide();
    }
}
if((amfi_no !='') || (amfi_expired != '')){
    if((amfi_no != 'None' && amfi_no !='') || (amfi_expired != '' &&amfi_expired != 'None')
        ||(amfi_start != 'None' && amfi_start != '')){
        document.getElementById('certification_amfi').checked =true;
        display_certification_details('certification_amfi',"unclicked");
        $('#id_amfi_document').show();
    }else{
        $('#id_amfi_document').hide();
    }
}
if ((irda_no !='') || (irda_exired != '')){
    if((irda_no !='None' && irda_no !='') || (irda_exired != 'None' && irda_exired != '')
        ||(irda_start != 'None' && irda_start != '')){
        document.getElementById('certification_irda').checked=true;
        display_certification_details('certification_irda',"unclicked");
        $('#id_irda_document').show();
    }else{
        $('#id_irda_document').hide();
    }
}
if((others !='') || (other_registration_no!= '') || (other_expiry_date!= '')){
    if((others !='None' && others !='')||(other_expiry_date !='None' && other_expiry_date!= '') || (other_registration_no!= 'None' && other_registration_no!= '')){
        document.getElementById('certification_others').checked=true;
        display_certification_details('certification_others',"unclicked");
    }else{
        $('#id_others_document').hide();
    }
}
if(is_rera == 'True'){
    document.getElementById('certification_rera').checked=true;
}
if(dsa_details != ''){
    document.getElementById('certification_dsa').checked=true;
}

$('.datetimepicker').on('keypress', function(e) {
    e.preventDefault(); // Don't allow direct editing
});

$("#datetimepicker_expiry_rera").datetimepicker({
    minView: 2,
    startView: 2,
    autoclose: true,
    format: 'dd-mm-yyyy',
    endDate: '+0d'
});

// attaching click event to sebi docuement icon
$("#id_sebi_document").bind('click', ['sebi'], show_regulatory_documents);
$("#id_amfi_document").bind('click', ['amfi'], show_regulatory_documents);
$("#id_irda_document").bind('click', ['irda'], show_regulatory_documents);
$("#id_others_document").bind('click', ['reg_others'], show_regulatory_documents);

function customCheckbox(checkboxName){
    var checkBox = $('input[name="'+ checkboxName +'"]');
    $(checkBox).each(function(){
        $(this).wrap( "<span class='custom-checkbox'></span>" );
        if($(this).is(':checked')){
            $(this).parent().addClass("selected");
        }
    });
    $(checkBox).click(function(){
        $(this).parent().toggleClass("selected");
    });
}
$(document).ready(function (){
    customCheckbox("certification_AMFI");
    customCheckbox("certification_IRDA");
    customCheckbox("certification_SEBI");
    customCheckbox("certification_OTHERS");
    customCheckbox("certification_RERA");
    customCheckbox("certification_DSA");
});

// value initializing
var id_dsa = 1;
if(dsa_id_value >1 ){
    var id_dsa = dsa_id_value;
}else{
    var id_dsa=1;
}

// for adding the additional fields in DSA details 
function add_dsa_fields() {
    if(document.getElementById('certification_dsa').checked){
        var dsa_validation_result = dsa_json_output_result();
        if(dsa_validation_result[1] == 0 ){
            id_dsa++;
            $('\
            <div id="div_dsa_id'+id_dsa+'" class="dsa_div_row row no-padding">'+
                '<div class="form-group col-md-2 col-sm-2 col-lg-2 checkbox-rcerrtification"></div>'+
                '<div class="form-group col-md-3 col-sm-3 col-lg-3 others">'+
                    '<input type="text" class="form-control" id="dsa_registration_no'+id_dsa+'" name="dsa_registration_no'+id_dsa+'" placeholder="Bank Name." value="" onchange="check_rera_or_dsa_field(id,'+"'"+"'"+','+"'"+'rera'+"'"+');">'+
                    '<span class="help-block register_with" id="help_dsa_registration_no'+id_dsa+'"></span>'+
                '</div>'+
                '<div class="form-group col-md-3 col-sm-3 col-lg-3 others">'+
                    '<input type="text" class="form-control" id="dsa_code_no'+id_dsa+'" name="dsa_code_no'+id_dsa+'" placeholder="DSA Codeee" value="" onchange="check_rera_or_dsa_field(id,'+"'"+"'"+','+"'"+'rera'+"'"+');">'+
                    '<span class="help-block register_with" id="help_dsa_code_no'+id_dsa+'"></span>'+
                '</div> '+
                '<div class="form-group col-md-3 col-sm-3 col-lg-3 others inside-form date-picker-last-view">'+
                    '<input type="text" class="form-control" id="dsa_how_long_associated'+id_dsa+'" name="dsa_how_long_associated'+id_dsa+'" placeholder="how long associated with?" value="" onchange="reraExperience(id,'+id_dsa+');check_rera_or_dsa_field(id,'+"'"+"'"+','+"'"+'rera'+"'"+');">'+
                    '<span class="help-block register_with" id="help_dsa_how_long_associated'+id_dsa+'"></span>'+
                '</div>'+
                '<a class="btn additional_btn dsa_remove" id="div_dsa_id'+id_dsa+'" onClick="remove_dsa_row(id);">'+
                    '<i class="fa fa-minus-circle" ></i>'+
                '</a>'+
            '</div>').appendTo(additional_dsa_fields);
        }
    }
}

// removing the row when they click minus button
function remove_dsa_row(id) {
    $('#'+id).remove();
}

// getting the validation result and converting fields data into json value
function dsa_json_output_result() {
    var input_dsa_ids, dsa_value;
    var dsa_input_values = [];
    var i=0, dsa_missed_field=0;
    var $inputs = $('#dsa_subdetails :input');
    $inputs.each(function (index){
        input_dsa_ids = $(this).attr('id');
        dsa_value = $.trim($('#'+input_dsa_ids).val());
        if ((i==0) || (i%3==0)) {
            if(dsa_value == ''){
                dsa_missed_field = 1;
                $('#help_'+input_dsa_ids).html('Please Enter Bank name');
                $('#'+input_dsa_ids).focus();
            }else{
                dsa_input_values[i] = '"dsa_bank_name"'+":"+'"'+dsa_value+'"'+",";
            }
        }
        if ((i==1) || (i%3==1)) {
            if(dsa_value == ''){
                dsa_missed_field = 1;
                $('#help_'+input_dsa_ids).html('Please Enter Dsa Code');
                $('#'+input_dsa_ids).focus();
            }else{
                dsa_input_values[i] = '"dsa_code"'+":"+'"'+dsa_value+'"'+",";
            }
        }
        if ((i==2) || (i%3==2)) {
            if(dsa_value == ''){
                dsa_missed_field = 1;
                $('#help_'+input_dsa_ids).html('Please Enter How long associated with?');
                $('#'+input_dsa_ids).focus();
            }else{
                dsa_input_values[i] = '"dsa_how_long_associated"'+":"+'"'+dsa_value+'"';
            }
        }
        i++;
    });
    var dsa_json_index = 0;
    var dsa_json_output = [];
    var output = '{';
    for (var i = 0; i < dsa_input_values.length; i++) {
        var output = output +dsa_input_values[i];
        if((i+1)%3 == 0 && i != 0){
            var output = output+'}';
            dsa_json_output[dsa_json_index] = output;
            dsa_json_index ++;
            var output = '{';
        }
    }
    var dsa_json_final_output = [dsa_json_output, dsa_missed_field]
    return dsa_json_final_output;
}

//common function to get the date 
function show_date(elementID,checkbox_status){
        if(document.getElementById(checkbox_status).checked){
            $(elementID).datetimepicker("show");
        }
    }

//common function to get the rera date 
function show_date_for_rera(count){
    $('#rera_expire_date'+count).datetimepicker("show");
}

//Check the status of crisil, sebi, irda 
function check_advisor_is_crisil_sebi_irda(id,status) {
    if (crisil_certificate_valid == 'True' && changes_accepted == false){
        $("#id_confirm_change").attr("onclick", "accept_changes_sebi_irda("+"'"+id+"'"+");");
        $("#id_cancel_change").attr("onclick", "cancel_accept_changes("+"'"+id+"'"+","+status+");");
        $('#check_confirm_for_change').modal('show');
    }else{
        disable_fields(id);
    }
}

//get the changes and sents to save_register_with_data
function accept_changes_sebi_irda(id) {
    disable_fields(id);
    changes_accepted = true;
    save_register_with_data(id);
    $('#check_confirm_for_change').modal('hide');
}

// Disable fields after verfication 
function disable_fields(id){
    if (id=='certification_sebi'){
        if(document.getElementById('certification_sebi').checked){
            $("#help_text_register_with").html('');
            if(sebi_status != 'verified' && sebi_status != 'doc_uploaded'){
                $("#sebi_registration_no").prop('readonly', false);
            }
            $("#sebi_start_date").prop('readonly', false);
            $("#sebi_expiry_date").prop('readonly', false);
            $("#datetimepicker_start_sebi").datetimepicker({
                minView: 2,
                startView: 2,
                autoclose: true,
                format: 'dd-mm-yyyy',
                endDate: '+0d'
            });
            $("#datetimepicker_expiry_sebi").datetimepicker({
                minView: 2,
                startView: 2,
                autoclose: true,
                format: 'dd-mm-yyyy',
                endDate: '+0d'
            });
            // excludes sebi_expiry_date field  
            // $( "input[name='sebi_expiry_date']" ).datetimepicker( "option", "disabled", false );
            // $("input[name='sebi_expiry_date']").datetimepicker({
            //     minView: 2,
            //     startView: 2,
            //     autoclose: true,
            //     format: 'dd-mm-yyyy'
            //
            // });

        }
        else{
            $("#sebi_registration_no").prop('readonly', true);
            $("#sebi_start_date").prop('readonly', true);
            $("#sebi_expiry_date").prop('readonly', true);
            $("#sebi_registration_no").val('');
            $("#sebi_registration_no").css('border', '1px #bfbfbf solid');
            $("#sebi_start_date").val('');
            $("#sebi_expiry_date").val('');
            $("#help_text_sebi_number").html('');
            $("#help_text_sebi_expire_date").html('');
            $('#datetimepicker_start_sebi').datetimepicker('remove');
            $('#datetimepicker_expiry_sebi').datetimepicker('remove');
            // excludes sebi_expiry_date field
            // $( "input[name='sebi_expiry_date']" ).datetimepicker( "option", "disabled", true );

        }
    }
    if(id == 'certification_irda'){
        if(document.getElementById('certification_irda').checked){
            $("#help_text_register_with").html('');
            if(irda_status != 'verified' && irda_status != 'doc_uploaded'){
                $("#irda_registration_no").prop('readonly', false);
            }
            $("#irda_start_date").prop('readonly', false);
            $("#irda_expiry_date").prop('readonly', false);
            $("#datetimepicker_start_irda").datetimepicker({
                minView: 2,
                startView: 2,
                autoclose: true,
                format: 'dd-mm-yyyy',
                endDate: '+0d'
            });
            $("#datetimepicker_expiry_irda").datetimepicker({
                minView: 2,
                startView: 2,
                autoclose: true,
                format: 'dd-mm-yyyy',
                endDate: '+0d'
            }); 
            // excludes irda_expiry_date field now
            // $("#irda_expiry_date").datetimepicker({
            //     minView: 2,
            //     startView: 2,
            //     autoclose: true,
            //     format: 'dd-mm-yyyy',
            //     endDate: '+0d'
            // });
            // $( "input[name='irda_expiry_date']" ).datetimepicker( "option", "disabled", false );
            // $("input[name='irda_expiry_date']").datetimepicker({
            //     minView: 2,
            //     startView: 2,
            //     autoclose: true,
            //     format: 'dd-mm-yyyy'
            // });
        }
        else{
            $("#irda_registration_no").prop('readonly', true);
            $("#irda_start_date").prop('readonly', true);
            $("#irda_expiry_date").prop('readonly', true);
            $("#irda_registration_no").val('');
            $("#irda_registration_no").css('border', '1px #bfbfbf solid');
            $("#irda_start_date").val('');
            $("#irda_expiry_date").val('');
            $("#help_text_irda_number").html('');
            $("#help_text_irda_expire_date").html('');
            $('#datetimepicker_start_irda').datetimepicker('remove');
            $('#datetimepicker_expiry_irda').datetimepicker('remove');
            // excludes irda_expiry_date field now
            // $( "input[name='irda_expiry_date']" ).datetimepicker( "option", "disabled", true );

        }
    }
    if(id == 'certification_amfi'){
        if(document.getElementById('certification_amfi').checked){
            $("#help_text_register_with").html('');
            if(amfi_status != 'verified' && amfi_status != 'doc_uploaded'){
                $("#amfi_registration_no").prop('readonly', false);
            }
            $("#amfi_start_date").prop('readonly', false);
            $("#amfi_expiry_date").prop('readonly', false);
            $("#datetimepicker_start_amfi").datetimepicker({
                minView: 2,
                startView: 2,
                autoclose: true,
                format: 'dd-mm-yyyy',
                endDate: '+0d'
            });
            $("#datetimepicker_expiry_amfi").datetimepicker({
                minView: 2,
                startView: 2,
                autoclose: true,
                format: 'dd-mm-yyyy',
                endDate: '+0d'
            });
            // excludes amfi_expiry_date field now
            // $( "input[name='amfi_expiry_date']" ).datetimepicker( "option", "disabled", false );
            // $("input[name='amfi_expiry_date']").datetimepicker({
            //     minView: 2,
            //     startView: 2,
            //     autoclose: true,
            //     format: 'dd-mm-yyyy'
            // });
        }
        else{
            $("#amfi_registration_no").prop('readonly', true);
            $("#amfi_start_date").prop('readonly', true);
            $("#amfi_expiry_date").prop('readonly', true);
            $("#amfi_registration_no").val('');
            $("#amfi_registration_no").css('border', '1px #bfbfbf solid');
            $("#irda_start_date").val('');
            $("#amfi_expiry_date").val('');
            $("#help_text_amfi_number").html('');
            $("#help_text_amfi_expire_date").html('');
            $('#datetimepicker_start_amfi').datetimepicker('remove');
            $('#datetimepicker_expiry_amfi').datetimepicker('remove');
            // excludes amfi_expiry_date field now
            // $( "input[name='amfi_expiry_date']" ).datetimepicker( "option", "disabled", true );

        }
    }
    if(id == 'certification_others'){
        if(document.getElementById('certification_others').checked){
            $("#help_text_register_with").html('');
            $("#other_organisation").prop('readonly', false);
            $("#other_registration_no").prop('readonly', false);
            $("#other_expiry_date").prop('readonly', false);
            $("#datetimepicker_other").datetimepicker({
                minView: 2,
                startView: 2,
                autoclose: true,
                format: 'dd-mm-yyyy',
                endDate: '+0d'
            });
            // exclude - other_expiry_date field 
            // $( "input[name='other_expiry_date']" ).datetimepicker( "option", "disabled", false );
            // var altFormat = $("input[name='other_expiry_date']").datetimepicker({
            //     minView: 2,
            //     startView: 2,
            //     autoclose: true,
            //     format: 'dd-mm-yyyy'
            // });
        }
        else {
            $("#other_organisation").prop('readonly', true);
            $("#other_registration_no").prop('readonly', true);
            $("#other_expiry_date").prop('readonly', true);
            $("#other_organisation").val('');
            $("#other_organisation").css('border', '1px #bfbfbf solid');
            $("#other_registration_no").val('');
            $("#other_registration_no").css('border', '1px #bfbfbf solid');
            $("#other_expiry_date").val('');
            $("#other_expiry_date").css('border', '1px #bfbfbf solid');
            $("#help_text_other_organisation").html('');
            $("#help_text_other_registration").html('');
            $("#help_text_other_expiredate").html('');
            $('#datetimepicker_other').datetimepicker('remove');
            // exclude - other_expiry_date field
            // $( "input[name='other_expiry_date']" ).datetimepicker( "option", "disabled", true );
        }
    }
    if(id == 'certification_rera'){
        if(document.getElementById('certification_rera').checked){
           $("#help_text_register_with").html('');
           $("#rera_registration_no1").prop('readonly', false);
           $("#rera_state1").prop('readonly', false);
           $("#rera_expire_date1").prop('readonly', false);
           $("#datetimepicker_expiry_rera").datetimepicker({
               minView: 2,
               startView: 2,
               autoclose: true,
               format: 'dd-mm-yyyy',
               endDate: '+0d'
           });
        // exclude rera_expire_date1 field
        //    $( "input[name='rera_expire_date1']" ).datetimepicker( "option", "disabled", false );
        //    var altFormat = $("input[name='rera_expire_date1']").datetimepicker({
        //         minView: 2,
        //         startView: 2,
        //         autoclose: true,
        //         format: 'dd-mm-yyyy'
        //    });
            $("#id_rera_document1").show();
        }
        else{
            $("#rera_registration_no1").prop('readonly', true);
            $("#rera_state1").prop('readonly', true);
            $("#rera_expire_date1").prop('readonly', true);
            $("#rera_registration_no1").val('');
            $("#rera_registration_no1").css('border', '1px #bfbfbf solid');
            $("#rera_state1").val('');
            $("#rera_state1").css('border', '1px #bfbfbf solid');
            $("#rera_expire_date1").val('');
            $("#help_rera_registration_no1").html('');
            $("#help_rera_state1").html('');
            $("#help_rera_expire_date1").html('');
            $("#id_rera_document1").hide();
            $("#rera_certificate1").val('');
            $("#rera_renewal_certificate1").val('');
            $("#rera_certificate_status").val('');
            $('#datetimepicker_expiry_rera').datetimepicker('remove');
            // exclude rera_expire_date1 field
            // $( "input[name='rera_expire_date1']" ).datetimepicker( "option", "disabled", true );
            var remove_ids = $(".rera_remove").parent().map(function(){
                return this.id;
            }).get();
            for(i=0; i<remove_ids.length; i++){
                $('#'+remove_ids[i]).remove();
            }
        }
    }
    if(id == 'certification_dsa'){
        if(document.getElementById('certification_dsa').checked){
            $("#help_text_register_with").html('');
            $("#dsa_registration_no1").prop('readonly', false);
            $("#dsa_code_no1").prop('readonly', false);
            $("#dsa_how_long_associated1").prop('readonly', false);
            // exclude rera_expire_date1 field
            // $( "input[name='rera_expire_date1']" ).datetimepicker( "option", "disabled", false );
        }
        else{
            $("#dsa_registration_no1").prop('readonly', true);
            $("#dsa_code_no1").prop('readonly', true);
            $("#dsa_how_long_associated1").prop('readonly', true);
            $('#dsa_hidden_input_field').val('');
            $('#dsa_registration_no1').val('');
            $('#dsa_code_no1').val('');
            $('#dsa_how_long_associated1').val('');
            $('#help_dsa_registration_no1').html('');
            $("#help_dsa_code_no1").html('');
            $("#help_dsa_how_long_associated1").html('');
            var remove_ids = $(".dsa_remove").parent().map(function(){
                return this.id;
            }).get();
            for(i=0; i<remove_ids.length; i++){
                $('#'+remove_ids[i]).remove();
            }

        }
    }
}

//If advisor try to change the RERA Details
function check_rera_or_dsa_field(id, input_value, register_type){
    if (crisil_certificate_valid == 'True' && changes_accepted == false){
        $("#id_confirm_change").attr("onclick", "accept_changes_rera_dsa("+"'"+id+"'"+","+"'"+register_type+"'"+");");
        $("#id_cancel_change").attr("onclick", "cancel_accept_changes_rera_dsa("+"'"+id+"'"+", "+"'"+input_value+"'"+");");
        $('#check_confirm_for_change').modal('show');
    }else{
        check_validation_rera_or_dsa(id);
    }
}

// confirmation to accept change rera, dsa details
function accept_changes_rera_dsa(id, register_type) {
    check_validation_rera_or_dsa(id);
    changes_accepted = true;
    $('#check_confirm_for_change').modal('hide');
}

// confirmation for cancel
function cancel_accept_changes_rera_dsa(id, value) {
    $("#"+id).val(value);
    $("#"+id).css('border','1px #bfbfbf solid');
    $("#help_"+id).html('');
    $('#check_confirm_for_change').modal('hide');
}

// save registation details
function save_register_with_data(id) {
    if(id == 'certification_sebi'){
        save_onchange('sebi_number','sebi_registration_no','help_text_sebi_number');
        save_onchange('sebi_expiry_date','sebi_expiry_date','help_text_sebi_expire_date');
    }
    if(id == 'certification_irda'){
        save_onchange('irda_number','irda_registration_no','help_text_irda_number');
        save_onchange('irda_expiry_date','irda_expiry_date','help_text_sebi_expire_date');
    }
    if(id == 'certification_amfi'){
        save_onchange('amfi_number','amfi_registration_no','help_text_amfi_number');
        save_onchange('amfi_expiry_date','amfi_expiry_date','help_text_amfi_expire_date');
    }
    if(id == 'certification_others'){
        save_onchange('other_registered_organisation','other_organisation');
        save_onchange('other_registered_number','other_registration_no');
        save_onchange('other_expiry_date','other_expiry_date');
    }
    if(id == 'certification_rera'){
        $('#hidden_value').val('');
    }
}

// checking field is null or not, and removing validation from below respective fields
function check_validation_rera_or_dsa(id) {
    var value = $("#"+id).val();
    if(value != ''){
        $("#"+id).css('border','1px #bfbfbf solid');
        $("#help_"+id).html('');
    }
}

// Checking Advisor is crisil verified and removing rera_fields
function check_and_remove_rera_dsa(id, register_type) {
    if (crisil_certificate_valid == 'True' && changes_accepted == false){
        $("#id_confirm_change").attr("onclick", "remove_rera_dsa("+"'"+id+"'"+","+"'"+register_type+"'"+");");
        $("#id_cancel_change").attr("onclick", "cancel_rera_dsa("+"'"+id+"'"+");");
        $('#check_confirm_for_change').modal('show');
    }else{
        remove_rera_dsa(id, register_type);
    }
}

// remove rera or dsa field
function remove_rera_dsa(id, register_type) {
    if(register_type == 'rera'){
        remove_rera_row(id);
    }
    if(register_type == 'dsa'){
        remove_dsa_row(id);
    }
    changes_accepted = true;
    $('#check_confirm_for_change').modal('hide');
}

//confirmation pop up to cancel 
function cancel_rera_dsa(id) {
    $('#check_confirm_for_change').modal('hide');
}

//get available certification details
function display_certification_details(id,action){
    if (id=="certification_sebi"){
        if(document.getElementById('certification_sebi').checked){
            if(action=="clicked"){
                $('#id_sebi_document').show();
                check_advisor_is_crisil_sebi_irda(id,true);
            }
            else {
                disable_fields(id);
            }
        }
        else{
            var sebi_registration_no_value = $("#sebi_registration_no").val();
            var sebi_expiry_date_value = $("#sebi_expiry_date").val();
            if(sebi_registration_no_value != '' || sebi_expiry_date_value != ''){
                check_advisor_is_crisil_sebi_irda(id,false);
            }else{
                $('#id_sebi_document').hide()
                disable_fields(id);
            }
        }
    }
    if(id=='certification_amfi'){
        if(document.getElementById('certification_amfi').checked){
            if(action=="clicked"){
                $('#id_amfi_document').show();
                check_advisor_is_crisil_sebi_irda(id,true);
            }
            else {
                disable_fields(id);
            }
        }
        else{
            var amfi_registration_value = $("#amfi_registration_no").val();
            var amfi_expiry_date = $('#amfi_expiry_date').val();
            if(amfi_registration_value != '' || amfi_expiry_date !=''){
                check_advisor_is_crisil_sebi_irda(id,false);
            }else{
                $('#id_amfi_document').hide();
                disable_fields(id);
            }
        }
    }
    if(id=='certification_irda'){
        if(document.getElementById('certification_irda').checked){
            if(action=="clicked"){
                $('#id_irda_document').show();
                check_advisor_is_crisil_sebi_irda(id,true);
            }
            else {
                disable_fields(id);
            }
        }
        else{
            var irda_registration_no_value = $("#irda_registration_no").val();
            var irda_expiry_date_value = $("#irda_expiry_date").val();
            if(irda_registration_no_value != '' || irda_expiry_date_value != ''){
                check_advisor_is_crisil_sebi_irda(id,false);
            }else{
                $('#id_irda_document').hide();
                disable_fields(id);
            }
        }
    }
    if(id=='certification_others'){
        if(document.getElementById('certification_others').checked){
            if(action=="clicked"){
                $('#id_others_document').show();
                check_advisor_is_crisil_sebi_irda(id,true);
            }
            else {
                disable_fields(id);
            }
        }
        else{
            var other_organisation = $("#other_organisation").val();
            var other_registration_no = $("#other_registration_no").val();
            var other_expiry_date = $("#other_expiry_date").val();
            if(other_organisation != ''
                || other_registration_no != ''
                || other_expiry_date != ''){
                    check_advisor_is_crisil_sebi_irda(id,false);
            }else{
                $('#id_others_document').hide();
                disable_fields(id);
            }
        }
    }
    if(id == 'certification_rera'){
        if(document.getElementById('certification_rera').checked){
            if(action=="clicked"){
                check_advisor_is_crisil_sebi_irda(id,true);
            }
            else {
                disable_fields(id);
            }
        }
        else{
            var rera_registration_no = $("#rera_registration_no1").val();
            var rera_state = $("#rera_state1").val();
            var rera_expire_date = $("#rera_expire_date1").val();
            if(rera_registration_no !=''
                || rera_state != ''
                || rera_expire_date !=''){
                    check_advisor_is_crisil_sebi_irda(id,false);
            }else{
                disable_fields(id);
            }
        }
    }
    if(id == 'certification_dsa'){
        if(document.getElementById('certification_dsa').checked){
            if(action=="clicked"){
                check_advisor_is_crisil_sebi_irda(id,true);
            }
            else {
                disable_fields(id);
            }
        }
        else{
            var dsa_registration_no = $("#dsa_registration_no1").val();
            var dsa_code = $("#dsa_code_no1").val();
            var dsa_how_long_associated = $("#dsa_how_long_associated1").val();
            if(dsa_registration_no != ''
                || dsa_code != ''
                || dsa_how_long_associated != ''){
                    check_advisor_is_crisil_sebi_irda(id,false);
            }else{
                disable_fields(id);
            }
        }

    }
}

// common function to clear error message
function clear_error_msg(id,name){
    if($("#"+id).val() != ''){
        var nationality_value = $("#"+id).val();
        document.getElementById(id).style.border='';
        $("#help_text_"+name).html('');
    }
    else{
        $("#"+id).focus();
    }
}

// validates rera experience
function reraExperience(str,id) {
    var re = /^[1-9][0-9]?$|^99$/;
    var validexperience = document.getElementById(str);
    var validexperience = document.getElementById('dsa_how_long_associated'+id);
        if(!validexperience.value.match(re) || validexperience == null ) {
            var a=document.getElementById('dsa_how_long_associated'+id).value = "";
            document.getElementById('dsa_how_long_associated'+id).style.border='1px solid #C32F2F';
            document.getElementById('help_dsa_how_long_associated'+id).innerHTML='Enter Valid Experience';
            $("#dsa_how_long_associated"+id).focus();
        }else{
            document.getElementById('dsa_how_long_associated'+id).style.border='';
            document.getElementById('help_dsa_how_long_associated'+id).innerHTML='';
        }
}

// validation and submission of regulatory registration
function submit_regulatory_regs(){
    var missed_field = 0;
    if ($("#certification_others").prop('checked') == true) {
        if ($('#other_registration_no').val().trim().length == 0) {
            $("#help_text_other_registration").html('Please Enter Reg.No');
            $('#other_registration_no').css('border', '1px solid #C32F2F');
            $("#other_registration_no").focus();
            missed_field = 1;
        } else {
            $("#help_text_other_registration").html('');
            $('#other_registration_no').css('border', '');
        }
        if ($('#other_organisation').val() == '') {
            $("#help_text_other_organisation").html('Please Enter Organisation name');
            $('#other_organisation').css('border', '1px solid #C32F2F');
            $("#other_organisation").focus();

        } else {
            $("#help_text_other_organisation").html('');
            $('#other_organisation').css('border', '');
        }
    }
    if (user_agent_country == default_country){
        if(document.getElementById('certification_dsa').checked){
            var final_dsa_json_result = dsa_json_output_result();
            $('#dsa_hidden_input_field').val(final_dsa_json_result[0]);
            if(final_dsa_json_result[1] != 0 ){
                missed_field = 1;
            }
        }
    }
    if($("#certification_irda").prop('checked') == true){
        if($('#irda_registration_no').val()==''){
            $('#help_text_irda_number').html('Please Enter IRDA Reg.No');
            $('#irda_registration_no').css('border','1px solid #C32F2F');
            $("#irda_registration_no").focus();
            missed_field = 1;
        }else{
            $('#help_text_irda_number').html('');
            $('#irda_registration_no').css('border','');
        }
    }
    if($("#certification_amfi").prop('checked') == true){
        if($('#amfi_registration_no').val()==''){
            $("#help_text_amfi_number").html('Please Enter AMFI Reg.No');
            $('#amfi_registration_no').css('border','1px solid #C32F2F');
            $("#amfi_registration_no").focus();
            missed_field = 1;
        }else{
            $("#help_text_amfi_number").html('');
            $('#amfi_registration_no').css('border','');
        }
    }
    if($("#certification_sebi").prop('checked') == true){
        if($('#sebi_registration_no').val()==''){
            $("#help_text_sebi_number").html('Please Enter SEBI Reg.No');
            $('#sebi_registration_no').css('border','1px solid #C32F2F');
            $("#sebi_registration_no").focus();
            missed_field = 1;
        }else{
            $("#help_text_sebi_number").html('');
            $('#sebi_registration_no').css('border','');
        }
    }
    if (user_agent_country == default_country) {
        var i =$('input[class="count_checkbox"]:checked').length;
        if($('input[class="count_checkbox"]:checked').length<1){
            $("#help_text_register_with").html('Please Select Your Register type');
            $("#certification_sebi").focus();
            missed_field = 1;
        }else{
            $("#help_text_register_with").html('');
        }
        document.getElementById('sebi_expiry_date').disabled = false;
        document.getElementById('amfi_expiry_date').disabled = false;
        document.getElementById('irda_expiry_date').disabled = false;
        if(is_rera_status != 'True'){
            document.getElementById('rera_expire_date1').disabled = false;
        }
    }
    document.getElementById('other_expiry_date').disabled = false;
    if (user_agent_country == default_country) {
        if(irda_certificate_status != 'True' && $("#irda_registration_no").val() != ''
        && document.getElementById('certification_irda').checked ){
            alert("Please Upload The IRDA Document");
            missed_field = 1;
        }
        if(sebi_certificate_status != 'True' && $("#sebi_registration_no").val() != ''
        && document.getElementById('certification_sebi').checked ){
            alert("Please Upload The SEBI Document");
            missed_field = 1;
        }
        if(amfi_certificate_status != 'True' && $("#amfi_registration_no").val() != ''
        && document.getElementById('certification_amfi').checked ){
            alert("Please Upload The AMFI Document");
            missed_field = 1;
        }
    }
    if (others_certificate_status != 'True' && $("#other_organisation").val() != ''
    && $("#other_registration_no").val() != '' && document.getElementById('certification_others').checked) {
        alert("Please Upload The Regulatory OTHERS Document");
        missed_field = 1;
    }
    // RERA Fields data fetching and making json
    if (user_agent_country == default_country) {
        if (document.getElementById('certification_rera').checked) {
            var rera_details = validate_rera_and_get_json(true);
            if (rera_details.missed_field) {
                document.getElementById('hidden_value').value = rera_details.final_rera_json;
            } else {
                missed_field = 1;
            }
        }
    }
    if (missed_field == 0){
        $('#regulatory_registration_form').submit();
    }
}

// Load Regulatory upload documents modal
function show_regulatory_documents(regulatory_type){
    var regulatory = regulatory_type.data[0];
    $.ajax({
        method : 'POST',
        url : '/signup/show_regulatory_doc_modal/',
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", csrf_token);
        },
        data:{
            'regulatory_type': regulatory
        },
        success: function(response){
            $("#advisor_registration_modal_div").html('');
            $("#advisor_registration_modal_div").html(response);
            $("#reg_doc_modal").html('');
            $("#reg_doc_modal").html(response);
            $("#id_regulatory_registration").modal('hide');
            show_bootstrap_modal('#regulatory_registration_doc_modal');
            $("#regulatory_registration_doc_modal")
                .find('button.close')
                .attr('onclick', "load_regulatory_modal('#id_regulatory_registration');")
                .removeAttr('data-dismiss');
            if (regulatory == 'sebi') {
                $("#regulatory_title").html('UPLOAD SEBI CERTIFICATE');
                $("#certificate_type").val('sebi_certificate');
                $("#renewal_type").val('sebi_renewal_certificate');
            }
            else if (regulatory == 'amfi') {
                $("#regulatory_title").html('UPLOAD AMFI CERTIFICATE');
                $("#certificate_type").val('amfi_certificate');
                $("#renewal_type").val('amfi_renewal_certificate');
            }
            else if (regulatory == 'irda') {
                $("#regulatory_title").html('UPLOAD IRDA CERTIFICATE');
                $("#certificate_type").val('irda_certificate');
                $("#renewal_type").val('irda_renewal_certificate');
            }
            else if (regulatory == 'reg_others') {
                $("#regulatory_title").html('UPLOAD OTHERS CERTIFICATE');
                $("#certificate_type").val('others_certificate');
                $("#renewal_type").val('others_renewal_certificate');
            }
        },
        error: function(response){
            alert('Unable to Process your request. \n Please try again after some time');
        }
    });
}

// Load the regulatory modal
function load_regulatory_modal(elem){
    $("#regulatory_registration_doc_modal").modal('hide');
    $(elem).modal({
        show: true,
        keyboard: false,
        backdrop: 'static'
    });
}
