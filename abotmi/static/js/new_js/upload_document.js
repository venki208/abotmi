var csrf_token = $("#id_csrf_token").val();
var token = csrf_token;
var remove_icon = '';

/**
 * @use -> used upload the documents and attaching docs
 * @param {formId} str -> form attribute id
 * @param {HTMLId} div_name -> attachement documents div id
 *      it will use for attaching uploaded documents
 * @param {HTMLId} paper -> upload button clip id
 */
function UploadDocuments(str, div_name, paper, success_alert=true) {
    var form_data = new FormData($('#'+str)[0]);
    $("#"+ div_name).find('.add-shadow').removeClass('add-shadow');
    $.ajax({
        type: 'POST',
        url: '/signup/upload_file/',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        async: true,
        success: function(data) {
            $("#"+paper).find('input[type="file"]').val('');
            var popup = data.required_documents;
            var input_value = $('#' + str).find('input[name="documents_type"]').val();
            if (input_value =='document_edu_qua1'){
                $("#documents_upload1").val(data.id);
                onChange_save_additional_qualification();
            } else if (input_value =='document_edu_qua2'){
                $("#documents_upload2").val(data.id);
                onChange_save_additional_qualification();
            } else if (input_value =='document_edu_qua3'){
                $("#documents_upload3").val(data.id);
                onChange_save_additional_qualification();
            }else if (input_value =='document_edu_qua4'){
                $("#documents_upload4").val(data.id);
                onChange_save_additional_qualification();
            }else if (input_value =='document_edu_qua5'){
                $("#documents_upload5").val(data.id);
                onChange_save_additional_qualification();
                $("#add_field").addClass('disabled');
            }else if (input_value =='highest_qualification_upload'){
                highest_qualification_status = 'True';
                document.getElementById('help-text-certificate').innerHTML='';
            }
            if (input_value == 'sebi_certificate') {
                sebi_certificate_status = 'True';
            } else if (input_value == 'amfi_certificate') {
                amfi_certificate_status = 'True';
            } else if (input_value == 'irda_certificate') {
                irda_certificate_status = 'True';
            } else if (input_value == 'others_certificate') {
                others_certificate_status = 'True';
            } else if (input_value == 'eipv_doc'){
                eipv_aadhaar=false;
            }

            // changing icon according to reupload or delete
            if (input_value == 'sebi_renewal_certificate' || input_value == 'amfi_renewal_certificate'
                || input_value == 'irda_renewal_certificate' || input_value == 'others_renewal_certificate'){
                    remove_icon = "&nbsp;&nbsp"+
                        "<i class='fa fa-trash download_link_color'></i>";
            }else{
                remove_icon = "&nbsp;&nbsp" +
                    "<i class='fa fa-trash download_link_color'></i>";
                $("#" + paper).addClass('hide');
            }

            // creating view and delete/reupload and attaching to uploaded div
            var download = document.getElementById(div_name);
            var remove_file = document.createElement('a');
            remove_file.innerHTML = remove_icon;
            remove_file.setAttribute('id',data.id);
            remove_file.setAttribute('class','hiding'+data.id);
            remove_file.setAttribute("onclick","removeDocument('"+data.id+"','"+paper+"');");
            var attach_text = document.createElement('p');
            attach_text.setAttribute('class','hiding'+data.id+ ' attach_class n-padding-r-5');
            attach_text.innerHTML = 'Attached';
            var download_file = document.createElement('a');
            download_file.setAttribute('id',data.id);
            download_file.setAttribute('href',data.url);
            download_file.setAttribute('class','hiding'+data.id+ ' download_link_color n-padding-r-5');
            download_file.setAttribute('onclick', "window.open('"+data.url+"', 'newwindow', 'toolbar=yes,scrollbars=yes,resizable=yes,top=250,left=500,width=550, height=550'); return false;");
            download_file.innerHTML = "<i class='fa fa-eye' aria-hidden='true'></i>";
            download.appendChild(attach_text);
            download.appendChild(download_file);
            download.appendChild(remove_file);

            $('#id_form_div').removeClass('hide');
            if (success_alert){
                $.toast({
                    text: 'Uploaded Successfully',
                    textAlign: 'center',
                    showHideTransition: 'slide',
                    position: 'top-center',
                    icon: 'success'
                });
            }
            document.getElementById('help_text_document').innerHTML = "";
        },
        error:function (response) {
            $.toast({
                heading: 'Error',
                text: 'Unable to upload the document <br /> Please try again.',
                showHideTransition: 'slide',
                position: 'top-center',
                icon: 'error'
            });
        }
    });
}

/**
 * @use: Used to deleteing the documents and removing from attachment div
 * @param {HTMLAttrID} id 
 * @param {HTMLAttrID} paper 
 */
function removeDocument(id,paper){
    var input_value = $("#"+paper).parent().find('input').val();
    if(confirm("Do you want to remove the document?")){
        if ($('.hiding' + id).find('i.fa-trash')[0]) {
            $.ajax({
                url: "/signup/delete_upload_file/",
                method: "POST",
                beforeSend: function (request) {
                    request.setRequestHeader("X-CSRFToken", token);
                },
                data: {
                    id: id
                },
                success: function (data) {
                    if (data == 'success'){
                        $("#"+paper).removeClass('hide');
                        var viewd_doc_inp_id = $("#viewed_doc_id").val();

                        if(viewd_doc_inp_id){
                            var rera_ren_inpu_doc_ids = $("#" + viewd_doc_inp_id).val();
                            var doc_ids = rera_ren_inpu_doc_ids.split(',');
                            for (i=0; i<doc_ids.length; i++){
                                if(doc_ids[i] == id){
                                    doc_ids.splice(i, 1);
                                }
                            }
                            $("#"+viewd_doc_inp_id).val(doc_ids.join());
                        }
                        var viewed_advice_certificate = $('#give_advice_doc').val();
                        if (viewed_advice_certificate) {
                            var doc_ids = viewed_advice_certificate.split(',');
                            for (i = 0; i < doc_ids.length; i++) {
                                if (doc_ids[i] == id) {
                                    doc_ids.splice(i, 1);
                                }
                            }
                            $("#give_advice_doc").val(doc_ids.join());
                        }

                        var viewed_advice_certificate = $('#advice_certificate').val();
                        if (viewed_advice_certificate) {
                            var doc_ids = viewed_advice_certificate.split(',');
                            for (i = 0; i < doc_ids.length; i++) {
                                if (doc_ids[i] == id) {
                                    doc_ids.splice(i, 1);
                                }
                            }
                            $("#advice_certificate").val(doc_ids.join());
                        }
                        $('.hiding' + id).remove();
                        $('#br'+id).remove();
                        $("#"+paper).removeClass('hide');
                    }else{
                        alert('Unable to delete document \n Please try again after some time');
                    }
                },
                error: function(response){
                    alert('Unable to delete document \n Please try again after some time');
                }
            });
        }else{
            $("#"+paper).removeClass('hide');
            $('.hiding' + id).remove();
            if (input_value == 'sebi_certificate'){
                sebi_certificate_status = 'False';
            }else if (input_value == 'amfi_certificate'){
                amfi_certificate_status = 'False';
            }else if (input_value == 'irda_certificate'){
                irda_certificate_status = 'False';
            }else if(input_value == 'others_certificate'){
                others_certificate_status = 'False';
            }
        }
    }
}

/**
 * @use: upload the document and return the ajax callback functions
 * @param {HTMLFormId} form_id -> need to pass HTML form attribute id
 */
function upload_document(form_id, form_obj){
    var form_data;
    if(form_id){
        form_data = new FormData($('#' + form_id)[0]);
    }else{
        console.log('it is here');
        form_data = form_obj;
    }
    return $.ajax({
        type: 'POST',
        url: '/signup/upload_file/',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        async: true
    });
}

/**
 * 
 * @param {HTMLAttrId} div_name 
 * @param {Json} data 
 * @param {HTMLAttrId} paper -> button clip id
 * @param {boolean} filename -> true/false
 *      true -> attach the document to div with filename
 *      else -> attach the document with out filename
 */
function attach_document(div_name, data, paper, filename, remove_func, success_alert=true){
    var download = document.getElementById(div_name);
    var remove_file = document.createElement('a');
    remove_file.innerHTML = remove_icon;
    remove_file.setAttribute('id', data.id);
    remove_file.setAttribute('class', 'hiding' + data.id);
    if (remove_func){
        remove_func = remove_func;
    }else{
        remove_func = "removeDocument('" + data.id + "','" + paper + "');"
    }
    remove_file.setAttribute("onclick", remove_func);
    var attach_text = document.createElement('span');
    attach_text.setAttribute('class', 'hiding' + data.id + ' attach_class n-padding-r-5');
    attach_text.setAttribute('title', data.file_name );
    if(filename == true){
        attach_text.innerHTML = 'Attached ' + data.file_name;
    }else{
        attach_text.innerHTML = 'Attached';
    }
    var download_file = document.createElement('a');
    download_file.setAttribute('id', data.id);
    download_file.setAttribute('href', data.url);
    download_file.setAttribute('class', 'hiding' + data.id + ' download_link_color n-padding-r-5');
    download_file.setAttribute('onclick', "window.open('" + data.url + "', 'newwindow', 'toolbar=yes,scrollbars=yes,resizable=yes,top=250,left=500,width=550, height=550'); return false;");
    download_file.innerHTML = "<i class='fa fa-eye' aria-hidden='true'></i>";
    download.appendChild(attach_text);
    download.appendChild(download_file);
    download.appendChild(remove_file);
    var break_tag = document.createElement('br');
    break_tag.setAttribute('id', 'br'+data.id);
    download.appendChild(break_tag);
    if (success_alert){
       $.toast({
            text: 'Uploaded Successfully.',
            textAlign: 'center',
            showHideTransition: 'slide',
            position: 'top-center',
            icon: 'success'
        });
    }
}

// Delete and remove the document, returns ajax callback functions
function remove_doc(id){
    return $.ajax({
        url: "/signup/delete_upload_file/",
        method: "POST",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        data: {
            id: id
        }
    });
}
