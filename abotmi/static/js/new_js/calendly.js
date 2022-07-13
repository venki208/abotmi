function show_calendly_modal(elem){
     $(elem).modal({
         show: true,
         keyboard: false,
         backdrop: 'static'
     });
}


function get_advisors_calendly_link(id) {
    if (id.length>0 && id != "None") {
        $.ajax({
            type: "POST",
            url: "/advisor_check/get_calendly_link/",
            data: {
                'id': id
            },
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            success: function (e, xhr, settings) {
                if (e.status_code == 200) {
                    window.open(settings.responseJSON.data, '_blank');
                } else if (e.status_code == 204) {
                    show_alert(
                        'warning',
                        '',
                        '<p>This advisor is not available to take an appointment now. Please try later.</p>'
                    );
                }else{
                     show_alert(
                         'warning',
                         '',
                         '<p>Unable to send Email</p>'
                     );
                }
            }
        });

    }else{show_alert(
        'warning',
        '',
        '<p>Advisor Email is unavailable/ Not a registered Advisor</p>'
    );
}}