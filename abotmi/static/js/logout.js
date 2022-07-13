// Logout function - this logs out the user
var token = $("#id_csrf_token").val();
function user_logout(){
    $.ajax({
        url: '/logout/',
        type: 'POST',
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken",token);
        },
        success: function(response){
            if(response=='success'){
                window.location.href = '/';
            }
        },
        error: function (response) {
            alert('Unable to logout/signout \n Please try again after some time')
        }
    });
}
