var playing_iframe = [];
var is_other_video_present, current_video_present, last_current_video_id;
var last_other_video_id;
last_other_video_id = $("#last_other_video_id").val();
is_other_video_present = $("#other_video_present").val();
current_video_present = $("#current_video_present").val();
last_current_video_id = $("#last_current_video_id").val();

players = [];

function onYouTubeIframeAPIReady() {
    var temp = $("iframe.iframe_class");
    for (var i = 0; i < temp.length; i++) {
        var t = new YT.Player($(temp[i]).attr('id'), {
            events: {
                'onStateChange': onPlayerStateChange
            }
        });
        players.push(t);
    }
}
onYouTubeIframeAPIReady();

function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING) {
        $.each(players, function (k, v) {
            if (this.getIframe().id != event.target.getIframe().id) {
                if (typeof this.stopVideo == 'function')
                this.stopVideo();
            }
        });
    }
    if(event.data === 0){
        var lastIndex = event.target.a.id.lastIndexOf('_');
        var current_next_btn= event.target.a.id.substr(lastIndex+1);
        if(is_other_video_present){
            if(last_other_video_id != current_next_btn){
                $('#play_next_'+current_next_btn)
                    .removeClass('display_none');
            }
        }
        if(current_video_present){
            if(last_current_video_id != current_next_btn){
                $('#play_next_current_'+current_next_btn)
                    .removeClass('display_none');
            }
        }
    }
}

function filter_videos() {
    var my_videos_div_arr = document.getElementsByClassName("current_advisor_videos_class");
    var other_videos_div_arr = document.getElementsByClassName("other_advisors_videos_class");
    var input, filter;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    check_for_loop(my_videos_div_arr, filter);
    check_for_loop(other_videos_div_arr, filter);
}

function check_for_loop(arr, filter) {
    for (var i = 0; i < arr.length; i++) {
        var title = arr[i].getElementsByClassName("video-title")[0];
        if (title.innerHTML.toUpperCase().indexOf(filter) > -1) {
            arr[i].style.display = "";
        } else {
            arr[i].style.display = "none";
        }
    }
}

function play_next_video(element) {
    var total_video_ids = JSON.parse(total_vid_id);
    var lastIndex = element.id.lastIndexOf('_');
    var current_next_btn = element.id.substr(lastIndex + 1);
    var index_current_video_id = total_video_ids.indexOf(parseInt(current_next_btn));
    var index_next_video_id = index_current_video_id + 1;
    if (index_next_video_id < total_video_ids.length) {
        var ddd = $("#advisors_videos_" + total_video_ids[index_next_video_id].toString());
        var videoURL = ddd.prop('src');
        videoURL += "&autoplay=1";
        ddd.prop('src', videoURL);
        $('html,body').animate({
            scrollTop: $(("#advisors_videos_" + total_video_ids[index_next_video_id].toString())).offset().top - 100
        }, 1000);
        onYouTubeIframeAPIReady("#advisors_videos_" + total_video_ids[index_next_video_id]);
    }
}

$(document).ready(function(){
    $("#growth_menu").addClass('active');
})