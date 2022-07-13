var add_inst_btn = $('[name="add_fin_inst_btn"]');
var f_c = fin_ins_len;
var inst_div = $("#inst_div");
var submit_btn = $("#financial_submit_btn");

// default financial instruments options
var exp_opt_dict = [
    'Select',
    'Equity',
    'Wealth Advisory',
    'Mutual Fund',
    'Insurance',
    'Real Estate',
    'Portfolio Management'
];

var selected_options = [];

// updating options if database has the data
if(f_c>0){
    update_options();
    if(f_c == 6){
        add_inst_btn.addClass('hide');
    }
}

// validating instruments fields and adding additional instruments fields
add_inst_btn.on('click', function(e){
    if (validate_instruments()){
        if (inst_div.find('select').length <= 6) {
            f_c ++;
            inst_div.append(
                '<div class="row form-group add-row">'+
                    instruments_div(f_c) + experience_div(f_c) + remove_btn_div(f_c) +
                '</div>'
            );
            update_options();
            if (inst_div.find('select').length == 6){
                add_inst_btn.addClass('hide');
            }
        }else{
            add_inst_btn.addClass('hide');
        }
        
    }
});

// generating instruments select option tag
var inst_opt_tags = function(count){
    dyn_options = '';
    
    // disable the selected options
    for (i = 0; i < exp_opt_dict.length; i++){
        if (selected_options.indexOf(exp_opt_dict[i]) >= 0){
            dyn_options += '<option value="' + exp_opt_dict[i] + '" disabled>' + exp_opt_dict[i] + '</option>';        
        }else{
            dyn_options += '<option value="'+exp_opt_dict[i]+'">'+exp_opt_dict[i]+'</option>';
        }
    }

    var sel_html = '<select id="instrument' + count+'" class="form-control">'+
                        dyn_options+
                    '</select>';
    return sel_html;
};

// generating experience input tag
var inp_tag = function(count){
    var input_html = '<input type="number" id="experience'+count+'" class="form-control" placeholder="Experience" min="0">';
    return input_html;
};

// generating financial instruments div
var instruments_div = function (count) {
    var inst_div = 
        '<div class="col-6">' +
            inst_opt_tags(count) +
            '<span class="help-block" id="help_instrument' + count + '"></span>' +
        '</div>';
    return inst_div;
};

// generating experience div
var experience_div = function(count){
    var exp_div = 
        '<div class="col-4">' +
            inp_tag(count) +
            '<span class="help-block" id="help_experience' + count + '"></span>' +
        '</div>';
    return exp_div;
};

// generaing remove button div
var remove_btn_div = function(count){
    var rem_btn_div = 
        '<div class="col-2">' +
            '<button class="btn exp_btn" id="remove_btn'+count+'" onclick="remove_inst('+"'"+count+"'"+')">'+
                '<i class="fa fa-times" aria-hidden="true"></i>' +
            '</button>'+
        '</div>';
    return rem_btn_div;
};

// onchange of select calling function
$("#inst_div").on('change', 'select', function(e){
    update_options();
});

// updating the options in all selected tags (disable & enable)
function update_options(){

    // Getting all selected options
    selected_options = $.map(inst_div.find('select'), function (elem, index) {
        return $(elem).val();
    });

    inst_div.find('select').each(function (elm) {
        // current select tag element selected value
        var curr_val = $(this).val();

        // disable the selected options to all select tags
        for (i = 0; i < selected_options.length; i++) {
            if (curr_val != selected_options[i]) {
                $('#' + this.id + ' option[value="' + selected_options[i] + '"]')
                    .attr('disabled', true);
            }
        }

        // Getting not selected options into array by comparing exp_opt_dict and selected options
        not_selected_options = exp_opt_dict.filter(function (obj) {
            return selected_options.indexOf(obj) == -1;
        });

        // removing disable from not selected options
        for (i = 0; i < not_selected_options.length; i++) {
            $('#' + this.id + ' option[value="' + not_selected_options[i] + '"]')
                .removeAttr('disabled');
        }
    });
}

// function for removing instruments div
function remove_inst(count){
    $("#remove_btn"+count).closest('.row').remove();
    update_options();
    add_inst_btn.removeClass('hide');
}

// validating the instruments
function validate_instruments(){
    var missed_field = 0;
    var input_tags = inst_div.find('.form-control');

    for (var i = input_tags.length - 1; i >= 0; i--){
        if (input_tags[i].type == 'select-one' && input_tags[i].value == 'Select'){
            $('#help_' + input_tags[i].id).html('Please select Financial Instrument');
            input_tags[i].focus();
            missed_field = 1;
        }
        else if (input_tags[i].type == 'number') {
            if (input_tags[i].value == ''){
                $('#help_' + input_tags[i].id).html('Please enter Experience');
                input_tags[i].focus();
                missed_field = 1;
            } else if (input_tags[i].value <= 0){
                $('#help_' + input_tags[i].id).html('Please enter valid Experience');
                input_tags[i].focus();
                missed_field = 1;
            } else if (input_tags[i].value > 99){
                $('#help_' + input_tags[i].id).html('Please enter valid Experience');
                input_tags[i].focus();
                missed_field = 1;
            }
        }else{
            $('#help_' + input_tags[i].id).html('');
        }
    }
    
    if(missed_field == 1){
        return false;
    }else{
        return true;
    }
}

// generating financial instruments data into json
function get_financila_instruments_json(){
    var input_tags = inst_div.find('.add-row');
    var fin_inst_data = [];
    for (i=0; i<input_tags.length; i++){
        fin_inst_data.push({
            'instrument': $(input_tags[i]).find('select').val(),
            'experience': $(input_tags[i]).find('input').val()
        });
    }
    return fin_inst_data;
}

// onclick of submit button calling save function
submit_btn.on('click', function(e){
    save_financial_instruments();
});

// validating and saving the financial instruments
function save_financial_instruments() {
    if (validate_instruments()) {
        var instrument_json = get_financila_instruments_json();
        $.ajax({
            method: 'POST',
            beforeSend: setHeader,
            url: '/my_identity/experience/',
            data: {
                instrument_json: JSON.stringify(instrument_json)
            },
            success: function (response) {
                if (response == 200) {
                    var res_html = '';
                    if(instrument_json.length > 0){
                        for (i = 0; i < instrument_json.length; i++) {
                            res_html += '<label><b>' + instrument_json[i].instrument + ': &nbsp;</b><span>' + instrument_json[i].experience + '</span></label><br />';
                        }
                    }
                    else{
                        res_html = 'Experience information not uploaded yet.';
                    }
                    $(".total_experience_span").html(res_html);
                    show_alert(
                        'success',
                        'editExperience',
                        '<p>Updated Experience successfully.</p>'
                    );
                }
            },
            error: function (response) {
                show_alert(
                    'error',
                    'editExperience',
                    '<p>Unable to process your request <br /> Please try again after sometime.</p>'
                );
            }
        });
    }
}