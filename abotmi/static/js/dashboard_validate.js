// Valdates the currency value with the regx
function validateCurrency(str) {
    curRegExp = /^(?:0|[1-9]\d*)(?:\.(?!.*000)\d+)?$/;
    var income = document.getElementById(str);
    if(!curRegExp.test(income.value)) {
        document.getElementById(str).value = "";
        alert("Enter valid input");
        return false;
    }
    if($("#"+str).val() == 0){
        document.getElementById(str).value = "";
        $("#help-text-gross_annual_income").html('Please Enter Valid Gross Annual Income');
        $("#gross_annual_income").focus();
    }else{
        $("#help-text-gross_annual_income").html('');
    }
}