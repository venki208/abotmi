var profile_url;
// Intializing the facebook for share
(function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_GB/sdk.js#xfbml=1&version=v2.6&appId=738135046316916";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

// intializing the twitter scripts for share
(function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0], p = /^http:/.test(d.location) ? 'http' : 'https';
    if (!d.getElementById(id)) {
        js = d.createElement(s);
        js.id = id;
        js.src = p + '://platform.twitter.com/widgets.js';
        fjs.parentNode.insertBefore(js, fjs);
    }
}(document, 'script', 'twitter-wjs'));

// Facebook likes count by ajax script
window.fbAsyncInit = function () {
    var url = $("#fb_link_url").val();
    FB.Event.subscribe('edge.create', function (response) {
        sm_ajax("fb");
    });
    // Code to detect clicking unlike
    FB.Event.subscribe('edge.remove', function (href) {
        sm_ajax("fb");
    });
};

function trackgoogle(reponse) {
    if (reponse.state == 'on')
        sm_ajax("g+");
    else
        sm_ajax("g+");
}

function sm_ajax(type) {
    var url = $("#fb_link_url").val();
    var type = type;
    $.ajax({
        url: "/blog/icore/sm_count/",
        method: "POST",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        data: {
            url: url,
            type: type
        },
        success: function (response) {
        }
    });
}

// Submitting the comment
$("#icore_add_comment").submit(function () {
    postComment();
    return false;
});

// Posting comment
var srcimage = "";
function postComment() {
    var comment = document.getElementById("comment").value;
    if (!comment) {
        alert("please enter some text to comment");
    }
    else {
        var comment_box_clearfix = document.getElementById("comment_box_clearfix");
        comment_box_clearfix.name = "comment_box1_clearfix";
        comment_box_clearfix.setAttribute("class", "comment-box clearfix");

        var image_div1 = document.createElement("div");
        image_div1.name = "user_img-circle";
        image_div1.id = "user_img-circle";
        image_div1.setAttribute("class", "user");
        comment_box_clearfix.appendChild(image_div1);

        var image_tag = document.createElement("IMG");
        image_tag.setAttribute("class", "img-circle");
        image_tag.setAttribute("src", profile_pic);
        image_tag.setAttribute("alt", "profile image");
        image_tag.setAttribute('style', 'width:64px; height:64px;');
        image_div1.appendChild(image_tag);

        var new_div = document.createElement("div");
        new_div.name = "comment-content";
        new_div.id = "comment-content";
        new_div.class = "comment-content";
        new_div.setAttribute("class", "comment-content");
        comment_box_clearfix.appendChild(new_div);

        var new_div2 = document.createElement('div');
        new_div2.name = "display_comments";
        new_div2.id = "display_comments";

        new_div.appendChild(new_div2);

        var br = document.createElement("br");

        var button = document.createElement("button");
        var user_name = user_first_name;

        $("<h4 class='comment-by-dummy'>").text(user_name).appendTo(new_div2);
        $("<p class='wordwrap'>").text(comment).appendTo(new_div2);

        document.getElementById('comment').value = "";
        if (document.getElementById("no_comment")) {
            document.getElementById("no_comment").style.display = "none";
        }

        $.ajax({
            url: "/blog/icore/add-comment/",
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", token);
            },
            method: "POST",
            data: {
                'post_id': post_id,
                'comment': comment,
            },
            success: function (response) { }
        });
    }
}

// going to back to previous page
function back() {
    window.history.back();
}

// setting rating
$(document).ready(function () {
    $("#rating").rateit('value', rating_val);
    if (is_advisor == 'False'){
        $("#rating").rateit('readonly', true);
    }
});

// Adding rating for post
$("#rating").bind('rated', function (event, value) {
    $.ajax({
        url: "/blog/icore/add-rating/",
        method: "POST",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        data: {
            post_id: icore_id,
            star_sum: value
        },
        success: function (response) {
        }
    });
});