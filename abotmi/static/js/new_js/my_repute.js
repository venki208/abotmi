var advisor_imges = [];
var viewed_cat_in_chart = [];
var current_user = {};
var position_image_obj = {};
var demo_profile_pic = http_host + $("#demo_profile_pic").val();
var current_pincode_from_local_storage = localStorage.getItem("current_pincode");
if (current_pincode_from_local_storage != null) {
    user_pincode = current_pincode_from_local_storage;
}
function back_pie_chart() {
    viewed_cat_in_chart.pop();
    dispaly_pie_graph();
}
function dispaly_pie_graph() {
    var mn_cat = null, sub_cat = null, tl_cat = null;
    if (viewed_cat_in_chart.length > 0) {
        for (var i = 0; i < viewed_cat_in_chart.length; i++) {
            if (viewed_cat_in_chart[i].class_name == "mn_cats") {
                mn_cat = viewed_cat_in_chart[i].category;
            } else if (viewed_cat_in_chart[i].class_name == "sub_cats") {
                sub_cat = viewed_cat_in_chart[i].category;
            } else {
                tl_cat = viewed_cat_in_chart[i].category;
            }
        }
    }
    if (tl_cat == null) {
        rpi_pei_chart('mn_categories', mn_cat, sub_cat, tl_cat);
    }
}
$(document).ready(function () {
    $('#show_repute_img').hide();
    $('#pie_chart_div').hide();
    $(".breakup_model").hide();
    demo_for_reputation_static_code();
    //Comented for demo purpose and for getting only static data
    // if(user_pincode != null || user_pincode != undefined || user_pincode != ""){
    //   call_native_api_call();
    // }else{
    //   edit_pincode_popup();
    // }
})

function call_native_api_call() {
    var csrf_token = $('#id_csrf_token').val();
    $.ajax({
        type: 'POST',
        url: '/reputation-index/call_native/',
        data: {},
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success: function (response) {
            if (response.status == 200) {
                get_advisors_rank(user_pincode);
            } else if (response.status == 500) {
                //show model to enter pincode
                edit_pincode_popup();
            } else if (response.status == 400) {
                alert(response.message);
            } else {
                alert('Unable to process your request now. Please try again after some time');
            }
        },
        error: function (response) {
            alert('Unable to process your request now. Please try again after some time');
        }
    });
}

function edit_pincode_popup() {
    var csrf_token = $('#id_csrf_token').val();
    $.ajax({
        method: 'GET',
        url: '/reputation-index/edit_pincode/',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success: function (response) {
            $("#my_repute_modal").html('');
            $("#my_repute_modal").html(response);
            show_bootstrap_modal('#id_pincode_modal');
        },
        error: function (response) {
            alert('Unable to process your request now. Please try again after some time');
        }
    });
}

function show_bootstrap_modal(elem) {
    $(elem).modal({
        show: true,
        keyboard: false,
        backdrop: 'static'
    });
}

function edit_pincode_func() {
    var pincode = $('#pincode').val();
    if (pincode != "") {
        $.ajax({
            method: 'POST',
            url: '/reputation-index/update_pincode/',
            data: { "pincode": pincode },
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            success: function (response) {
                if (response.status == 200) {
                    $('#id_pincode_modal').modal('hide');
                    call_native_api_call();
                } else if (response.status == 400) {
                    alert(response.message);
                    $('#pincode').val("");
                } else {
                    alert(response.message);
                }
            },
            error: function (response) {
                alert('Unable to process your request now. Please try again after some time');
            }
        });
    } else {
        alert('Please enter your native pincode');
    }
}

function demo_for_reputation_static_code() {
    var csrf_token = $('#id_csrf_token').val();
    var response = reputation_index_static_data;
    advisor_imges = response.data.advisors;
    current_user = response.data.meta;
    display_images();
}

function get_advisors_rank(pincode) {
    $.ajax({
        type: 'POST',
        url: '/reputation-index/get_advisors_rank/',
        data: { "username": user_profile_email, "pincode": pincode },
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success: function (response) {
            if (response.status) {
                advisor_imges = response.data.advisors;
                current_user = response.data.meta;
                display_images();
            } else {
                alert(response.message);
            }
        },
        error: function (response) {
            alert('Unable to process your request now. Please try again after some time');
        }
    });
}

function display_images() {
    var t = Date.now();
    var upwrdz_big_img = new Image();
    upwrdz_big_img.src = $("#bg_image").val();//'https://dev.upwrdz.com/static/new_images/logo-big.png';
    var length = 12; //Put 6 for four sqware cobmination
    var ylength = 12; //Put 6 for four sqware cobmination
    var current_user_rank = current_user.rank;
    $("#current_adv_text").html(current_user.name + "<br/>" + current_user.points);
    if (current_user.image != "") {
        $("#current_adv_pic").attr("src", current_user.image);
        $("#current_adv_pic").attr("alt", "");
    } else {
        $("#current_adv_pic").attr("src", demo_profile_pic);
    }
    $("#current_adv_pic").attr("src", demo_profile_pic); //Need to remove this line once demo code is removed.
    var advisor_img_positions1 = [10, 9, 22, 21, 8, 34];
    var advisor_img_positions2 = [20, 32, 33, 7, 46];
    var advisor_img_positions3 = [31, 43, 44, 19];
    var advisor_img_positions4 = [42, 54, 55];
    var advisor_img_positions5 = [65, 66];
    var advisor_img_positions6 = [76];
    if (!current_user.is_top_6) {
        advisor_img_positions3 = [53, 54, 66, 65];
        advisor_img_positions4 = [64, 76, 77];
        advisor_img_positions5 = [87, 88];
        advisor_img_positions6 = [98];
    }

    var groups = _.groupBy(advisor_imges, 'rank');
    var sort_arr = []
    var index = 1;
    for (var key in groups) {
        sort_arr = _.sortBy(groups[key], function (adv) {
            if (adv.is_current_user == 1) {
                return adv
            }
        })
        var current_position = "";
        switch (index) {
            case 1: current_position = advisor_img_positions1; break;
            case 2: current_position = advisor_img_positions2; break;
            case 3: current_position = advisor_img_positions3; break;
            case 4: current_position = advisor_img_positions4; break;
            case 5: current_position = advisor_img_positions5; break;
            case 6: current_position = advisor_img_positions6; break;
        }
        $.each(current_position, function (i, v) {
            position_image_obj[v] = sort_arr[i];
        });
        index++;
    }
    upwrdz_big_img.onload = function () {
        var width = this.width,
            height = this.height,
            _length = -length,
            i, j;
        var $basicDiv = jQuery('<div/>', {
            class: 'splitImg',
            css: {
                'width': Math.floor(width / length),
                'height': Math.floor(height / ylength),
                'background-image': 'url(' + upwrdz_big_img.src + ')',
            }
        });
        var $upwrdz_big_img_div = $('#upwrdz_big_img_div').width(width);
        var index = 0;
        for (i = 0; i > _length; i--) {
            for (j = 0; j > _length; j--) {
                $basicDiv.clone().css({ 'background-position': `${width / length * j}px ${height / ylength * i}px`, 'color': '#fff' }).appendTo($upwrdz_big_img_div);
                $basicDiv.attr('id', 'index_' + index);
                // $basicDiv.text(index);
                index++;
            }
        }
        for (var key in position_image_obj) {
            if (position_image_obj[key] != undefined) {
                if (current_user.username == position_image_obj[key].username) {
                    $("#current_adv_key").val(key);
                }
                if (position_image_obj[key].native) {
                    $("#index_" + key).append('<img class="img_hover" id="advisor_image_' + key + '"    onclick="get_selected_advisor_details(' + key + ')" width="100%" />');
                } else {
                    $("#index_" + key).attr("class", "transit_advisor");
                    $("#index_" + key).append('<img class="transit transit_advisor img_hover" onclick="get_selected_advisor_details(' + key + ')" id="advisor_image_' + key + '"    width="100%" />');
                }
                if (position_image_obj[key].image != "") {
                    $("#advisor_image_" + key).attr("src", position_image_obj[key].image);
                    $("#advisor_image_" + key).attr("alt", "");
                } else {
                    $("#advisor_image_" + key).attr("src", demo_profile_pic);
                }
            }
        }
    }
}
function get_selected_advisor_details(key) {
    if (current_user.rank != position_image_obj[key].rank) {
        $("#compare_adv_pic").attr("src", "");
        $("#compare_adv_key").val(key);
        $("#compare_adv_text").html(position_image_obj[key].name + "<br/>" + position_image_obj[key].points);
        if (position_image_obj[key].image != "") {
            $("#compare_adv_pic").attr("src", position_image_obj[key].image);

            $("#compare_adv_pic").attr("alt", "");
        } else {
            $("#compare_adv_pic").attr("src", demo_profile_pic);
        }
    } else {
        alert("You can not select your own image for comparison")
    }
}
function open_compare_model() {
    var compare_advisor = position_image_obj[$("#compare_adv_key").val()];
    if (compare_advisor != undefined) {
        var table_str = "<table>" +
            "<tr>" + "<th>Advisors</th>" + "<th>" + current_user.name + "</th>" + "<th>" + compare_advisor.name + "</th>" + "</tr>";
        $.each(current_user.breakup.category_parts, function (key, value) {
            table_str = table_str + "<tr>" + "<td>" + key + "</td>" + "<td>" + value + "</td>" + "<td>" + compare_advisor.breakup.category_parts[key] + "</td>" + "</tr>";
        });
        table_str = table_str + "<tr>" + "<td>Total Points</td>" + "<td>" + current_user.points + "</td>" + "<td>" + compare_advisor.points + "</td>" + "</tr>";
        table_str = table_str + "</table>";
        $("#adv_compare_table").empty();
        $("#adv_compare_table").append(table_str);
        $('#display_adv_compare').modal({
            keyboard: false,
            escapeClose: true,
            clickClose: false,
            showClose: false
        });
    } else {
        alert("Please select advisor to compare");
    }
}

var output = {};
function open_breakup_model() {
    $('#show_repute_img').hide();
    $('#rpi_big_img').hide();
    $('#show_repute_img').show();
    $('#pie_chart_div').show();
    $(".breakup_model").show();
    if (current_user != undefined) {
        output['name'] = "Reputation Index";
        output['children'] = [];
        var main_cats = {}; //This is only for getting no of cats available and color
        var crb = current_user.breakup;
        if (crb.mn_categories != undefined) {
            for (var mn_indx in crb.mn_categories) {
                mn_cat_op = {};
                if (crb.points != 0) {
                    var mncat_name = crb.mn_categories[mn_indx];
                    if (crb[mncat_name] != undefined && crb[mncat_name].points > 0) {
                        mn_cat_op['name'] = mncat_name;
                        mn_cat_op['points'] = crb[mncat_name].points;
                        mn_cat_op['oaPercentage'] = get_int_or_float_number(mn_cat_op['points'] * 100 / crb.points);
                        mn_cat_op['percentage'] = get_int_or_float_number(mn_cat_op['points'] * 100 / crb.points);
                        mn_cat_op['fill_color'] = get_color_code_arr_for_all_main_cats(mncat_name);
                        main_cats[mncat_name] = mn_cat_op['fill_color'];
                        mn_cat_op['children'] = [];
                        for (var sbcat_indx in crb[mncat_name].sub_cats) {
                            var subcat_name = crb[mncat_name].sub_cats[sbcat_indx];
                            if (crb[mncat_name][subcat_name] != undefined) {
                                sb_cat_op = {}
                                sb_cat_op['name'] = subcat_name;
                                sb_cat_op['points'] = crb[mncat_name][subcat_name].points;
                                sb_cat_op['mn_cat_name'] = mncat_name;
                                sb_cat_op['oaPercentage'] = get_int_or_float_number(sb_cat_op['points'] * 100 / crb.points);
                                sb_cat_op['percentage'] = get_int_or_float_number(sb_cat_op['points'] * 100 / mn_cat_op['points']);
                                sb_cat_op['fill_color'] = sub_cat_tl_cat_color(mncat_name, "sub_cat");
                                sb_cat_op['children'] = [];
                                for (var tlcat_indx in crb[mncat_name][subcat_name].third_l_cats) {
                                    var tl_cat_name = crb[mncat_name][subcat_name].third_l_cats
                                    [tlcat_indx];
                                    tl_cat_op = {};
                                    if (crb[mncat_name][subcat_name][tl_cat_name] != undefined) {
                                        tl_cat_op['name'] = tl_cat_name;
                                        tl_cat_op['fill_color'] = sub_cat_tl_cat_color(mncat_name, "tl_cat");
                                        tl_cat_op['size'] = crb[mncat_name][subcat_name][tl_cat_name].points;
                                        tl_cat_op['sb_cat_name'] = subcat_name
                                        tl_cat_op['mn_cat_name'] = mncat_name
                                        tl_cat_op['points'] = crb[mncat_name][subcat_name][tl_cat_name].points;
                                        tl_cat_op['oaPercentage'] = get_int_or_float_number(tl_cat_op['points'] * 100 / crb.points);
                                        tl_cat_op['percentage'] = get_int_or_float_number(tl_cat_op['points'] * 100 / sb_cat_op['points']);
                                        sb_cat_op['children'].push(tl_cat_op);
                                    }
                                }
                                mn_cat_op['children'].push(sb_cat_op);
                            }
                        }
                        output['children'].push(mn_cat_op);
                    }
                }
            }
        }
        var output_json = JSON.stringify(output, null, '\t');
        var repute_map_show = $('#repute_map_show');
        open_breakup_piechart(output['children'], main_cats);
        //Old plugin code commented for future use
        // open_breakup_piechart(output);
    }
}

function get_int_or_float_number(percent) {
    if (Number.isInteger(percent)) {
        return parseInt(percent)
    } else {
        return percent.toFixed(3)
    }
}

function show_repute_image() {
    $('#show_breakup').show();
    $('#pie_chart_div').hide();
    $(".breakup_model").hide();
    $('#show_repute_img').hide();
    $('#rpi_big_img').show();
    var s = d3.selectAll('svg');
    s.remove();
}

var TW_COLOR = ['#5C6BC0', '#9ba9f3'];
var EST_COLOR = ['#BA68C8', '#CE93D8'];
var EXP_COLOR = ['#F06292', '#F48FB1'];
var REP_IND_COLOR = ['#311B92', '#9C27B0', '#E91E63'];

function get_color_code_arr_for_all_main_cats(mn_cat) {
    color_code = null;
    if (mn_cat == "trustworthiness") {
        color_code = REP_IND_COLOR[0];
    } else if (mn_cat == "establishment") {
        color_code = REP_IND_COLOR[1];
    } else if (mn_cat == "expertise") {
        color_code = REP_IND_COLOR[2];
    }
    return color_code;
}

function sub_cat_tl_cat_color(mn_cat, c_type) {
    var color_code = null;
    var ind = 0;
    if (c_type == "tl_cat") {
        ind = 1;
    }
    if (mn_cat == "trustworthiness") {
        color_code = TW_COLOR[ind];
    } else if (mn_cat == "establishment") {
        color_code = EST_COLOR[ind];
    } else if (mn_cat == "expertise") {
        color_code = EXP_COLOR[ind];
    }
    return color_code;
}

function get_color_code_arr(mn_cat) {
    var color_arr = null;
    if (mn_cat == "trustworthiness") {
        color_arr = TW_COLOR;
    } else if (mn_cat == "expertise") {
        color_arr = EXP_COLOR;
    } else if (mn_cat == "establishment") {
        color_arr = EST_COLOR;
    } else {
        color_arr = REP_IND_COLOR;
    }
    return color_arr;
}

function cancel_pincode_confirmation_popup() {
    $('#current_pincode').val("");
    $('#pincode_confirmation_modal').modal('hide');
}

function validate_pin(pin) {
    return /^[1-9]\d{3}$|^[1-9]\d{5}$/.test(pin);
}

function transit_hyperlocal_api_call() {
    var pincode = $('#current_pincode').val();
    if (validate_pin(pincode)) {
        localStorage.setItem("current_pincode", pincode);
        $.ajax({
            type: "POST",
            url: "/reputation-index/advisor_reputation_for_hyperlocal/",
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            data: { "pincode": pincode, "hyperlocal_type": "transient" },
            success: function (response) {
                alert(response.message);
                cancel_pincode_confirmation_popup();
                get_advisors_rank(pincode);
            }
        });
    } else {
        alert("pincode should be 4 or 6 digit number");
    }
}

function show_check_pincode_model() {
    show_bootstrap_modal('#pincode_confirmation_modal');
    initMap();
}

// function showing bootstrap modal 
function show_bootstrap_modal(elem) {
    $(elem).modal({
        show: true,
        keyboard: false,
        backdrop: 'static'
    });
}

/**
 * Share with code starts here
 */

// facebook share function
function fb_share() {
    var page = advisor_profile_url;
    var fbpopup = window.open("https://www.facebook.com/sharer/sharer.php?u=" + page, "pop", "width=600, height=400, scrollbars=no");
}

// facebook LinkedIn function
function LinkedInShare() {
    window.open("https://www.linkedin.com/shareArticle?mini=true&url=" + advisor_profile_url + "&title=UPWRDZ&summary=My%20UPWRDZ%20Shared%20Profile&source=LinkedIn", 'linkedin', 'height=400,width=600');
}

// facebook googleplus function
function googleplusbtn() {
    window.open('https://plus.google.com/share?url=' + advisor_profile_url + '', '', 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=200,width=600');
    return false;
}

// facebook twitter function
function twitter_share() {
    var width = 575,
        height = 400,
        left = ($(window).width() - width) / 2,
        top = ($(window).height() - height) / 2,
        url = "https://twitter.com/intent/tweet?url=" + advisor_profile_url,
        opts = 'status=1' +
            ',width=' + width +
            ',height=' + height +
            ',top=' + top +
            ',left=' + left;

    window.open(url, 'twitter', opts);
    return false;
}

 /**
 * Share with code ends here
 */
