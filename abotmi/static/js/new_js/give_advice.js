var csrf_token = $("#id_csrf_token").val();

// Loading the Give advice modal with setting fields empty
function give_advice(id){
    $('#give_advice_doc_id').find('.attach_class').remove();
    $('#give_advice_doc_id').find('.fa-eye').remove();
    $('#give_advice_doc_id').find('.download_link_color').remove();
    $('#give_advice_doc_id').find('br').remove();
    $('#give_advice_doc').val('');
    $('#advisors_answer').val('');
    $("#help_advisors_answer").html('');
    $('#give_advice_modal').modal({
        show: true,
        keyboard: false,
        backdrop: 'static'
    });
    $('#question_ids').val(id);
    $('#view_question_id').val(id);
}

// Loading answers for respective Advice question
function view_answers(id){
    var token = csrf_token;
    var question_id = $('#view_question_id').val();
    $.ajax({
        type: "POST",
        url: "/member/view_all_answers/",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        data:{
            question_id:id
        },
        success: function (response) {
            $('#give_advice_common_model').html('');
            $('#give_advice_common_model').html(response);
            $('#view_advices_modal').modal({
                show: true,
                keyboard: false,
                backdrop: 'static'
            });
        }
    });
}

// Submitting Give advice(Answer) form
function submit_advice(id){
    var token = csrf_token;
    var advisors_answer = $('#advisors_answer').val().trim();
    var question_id = $('#question_ids').val();
    if(advisors_answer!="" && question_id!=""){
        $.ajax({
            type: "POST",
            url: "/member/submit_advice/",
            data: {
                advice: advisors_answer,
                question_id: question_id,
                give_advice_doc: $('#give_advice_doc').val()
            },
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", token);
            },
            complete: function (e, xhr, settings) {
                var status = e.status;
                if (status == 200) {
                    $('#advisors_answer').val('');
                    $('#give_advice_modal').find('.attach_class').remove();
                    $('#give_advice_modal').find('.fa-eye').remove();
                    $('#give_advice_modal').find('.download_link_color').remove();
                    $('#give_advice_modal').find('br').remove();
                    show_alert(
                        'success',
                        'give_advice_modal',
                        '<p>Your advice has submitted.</p>'
                    );
                }
                else {
                    show_alert(
                        'error',
                        'give_advice_modal',
                        '<p>Unable to submit the advice. Please try again later</p>'
                    );
                }
            }
        });
    }else{
        $("#help_advisors_answer").html('Please Enter Your Advice');
    }
}

// Loading Get ADvice(Question) Documents for downloading
function download_docs(question_id){
    var token = csrf_token;
    $.ajax({
        type: "POST",
        url: "/member/download_docs/",
        data: {
            question_id: question_id
        },
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        success: function (response) {
            $("#view_document_model").remove();
            $('#give_advice_common_model').append(response);
            $('#view_advices_modal').modal('hide');
            $('#view_document_model').modal({
                show: true,
                backdrop: 'static',
                keyboard: false,
            });
        }
    });
}

// Loading Give Advice(Answer) documents to download
function download_answer_docs(question_id) {
    var token = csrf_token;
    $.ajax({
        type: "POST",
        url: "/member/download_advisors_docs/",
        data: {
            answer_id: question_id
        },
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        success: function (response) {
            $('#give_advice_model').append(response);
            $('#view_document_model').modal({
                show: true,
                backdrop: 'static',
                keyboard: false,
            });
        }
    });
}

// Uploading documents for Advice answer
function upload_advisor_docs(form_id){ 
    var no_files = $("#give_advice_doc").val();  
    no_files = no_files.split(',');
    no_files = no_files.length;
    if (no_files<5){
        var upload_doc = upload_document(form_id);
        upload_doc.success(function(response){
            remove_icon = "&nbsp;&nbsp" + "<i class='fa fa-trash download_link_color'></i>";
            var adv_doc = $('#give_advice_doc').val();
            if(adv_doc){
                adv_doc = adv_doc + "," + response.id;
            }else {
                adv_doc = response.id;
            }
            $('#give_advice_doc').val(adv_doc);
            attach_document('give_advice_doc_id', response , 'paper_clip', '', '', true);
        });
        upload_doc.error(function(response){
            alert('Unable to Upload file \n Please try again after some time');
        });
    }   
    else { alert('Maximum uploadable files are five.');} 
}
