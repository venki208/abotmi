var form_id;
var csrf_token = csrf_token;

/**
 * @use -> used upload the documents and attaching docs
 * @param {HTMLFormId} form_id -> need to pass HTML form attribute id
 * @param {HTMLAttrID} uploaded_div 
 * @param {HTMLAttrID} paper_clip 
 */
function upload_verf_doc(form_id, uploaded_div, paper_clip) {
    enable_overaly();
    form_id = form_id;
    var upload_res = upload_document(form_id);
    upload_res.success(function (response) {
        disable_overlay();
        $("#" + form_id).find('input[type="file"]').val('');
        $("#" + form_id).parent().find('.preview')
            .addClass('hide')
            .find('#preview_img_tag').attr('src', '');
        remove_icon = "<i class='fa fa-trash download_link_color'></i>";
        $("#attachment_div")
            .html('')
            .removeClass('hide');
        attach_document(uploaded_div, response, paper_clip, false, 'remove_document_file(' + "'" + response.id + "'" + ',' + "'" + form_id + "'" + ')', false);
        $.toast({
            text: 'Uploaded Successfully.',
            textAlign: 'center',
            showHideTransition: 'slide',
            position: 'top-center',
            icon: 'success'
        });
        document.getElementById('help_text_verification_process').innerHTML = "";
        if(form_id == 'passport_form'){
            passport.push(response.id);
        }else if(form_id == 'dl_form'){
            driving_licence.push(response.id);
        }else if(form_id == 'id_card_form'){
            id_card.push(response.id);
        }
    });
    upload_res.error(function (response) {
        $.toast({
            heading: 'Error',
            text: 'Unable to upload the document <br /> Please try again.',
            showHideTransition: 'slide',
            position: 'top-center',
            icon: 'error'
        });
    });
}

function remove_document_file(id, form_id){
    if(form_id == 'passport_form'){
        passport.pop(id);
    }else if(form_id == 'dl_form'){
        driving_licence.pop(id);
    }else if(form_id == 'id_card_form'){
        id_card.pop(id);
    }
    removeDocument(id);
}

function update_verification_type() {
    $.ajax({
        type: 'POST',
        url: '/signup/update_verification_type/',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        data: {
            documents_type: $("#documents_type").val()
        },
        success: function (response) {},
        error: function (response) {}
    });
}

function reupload_verf_doc() {
    $("#attachment_div").addClass('hide');
    $("#upload_doc").removeClass('hide');
}

// validating verification step
function validate_verfication() {
    var is_upload;
    country_stat = validate_field_onkeypress('country', "help-text-country", "Country");
    if(passport.length > 0 || driving_licence.length > 0 || id_card.length > 0){
        is_upload = true;
        document.getElementById('help_text_verification_process').innerHTML = "";
    }else{
        is_upload = false;
        document.getElementById('help_text_verification_process').innerHTML = "Please Upload any one of the document";
        $('html, body').animate({
            scrollTop: $("#verification_div").offset().top-90
        }, 100);
    }
    if(is_upload && country_stat == 0){
        return true;
    }
    else{
        return false;
    }
}

$("#verification_next").on('click', function (e) {
    if (validate_verfication()) {
        save_onchange("country", "country", "help-text-country");
        window.location.href = "/signup/personal_information/";
    }
});

function save_onchange(name, id, error_message_block_id) {
    var value = $("#" + id).val();
    if (validate_verfication()) {
        $.ajax({
            url: "/signup/onchange_save_field/",
            method: "POST",
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            data: {
                username: username,
                value: value,
                name: name
            },
            success: function (response) {},
            error: function (response) {},
        });
    }
}

// Loading preview of selected image
function load_preview(input) {
    if (input.files && input.files[0]) {
        var verf_block = $(input).closest('.verf_block').find('.preview');
        var reader = new FileReader();
        if(input.files[0].type =='application/pdf'){
            reader.onload = function (e) {
                $("#preview_img_tag").addClass('hide');
                verf_block
                    .removeClass('hide')
                    .find('iframe')
                        .attr('src', e.target.result)
                        .removeClass('hide');
                verf_block.find('img').addClass('hide');
            };
        }
        else{
            reader.onload = function (e) {
                verf_block
                    .removeClass('hide')
                    .find('img')
                        .attr('src', e.target.result)
                        .removeClass('hide');
                verf_block.find('iframe').addClass('hide');
            };
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function submit_verfication() {
    $.ajax({
        type: 'POST',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        url: "/signup/submit_verification/",
        data: {
            passport_no: $("#passport_no").val()
        },
        success: function (response) {
            if (response == 200) {
                window.location.href = '/signup/register_advisor/';
            } else {
                alert('Unable submit the form. \n Please try again');
            }
        },
        error: function (response) {
            alert('Unable submit the form. \n Please try again');
        }
    });
}


function enable_overaly(){
    $("#overlay-div").addClass('overlay-div');
}


function disable_overlay(){
    $("#overlay-div").removeClass('overlay-div');
}