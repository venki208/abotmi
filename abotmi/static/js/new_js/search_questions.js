var csrf_token = $("#id_csrf_token").val();

// settimeout function
var delay = (function () {
    var timer = 0;
    return function (callback, ms) {
        clearTimeout(timer);
        timer = setTimeout(callback, ms);
    };
})();

$(document).click(function(){
  $("#no_result_hide").hide();
});

// Searching Answers
$(function () {
    $("#search_answers").on('keyup keydown', function () {
        delay(function () {
            var search = $('#search_answers').val();
            search = search.replace(/^\s+|\s+$/gm, '');
            if ($('#search_answers').val().length > 0) {
                $('#list_ad').html('').load("/member/answers_archive/?search=" + search);
            }else {
                $('#dropdown_hide').fadeToggle();
            }
        }, 800);
        $('#send_button').prop('disabled', false);
        $("#help_text_search_div").html('')
    });
});

// Loading the Answer
function add_client_to_input(id, members_div, q_id) {
    $('#search_answers').val(id);
    $('#search-dropdown').css('display', 'block');
    window.location.href = '/member/read_more_answer/?question_id=' + q_id;
}
