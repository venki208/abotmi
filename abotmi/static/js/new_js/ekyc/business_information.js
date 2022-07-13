var token = csrf_token;

$("#t-a-t-v").val(avg_transaction);
function training_program() {
    if (document.getElementById('question_four_no').checked == true) {
        document.getElementById('help-text-question_four').innerHTML = '"To become a digital asset advisor, we will require that you undergo an online training program offered by The Digital Assets Academy"';
    } else {
        document.getElementById('help-text-question_four').innerHTML = '';
    }
}

function check_field(id) {
    $("#" + id).removeClass('not_valid');
    $("#help_" + id).html('');
}

function loadingStartPage() {
    if (question_1_ans == "yes") {
        $('#question_one_yes').prop('checked', true);
        $('#question1_div_area').css("display", "flex");
    }
    else if (question_1_ans == "no") {
        document.getElementById('question_one_no').checked = true;
        document.getElementById('question_one_yes').checked = false;
        document.getElementById('y-o-b').value = '';
        document.getElementById('t-n-o-c').value = 0;
        document.getElementById('t-a-t-v').value = 'select';
    }

    if (question_2_ans == "yes") {
        $('#question_two_yes').prop('checked', true);
        $('#question_two_no').prop('checked', false);
        $('#question2_div_area').css("display", "flex");
        $('#question_two_no').attr('onchange', "clickResponse(0,'question2_div_area','question_two_yes','question_two_no','infra_address');");
    }
    else if (question_2_ans == "no") {
        $('#question_two_yes').prop('checked', false);
        $('#question_two_no').prop('checked', true);
        $('#question_two_no').attr('onchange', "clickResponse(0,'question2_div_area','question_two_yes','question_two_no','infra_address');");

    }
    else {
        $("#question_two_no").attr('onchange', "clickResponse(0,'question2_div_area','question_two_yes','question_two_no','infra_address'); onchange_savequestions(id);");
    }

    if (question_3_ans == "no") {
        $('#question_three_yes').prop('checked', false);
        $('#question_three_no').prop('checked', true);
        $('#question_three_no').attr('onchange', "clickResponse(0,'question3_div_area','question_three_yes','question_three_no','');");
    }
    else if (question_3_ans == "yes") {
        $('#question_three_yes').prop('checked', true);
        $('#question_three_no').prop('checked', false);
        $('#question3_div_area').css("display", "flex");
        $('#question_three_no').attr('onchange', "clickResponse(0,'question3_div_area','question_three_yes','question_three_no','');");
    }
    else {
        $('#question_three_no').attr('onchange', "clickResponse(0,'question3_div_area','question_three_yes','question_three_no','');");
    }
    // var office_add = office_add;
    // var hidden_office_add = hidden_office_add;
    office_add = office_add.replace(/!/g, " ");
    office_add = office_add.replace(/[$]/g, "\n");
    document.getElementById('infra_address').innerHTML = office_add;
    $("#infra_address").attr("onchange", "onchange_savequestions(id);");
    // var num = num;
    if (num != "") {
        organisation_div.innerHTML = "";
        count = 0;
        for (var ivalue = 1; ivalue <= num; ivalue++) {
            x++;
            allids.push(x);
            // var on_val = on_val;
            q1 = on_val.replace(/u&#39;/gi, "\"");
            q1 = q1.replace(/&#39;/gi, "\"");
            var obj = JSON.parse(q1);
            var name = obj[count].Answer;
            count++;
            var official_email_id = obj[count].Answer;
            count++;
            var registration_id = obj[count].Answer;
            count++;
            var year = obj[count].Answer;
            count++;
            var wrapper = $("#organisation_div");
            $(wrapper).append('\
                    <div class="row n-margin-0" id="financial_organisation'+ ivalue + '">' +
                '<div class="col-md-11 col-xs-11 col-sm-11">' +
                '<div class="col-md-3 col-xs-12 col-sm-6">' +
                '<div class="control">' +
                '<label><b>Organization Name</b></label>' +
                '<input type="text" class="form-control" name="institution_name' + ivalue + '" id="institution_name' + ivalue + '" onchange="validate_organisation_name(' + ivalue + ');checking_modified(id,' + "'" + name + "'" + ');" value="' + name + '"></input>' +
                '<span class="help-block" id="help_institution_name' + ivalue + '"></span>' +
                '</div>' +
                '</div>' +
                '<div class="col-md-3 col-xs-12 col-sm-6">' +
                '<div class="control">' +
                '<label><b>Company URL</b></label>' +
                '<input type="text" class="form-control lower_case" name="official_email_id' + ivalue + '" id="official_email_id' + ivalue + '" onchange="CheckIsValidDomain(' + ivalue + ');checking_modified(id,' + "'" + official_email_id + "'" + ');" value="' + official_email_id + '"></input>' +
                '<span class="help-block" id="help_official_email_id' + ivalue + '"></span>' +
                '</div>' +
                '</div>' +
                '<div class="col-md-3 col-xs-12 col-sm-6">' +
                '<div class="control">' +
                '<label><b>Official Email/Registration Id</b></label>' +
                '<input type="text" class="form-control" name="registration_id' + ivalue + '" id="registration_id' + ivalue + '" onchange="validate_registration_id(' + ivalue + ');checking_modified(id,' + "'" + registration_id + "'" + ');" value="' + registration_id + '"></input>' +
                '<span class="help-block" id="help_registration_id' + ivalue + '"></span>' +
                '</div>' +
                '</div>' +
                '<div class="col-md-3 col-xs-12 col-sm-6">' +
                '<div class="control">' +
                '<label><b>Year’s&nbsp;associated&nbsp;with&nbsp;the&nbsp;organization&nbsp;?</b></label>' +
                '<input type="text" name="year_of_association' + ivalue + '" onchange="validate_year_of_association(' + ivalue + ');checking_modified(id,' + "'" + year + "'" + ');" class="form-control" id="year_of_association' + ivalue + '" value="' + year + '"></input>' +
                '<span class="help-block" id="help_year_of_association' + ivalue + '"></span>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '<div class="col-md-1 col-xs-1 col-sm-1" style="padding-bottom=10px;">' +
                '<p>&nbsp;</p>' +
                '<a class = "remove_field" id = "remove_field" onClick="remove_data(' + ivalue + ');">' + 
                '<img style="margin-top: 30px; width: 30px;"src="/static/new_images/delete-icon.png">' +
                '</a>' +
                '</div>' +
                '</div>');
        }
    }
    else
        organisation_div.innerHTML = "";
    if (question_4_ans == "yes") {
        $('#question_four_yes').prop('checked', true);
        $('#question_four_no').prop('checked', false);
    }
    if (question_4_ans == "no") {
        $('#question_four_yes').prop('checked', false);
        $('#question_four_no').prop('checked', true);
    }
}

//===============================================================
//This isFilledAllData function is used for check all field fill or not, if fill all data which will send the true or else false.
//================================================================
function isFilledAllData() {
    var visit = 0;
    if (document.getElementById('question_four_yes').checked == false && document.getElementById('question_four_no').checked == false) {
        visit++;
        $("#validate_question_four_yes").append('<style>input[type=radio]+#validate_question_four_yes::before{border-color: #C32F2F;}</style>');
        $("#validate_question_four_no").append('<style>input[type=radio]+#validate_question_four_no::before{border-color: #C32F2F;}</style>');
        document.getElementById('question_four_yes').focus();
        $("#4_quest").html('Please answer the question');
    }
    if (document.getElementById('question_three_yes').checked == false && document.getElementById('question_three_no').checked == false) {
        visit++;
        $("#validate_question_three_yes").append('<style>input[type=radio]+#validate_question_three_yes::before{border-color: #C32F2F;}</style>');
        $("#validate_question_three_no").append('<style>input[type=radio]+#validate_question_three_no::before{border-color: #C32F2F;}</style>');
        document.getElementById('question_three_yes').focus();
        $("#3_quest").html('Please answer the question');
    }
    if (document.getElementById('question_two_yes').checked == false && document.getElementById('question_two_no').checked == false) {
        visit++;
        $("#validate_question_two_yes").append('<style>input[type=radio]+#validate_question_two_yes::before{border-color: #C32F2F;}</style>');
        $("#validate_question_two_no").append('<style>input[type=radio]+#validate_question_two_no::before{border-color: #C32F2F;}</style>');
        document.getElementById('question_two_yes').focus();
        $("#2_quest").html('Please answer the question');
    }
    if (document.getElementById('question_one_no').checked == false && document.getElementById('question_one_yes').checked == false) {
        visit++;
        $("#validate_question_one_no").append('<style>input[type=radio]+#validate_question_one_no::before{border-color: #C32F2F;}</style>');
        $("#validate_question_one_yes").append('<style>input[type=radio]+#validate_question_one_yes::before{border-color: #C32F2F;}</style>');
        document.getElementById('question_one_yes').focus();
        $("#1_quest").html('Please answer the question');
        $('html, body').animate({
            scrollTop: $("#question_one_no").offset().top - 150
        }, 0);
    }
    if (visit == 0) {
        return true;
    } else {
        return false;
    }
}


function onchange_savequestions(id){
    if($('#'+id).val() != ''){
        $('#'+id).removeClass('not_valid');
        $("#help-"+id).html('');
    }
        
    var questions, question1_opiton, question2_opiton, question3_opiton;
    var number_of_institutions, question4_opiton, experience;
    var num_clients, average_value, office_address, count_institute, num_advisors;
    var i=$("#tags").find("span").length;
    // on change first question removing red color.
    if($('#question_one_yes').prop('checked') ==  true){
        document.getElementById('question_one_yes').style.boxShadow='';
        document.getElementById('question_one_no').style.boxShadow='';
        $("#1_quest").html('');
        if($('#y-o-b').val() == '' || $('#total_client_served').val() == '' || $('#advisor_is_connected_with').val() == '' || $('#y-o-b').val() > 100){
            return false;
        }
    }
    if($('#question_one_no').prop('checked') == true){
        document.getElementById('question_one_yes').style.boxShadow='';
        document.getElementById('question_one_no').style.boxShadow='';
        $("#1_quest").html('');
    }
    // end of first question
    // on change of second question removing red color.
    if($('#question_two_yes').prop('checked') == true){
        document.getElementById('question_two_yes').style.boxShadow='';
        document.getElementById('question_two_no').style.boxShadow='';
        $("#2_quest").html('');
        if($('#infra_address').val() == ''){
            return false;
        }
    }
    if($('#question_two_no').prop('checked') == true){
        document.getElementById('question_two_yes').style.boxShadow='';
        document.getElementById('question_two_no').style.boxShadow='';
        $("#2_quest").html('');
    }
    // end of second question
    // on change of third question removing red color
    if($('#question_three_yes').prop('checked') == true){
        document.getElementById('question_three_yes').style.boxShadow='';
        document.getElementById('question_three_no').style.boxShadow='';
        $("#3_quest").html('');
        missed_field_add=0;
            for(var j=0; j<allids.length; j++) {
                var i=allids[j];
                var re = /^[1-9][0-9]?$|^99$/;
                if($('#year_of_association'+i).val() == ""){
                    $("#year_of_association"+i).addClass("not_valid");
                    $("#help_year_of_association"+i).html('Please Enter Year of  Organization');
                    document.getElementById('year_of_association'+i).focus();
                    missed_field_add = 1;
                }else{
                    var validexperience = document.getElementById('year_of_association'+i);
                    if(!validexperience.value.match(re) || validexperience == null ) {
                        document.getElementById('year_of_association'+i).style.border='1px solid #C32F2F';
                        document.getElementById('help_year_of_association'+i).innerHTML='Enter Valid Year of  Organization';
                        $("#year_of_association"+i).focus();
                        missed_field_add = 1;
                    }else{
                        $("#year_of_association"+i).removeClass('not_valid');
                        document.getElementById('help_year_of_association'+i).innerHTML='';
                    }
                }

                if($('#registration_id'+i).val() == ""){
                    $("#help_registration_id"+i).html('Please Enter Official Email/Registration id');
                    $("#registration_id"+i).addClass("not_valid");
                    document.getElementById('registration_id'+i).focus();
                    missed_field_add = 1;
                }else{
                    $("#help_registration_id"+i).html('');
                    $("#registration_id"+i).removeClass('not_valid');
                }

                if($('#official_email_id'+i).val() == ""){
                    $("#help_official_email_id"+i).html('Please Enter Company URL');
                    $("#official_email_id"+i).addClass("not_valid");
                    document.getElementById('official_email_id'+i).focus();
                    missed_field_add = 1;
                }else{
                    var email = $('#official_email_id'+i).val()
                    var status =document.getElementById('help_official_email_id'+i).innerText;
                    var re = new RegExp(/^(http[s]?:\/\/){0,1}(www\.){0,1}[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,5}[\.]{0,1}/);
                    if(!re.test(email)) {
                        $("#help_official_email_id"+i).html('Please Enter valid Company URL');
                        $("#official_email_id"+i).addClass("not_valid");
                        document.getElementById('official_email_id'+i).focus();
                        missed_field_add = 1;
                    }else if(status=='Please Enter valid Company URL'){
                        $("#official_email_id"+i).addClass("not_valid");
                        document.getElementById('official_email_id'+i).focus();
                        missed_field_add = 1;
                    }else{
                        $("#help_official_email_id"+i).html('');
                        $("#official_email_id"+i).removeClass('not_valid');
                    }
                }
                if($('#institution_name'+i).val() == ""){
                    $("#help_institution_name"+i).html('Please Enter Organization Name');
                    $("#institution_name"+i).addClass("not_valid");
                    document.getElementById('institution_name'+i).focus();
                    missed_field_add = 1;
                }else{
                    var alpha = /^[a-zA-Z()\s]+$/.test($('#institution_name'+i).val());
                    if(alpha){
                        $("#help_institution_name"+i).html('');
                        $("#help_institution_name"+i).removeClass('not_valid');
                    }else {
                        $("#help_institution_name"+i).html('Please Enter only Characters');
                        $("#institution_name"+i).addClass("not_valid");
                        document.getElementById('institution_name'+i).focus();
                        missed_field_add = 1;
                    }
                }
            }

        if(missed_field_add==1){
            return false
        }
    }
    if($('#question_three_no').prop('checked') == true){
        $("#3_quest").html('');
        document.getElementById('question_three_yes').style.boxShadow='';
        document.getElementById('question_three_no').style.boxShadow='';
    }
    // end of third question
    // on change fourth question removing red color
    if($('#question_four_yes').prop('checked') == true || $('#question_four_no').prop('checked') == true){
        document.getElementById('question_four_yes').style.boxShadow='';
        document.getElementById('question_four_no').style.boxShadow='';
        $("#4_quest").html('');
    }
    // end of eight question
    //===============
    //Question 1 DATA
    //===============
    if (document.getElementById('question_one_yes').checked){
        question1_opiton = "yes";
        if(document.getElementById('y-o-b').value=='')
            return false;
        if(document.getElementById('t-n-o-c').value=='')
            return false;
        if(document.getElementById('t-a-t-v').value=='select')
            return false;
        experience = $("#y-o-b").val();
        num_clients = $("#total_client_served").val();
        average_value = $("#t-a-t-v").val();
        num_advisors = $("#advisor_is_connected_with").val();

    }
    else if (document.getElementById('question_one_no').checked){
        question1_opiton = "no";
        experience = "";
        num_clients = "";
        average_value = "";
        num_advisors = "";
    }
    else{
        experience = "";
        num_clients = "";
        average_value = "";
        num_advisors = "";
    }
    //===============
    //Question 2 DATA
    //===============
    if (document.getElementById('question_two_yes').checked){
        question2_opiton="yes";
        if(document.getElementById('infra_address').value==''){
            return false;
        }
        office_address = $("#infra_address").val();
        office_address = office_address.replace(/\n/g, "$");
        office_address = office_address.replace(/ /g, "!");

    }
    else if (document.getElementById('question_two_no').checked){
        question2_opiton="no";
        office_address = "";
    }
    else{
        office_address = "";
    }
    //===============
    //Question 3 DATA
    //===============
    if (document.getElementById('question_three_yes').checked){
        question3_opiton="yes";
        number_of_institutions="";
        // var num = num;
        count_institute = 0;
        if (num!="") {
            count_institute = allids.length;
            // var on_val = on_val;
            q1=on_val.replace(/u&#39;/gi,"\"");
            number_of_institutions=q1.replace(/&#39;/gi,"\"");
        }else{
            number_of_institutions='['+number_of_institutions+']';
        }
    }
    else if (document.getElementById('question_three_no').checked){
        question3_opiton="no";
        count_institute = "";
        number_of_institutions ="{}";
    }
    else{
        count_institute = "";
        number_of_institutions ="{}";
    }
    //===============
    //Question 4 DATA
    //===============
    if (document.getElementById('question_four_yes').checked){
        question4_opiton="yes";
    }
    else if (document.getElementById('question_four_no').checked){
        question4_opiton="no";
    }
    questions = '[{"Question":"1. '+question1+'", "Answer":"'+question1_opiton+'","Remark":[{"Question":"Experience","Answer":"'+experience+'"},{"Question":"Total Number of clients so far","Answer":"'+num_clients+'"},{"Question":"Average transaction value","Answer":"'+average_value+'"},{"Question":"Total Advisors connected","Answer":"'+num_advisors+'"}]},{"Question": "2. '+question2+'", "Answer":"'+question2_opiton+'","Remark":"'+office_address+'"},{"Question": "3. '+question3+'", "Answer":"'+question3_opiton+'","Remark":[{"Question":"Number of Institutions","Answer":"'+count_institute+'","Remark":'+number_of_institutions+'}]},{"Question": "4. '+question4+'", "Answer":"'+question4_opiton+'"}]';
    $.ajax({
        url : '/signup/onchange_save_questions/',
        method : 'POST',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token );
        },
        data : {
            username : user_name,
            name     : 'questions',
            questions : questions,
            total_client_served : $("#total_client_served").val(),
            total_advisors_connected : $("#advisor_is_connected_with").val()
        },
        success:function(response){
        },
        error:function(response){
        }
    });
}


//------------------------------------------------
// on change function of redio button questions
//------------------------------------------------
function clickResponse(check, str, redio1, redio2, hide_id) {
    $("#validate_" + redio1).append('<style>input[type=radio]+#validate_' + redio1 + '::before{border-color: #adb8c0;}</style>');
    $("#validate_" + redio2).append('<style>input[type=radio]+#validate_' + redio2 + '::before{border-color: #adb8c0;}</style>');
    if (check == 0) {
        document.getElementById(redio1).checked = false;
        document.getElementById(redio2).checked = true;
        if (str == 'question1_div_area') {
            document.getElementById('y-o-b').value = '';
            document.getElementById('t-n-o-c').value = 0;
            document.getElementById('t-a-t-v').value = 'select';
        }
        if (str == 'question2_div_area') {
            document.getElementById('infra_address').value = '';
            onchange_savequestions(redio2);
            $('#check_confirm_for_change').modal('hide');
        }
        if (str == 'question3_div_area') {
            count_institute = "";
            number_of_institutions = "{}";
            allids = [];
            document.getElementById('organisation_div').innerHTML = '';
            $("#3_quest").html('');
        }
        if (str != "") {
            document.getElementById(str).style.display = 'none';
        }
    }
    else {
        document.getElementById(redio2).checked = false;
        document.getElementById(redio1).checked = true;
        if (str != "")
            document.getElementById(str).style.display = 'flex';
        if (str != 'question3_div_area') {
            if (hide_id != "")
                document.getElementById(hide_id).focus();
        }
    }
}

function getDomain(url) {
    var domain = "",
        page = "";
    //remove "http://"
    if (url.indexOf("http://") == 0) {
        url = url.substr(7);
    }
    if (url.indexOf("https://") == 0) {
        url = url.substr(7);
    }
    //remove "www."
    if (url.indexOf("www.") == 0) {
        url = url.substr(4);
    }
    domain = url
    return domain;
}

function CheckIsValidDomain(i) {
    var token = csrf_token;
    var domain = document.getElementById('official_email_id' + i).value;
    var re = new RegExp(/^(http[s]?:\/\/){0,1}(www\.){0,1}[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,5}[\.]{0,1}/);
    if (!domain.match(re)) {
        $("#official_email_id" + i).addClass("not_valid");
        document.getElementById('help_official_email_id' + i).innerHTML = 'Please Enter valid Company URL';
        $("#official_email_id" + i).focus();
    } else {
        $.ajax({
            url: '/signup/check_valid_domain/',
            method: 'POST',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", token);
            },
            data: {
                'comapny_url': domain
            },
            success: function (response) {
                if (response == 'success') {
                    $("#official_email_id" + i).removeClass('not_valid');
                    document.getElementById('help_official_email_id' + i).innerHTML = '';
                    modify_web_url('official_email_id' + i);
                } else {
                    $("#official_email_id" + i).addClass("not_valid");
                    document.getElementById('help_official_email_id' + i).innerHTML = 'Please Enter valid Company URL';
                    $("#official_email_id" + i).focus();
                }
            },
            error: function (response) {
            },
        });
    }
}

function validate_registration_id(i) {
    var email_id = $('#registration_id' + i).val();
    if ($('#registration_id' + i).val() == "") {
        $("#help_registration_id" + i).html('Please Enter Official Email/Registration id');
        $("#registration_id" + i).addClass("not_valid");
        document.getElementById('registration_id' + i).focus();
    }
    else {
        email_ajax(i);
    }
}
function email_ajax(i) {
    var token = csrf_token;
    var email_id = $('#registration_id' + i).val();
    $.ajax({
        type: "POST",
        url: "/signup/check_email_for_business_information/",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        data: { 'username': email_id },
        success: function (response) {
            if (response == 'true') {
                document.getElementById('help_registration_id' + i).innerHTML = '';
                $("#registration_id" + i).removeClass('not_valid');
            }
            else {
                $('#registration_id' + i).val('');
                document.getElementById('help_registration_id' + i).innerHTML = "Email Already Exist";
            }
        }
    });
}

function validate_organisation_email(i) {
    if ($('#official_email_id' + i).val() == "") {
        $("#help_official_email_id" + i).html('Please Enter Comapny URL');
        $("#official_email_id" + i).addClass("not_valid");
        document.getElementById('official_email_id' + i).focus();
    } else {
        var email = $('#official_email_id' + i).val()
        var re = /\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/;
        if (!re.test(email)) {
            $("#help_official_email_id" + i).html('Please Enter valid Email Id');
            $("#official_email_id" + i).addClass("not_valid");
            document.getElementById('official_email_id' + i).focus();
        } else {
            check_field('official_email_id' + i);
        }
    }
}
function validate_organisation_name(i) {
    if ($('#institution_name' + i).val() == "") {
        $("#help_institution_name" + i).html('Please Enter Organisation Name');
        $("#institution_name" + i).addClass("not_valid");
        document.getElementById('institution_name' + i).focus();
    } else {
        var alpha = /^[a-zA-Z()\s]+$/.test($('#institution_name' + i).val());
        if (alpha) {
            check_field('institution_name' + i);
        } else {
            $("#help_institution_name" + i).html('Please Enter only Characters');
            $("#institution_name" + i).addClass("not_valid");
            document.getElementById('institution_name' + i).focus();
        }
    }
}

//==============================================================
//This function is used to creating the financial institutions json
//============================================================
function creating_institutions_json() {
    var institutions = "";
    for (var j = 0; j < allids.length; j++) {
        var h = allids[j];
        var institution_name = document.getElementById("institution_name" + h).value;
        var official_email_id = document.getElementById("official_email_id" + h).value;
        var registration_id = document.getElementById("registration_id" + h).value;
        var year_of_association = document.getElementById("year_of_association" + h).value;
        if (h == allids[0])
            institutions = institutions + '{"Question":"institution_name","Answer":"' + institution_name + '"},{"Question":"official_email_id","Answer":"' + official_email_id + '"},{"Question":"registration_id","Answer":"' + registration_id + '"},{"Question":"year_of_association","Answer":"' + year_of_association + '"}';
        else
            institutions = institutions + ',{"Question":"institution_name","Answer":"' + institution_name + '"},{"Question":"official_email_id","Answer":"' + official_email_id + '"},{"Question":"registration_id","Answer":"' + registration_id + '"},{"Question":"year_of_association","Answer":"' + year_of_association + '"}';
    }
    institutions = '[' + institutions + ']';
    return institutions;
}

function advisorQuestionAnwserSave() {
    var token = csrf_token;
    var visit = isFilledAllData();
    var question1_opiton, question2_opiton, question3_opiton;
    var number_of_institutions, question4_opiton, experience;
    var num_clients, average_value, office_address, count_institute, num_advisors;
    // =========================
    // validation for question one
    // after clicking yes checking the fields are empty or not
    // =========================
    if (document.getElementById('question_three_yes').checked) {
        var institution_name_missed = 0;
        var official_email_id_missed = 0;
        var registration_id_missed = 0;
        var year_of_association_missed = 0;
        if (allids.length > 0) {
            for (j = allids.length; j >= 1; j--) {
                var i = allids[j - 1];
                if ($('#year_of_association' + i).val() == "") {
                    year_of_association_missed = year_of_association_missed + 1;
                    $("#year_of_association" + i).addClass("not_valid");
                    $("#help_year_of_association" + i).html('Please Enter Years of Association');
                    document.getElementById('year_of_association' + i).focus();
                } else {
                    var re = /^[1-9][0-9]?$|^99$/;
                    var validexperience = document.getElementById('year_of_association' + i);
                    if (!validexperience.value.match(re)) {
                        year_of_association_missed = year_of_association_missed + 1;
                        document.getElementById('year_of_association' + i).style.border = '1px solid #C32F2F';
                        document.getElementById('help_year_of_association' + i).innerHTML = 'Enter Valid Years of Association';
                        $("#year_of_association" + i).focus();
                    } else {
                        $("#year_of_association" + i).removeClass('not_valid');
                        document.getElementById('help_year_of_association' + i).innerHTML = '';
                    }
                }
                if ($('#registration_id' + i).val() == "") {
                    registration_id_missed = registration_id_missed + 1;
                    $("#help_registration_id" + i).html('Please Enter Official Email/Registration id');
                    $("#registration_id" + i).addClass("not_valid");
                    document.getElementById('registration_id' + i).focus();
                } else {
                    $("#help_registration_id" + i).html('');
                    $("#registration_id" + i).removeClass('not_valid');
                }

                if ($('#official_email_id' + i).val() == "") {
                    official_email_id_missed = official_email_id_missed + 1;
                    $("#help_official_email_id" + i).html('Please Enter Company URL');
                    $("#official_email_id" + i).addClass("not_valid");
                    document.getElementById('official_email_id' + i).focus();
                } else {
                    var email = $('#official_email_id' + i).val()
                    var status = document.getElementById('help_official_email_id' + i).innerText;
                    var re = new RegExp(/^(http[s]?:\/\/){0,1}(www\.){0,1}[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,5}[\.]{0,1}/);
                    if (!re.test(email)) {
                        official_email_id_missed = official_email_id_missed + 1;
                        $("#help_official_email_id" + i).html('Please Enter valid Company URL');
                        $("#official_email_id" + i).addClass("not_valid");
                        document.getElementById('official_email_id' + i).focus();
                    } else if (status == 'Please Enter valid Company URL') {
                        $("#official_email_id" + i).addClass("not_valid");
                        document.getElementById('official_email_id' + i).focus();
                        official_email_id_missed = official_email_id_missed + 1;
                    } else {
                        $("#help_official_email_id" + i).html('');
                        $("#official_email_id" + i).removeClass('not_valid');
                        for (var k = 0; k < allids.length; k++) {
                            emailj = $('#official_email_id' + allids[j - 1]).val();
                            emailk = $('#official_email_id' + allids[k]).val();
                            var domainnamej = getDomain(emailj);
                            var domainnamek = getDomain(emailk);
                            if (allids[j - 1] != allids[k] && domainnamej == domainnamek) {
                                $("#official_email_id" + allids[k]).addClass("not_valid");
                                document.getElementById('help_official_email_id' + allids[k]).innerHTML = "Duplicate email domain entry";
                                $("#official_email_id" + allids[j - 1]).addClass("not_valid");
                                document.getElementById('help_official_email_id' + allids[j - 1]).innerHTML = "Duplicate email domain entry";
                                official_email_id_missed = official_email_id_missed + 1;
                            }
                        }
                    }
                }

                if ($('#institution_name' + i).val() == "") {
                    institution_name_missed = institution_name_missed + 1;
                    $("#help_institution_name" + i).html('Please Enter Organisation Name');
                    $("#institution_name" + i).addClass("not_valid");
                    document.getElementById('institution_name' + i).focus();
                } else {
                    if ($('#institution_name' + i).val() != '') {
                        var alpha = /^[a-zA-Z()\s]+$/.test($('#institution_name' + i).val());
                        if (alpha) {
                            $("#help_institution_name" + i).html('');
                            $("#help_institution_name" + i).removeClass('not_valid');
                        }
                        else {
                            institution_name_missed = institution_name_missed + 1;
                            $("#help_institution_name" + i).html('Please Enter only Characters');
                            $("#institution_name" + i).addClass("not_valid");
                            document.getElementById('institution_name' + i).focus();
                        }
                    }
                }
            }
            if (institution_name_missed > 0) {
                return false;
            }
            if (year_of_association_missed > 0) {
                return false;
            }
            if (official_email_id_missed > 0) {
                return false;
            }
            if (registration_id_missed > 0) {
                return false;
            }
        } else {
            document.getElementById('help-text-add_financial_organisation_main').innerHTML = 'Please Enter Minimum One Financial Organization';
            $('html, body').animate({
                scrollTop: $("#question3_div_area").offset().top - 150
            }, 0);
            return false;
        }
    }
    if (document.getElementById('question_two_yes').checked) {
        if ($("#infra_address").val() == '') {
            $("#infra_address").addClass("not_valid");
            $('#help-infra_address').html('Please Enter Office Address');
            document.getElementById('infra_address').focus();
        }
    }
    if (document.getElementById('question_one_yes').checked) {
        if ($('#t-a-t-v').val() == "select" || $('#t-a-t-v').val() == "") {
            $("#t-a-t-v").addClass("not_valid");
            $("#help-t-a-t-v").html('Please enter Average transaction value');
            document.getElementById('t-a-t-v').focus();
        }
        if ($('#y-o-b').val() == "") {
            document.getElementById('y-o-b').focus();
            $("#y-o-b").addClass("not_valid");
            $('#help-y-o-b').html('Please Enter Years of business');
        }
        else if ($('#y-o-b').val() >= 100 || $('#y-o-b').val() < 1) {
            $("#y-o-b").addClass("not_valid");
            $('#help-y-o-b').html('Year of business should be 1-99');
            $("#y-o-b").val('');
            document.getElementById('y-o-b').focus();
        }
    }
    if (visit == false) {
        return false;
    }
    //===============
    //Question 1 DATA
    //===============
    if (document.getElementById('question_one_yes').checked) {
        question1_opiton = "yes";
        if (document.getElementById('y-o-b').value == '')
            return false;
        if (document.getElementById('t-n-o-c').value == '')
            return false;
        if (document.getElementById('t-a-t-v').value == 'select')
            return false;
        experience = $("#y-o-b").val();
        num_clients = $("#total_client_served").val();
        average_value = $("#t-a-t-v").val();
        num_advisors = $("#advisor_is_connected_with").val();
    }
    else if (document.getElementById('question_one_no').checked) {
        question1_opiton = "no";
        experience = "";
        num_clients = "";
        average_value = "";
        num_advisors = "";
    }
    else {
        experience = "";
        num_clients = "";
        average_value = "";
        num_advisors = "";
    }
    //===============
    //Question 2 DATA
    //===============
    if (document.getElementById('question_two_yes').checked) {
        question2_opiton = "yes";
        if (document.getElementById('infra_address').value == '') {
            return false;
        }
        office_address = $("#infra_address").val();
        office_address = office_address.replace(/\n/g, "$");
        office_address = office_address.replace(/ /g, "!");
    }
    else if (document.getElementById('question_two_no').checked) {
        question2_opiton = "no";
        office_address = "";
    }
    else {
        office_address = "";
    }
    //===============
    //Question 3 DATA
    //===============
    if (document.getElementById('question_three_yes').checked) {
        question3_opiton = "yes";
        count_institute = allids.length;
        number_of_institutions = creating_institutions_json();
    }
    else if (document.getElementById('question_three_no').checked) {
        question3_opiton = "no";
        count_institute = "";
        number_of_institutions = "{}";
    }
    else {
        count_institute = "";
        number_of_institutions = "{}";
    }
    //===============
    //Question 4 DATA
    //===============
    if (document.getElementById('question_four_yes').checked)
        question4_opiton = "yes";
    else if (document.getElementById('question_four_no').checked)
        question4_opiton = "no";
    var missed_field = 0;
    if (document.getElementById('question_one_yes').checked) {
        var re = /^[0-9\b]+$/;
        var advisor_is_connected_with = $("#advisor_is_connected_with").val();
        if (advisor_is_connected_with == '' || advisor_is_connected_with == null) {
            document.getElementById('advisor_is_connected_with').style.border = '1px solid #C32F2F';
            document.getElementById('help_text_advisor_is_connected_with').innerHTML = 'Please Enter Total Advisors connected';
            missed_field = 1;
            $("#advisor_is_connected_with").focus();
        } else if ($("#advisor_is_connected_with").val().match(re)) {
            document.getElementById('advisor_is_connected_with').style.border = '';
            document.getElementById('help_text_advisor_is_connected_with').innerHTML = '';
        } else {
            var a = document.getElementById('advisor_is_connected_with').value = "";
            document.getElementById('advisor_is_connected_with').style.border = '1px solid #C32F2F';
            document.getElementById('help_text_advisor_is_connected_with').innerHTML = 'Enter Valid Input';
            missed_field = 1;
            $("#advisor_is_connected_with").focus();
        }
        var total_client_served = $("#total_client_served").val();
        if (total_client_served == '' || total_client_served == null) {
            document.getElementById('total_client_served').style.border = '1px solid #C32F2F';
            document.getElementById('help_text_total_client_served').innerHTML = 'Please Enter Total Client Served';
            missed_field = 1;
            $("#total_client_served").focus();
        } else if (total_client_served.match(re)) {
            document.getElementById('total_client_served').style.border = '';
            document.getElementById('help_text_total_client_served').innerHTML = '';
        } else {
            var a = document.getElementById('total_client_served').value = "";
            document.getElementById('total_client_served').style.border = '1px solid #C32F2F';
            document.getElementById('help_text_total_client_served').innerHTML = 'Enter Valid Input';
            missed_field = 1;
            $("#total_client_served").focus();
        }
    }
    if (missed_field == 0) {
        $('#submit1').prop('disabled', true);
        $.ajax({
            method: "POST",
            url: "/signup/user_profile_answer/",
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", token);
            },
            data: {
                questions: '[{"Question":"1. '+question1+'", "Answer":"' + question1_opiton + '","Remark":[{"Question":"Experience","Answer":"' + experience + '"},{"Question":"Total Number of clients so far","Answer":"' + num_clients + '"},{"Question":"Average transaction value","Answer":"' + average_value + '"},{"Question":"Total Advisors connected","Answer":"' + num_advisors + '"}]},{"Question":"2. '+question2+'", "Answer":"' + question2_opiton + '","Remark":"' + office_address + '"},{"Question":"3. '+question3+'", "Answer":"' + question3_opiton + '","Remark":[{"Question":"Number of Institutions","Answer":"' + count_institute + '","Remark":' + number_of_institutions + '}]},{"Question":"4. '+question4+'", "Answer":"' + question4_opiton + '"}]',
                is_submitted_questions: visit,
            },
            success: function (response) {
                window.location.href = '/signup/education/';
                $('#submit1').prop('disabled', false);
            },
            error: function(response){
                alert('Unable to submit the form. \n Please try again after some time');
                $('#submit1').prop('disabled', false);
            }
        });
    }
}


//code for 3.Are you associated with any Financial Organisation
var wrapper = $("#organisation_div");
var add_button = $("#add_financial_organisation");
function add_additional_organisation() {
    document.getElementById('help-text-add_financial_organisation_main').innerHTML = '';
    missed_field_add = 0;
    if (allids.length > 0) {
        for (var j = 0; j < allids.length; j++) {
            var i = allids[j];
            var re = /^[1-9][0-9]?$|^99$/;
            if ($('#year_of_association' + i).val() == "") {
                $("#year_of_association" + i).addClass("not_valid");
                $("#help_year_of_association" + i).html('Please Enter Years of Association');
                document.getElementById('year_of_association' + i).focus();
                missed_field_add = 1;
            } else {
                var validexperience = document.getElementById('year_of_association' + i);
                if (!validexperience.value.match(re) || validexperience == null) {
                    document.getElementById('year_of_association' + i).style.border = '1px solid #C32F2F';
                    document.getElementById('help_year_of_association' + i).innerHTML = 'Enter Valid Years of Association';
                    $("#year_of_association" + i).focus();
                    missed_field_add = 1;
                } else {
                    $("#year_of_association" + i).removeClass('not_valid');
                    document.getElementById('help_year_of_association' + i).innerHTML = '';
                }
            }

            if ($('#registration_id' + i).val() == "") {
                $("#help_registration_id" + i).html('Please Enter Official Email/Registration id');
                $("#registration_id" + i).addClass("not_valid");
                document.getElementById('registration_id' + i).focus();
                missed_field_add = 1;
            } else {
                $("#help_registration_id" + i).html('');
                $("#registration_id" + i).removeClass('not_valid');
            }

            if ($('#official_email_id' + i).val() == "") {
                $("#help_official_email_id" + i).html('Please Enter Company URL');
                $("#official_email_id" + i).addClass("not_valid");
                document.getElementById('official_email_id' + i).focus();
                missed_field_add = 1;
            } else {
                var email = $('#official_email_id' + i).val()
                var status = document.getElementById('help_official_email_id' + i).innerText;
                var re = new RegExp(/^(http[s]?:\/\/){0,1}(www\.){0,1}[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,5}[\.]{0,1}/);
                if (!re.test(email)) {
                    $("#help_official_email_id" + i).html('Please Enter valid Company URL');
                    $("#official_email_id" + i).addClass("not_valid");
                    document.getElementById('official_email_id' + i).focus();
                    missed_field_add = 1;
                } else if (status == 'Please Enter valid Company URL') {
                    $("#official_email_id" + i).addClass("not_valid");
                    document.getElementById('official_email_id' + i).focus();
                    missed_field_add = 1;
                } else {
                    $("#help_official_email_id" + i).html('');
                    $("#official_email_id" + i).removeClass('not_valid');
                    for (var k = 0; k < allids.length; k++) {
                        emailj = $('#official_email_id' + allids[j]).val();
                        emailk = $('#official_email_id' + allids[k]).val();
                        var domainnamej = getDomain(emailj);
                        var domainnamek = getDomain(emailk);
                        if (allids[j] != allids[k] && domainnamej == domainnamek) {
                            document.getElementById('official_email_id' + allids[k]).style.border = '1px solid #C32F2F';
                            document.getElementById('help_official_email_id' + allids[k]).innerHTML = "Duplicate email domain entry";
                            document.getElementById('official_email_id' + allids[j]).style.border = '1px solid #C32F2F';
                            document.getElementById('help_official_email_id' + allids[j]).innerHTML = "Duplicate email domain entry";
                            missed_field_add++;
                        }
                    }
                }
            }
            if ($('#institution_name' + i).val() == "") {
                $("#help_institution_name" + i).html('Please Enter Organization Name');
                $("#institution_name" + i).addClass("not_valid");
                document.getElementById('institution_name' + i).focus();
                missed_field_add = 1;
            } else {
                var alpha = /^[a-zA-Z()\s]+$/.test($('#institution_name' + i).val());
                if (alpha) {
                    $("#help_institution_name" + i).html('');
                    $("#help_institution_name" + i).removeClass('not_valid');
                } else {
                    $("#help_institution_name" + i).html('Please Enter only Characters');
                    $("#institution_name" + i).addClass("not_valid");
                    document.getElementById('institution_name' + i).focus();
                    missed_field_add = 1;
                }
            }
        }
    }
    if (missed_field_add == 0) {
        if (allids.length < max_fields) { //max input box allowed
            x++; //text box increment
            allids.push(x);
            $(wrapper).append('\
            <div class="row n-margin-0" id="financial_organisation'+ x + '">' +
                '<div class="col-md-11 col-xs-12 col-sm-11">' +
                '<div class="row">' +
                '<div class="col-md-3 col-xs-12 col-sm-6">' +
                '<div class="control">' +
                '<label><b>Organization Name</b></label>' +
                '<input type="text" class="form-control" name="institution_name' + x + '" id="institution_name' + x + '" onchange="validate_organisation_name(' + x + ');"></input>' +
                '<span class="help-block" id="help_institution_name' + x + '"></span>' +
                '</div>' +
                '</div>' +
                '<div class="col-md-3 col-xs-12 col-sm-6">' +
                '<div class="control">' +
                '<label><b>Company URL</b></label>' +
                '<input type="text" class="form-control lower_case" name="official_email_id' + x + '" id="official_email_id' + x + '" onchange="CheckIsValidDomain(' + x + ');"></input>' +
                '<span class="help-block" id="help_official_email_id' + x + '"></span>' +
                '</div>' +
                '</div>' +
                '<div class="col-md-3 col-xs-12 col-sm-6">' +
                '<div class="control">' +
                '<label><b>Official Email/Registration id</b></label>' +
                '<input type="text" class="form-control" name="registration_id' + x + '" id="registration_id' + x + '" onchange="validate_registration_id(' + x + ');"></input>' +
                '<span class="help-block" id="help_registration_id' + x + '"></span>' +
                '</div>' +
                '</div>' +
                '<div class="col-md-3 col-xs-12 col-sm-6">' +
                '<div class="control">' +
                '<label><b>Year’s&nbsp;associated&nbsp;with&nbsp;the&nbsp;organization&nbsp;?</b></label>' +
                '<input type="text" name="year_of_association' + x + '" onchange="validate_year_of_association(' + x + ');" class="form-control" id="year_of_association' + x + '"></input>' +
                '<span class="help-block" id="help_year_of_association' + x + '"></span>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '<div class="col-md-1 col-xs-12 col-sm-1" style="padding-bottom=10px;">' +
                '<span>&nbsp;</span>' + 
                '<a class = "remove_field" id = "remove_field" onClick="remove_data(' + x + ');">' +
                '<img style="margin-top: 30px; width: 30px;"src="/static/new_images/delete-icon.png">' +
                '</a>' +
                '</div>' +
                '</div>');
        }
    }
}
function remove_data(id) {
    $('#financial_organisation' + id).remove();
    var i = allids.indexOf(id);
    if (i != -1) {
        allids.splice(i, 1);
    }
}

function validate_year_of_association(i) {
    var re = /^[1-9][0-9]?$|^99$/;
    if ($('#year_of_association' + i).val() == "") {
        $("#year_of_association" + i).addClass("not_valid");
        $("#help_year_of_association" + i).html('Please Enter Years of Association');
        document.getElementById('year_of_association' + i).focus();
    } else {
        var validexperience = document.getElementById('year_of_association' + i);
        if (!validexperience.value.match(re) || validexperience == null) {
            $("#year_of_association" + i).addClass("not_valid");
            document.getElementById('help_year_of_association' + i).innerHTML = 'Enter Valid Years of Association';
            $("#year_of_association" + i).focus();
        } else {
            $("#year_of_association" + i).removeClass('not_valid');
            document.getElementById('help_year_of_association' + i).innerHTML = '';
        }
    }
}

function getAddress(check, str, redio1, redio2, hide_id, address1) {
    $("#validate_" + redio1).append('<style>input[type=radio]+#validate_' + redio1 + '::before{border-color: #adb8c0;}</style>');
    $("#validate_" + redio2).append('<style>input[type=radio]+#validate_' + redio2 + '::before{border-color: #adb8c0;}</style>');
    if (check == 0) {
        document.getElementById(redio1).checked = false;
        document.getElementById(redio2).checked = true;
        if (str == 'question1_div_area') {
            document.getElementById('y-o-b').value = '';
            document.getElementById('t-n-o-c').value = 0;
            document.getElementById('t-a-t-v').value = '--Select--';
        }
        if (str == 'question2_div_area') {
            document.getElementById('infra_address').value = '';
        }
        if (str == 'question3_div_area') {
            document.getElementById('instutite_div').innerHTML = '';
        }
        if (str != "")
            document.getElementById(str).style.display = 'none';
    }
    else {
        if (document.getElementById('infra_address').value == '') {
            if ('{{user_profile.primary_communication}}' == 'office') {
                document.getElementById('infra_address').value = address1;
            }
        }
        document.getElementById(redio2).checked = false;
        document.getElementById(redio1).checked = true;
        if (str != "")
            document.getElementById(str).style.display = 'block';
        if (hide_id != "")
            document.getElementById(hide_id).focus();
    }
    get_full_address();
}

function get_full_address(){
    var office_full_address = '';
    if ($.trim($("#company_address1").val())){
        office_full_address += $.trim($("#company_address1").val());
    }
    if($.trim($("#company_address2").val())){
        if (office_full_address){
            office_full_address += " "+$.trim($("#company_address2").val());
        }else{
            office_full_address += $.trim($("#company_address2").val())
        }
    }
    if($.trim($('#company_city').val())){
        if (office_full_address){
            office_full_address += " "+"\n"+$.trim($('#company_city').val());
        }else{
            office_full_address += $.trim($('#company_city').val());
        }
    }
    if($.trim($('#company_state').val())){
        if (office_full_address){
            office_full_address += ", "+$.trim($('#company_state').val());
        }else{
            office_full_address += $.trim($('#company_state').val());
        }
    }
    if($.trim($('#company_pincode').val())){
        if (office_full_address){
            office_full_address += " "+$.trim($('#company_pincode').val());
        }else{
            office_full_address += $.trim($('#company_pincode').val());
        }
    }
    if($.trim($('#company_country').val())){
        if (office_full_address){
            office_full_address += " "+"\n"+$.trim($('#company_country').val());
        }else{
            office_full_address += $.trim($('#company_country').val());
        }
    }
    document.getElementById("infra_address").value = office_full_address;
}

$("#total_no_clients").keydown(function (e) {
    // Allow: backspace, delete, tab, escape, enter and .
    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
        // Allow: Ctrl+A, Command+A
        (e.keyCode == 65 && (e.ctrlKey === true || e.metaKey === true)) ||
        // Allow: home, end, left, right, down, up
        (e.keyCode >= 35 && e.keyCode <= 40)) {
        // let it happen, don't do anything
        return;
    }
    // Ensure that it is a number and stop the keypress
    if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
        e.preventDefault();
    }
});
$("#y-o-b").keydown(function (e) {
    // Allow: backspace, delete, tab, escape, enter and .
    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
        // Allow: Ctrl+A, Command+A
        (e.keyCode == 65 && (e.ctrlKey === true || e.metaKey === true)) ||
        // Allow: home, end, left, right, down, up
        (e.keyCode >= 35 && e.keyCode <= 40)) {
        // let it happen, don't do anything
        return;
    }
    // Ensure that it is a number and stop the keypress
    if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
        e.preventDefault();
    }
});
$("#t-n-o-c").keydown(function (e) {
    // Allow: backspace, delete, tab, escape, enter and .
    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
        // Allow: Ctrl+A, Command+A
        (e.keyCode == 65 && (e.ctrlKey === true || e.metaKey === true)) ||
        // Allow: home, end, left, right, down, up
        (e.keyCode >= 35 && e.keyCode <= 40)) {
        // let it happen, don't do anything
        return;
    }
    // Ensure that it is a number and stop the keypress
    if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
        e.preventDefault();
    }
});

function modify_web_url(id) {
    value = $("#" + id).val();
    if (!/^(f|ht)tps?:\/\//i.test(value)) {
        if (value.indexOf("www.") != 0) {
            $("#" + id).val('http://www.' + value);
        } else {
            $("#" + id).val('http://' + value);
        }
    } else if (!/((?:www\.)(?:[-a-z0-9]+\.)*[-a-z0-9]+.*)/i.test(value)) {
        value = value.replace(/^http(s)?\:\/\//i, "");
        $("#" + id).val('http://www.' + value);
    }
}

function validate_business_information_form(){
    var visit_status = isFilledAllData();
    var missed_field_q = false;
    if (document.getElementById('question_three_yes').checked) {
        var institution_name_missed = 0;
        var official_email_id_missed = 0;
        var registration_id_missed = 0;
        var year_of_association_missed = 0;
        if (allids.length > 0) {
            for (j = allids.length; j >= 1; j--) {
                var i = allids[j - 1];
                if ($('#year_of_association' + i).val() == "") {
                    year_of_association_missed = year_of_association_missed + 1;
                    $("#year_of_association" + i).addClass("not_valid");
                    $("#help_year_of_association" + i).html('Please Enter Years of Association');
                    document.getElementById('year_of_association' + i).focus();
                } else {
                    var re = /^[1-9][0-9]?$|^99$/;
                    var validexperience = document.getElementById('year_of_association' + i);
                    if (!validexperience.value.match(re)) {
                        year_of_association_missed = year_of_association_missed + 1;
                        document.getElementById('year_of_association' + i).style.border = '1px solid #C32F2F';
                        document.getElementById('help_year_of_association' + i).innerHTML = 'Enter Valid Years of Association';
                        $("#year_of_association" + i).focus();
                    } else {
                        $("#year_of_association" + i).removeClass('not_valid');
                        document.getElementById('help_year_of_association' + i).innerHTML = '';
                    }
                }
                if ($('#registration_id' + i).val() == "") {
                    registration_id_missed = registration_id_missed + 1;
                    $("#help_registration_id" + i).html('Please Enter Official Email/Registration id');
                    $("#registration_id" + i).addClass("not_valid");
                    document.getElementById('registration_id' + i).focus();
                } else {
                    $("#help_registration_id" + i).html('');
                    $("#registration_id" + i).removeClass('not_valid');
                }

                if ($('#official_email_id' + i).val() == "") {
                    official_email_id_missed = official_email_id_missed + 1;
                    $("#help_official_email_id" + i).html('Please Enter Company URL');
                    $("#official_email_id" + i).addClass("not_valid");
                    document.getElementById('official_email_id' + i).focus();
                } else {
                    var email = $('#official_email_id' + i).val()
                    var status = document.getElementById('help_official_email_id' + i).innerText;
                    var re = new RegExp(/^(http[s]?:\/\/){0,1}(www\.){0,1}[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,5}[\.]{0,1}/);
                    if (!re.test(email)) {
                        official_email_id_missed = official_email_id_missed + 1;
                        $("#help_official_email_id" + i).html('Please Enter valid Company URL');
                        $("#official_email_id" + i).addClass("not_valid");
                        document.getElementById('official_email_id' + i).focus();
                    } else if (status == 'Please Enter valid Company URL') {
                        $("#official_email_id" + i).addClass("not_valid");
                        document.getElementById('official_email_id' + i).focus();
                        official_email_id_missed = official_email_id_missed + 1;
                    } else {
                        $("#help_official_email_id" + i).html('');
                        $("#official_email_id" + i).removeClass('not_valid');
                        for (var k = 0; k < allids.length; k++) {
                            emailj = $('#official_email_id' + allids[j - 1]).val();
                            emailk = $('#official_email_id' + allids[k]).val();
                            var domainnamej = getDomain(emailj);
                            var domainnamek = getDomain(emailk);
                            if (allids[j - 1] != allids[k] && domainnamej == domainnamek) {
                                $("#official_email_id" + allids[k]).addClass("not_valid");
                                document.getElementById('help_official_email_id' + allids[k]).innerHTML = "Duplicate email domain entry";
                                $("#official_email_id" + allids[j - 1]).addClass("not_valid");
                                document.getElementById('help_official_email_id' + allids[j - 1]).innerHTML = "Duplicate email domain entry";
                                official_email_id_missed = official_email_id_missed + 1;
                            }
                        }
                    }
                }

                if ($('#institution_name' + i).val() == "") {
                    institution_name_missed = institution_name_missed + 1;
                    $("#help_institution_name" + i).html('Please Enter Organization Name');
                    $("#institution_name" + i).addClass("not_valid");
                    document.getElementById('institution_name' + i).focus();
                } else {
                    if ($('#institution_name' + i).val() != '') {
                        var alpha = /^[a-zA-Z()\s]+$/.test($('#institution_name' + i).val());
                        if (alpha) {
                            $("#help_institution_name" + i).html('');
                            $("#help_institution_name" + i).removeClass('not_valid');
                        } else {
                            institution_name_missed = institution_name_missed + 1;
                            $("#help_institution_name" + i).html('Please Enter only Characters');
                            $("#institution_name" + i).addClass("not_valid");
                            document.getElementById('institution_name' + i).focus();
                        }
                    }
                }
            }
            if (institution_name_missed > 0) {
                missed_field_q = true;
                // return false;
            }
            if (year_of_association_missed > 0) {
                missed_field_q = true;
                // return false;
            }
            if (official_email_id_missed > 0) {
                missed_field_q = true;
                // return false;
            }
            if (registration_id_missed > 0) {
                missed_field_q = true;
                // return false;
            }
        } else {
            document.getElementById('help-text-add_financial_organisation_main').innerHTML = 'Please Enter Minimum One Financial Organization';
            missed_field_q = true;
            $('html, body').animate({
                scrollTop: $("#question3_div_area").offset().top - 150
            }, 0);
            // return false;
        }
    }
    if (document.getElementById('question_two_yes').checked) {
        if ($("#infra_address").val() == '') {
            $("#infra_address").addClass("not_valid");
            $('#help-infra_address').html('Please Enter Office Address');
            document.getElementById('infra_address').focus();
            missed_field_q = true;
        }
    }
    if (document.getElementById('question_one_yes').checked) {
        if ($('#t-a-t-v').val() == "select" || $('#t-a-t-v').val() == "") {
            $("#t-a-t-v").addClass("not_valid");
            $("#help-t-a-t-v").html('Please enter Average transaction value');
            document.getElementById('t-a-t-v').focus();
            missed_field_q = true;
        }
        if($("#advisor_is_connected_with").val() == ""){
            $("#help_text_advisor_is_connected_with").html('Please Enter Total Advisors connected');
            missed_field_q = true;
        }
        if($("#total_client_served").val() == ""){
            $("#help_text_total_client_served").html('Please Enter Total Client Served');
            missed_field_q = true;
        }
        if ($('#y-o-b').val() == "") {
            document.getElementById('y-o-b').focus();
            $("#y-o-b").addClass("not_valid");
            $('#help-y-o-b').html('Please Enter Years of business');
            missed_field_q = true;
        } else if ($('#y-o-b').val() >= 100 || $('#y-o-b').val() < 1) {
            $("#y-o-b").addClass("not_valid");
            $('#help-y-o-b').html('Year of business should be 1-99');
            $("#y-o-b").val('');
            document.getElementById('y-o-b').focus();
            missed_field_q = true;
        }
    }
    if (missed_field_q || !visit_status) {
        return false;
    }else{
        return true;
    }
}