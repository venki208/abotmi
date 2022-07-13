var csrf_token = $("#id_csrf_token").val();
// Validating the Youtube URL

$("#video_url").on('keyup keypress change input', function(e){
    var url = this.value;
    if (url) {
        var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|\?v=)([^#\&\?]*).*/;
        var match = url.match(regExp);
        if (match && match[2].length == 11) {
            // Do anything for being valid
            $("#video_url_validation_null").hide();
            $("#video_preview").prop("disabled", false);
            $("#submitid").show();
        } else {
            $("#video_url_validation_null").show();
            $("#submitid").hide();
            // Do anything for not being valid
        }
    }
});

function load_video_preview(){
    var regExp1 = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|\?v=)([^#\&\?]*).*/;
    var urlPath = $("#video_url").val();
    var matches = urlPath.match(regExp1);    
    if (matches) {
        urlPath = urlPath.split("?v=")[1];
        $("#myIframe").show();
        //document.getElementById('myIframe').src = "https://www.youtube.com/embed/"+urlPath;
        $('#myIframe').attr('src', 'https://www.youtube.com/embed/' + matches[2] + '?autoplay=1&enablejsapi=1');
        $("#submitid").show();
    }else {
        alert("No preview! please enter url in https://www.youtube.com/watch?v=xyz format");
    }
 }

// Uploading the Video url
function advisor_video_upload(){
    var video_title = document.getElementById('video_title').value;
    var video_description = document.getElementById('video_description').value;
    var video_url = document.getElementById('video_url').value;
    var pattern2 = /(?:http?s?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.+)/g;
    video_url = video_url.replace(pattern2, "https://www.youtube.com/embed/$1");
    if (video_title && video_description && video_url) {
        $.ajax({
            type:"POST",
            url:"/dashboard/advisor_video_upload/",
            data:{
                video_title:video_title,
                video_description:video_description,
                video_url:video_url
            },
            beforeSend: function(request){
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            success:function(response){
                $('#video-upload-modal').modal('hide');
            }
        });
    }else{
        if (!video_title) {
            $("#video_title_validation").show();
        }else {
            $("#video_title_validation").hide();
        }

        if (!video_description) {
            $("#video_desc_validation").show();
        }else {
            $("#video_desc_validation").hide();
        }
    }
}
