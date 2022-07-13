var wrapper = $(".input_fields_wrapper");
var add_certificate = $("#add_certificate_btn");
var x = 1; //initlal text box count


$(document).ready(function () {

    // Adding year options to certification and eductation year fields
    var date = new Date();
    dateArray = [];
    curYear = date.getFullYear();
    // For from year
    for (var j = 0; j < 65; j++) {
        dateArray[j] = (curYear - 64) + j;
        options.push('<option value=' + dateArray[j] + '>' + dateArray[j] + '</option>');
    }
    // To Year
    curYear = curYear + 10;
    for (var j = 0; j < 75; j++) {
        dateArray[j] = (curYear - 74) + j;
        to_year_options.push('<option value=' + dateArray[j] + '>' + dateArray[j] + '</option>');
    }
    $("#to_year").append(to_year_options);

    $("[name='from_year']").append(options);
    $("[name='to_year']").append(to_year_options);
    // setting education from year and to year
    $("#from_year").val(edu_from_year);
    $("#to_year").val(edu_to_year);

    $(".input_fields_wrapper select").each(function(e){
        $(this).val($(this).attr('cert_year_val'));
    });
});


// Adding additional certification form
$(add_certificate).click(function (e) { //on add input button click
    x++; //text box increment
    var first_row = '<div class = "form-row row"><div class="form-group col-md-6"><label for="certificate_name">Certification name:</label><input type="text" class="form-control" id="certificate_name" name="certificate_name" placeholder="" pattren="[a-zA-Z0-9._]{3,40}" required></div><div class="form-group col-md-6"><label for="certificate_authority">Certification authority:</label><input type="text" class="form-control" id="certificate_authority" name="certificate_authority" placeholder="" pattren="[a-zA-Z0-9._]{3,40}" required></div></div>';
    var second_row = '<div class = "form-row row"><div class="form-group col-md-6"><label for="licence_number">Licence number</label><input type="text" class="form-control" id="licence_number" name="licence_number" placeholder="" pattren="[a-zA-Z0-9]{3,40}" required></div><div class="form-group col-md-6"><label for="certificate_url">Certification URL</label><input type="url" class="form-control" id="certificate_url" name="certificate_url" placeholder="" required></div></div>';
    var third_row = '<div class="form-row row">'+
                        '<div class="form-group col-md-6">'+
                            '<label for="from_year">From Year</label>'+
                            '<select name="from_year" class="form-control" id="certificate_from_year" value="" required="true" is-select="true">'+
                                '<option value="">Select</option>'+
                                options+
                            '</select>'+
                            '<span class="help-block" id="help-text-from_year"></span>'+
                        '</div>'+
                        '<div class="form-group col-md-6">'+
                            '<label for="to_year">To Year (or expected)</label>'+
                            '<select name="to_year" class="form-control" id="certificate_to_year" value=""  is-select="true">'+
                                '<option value="">Select</option>'+
                                to_year_options+
                            '</select>'+
                            '<span class="help-block" id="help-text-to-year"></span>'+
                        '</div>'+
                    '</div>'

    var cert_check_box = '<div class="form-row row form-group ml-2">'+
                            '<div class="checkbox col-md-12">'+
                                '<label>'+
                                    '<input class="form-check-input" type="checkbox" id="gridCheck" name="gridCheck"> This Certification does not expire'+
                                '</label>'+
                            '</div>'+
                        '</div>';

    var upload_file = '<div class="form-row row form-group">' +
                        '<div class="upload_file" name="upload_div">' +
                            '<div class="col-md-12 form-inline">'+
                                '<div class="form-group">' +
                                    '<label> Upload Certificate (Transcript, Diploma)'+
                                        '<span class="btn btn-default">'+
                                            '<i class="fa fa-paperclip" aria-hidden="true"></i>'+
                                            '<input type="file" id="file_upload" name="cert_document" class="file form-control hide" accept="image/*">' +
                                            '<input type="hidden" name="certificate_doc">'+
                                            '<input type="hidden" name="certificate_doc_id">'+
                                        '</span>'+
                                    '</label>'+
                                '</div>'+
                            '</div>' + 
                        '</div>' +
                        '<div class="attached_div upload-icons" name="attached_div">'+
                        '</div>'+
                    '</div>';

    var form_element = '<form class = "certificate" role="form" data-toggle="validator" method="post" action="">' + first_row + second_row + third_row + cert_check_box + upload_file +'</form>'
    var wrapper_element = '<div><div class="input_fields_wrapper" id="form_validation">' + form_element + '</div><a class="remove_field">Delete Certificate</a></div>';

    $(wrapper).append(wrapper_element); //add input box

});

$(wrapper).on("click",".remove_field", function(e){ //user click on remove text
    $(this).parent('div').remove(); x--;
});


// Delete certificate function
function remove_certificate(form_id){
    $('#certificate_form_id'+ form_id).remove();
    $('html, body').animate({
        scrollTop: $('#certification_div').offset().top
    }, 'fast');
}


// Validating certification form
function validate_certification_form(){
    var v = $(".input_fields_wrapper").find('form');
    var l = v.length;
    $(".error").remove();
    var missed = 0;
    for(var i=0;i<l;i++){
        var certificate_name = $(v[i]).find('[name="certificate_name"]').val();
        var certificate_authority =  $(v[i]).find('[name="certificate_authority"]').val();
        var licence_number = $(v[i]).find('[name="licence_number"]').val();
        var certificate_url = $(v[i]).find('[name="certificate_url"]').val();
        var from_year = $(v[i]).find('[name="from_year"]').val();
        var to_year = $(v[i]).find('[name="to_year"]').val();
        var gridCheck = $(v[i]).find('[name="gridCheck"]').prop('checked');
        var certificate_doc_id = $(v[i]).find('[name="certificate_doc_id"]').val();
        
        if(((certificate_name ||
            certificate_authority ||
            licence_number ||
            certificate_url||
            from_year || 
            to_year ||
            gridCheck || 
            certificate_doc_id) && i == 0) || i > 0){
            if(!certificate_doc_id){
                $(v[i]).find('[name="certificate_doc_id"]').closest('.form-group').append(
                    '<span class="error help-block">Please upload the certificate document</span>'
                );
                scroll_top_certification(v[i]);
                missed = 1;
            }
            if(gridCheck==false){
                if(!(1954<=to_year)||!(to_year<=2029)||(from_year>to_year)){
                    $(v[i]).find('[name="to_year"]').parent().append('<span class="error help-block">Please provide the valid To year</span>');
                    $(v[i]).find('[name="to_year"]').focus();
                    missed = 1;
                }
            }
            if (!(1954<=from_year)||!(from_year<=2019)) {
                $(v[i]).find('[name="from_year"]').parent().append('<span class="error help-block">Please provide the valid From year</span>');
                $(v[i]).find('[name="from_year"]').focus();
                missed = 1;
            }
            if ($.trim(certificate_url).length < 1) {
                $(v[i]).find('[name="certificate_url"]').parent().append(
                    '<span class="error help-block">Please enter an URL</span>');
                $(v[i]).find('[name="certificate_url"]').focus();
                missed = 1;
            } else {
                var regEx = (/(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g);
                var validUrl = regEx.test(certificate_url);
                if (!validUrl) {
                    $(v[i]).find('[name="certificate_url"]').parent().append(
                        '<span class="error help-block">Please enter a valid Certificate URL</span>');
                    $(v[i]).find('[name="certificate_url"]').focus();
                    missed = 1;
                }
            }
            if (!$.trim(licence_number)) {
                $(v[i]).find('input[name="licence_number"]').parent().append('<span class="error help-block">Please enter a valid Licence number</span>');
                $(v[i]).find('[name="licence_number"]').focus();
                missed = 1;
            }
            if ($.trim(certificate_authority).length < 3) {
                $(v[i]).find('[name="certificate_authority"]').parent().append('<span class="error help-block">Please enter a valid Certificate Authority</span>');
                $(v[i]).find('[name="certificate_authority"]').focus();
                missed = 1;
            }
            if ($.trim(certificate_name).length < 3) {
                $(v[i]).find('[name="certificate_name"]').parent().append('<span class="error help-block">Please enter a valid Certificate Name</span>');
                $(v[i]).find('[name="certificate_name"]').focus();
                missed = 1;
            }
        }

    }
    return missed;
}


// Getting certification json output
function get_certificate_json(){
    var v = $(".input_fields_wrapper").find('form');
    
    certificate_list = [];

    for(var i=0;i<v.length;i++){
        certificate_list.push({
            "certificate_doc_id" : $(v[i]).find('[name="certificate_doc_id"]').val(),
            "certification_name" : $(v[i]).find('[name="certificate_name"]').val(),
            "certi_authority" : $(v[i]).find('[name="certificate_authority"]').val(),
            "licence_number" : $(v[i]).find('[name="licence_number"]').val(),
            "certi_url" : $(v[i]).find('[name="certificate_url"]').val(),
            "from_year" : $(v[i]).find('[name="from_year"]').val(),
            "to_year" : $(v[i]).find('[name="to_year"]').val(),
            "is_expire" : $(v[i]).find('[name="gridCheck"]').prop('checked'),
            "certificate_doc": $(v[i]).find('[name="certificate_doc"]').val()
        });
    }
    return certificate_list

}


// uploading certification documents
$("#certification_div").on('change', 'input[name="cert_document"]', function(e){
    var file_input = this;
    var form_ob = new FormData();
    form_ob.append("document", this.files[0]);
    form_ob.append("documents_type", 'certificate')
    form_ob.append("reload", true)
    var upload_res = upload_document('', form_ob);
    upload_res.success(function(response){
        var download_link = response.url;
        var doc_id = response.id;
        $(file_input).closest('.form-row').find('div[name="upload_div"]').addClass('hide');
        $(file_input).closest('.form-row').find('input[name="certificate_doc"]').val(download_link);
        $(file_input).closest('.form-row').find('input[name="certificate_doc_id"]').val(doc_id);
        var attached_link = "<span class='child_eipv_span n-padding-r-5 n-span-pink-color'>Attached&nbsp; <a class='hiding"+doc_id+"' onclick=preview_image('" + download_link + "'); data-toggle='tooltip' data-placement='bottom' title='Preview image' style='margin-right:5px;'><i class='fa fa-eye' aria-hidden='true'></i></a><a class='hiding"+doc_id+"' onclick=remove_certificate_doc('"+doc_id+"'); data-toggle='tooltip' data-placement='bottom' title='Reset/Re upload'><i class='fa fa-trash download_link_color' aria-hidden='true'></i></a></span>";
        $(file_input).closest('.form-row').find('div.attached_div').html(attached_link);
        $.toast({
            text: 'Uploaded Successfully.',
            textAlign: 'center',
            showHideTransition: 'slide',
            position: 'top-center',
            icon: 'success'
        });
    });
    upload_res.error(function(response){
        show_alert(
            'error',
            '',
            '<p>Unable upload please try again after sometime.</p>'
        );
    });

});


// preview image pop up 
function preview_image(url) {
    $("#image_show_body").html('');
    $("#image_show_body").html("<img src='" + url + "' class='img-responsive img-fluid'></img>");
    $("#show_image_model").modal('show');
}

// removing the doc
function remove_certificate_doc(id){
    $('.hiding'+id).closest('.form-row').find('div[name="upload_div"]').removeClass('hide');
    $('.hiding'+id).closest('.form-row').find('input[type="file"]').val('');
    $('.hiding'+id).closest('.form-row').find('input[name="certificate_doc"]').val('');
    $('.hiding'+id).closest('.form-row').find('input[name="certificate_doc_id"]').val('');
    $('.hiding'+id).parent().html('');
}

