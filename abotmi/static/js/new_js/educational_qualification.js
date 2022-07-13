var csrf_token = $("#id_csrf_token").val();
var highest_qul_input = $("#highest_qualification");
var year_pass_input = $("#year_passout");
var col_name_input = $("#college_name");
var oth_col_name_input = $("#others_college_name");

// setting readonly mode if highest Education qualification is preset
$(document).ready(function () {
    if (edu_category != '') {
        $("#div_highest_qualification").removeClass('hide');
        $("#div_additional_qualification").removeClass('hide');
    }
    if (edu_category == graduation_value) {
        document.getElementById("graduation").checked = true;
    }
    else if (edu_category == post_graduation_value) {
        document.getElementById("post_graduation").checked = true;
    }
    else if (edu_category == doctorate_value) {
        document.getElementById("doctorate").checked = true;
    }
    else if (edu_category == post_doctorate_value) {
        document.getElementById("post_doctorate").checked = true;
    }
    else if (edu_category == professional_qualification_value) {
        document.getElementById("professional_qualification").checked = true;
    }
    else if (edu_category == other_qualification_value) {
        document.getElementById("other_qualification").checked = true;
    }

    select = year_pass_input[0];
    var date = new Date(), dateArray = [], i;
    curYear = date.getFullYear();
    for (i = 0; i < 65; i++) {
        dateArray[i] = (curYear - 65) + i;
        var opt = document.createElement('option');
        opt.value = dateArray[i];
        opt.innerHTML = dateArray[i];
        select.appendChild(opt);
    }
    if (highest_qualification !=''){
        highest_qul_input.attr('readonly', true);
    }

    if (college_name != '') {
        if (jQuery.inArray(college_name, college_list_array) < 0) {
            $("#others_college_div").show();
            oth_col_name_input
                .val(college_name)
                .attr('readonly', true);
            col_name_input
                .val('others')
                .attr('disabled', true);
        } else {
            col_name_input
                .val(college_name)
                .attr('disabled', true);
        }
    }

    if (year_of_passing != 'sele' || year_of_passing != '') {
        year_pass_input.val(year_of_passing);
        year_pass_input.attr('disabled', true);
    }else{
        year_pass_input.val('select');
    }
});

// Attaching/Binding click event
$("#highest_qualification_upload_cert").bind(
    'click',
    ['highest_qualification_upload_cert'],
    show_education_qualification
);

// function for show the bootstrap modal
function show_bootstrap_modal(elem) {
    $(elem).modal({
        show: true,
        keyboard: false,
        backdrop: 'static'
    });
}

// Load Regulatory upload documents modal
function show_education_qualification(certificate_type){
    var certificate_type = certificate_type.data[0];
    $.ajax({
        method : 'POST',
        url : '/signup/show_education_qualification/',
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", csrf_token);
        },
        data:{
            'education_qualification_type': certificate_type
        },
        success: function(response){
            $("#personal_information_modal_div").html('');
            $("#personal_information_modal_div").html(response);
            $("#educationModal").modal('hide');
            show_bootstrap_modal('#add_educational_qualification_modal');
            $("#add_educational_qualification_modal")
                .find('button.close')
                .attr('onclick', "load_education_modal('#educationModal');")
                .removeAttr('data-dismiss');
            $("#education_title").html('UPLOAD CERTIFICATE');
            if(certificate_type=='edu_qua_certificate1'){
                $("#edu_documents_type").val('document_edu_qua1');
            }
            else if (certificate_type=='edu_qua_certificate2') {
                $("#edu_documents_type").val('document_edu_qua2');
            }
            else if (certificate_type=='edu_qua_certificate3') {
                $("#edu_documents_type").val('document_edu_qua3');
            }
            else if (certificate_type=='edu_qua_certificate4') {
                $("#edu_documents_type").val('document_edu_qua4');
            }
            else if (certificate_type=='edu_qua_certificate5') {
                $("#edu_documents_type").val('document_edu_qua5');
            }
            else if(certificate_type=='highest_qualification_upload_cert'){
                $("#edu_documents_type").val('highest_qualification_upload');
            }
        },
        error: function(response){
            alert('Unable to Process your request. \n Please try again after some time');
        }
    });
}

// Loading Education Modal
function load_education_modal(elem){
    $("#add_educational_qualification_modal").modal('hide');
    $(elem).modal({
        show: true,
        keyboard: false,
        backdrop: 'static'
    });
}

// Loading Additional Qualification
var ivalue = 0;
function loading_additional_qualification() {
    var q = add_additional_qualification;
    var remove_btn_html, doc_status;
    if(q!="") {
        q=q.replace(/&quot;/gi,"\"");
        q='{"row":'+q+'}';
        var obj = JSON.parse(q);
        ivalue=obj.row.length;
        for (var i = 0; i <obj.row.length; i++) {
            var data = obj.row[i];
            k=i+1;
            doc_status = data.document_verified;
            if(doc_status != 'verified'){
                remove_btn_html = "<label>" +
                    "<a class='remove_field btn additional_btn' id='remove_field' onclick='remove_additional_qualification();'>" +
                    "<i class='fa fa-minus-circle'>" +
                    "</i>" +
                    "</a>" +
                    "</label>";
            }else{
                remove_btn_html = '';
            }
            if(i==0){
                my_div1.innerHTML ="<div class='col-sm-12 col-xs-12'>"+
                    "<div class='row'>"+
                        "<div class='col-sm-4 col-xs-12'>"+
                            "<div class='form-group control-group'>"+
                                "<div class='control'>"+
                                    "<p>Additional Qualification</p>"+
                                    "<input type='text' class='form-control' name='additional_qualification"+k+"' id='additional_qualification"+k+"' value='"+data.additional_qualification+"' onchange='onChange_save_additional_qualification();' placeholder='CFA'>"+
                                "</div>"+
                            "</div>"+
                        "</div>"+
                        "<div class='col-sm-3 col-xs-12'>"+
                            "<div class='form-group control-group'>"+
                                "<div class='control'>"+
                                    "<p>Year of Completion</p>"+
                                    "<select name='additional_year_passout"+k+"' class='form-control' id='additional_year_passout"+k+"' onchange='onChange_save_additional_qualification();'>"+
                                        "<option value='"+data.year_passout+"'>"+data.year_passout+"</option>"+
                                    "</select>"+
                                "</div>"+
                            "</div>"+
                        "</div>"+
                        "<div class='col-sm-3 col-xs-12'>"+
                            "<div class='form-group control-group'>"+
                                "<div class='control'>"+
                                    "<p>University / Board</p>"+
                                    "<input type='text' class='form-control' name='additional_high_board"+k+"' id='additional_high_board"+k+"' value='"+data.university+"' onchange='onChange_save_additional_qualification();' placeholder='University / Board'>"+
                                "</div>"+
                            "</div>"+
                        "</div>"+
                        "<div class='col-sm-2 col-xs-12 add-addtional-qualification-docu'>"+
                        "<div class='row'>"+
                            "<p>"+"&nbsp;"+"</p>"+
                            "<label id='document_edu_qua"+k+"' name='document_edu_qua"+k+"' class='fileinput fileinput-edu_qua' data-provides='fileinput'>"+
                                "<span class='btn additional_btn btn-file' id='edu_qua_certificate"+k+"'>"+
                                    "<i class='fa fa-paperclip' aria-hidden='true'>"+
                                    "</i>"+
                                "</span>"+
                            "</label>"+
                            remove_btn_html+
                            "<input type='hidden' name='documents_upload"+k+"' id='documents_upload"+k+"' value='"+data.documents_upload+"'>"+
                        "</div>"+
                        "</div>"+
                    "</div>"+
                "</div>";
                $("#edu_qua_certificate"+k).bind('click', ['edu_qua_certificate'+k], show_education_qualification);
                if (doc_status == 'verified') {
                    $("#additional_qualification"+k).prop('readonly', true);
                    $("#additional_year_passout"+k).prop('disabled', true);
                    $("#additional_high_board"+k).prop('readonly', true);
                }
            }else{
                var divdata ="<div class='col-sm-12 col-xs-12'>"+
                    "<div class='row'>"+
                        "<div class='col-sm-4 col-xs-12'>"+
                            "<div class='form-group control-group'>"+
                                "<div class='control'>"+
                                    "<input type='text' class='form-control' name='additional_qualification"+k+"' id='additional_qualification"+k+"' value='"+data.additional_qualification+"' onchange='onChange_save_additional_qualification();' placeholder='CFA'>"+
                                "</div>"+
                            "</div>"+
                        "</div>"+
                        "<div class='col-sm-3 col-xs-12'>"+
                            "<div class='form-group control-group'>"+
                                "<div class='control'>"+
                                    "<select name='additional_year_passout"+k+"' class='form-control' id='additional_year_passout"+k+"' onchange='onChange_save_additional_qualification();'>"+
                                        "<option value='"+data.year_passout+"'>"+data.year_passout+"</option>"+
                                    "</select>"+
                                "</div>"+
                            "</div>"+
                        "</div>"+
                        "<div class='col-sm-3 col-xs-12'>"+
                            "<div class='form-group control-group'>"+
                                "<div class='control'>"+
                                    "<input type='text' class='form-control' name='additional_high_board"+k+"' id='additional_high_board"+k+"' value='"+data.university+"' onchange='onChange_save_additional_qualification()' placeholder='University / Board' >"+
                                "</div>"+
                            "</div>"+
                        "</div>"+
                        "<div class='col-sm-2 col-xs-12 add-addtional-qualification-docu'>"+
                            "<div class='row'>"+
                            "<label id='document_edu_qua"+k+"' name='document_edu_qua"+k+"' class='fileinput fileinput-edu_qua' data-provides='fileinput'>"+
                                "<span class='btn additional_btn btn-file' id='edu_qua_certificate"+k+"'>"+
                                    "<i class='fa fa-paperclip' aria-hidden='true'>"+
                                    "</i>"+
                                "</span>"+
                            "</label>"+
                    remove_btn_html +
                    "<input type='hidden' name='documents_upload" + k + "' id='documents_upload" + k + "' value='" + data.documents_upload + "'>" +
                            "</div>"+

                        "</div>"+
                    "</div>"+
                "</div>";
                switch (k) {
                    case 2:
                        my_div2.innerHTML = divdata;
                        break;
                    case 3:
                        my_div3.innerHTML = divdata;
                        break;
                    case 4:
                        my_div4.innerHTML = divdata;
                        break;
                    case 5:
                        my_div5.innerHTML =divdata;
                        break;
                    }
                $("#edu_qua_certificate"+k).bind('click', ['edu_qua_certificate'+k], show_education_qualification);
                if (doc_status == 'verified') {
                    $("#additional_qualification" + k).prop('readonly', true);
                    $("#additional_year_passout" + k).prop('disabled', true);
                    $("#additional_high_board" + k).prop('readonly', true);
                }
            }
            select = document.getElementById('additional_year_passout'+k);
            var date = new Date(), dateArray = new Array(), j;
            curYear = date.getFullYear();
            for(j = 0; j<65; j++) {
                dateArray[j] = (curYear-65)+j;
                var opt = document.createElement('option');
                opt.value = dateArray[j];
                opt.innerHTML = dateArray[j];
                select.appendChild(opt);
            }
        }
    }
}

// Adding dynamic fields to Additional Qualification
function changeIt(){
    if(validate_additional_qualifications(true)){
    ivalue ++;
        if(ivalue<=5){
            if(ivalue==1){
                my_div1.innerHTML =
                "<div class='col-xs-12'>"+
                    "<div class='row'>"+
                        "<div class='col-sm-4 col-xs-12'>"+
                            "<div class='form-group control-group'>"+
                                "<div class='control'>"+
                                    "<p>Additional Qualification</p>"+
                                    "<input type='text' class='form-control' name='additional_qualification"+ivalue+"' id='additional_qualification"+ivalue+"' value='' onchange='onChange_save_additional_qualification();'>"+
                                    "<span class='help-block' id='help_highest_qualification"+ivalue+"'>"+"</span>"+
                                "</div>"+
                            "</div>"+
                        "</div>"+
                        "<div class='col-sm-3 col-xs-12'>"+
                            "<div class='form-group control-group'>"+
                                "<div class='control'>"+
                                    "<p>Year of Completion</p>"+
                                    "<select name='additional_year_passout"+ivalue+"' value=''  onchange='onChange_save_additional_qualification();' class='form-control' id='additional_year_passout"+ivalue+"'>"+
                                        "<option value='select'>--Select--</option>"+
                                    "</select>"+
                                    "<span class='help-block' id='help_year_passout"+ivalue+"'>"+"</span>"+
                                "</div>"+
                            "</div>"+
                        "</div>"+
                        "<div class='col-sm-3 col-xs-12'>"+
                            "<div class='form-group control-group'>"+
                                "<div class='control'>"+
                                    "<p>University / Board</p>"+
                                    "<input type='text' class='form-control' name='additional_high_board"+ivalue+"' id='additional_high_board"+ivalue+"' value=''  onchange='onChange_save_additional_qualification();' >"+
                                    "<span class='help-block' id='help_college_name"+ivalue+"'>"+"</span>"+
                                "</div>"+
                            "</div>"+
                        "</div>"+
                        "<div class='col-sm-2 col-xs-12 add-addtional-qualification-docu'>"+
                        "<div class='row'>"+
                            "<p>"+"&nbsp;"+"</p>"+
                            "<label id='document_edu_qua"+ivalue+"' name='document_edu_qua"+ivalue+"' class='fileinput fileinput-edu_qua' data-provides='fileinput'>"+
                                "<span class='btn additional_btn btn-file' id='edu_qua_certificate"+ivalue+"'>"+
                                    "<i class='fa fa-paperclip' aria-hidden='true'>"+
                                    "</i>"+
                                "</span>"+
                            "</label>"+
                            "<label>"+
                            "<a class='remove_field btn additional_btn' id='remove_field' onclick='remove_additional_qualification();'>"+
                                "<i class='fa fa-minus-circle'>"+
                                "</i>"+
                            "</a>"+
                            "</label>"+
                            "<input type='hidden' name='documents_upload"+ivalue+"' id='documents_upload"+ivalue+"' value=''>"+
                        "</div>"+
                        "</div>"+
                    "</div>"+
                "</div>";
                $("#edu_qua_certificate"+ivalue).bind('click', ['edu_qua_certificate'+ivalue], show_education_qualification);
            }else{
                var divdata=
                "<div class='col-sm-12 col-xs-12'>"+
                    "<div class='row'>"+
                        "<div class='col-sm-4 col-xs-12'>"+
                            "<div class='form-group control-group'>"+
                                "<div class='control'>"+
                                    "<input type='text' class='form-control' name='additional_qualification"+ivalue+"' id='additional_qualification"+ivalue+"' value=''  onchange='onChange_save_additional_qualification();'>"+
                                    "<span class='help-block' id='help_highest_qualification"+ivalue+"'>"+"</span>"+
                                "</div>"+
                            "</div>"+
                        "</div>"+
                        "<div class='col-sm-3 col-xs-12'>"+
                            "<div class='form-group control-group'>"+
                                "<div class='control'>"+
                                    "<select name='additional_year_passout"+ivalue+"' value='' onchange='onChange_save_additional_qualification();' class='form-control' id='additional_year_passout"+ivalue+"'>"+
                                        "<option value='select'>--Select--</option>"+
                                    "</select>"+
                                    "<span class='help-block' id='help_year_passout"+ivalue+"'>"+"</span>"+
                                "</div>"+
                            "</div>"+
                        "</div>"+
                        "<div class='col-sm-3 col-xs-12'>"+
                            "<div class='form-group control-group'>"+
                                "<div class='control'>"+
                                    "<input type='text' class='form-control' name='additional_high_board"+ivalue+"' id='additional_high_board"+ivalue+"' value='' onchange='onChange_save_additional_qualification();' >"+
                                    "<span class='help-block' id='help_college_name"+ivalue+"'>"+"</span>"+
                                "</div>"+
                            "</div>"+
                        "</div>"+
                        "<div class='col-sm-2 col-xs-12 add-addtional-qualification-docu'>"+
                        "<div class='row'>"+
                            "<label id='document_edu_qua"+ivalue+"' name='document_edu_qua"+ivalue+"' class='fileinput fileinput-edu_qua' data-provides='fileinput'>"+
                                "<span class='btn additional_btn btn-file' id='edu_qua_certificate"+ivalue+"'>"+
                                    "<i class='fa fa-paperclip' aria-hidden='true'>"+
                                    "</i>"+
                                "</span>"+
                            "</label>"+
                            "<label>"+
                            "<a class='remove_field btn additional_btn' id='remove_field' onclick='remove_additional_qualification();'>"+
                                "<i class='fa fa-minus-circle'>"+
                                "</i>"+
                            "</a>"+
                            "</label>"+
                            "<input type='hidden' name='documents_upload"+ivalue+"' id='documents_upload"+ivalue+"' value=''>"+
                        "</div>"+
                        "</div>"+
                    "</div>"+
                "</div>";
                switch (ivalue) {
                        case 2:
                            my_div2.innerHTML = divdata;
                            break;
                        case 3:
                            my_div3.innerHTML = divdata;
                            break;
                        case 4:
                            my_div4.innerHTML = divdata;
                            break;
                        case 5:
                            my_div5.innerHTML = divdata;
                            break;
                        }
                    $("#edu_qua_certificate"+ivalue).bind('click', ['edu_qua_certificate'+ivalue], show_education_qualification);
            }
            select = document.getElementById('additional_year_passout'+ivalue);
            var date = new Date(), dateArray = new Array(), i;
            curYear = date.getFullYear();
                for(i = 0; i<65; i++) {
                    dateArray[i] = (curYear-65)+i;
                    var opt = document.createElement('option');
                    opt.value = dateArray[i];
                    opt.innerHTML = dateArray[i];
                    select.appendChild(opt);
                }
        }
    }
}

// Removing Additional qualification detail row
function remove_additional_qualification(){
    if(ivalue>0){
        switch (ivalue) {
        case 1:
            $("#my_div1").empty();
            break;
        case 2:
            $("#my_div2").empty();
            break;
        case 3:
            $("#my_div3").empty();
            break;
        case 4:
            $("#my_div4").empty();
            break;
        case 5:
            $("#my_div5").empty();
            $("#add_field").removeClass('disabled');
            break;
        }
        ivalue --;
        onChange_save_additional_qualification();
    }
}

// Saving on Additional Educational Qualification data by on changing
function onChange_save_additional_qualification(){
    var advisor_additional_qualifications = creating_additional_qualification_json();
    if (validate_additional_qualifications(false)){
        save_onchange_qualification(
            "additional_qualification",advisor_additional_qualifications);
    }
}

// Creating Json of Additional Qualification data
function creating_additional_qualification_json(){
    var additional_qualification="";
    for(i=1; i<=ivalue&&i<=5; i++){
        add_qualification = document.getElementById("additional_qualification"+i).value;
        year_of_completion = document.getElementById("additional_year_passout"+i).value;
        university = document.getElementById("additional_high_board"+i).value;
        documents_uploads = document.getElementById("documents_upload"+i).value;
        edu_qua_certificate = "document_edu_qua"+i;
        if(i==1){
         additional_qualification=additional_qualification+'{"additional_qualification":"'+add_qualification+'", "year_passout":"'+year_of_completion+'","university":"'+university+'","edu_qua_certificate":"'+edu_qua_certificate+'","document_verified":"not_verified","documents_upload":"'+documents_uploads+'"}';
        }else{
         additional_qualification=additional_qualification+',{"additional_qualification":"'+add_qualification+'", "year_passout":"'+year_of_completion+'","university":"'+university+'","edu_qua_certificate":"'+edu_qua_certificate+'","document_verified":"not_verified","documents_upload":"'+documents_uploads+'"}';
        }
    }
    var advisor_additional_qualifications='['+additional_qualification+']';
    return advisor_additional_qualifications;
}

// Validating the Additional Qualification
function validate_additional_qualifications(is_valid){
    flag=true;
    if(ivalue<=5){
        for(i=1; i<=ivalue; i++){
            add_qualification=document.getElementById("additional_qualification"+i).value;
            year_of_completion=document.getElementById("additional_year_passout"+i).value;
            university=document.getElementById("additional_high_board"+i).value;
            documents_uploads=document.getElementById("documents_upload"+i).value;
            var alpha = /^[a-zA-Z]+(([\'\,\.\- ][a-zA-Z ])?[a-zA-Z]*)*$/.test(add_qualification);
            if (add_qualification == null || add_qualification == "") {
                if (is_valid){
                    alert("Additional Qualification "+i+" must be filled out");
                }
                flag=false;
            }else if(year_of_completion == null || year_of_completion =="select") {
                if(is_valid) {
                    alert("Select Year Of Completion "+i+"");
                }
                flag=false;
            } else if (university == null || university == "") {
                if (is_valid) {
                    alert("University "+i+" must be filled out");
                }
                flag=false;
            }else if(documents_uploads == null || documents_uploads == "") {
                if (is_valid) {
                    alert("documents"+i+" must be uploaded");
                }
                flag=false;
            } else if (alpha == false) {
                if (is_valid) {
                    alert("Enter Only Characters. Additional Qualification "+i);
                 }
                flag=false;
            }
        }
    }
    else{
        flag=true;
    }
    return flag;
}

// Enable the Educational Qualification fields
function check_qualification(){
    if ($('input[name="educational_qualification"]:checked').length>0) {
        var ed_cat = $('input[name="educational_qualification"]');
        for (i = 0; i < ed_cat.length; i++) {
            $("#validate_" + ed_cat[i].id).append('<style>input[type=radio]+#validate_' + ed_cat[i].id +'::before{border-color:#adb8c0;}</style>');
        }
        $("#help-text-education_qualification").html('');
        $("#div_highest_qualification").removeClass('hide');
        $("#div_additional_qualification").removeClass('hide');
        highest_qul_input
            .val('')
            .attr('readonly', false);
        year_pass_input
            .val('select')
            .attr('disabled', false);
        col_name_input
            .val('')
            .attr('disabled', false);
        oth_col_name_input
            .val('')
            .attr('readonly', false);
        $("#others_college_div").hide();
    }
}

// On change saving Educational Qualification
function save_onchange_qualification(name,value){
    var token = csrf_token;
    $.ajax({
        url:"/signup/onchange_save_field/",
        method: "POST",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token );
        },
        data :{
            username : user_name,
            value : value,
            name : name
        }
    });
}

// Getting selected Educational catogery
function get_educational_category(){
    var category;
    if(document.getElementById('graduation').checked){
        category = graduation_value;
    }
    else if (document.getElementById('post_graduation').checked) {
        category = post_graduation_value;
    }
    else if (document.getElementById('doctorate').checked) {
        category = doctorate_value;
    }
    else if (document.getElementById('post_doctorate').checked) {
        category = post_doctorate_value;
    }
    else if (document.getElementById('professional_qualification').checked) {
        category = professional_qualification_value;
    }
    else if (document.getElementById('other_qualification').checked) {
        category = other_qualification_value;
    }
    if (category != ""){
        document.getElementById('help-text-education_qualification').innerHTML='';
    }
    return category;
}

// Showing/Hiding college name div to enter other college name
$('#college_name').on('change', function () {
    if ($(this).val() == "others") {
        $("#others_college_div").show();
    }
    else {
        $("#others_college_div").hide();
    }
});
