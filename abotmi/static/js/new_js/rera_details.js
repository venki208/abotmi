var csrf_token = $("#id_csrf_token").val();
var parent_class;

// Adding RERA Fields Dynamically
function add_rera_fields() {
    var rera_validation = validation_rera_fields();
    if (rera_validation == true) {
        id_rera++;
        if (($("#id_regulatory_registration").data('bs.modal') || {}).isShown == undefined){
            parent_class = 'col-md-12';
        }else{
            parent_class = 'row';
        }
        rera_additional_field = return_date_input_tag(id_rera);
        $('<div id="div_id' + id_rera + '" class="rera_div_row '+parent_class+' no-padding">' +
            '<div class="form-group col-md-2 col-sm-2 col-lg-2 checkbox-rcerrtification"></div>' +
            '<div class="form-group col-md-3 col-sm-3 col-lg-3 others">' +
                '<input type="text" class="form-control" id="rera_registration_no' + id_rera + '" name="rera_registration_no' + id_rera + '" placeholder="Registration Number" value="" onchange="check_rera_or_dsa_field(id,' + "'" + "'" + ',' + "'" + 'rera' + "'" + ');">' +
                '<span class="help-block register_with" id="help_rera_registration_no' + id_rera + '"></span>' +
            '</div>' +
            '<div class="form-group col-md-3 col-sm-3 col-lg-3 others">' +
                '<input type="text" class="form-control" id="rera_state' + id_rera + '" name="rera_state' + id_rera + '" placeholder="State" value="" onchange="check_rera_or_dsa_field(id,' + "'" + "'" + ',' + "'" + 'rera' + "'" + ');">' +
                '<span class="help-block register_with" id="help_rera_state' + id_rera + '"></span>' +
            '</div>' +
            '<div class="form-group col-md-3 col-sm-3 col-lg-3 others inside-form date-picker-last-view">' +
                rera_additional_field+
            '</div>' +
            '<input type="hidden" name="rera_certificate" id="rera_certificate'+id_rera+'">'+
            '<input type="hidden" name="rera_renewal_certificate" id="rera_renewal_certificate'+id_rera+'">'+
            '<input type="hidden" name="rera_certificate_status" id="rera_certificate_status' + id_rera +'">'+
            '<label id="id_rera_document' + id_rera +'" class="fileinput btn-minus" data-provides="fileinput" onclick="show_rera_documents(id);">'+
                '<span class="btn additional_btn btn-file">' +
                    '<i class="fa fa-paperclip" aria-hidden="true"></i>' +
                '</span>' +
            '</label >' +
            '<a class="btn additional_btn rera_remove" id="div_id' + id_rera + '" onClick="remove_rera_row(id);">' +
                '<i class="fa fa-minus-circle" ></i>' +
            '</a>' +
        '</div>').appendTo(additional_rera_fields);
        if (($("#id_regulatory_registration").data('bs.modal') || {}).isShown == undefined){
            $(".datepicker").datepicker({
                changeMonth: true,
                changeYear: true,
                dateFormat: "dd-mm-yy",
                yearRange: "Date():+5Y",
                minDate: 'Date()'
            });
        }else{
            $(".datetimepicker").datetimepicker({
                minView: 2,
                startView: 2,
                autoclose: true,
                format: 'dd-mm-yyyy'
            });
        }
    }
}

// Removing RERA rows
function remove_rera_row(id) {
    $('#' + id).remove();
}

// Validating RERA Fields
function validation_rera_fields() {
    var check_value_id = id_rera;
    var rera_registration_no = $("#rera_registration_no" + id_rera).val();
    var rera_state = $("#rera_state" + id_rera).val();
    var rera_expire_date = $("#rera_expire_date" + id_rera).val();
    var rera_certificate = $("#rera_certificate"+id_rera).val();
    var validation_rera_fields_id = 0;
    if (document.getElementById('certification_rera').checked == true) {
        if (rera_registration_no == '') {
            $("#help_rera_registration_no" + id_rera).html('Please Enter RERA Reg.No');
            validation_rera_fields_id = 1;
        } if (rera_state == '') {
            $("#help_rera_state" + id_rera).html('Please Enter RERA State');
            validation_rera_fields_id = 1;
        }
        // Commented on 29/09/2016 based on the requirement
        // if(rera_expire_date == ''){
        //     $("#help_rera_expire_date"+id_rera).html('Please Enter RERA Valid upto');
        //     validation_rera_fields_id = 1;
        // }
        if (rera_certificate == ''){
            validation_rera_fields_id = 1;
            $("#rera_certificate"+id_rera).parent().find('.fileinput').addClass('add-shadow');
            var parent_id = $("#rera_certificate"+id_rera).parent().attr('id');
            if (($("#id_regulatory_registration").data('bs.modal') || {}).isShown == false){
                scroll_to('#' + parent_id);
            }
            alert('Please Upload RERA Documents');
        }
        if (validation_rera_fields_id == 1) {
            return false;
        } else {
            return true;
        }
    }
    else {
        return false;
    }
}

// Valdating RERA fields and forming values into json
function validate_rera_and_get_json(is_validate){
    var $inputs = $('#rera_subdetails :input');
    var rera_json_str = [];
    var i = 0;
    var second_id = 0;
    $inputs.each(function (index) {
        var input_ids;
        input_ids = $(this).attr('id');
        values = $("#" + input_ids).val();
        if (i == 0 || (i % 6 == 0)) {
            if (values == '') {
                second_id = +1;
                if (is_validate) {
                    $("#help_" + input_ids).html('Please Enter RERA Reg.No');
                    $("#" + input_ids).css("border", "1px solid #C32F2F");
                    $("#" + input_ids).focus();
                }
            } else {
                rera_json_str[i] = '"rera_registration_no"' + ":" + '"' + values + '"' + ",";
            }
        }
        if (i == 1 || (i % 6 == 1)) {
            if (values == '') {
                second_id = +1;
                if (is_validate) {
                    $("#help_" + input_ids).html('Please Enter RERA State');
                    $("#" + input_ids).css("border", "1px solid #C32F2F");
                    $("#" + input_ids).focus();
                }
            } else {
                var alpha = /^[a-zA-Z()\s]+$/.test(values);
                if (!alpha) {
                    if (is_validate) {
                        $("#" + input_ids).css("border", "1px solid #C32F2F");
                        $("#" + input_ids).focus();
                        $("#help_" + input_ids).html('Please Enter valid RERA State');
                    }
                    second_id = +1;
                }
                rera_json_str[i] = '"rera_state"' + ":" + '"' + values + '"' + ",";
            }
        }
        if (i == 2 || (i % 6 == 2)) {
            // Commented on 29/09/2016 based on the requirement
            if (values == '') {
                // second_id =+1;
                // $("#help_"+input_ids).html('Please Enter RERA Valid upto');
                // $("#"+input_ids).css("border", "1px solid #C32F2F");
                // $("#"+input_ids).focus();
                $("#" + input_ids).datepicker("hide");
                rera_json_str[i] = '"rera_expire_date"' + ":" + '"' + values + '"' + ",";
            } else {
                rera_json_str[i] = '"rera_expire_date"' + ":" + '"' + values + '"' + ",";
            }
        }
        if (i == 3 || (i % 6 == 3)) {
            if (values == '') {
                second_id = +1;
                $("#" + input_ids).parent().find('.fileinput').addClass('add-shadow');
                var parent_id = $("#" + input_ids).parent().attr('id');
                if (($("#id_regulatory_registration").data('bs.modal') || {}).isShown == false) {
                    scroll_to('#'+parent_id);
                }
                alert('Please Upload RERA Documents');
            }
            rera_json_str[i] = '"rera_certificate"' + ":" + '"' + values + '"'+ ",";
        }
        if (i == 4 || (i % 6 == 4)) {
            rera_json_str[i] = '"rera_renewal_certificate"' + ":" + '"' + values + '"' + ",";
        }
        if (i == 5 || (i % 6 == 5)) {
            rera_json_str[i] = '"rera_certificate_status"' + ":" + '"' + values + '"';
        }
        i++;
    });
    var json_index = 0;
    var json_labels = [];
    var rera_output = '{';
    for (var i = 0; i < rera_json_str.length; i++) {
        var rera_output = rera_output + rera_json_str[i];
        if ((i + 1) % 6 == 0 && i != 0) {
            var rera_output = rera_output + '}';
            json_labels[json_index] = rera_output;
            json_index++;
            var rera_output = '{';
        }
    }
    // document.getElementById('hidden_value').value = json_labels;
    if (second_id > 0) {
        missed_field = false;
    }else{
        missed_field = true;
    }
    return {
        missed_field : missed_field,
        final_rera_json: json_labels
    };
}

// Showing RERA Documents Modal
function show_rera_documents(id){
    var certificate_input = $('#'+id).parent().find('input[name="rera_certificate"]');
    $("#" + id).removeClass('add-shadow');
    var certi_val = certificate_input.val();
    var certi_id = certificate_input.attr('id');
    var renewal_cert_input = $('#'+id)
                                .parent()
                                .find('input[name="rera_renewal_certificate"]');
    var renewal_cert_val = renewal_cert_input.val();
    var renewal_cert_id = renewal_cert_input.attr('id');
    $.ajax({
        method: 'POST',
        url: '/signup/show_regulatory_doc_modal/',
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", csrf_token);
        },
        data:{
            regulatory_type: 'rera',
            certificate_id: certi_val,
            renewal_certificate_id: renewal_cert_val
        },
        success: function(response){
            $("#advisor_registration_modal_div").html('');
            $("#advisor_registration_modal_div").html(response);
            $("#regulatory_title").html('UPLOAD RERA CERTIFICATE');
            $("#certificate_type").val('rera_certificate');
            $("#certificate_type").parent().find("input[name='reupload']").val(false);
            $("#renewal_type").val('rera_renewal_certificate');
            $("form#upload_doc0")
                .find('input[type="file"]')
                .removeAttr('onchange')
                .bind('change', ['upload_doc0', 'proof_indian', 'paper_clip0', certi_id], upload_rera_doc);
            $("form#upload_doc1")
                .find('input[type="file"]')
                .removeAttr('onchange')
                .bind('change', ['upload_doc1', 'renewal_document_div', 'paper_clip1', renewal_cert_id], upload_rera_doc);
            $("#viewed_doc_id").val(renewal_cert_id);
            if (($("#id_regulatory_registration").data('bs.modal') || {}).isShown){
                $("#id_regulatory_registration").modal('hide');
                $("#regulatory_registration_doc_modal")
                    .find('button.close')
                    .attr('onclick', "load_regulatory_modal('#id_regulatory_registration');")
                    .removeAttr('data-dismiss');
            }
            show_bootstrap_modal('#regulatory_registration_doc_modal');
        },
        error: function(response){
            alert('Unable to Process your request \n Please try again after some time');
        }
    });
}

// Uploading RERA Documents
function upload_rera_doc(doc_data){
    var form_id = doc_data.data[0];
    var attachment_div = doc_data.data[1];
    var paper_clip_id = doc_data.data[2];
    var rera_doc_input_id = doc_data.data[3];
    var upload_doc = upload_document(form_id);
    upload_doc.success(function(response){
        var input_value = $('#' + form_id).find('input[name="documents_type"]').val();
        if (input_value == 'rera_renewal_certificate') {
            remove_icon = "&nbsp;&nbsp" +
                "<i class='glyphicon glyphicon-trash download_link_color'></i>";
            var ren_doc_ids = $("#" + rera_doc_input_id).val();
            if(ren_doc_ids){
                ren_doc_ids = ren_doc_ids +","+response.id ;
            }else{
                ren_doc_ids = response.id;
            }
            $("#" + rera_doc_input_id).val(ren_doc_ids);
        } else {
            remove_icon = "&nbsp;&nbsp" +
                "<i class='glyphicon glyphicon-repeat download_link_color'></i>";
            $("#" + paper_clip_id).addClass('hide');
            $("#" + rera_doc_input_id).val(response.id);
        }
        attach_document(attachment_div, response, paper_clip_id);
    });
    upload_doc.error(function(response){
        alert('Unable to Upload file \n Please try again after some time');
    });
}
