var wpb_url = wpb_url;
var token = csrf_token;

function launch_wpb(){    
    var url_link = "/wpb/create_session/";
    $.ajax({
        url: url_link,
        type: 'POST',
        beforeSend: function (request){
            request.setRequestHeader("X-CSRFToken",token);
        },
        success: function(response){
            window.open(wpb_url+"/api/user/abotmi_user_creation/"+response+"/", '_blank');
        }
    });
}

// stram joining functions
function joining_course(course_id,course_name){
    var url_link = "/wpb/create_session/";
    $.ajax({
        type: "POST",
        url: url_link,
        data:{'course_id': course_id,'course_name':course_name},
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        success: function(response){
            window.open(wpb_url+"/api/user/abotmi_user_creation/"+response+"/"+course_id, '_blank');
        }
    });
}