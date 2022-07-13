var csrf_token = $("#id_csrf_token").val();

// Validating and Submitting the Get Advice(Advice Question)
function add_advice(){
    var token = csrf_token;
    var title = '';
    var message = '';
    var missed_field = 0;
    var title = $("#title").val().trim();
    var advisor_id = $("#advisor_id").val();
    var advisor_name = $("#advisor_name").val();
    var advisor_email = $("#advisor_email").val();
    var message = $("#message").val().trim();
    if (title != ''){
        $("#error_title1").html('');
        missed_field = 0;
    }else {
        missed_field = 1;
        $("#error_title1").html('Please Enter Title');
    }
    if (message != ''){
        $("#error_message1").html('');
        missed_field = 0;
    }else {
        missed_field = 1;
        $("#error_message1").html('Please Enter Message');
    }
    if(missed_field == 0){
        $.ajax({
            type: "POST",
            url: "/member/advice_form/",
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", token);
            },
            data: {
                title: title,
                message : message,
                document_ids : $("#advice_certificate").val(),
                advisor_id: advisor_id,
                advisor_name: advisor_name,
                advisor_email: advisor_email
            },
            success: function (response) {
                if (ses_inv_chk_login && social_auth_ses){
                    $('#get-advice-modal').modal('hide');
                    $('#success_advice_model').modal({
                        show: true,
                        backdrop: 'static',
                        keyboard: false
                    });
                }
                else if(response == 'success'){
                    $("#invite_success_text")
                        .fadeIn()
                        .fadeOut(2500, 'swing');
                    $("#title").val('');
                    $("#message").val('');
                    $('#get-advice-modal').find('.attach_class').remove();
                    $('#get-advice-modal').find('.fa-eye').remove();
                    $('#get-advice-modal').find('.download_link_color').remove();
                    setTimeout(function () { $('#get-advice-modal').modal('hide'); }, 2500);
                }else{
                    alert('Some thing went wrong!');
                }
            },
            error:function (response) {
                alert('Unable to Upload \n Please try again after some time');
            }
        });
    }
}

// Uploading the Get advice question document
function upload_advice_doc(form_id) {
    var no_files = $("#advice_certificate").val();
    no_files = no_files.split(',');
    no_files = no_files.length;
    if (no_files < 5) {
        var upload_doc = upload_document(form_id);
        upload_doc.success(function(response){
            remove_icon = "&nbsp;&nbsp" +
                "<i class='fa fa-trash download_link_color'></i>";
            var adv_doc = $('#advice_certificate').val();
            if(adv_doc){
                adv_doc = adv_doc +","+ response.id;
            }else {
                adv_doc = response.id;
            }
            $('#advice_certificate').val(adv_doc);
            attach_document('uploaded_files', response , 'paper_clip0', true);
            $("#document").val('');
        });
        upload_doc.error(function(response){
            alert('Unable to Upload file \n Please try again after some time');
        });
    } 
    else { alert('Maximum uploadable files are five.');}
}
