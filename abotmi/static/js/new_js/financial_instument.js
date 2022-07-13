var max_fields= 6;
var wrapper=$(".input_fields_wrap");
var add_button = $(".add_field");
var x=0;
var allids = [];
var wrapper=$(".input_fields_wrap");
var add_button = $(".add_field");

// Loding script on Page ready
$(document).ready(function (){
    x=document.getElementById('financial_count').value;
    for(i=1; i<=x; i++){
        allids.push(i);
    }
    filter_financial_instruments();
});

/** 
 * @use: Validatin and Adding Additional Financial instrument fields
*/
$(add_button).click(function(e){
    document.getElementById('help-text-financial_instruments_main').innerHTML='';
    missed_field_add=0;
    for(var j=0; j<allids.length; j++) {
        var i=allids[j];
        var re = /^[1-9][0-9]?$|^99$/;
        var validexperience = document.getElementById('financial_experience'+i);
        if(!validexperience.value.match(re) || validexperience == null ) {
            var a=document.getElementById('financial_experience'+i).value = "";
            document.getElementById('financial_experience'+i).style.border='1px solid #C32F2F';
            document.getElementById('help-text-financial_experience'+i).innerHTML='Enter Valid Experience';
            $("#financial_experience"+i).focus();
            missed_field_add = 1;
        }else{
            document.getElementById('financial_experience'+i).style.border='';
            document.getElementById('help-text-financial_experience'+i).innerHTML='';
        }
    }
    for(var j=0; j<allids.length; j++) {
        var i=allids[j];
        validinstruments="";
        var validinstruments = document.getElementById('financial_instruments'+i).value;
        if(validinstruments == 'Select'|| validinstruments == 'select'){
            document.getElementById('financial_instruments'+i).style.border='1px solid #C32F2F';
            document.getElementById('help-text-financial_instruments'+i).innerHTML='Please Select Financial Instruments Sold';
            $("#financial_instruments"+i).focus();
                missed_field_add = 1;
        }else{
            document.getElementById('financial_instruments'+i).style.border='';
            document.getElementById('help-text-financial_instruments'+i).innerHTML='';
        }
    }
    e.preventDefault();
    if(missed_field_add==0){
        if(allids.length < max_fields){ //max input box allowed
            x++; //text box increment
            allids.push(x);
            $(wrapper).append(
                '<div class="row row_financial" id="financial'+x+'">'+
                    '<div  class="col-sm-5 col-md-5 col-lg-5 selection-btn left-no-padding">'+
                        '<select class="form-group form-control" name="financial_instruments'+x+'" id = "financial_instruments'+x+'" onChange="validate_financial_instruments(id,'+x+');filter_financial_instruments();"></select>'+
                        '<span class="help-block" id="help-text-financial_instruments'+x+'"></span>'+
                    '</div>'+
                    '<div class="col-sm-5 col-md-5 col-lg-5 selection-btn">'+
                        '<input type="text" class="form-group form-control" name="financial_experience'+x+'" id="financial_experience'+x+'" placeholder="Financial Experience11" onChange="validateExperience(id,'+x+');" >'+
                        '<span class="help-block" id="help-text-financial_experience'+x+'"></span>'+
                    '</div> '+
                    '<a class = "remove_field btn additional_btn" id = "remove_field" onClick="remove_data('+x+');">'+
                        '<i class="fa fa-minus-circle" ></i>'+
                    '</a>'+
                '</div>'
            );
            $('#financial_instruments'+x).html(''); //Clear
            y = x-1;
            $('#financial_ins option').clone().appendTo('#financial_instruments'+x);
        }
    }
    onclick_add_filter_financial_instruments();
});

// Validating the Financial instrument select option
function check_select(){
    var e = document.getElementById("financial_instruments1");
    var strUser = e.options[e.selectedIndex].value;
    if (strUser == "select"){
        document.getElementById('financial_instruments1').style.border='1px solid #C32F2F';
        document.getElementById('help-text-financial_instruments1').innerHTML='Please Select Financial Instruments Sold';
        $("#financial_instruments1").focus();
        return false;
    }else{
        document.getElementById('financial_instruments1').style.border='';
        document.getElementById('help-text-financial_instruments1').innerHTML='';
    }
}

// Removing the selected option from Financial instrument types dropdown
function filter_financial_instruments(){
    for(var p=1; p<=allids.length; p++) {
        var i=allids[p-1];
        var selected_option = document.getElementById("financial_instruments"+i).value;
        for(var q=1; q<=allids.length; q++) {
            var j=allids[q-1];
            if(j!=i){
                var f = document.getElementById("financial_instruments"+j);
                for (var k=0; k<f.length; k++){
                    if (f.options[k].value == selected_option && f.options[k].value!='Select' ){
                        f.remove(k);
                    }
                }
            }
        }
        if(allids.length != 1){
          document.getElementById("financial_instruments"+i).disabled = true;
        }
    }
}

// Adding Financial instrument type option to select option dropdown after removing fields
function onclick_add_filter_financial_instruments(){
    for(var p=1; p<=allids.length; p++) {
        var i=allids[p-1];
        var e = document.getElementById("financial_instruments"+i);
        var strUser = e.options[e.selectedIndex].value;
        for(var q=1; q<=allids.length; q++) {
            var j=allids[q-1];
            if(j!=i){
                var f = document.getElementById("financial_instruments"+j);
                for (var k=0; k<f.length; k++){
                    if (f.options[k].value == strUser && f.options[k].value!='Select' ){
                        f.remove(k);
                    }
                }
            }
        }
    }
}

// Removing the Financial instrument data and fields
function remove_data(id){
    var e = document.getElementById("financial_instruments"+id);
    var strUser = e.options[e.selectedIndex].value;
    add_options(strUser);
    $('#financial'+id).remove();
    var i = allids.indexOf(id);
    if(i != -1) {
        allids.splice(i, 1);
    }
}

// Adding options to new financail instrument fields
function add_options(strUser){
    removed_text='Select';
    if(strUser=='Equity'){
        removed_text='Equity'
    }else if(strUser=='Wealth Advisory'){
        removed_text='Wealth Advisory'
    }else if(strUser=='Mutual Fund'){
        removed_text= "Mutual Fund"
    }else if (strUser=='Insurance'){
        removed_text= "Insurance"
    }else if(strUser=='Real Estate'){
        removed_text= "Real Estate"
    }else if(strUser=='PortFolio Management'){
        removed_text= "PortFolio Management"
    }else{
        removed_text='Select';
    }
    if(removed_text!='Select'){
        for(var j=0; j<allids.length; j++) {
            var i=allids[j];
            var e = document.getElementById("financial_instruments"+i);
            myOption = document.createElement("option");
            myOption.text = removed_text;
            myOption.value = removed_text;
            e.appendChild(myOption);
        }
    }
}

// Validating the Financial Experiance fields
function validateExperience(str,id) {
    var re = /^[1-9][0-9]?$|^99$/;
    var validexperience = document.getElementById('financial_experience'+id);
        if(!validexperience.value.match(re) || validexperience == null ) {
            var a=document.getElementById('financial_experience'+id).value = "";
            document.getElementById('financial_experience'+id).style.border='1px solid #C32F2F';
            document.getElementById('help-text-financial_experience'+id).innerHTML='Enter Valid Experience';
            $("#financial_experience"+id).focus();
        }else{
            document.getElementById('financial_experience'+id).style.border='';
            document.getElementById('help-text-financial_experience'+id).innerHTML='';
        }
}

// Validating the Financial instruments
function validate_financial_instruments(str,id) {
    var validinstruments = document.getElementById('financial_instruments'+id).value;
    if(validinstruments == 'select'|| validinstruments == ''){
        document.getElementById('financial_instruments'+id).style.border='1px solid #C32F2F';
        document.getElementById('help-text-financial_instruments'+id).innerHTML='Please Select Financial Instruments Sold';
        $("#financial_instruments"+id).focus();
    }else{
        document.getElementById('financial_instruments'+id).style.border='';
        document.getElementById('help-text-financial_instruments'+id).innerHTML='';
    }
    filter_financial_instruments();
}

// Submitting the Financial Instruments
function submit_creditbility_form(){
    var missed_field = 0;
    if(allids.length>0){
        document.getElementById('help-text-financial_instruments_main').innerHTML='';
        for(var j=0; j<allids.length; j++) {
            var i=allids[j];
            var re = /^[1-9][0-9]?$|^99$/;
            var validexperience = document.getElementById('financial_experience'+i);
            if(!validexperience.value.match(re) || validexperience == null ) {
                var a=document.getElementById('financial_experience'+i).value = "";
                document.getElementById('financial_experience'+i).style.border='1px solid #C32F2F';
                document.getElementById('help-text-financial_experience'+i).innerHTML='Enter Valid Experience';
                $("#financial_experience"+i).focus();
                missed_field = 1;
            }else{
                document.getElementById('financial_experience'+i).style.border='';
                document.getElementById('help-text-financial_experience'+i).innerHTML='';
            }
        }
        for(var j=0; j<allids.length; j++) {
            var i=allids[j];
            validinstruments="";
            var validinstruments = document.getElementById('financial_instruments'+i).value;
            if(validinstruments == 'Select'|| validinstruments == 'select'){
                document.getElementById('financial_instruments'+i).style.border='1px solid #C32F2F';
                document.getElementById('help-text-financial_instruments'+i).innerHTML='Please Select Financial Instruments Sold';
                $("#financial_instruments"+i).focus();
                    missed_field = 1;
            }else{
                document.getElementById('financial_instruments'+i).style.border='';
                document.getElementById('help-text-financial_instruments'+i).innerHTML='';
            }
        }
     }

    var value1='';
    var value2 ='';
    for(var j=0; j<allids.length; j++) {
        var i=allids[j];
        var instruments = document.getElementById('financial_instruments'+i).value;
        var experience = document.getElementById('financial_experience'+i).value;
        if(j==0){
            value1 = '[{"instruments":"'+instruments+'","experience":"'+experience+'"}';

        }else if(i==x){
            value2 = ',{"instruments":"'+instruments+'","experience":"'+experience+'"}';

        }else{
            value2 = ',{"instruments":"'+instruments+'","experience":"'+experience+'"}';
        }
            value1 = value1+value2;

    }
    value3=']';
    if (value1 != ''){
        value1=value1+value3;
    }
    document.getElementById("hidden_input").value = value1;
    if (missed_field == 0){
        $('#financial_ins_form').submit();
    }
}
