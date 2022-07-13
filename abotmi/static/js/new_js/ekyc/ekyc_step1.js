var token = token;
var img_data, document_type;
var capture_btn = $("#capture_button");

// intializing camera
Webcam.set({
    width: 640,
    height: 480,
    dest_width: 640,
    dest_height: 480,
    image_format: 'jpeg',
    jpeg_quality: 90
});

$("[name='capture_type_radio']").on('click', function (e) {
    sel_type = $(this).val();
    if (sel_type == 'camera') {
        $("#camera_div").removeClass('hide');
        $("#upload_div").addClass('hide');
        start_camera();
    } else {
        off_camera();
        $("#camera_div").addClass('hide');
        $("#upload_div").removeClass('hide');
    }
});

function start_camera() {
    Webcam.attach('#my_camera');
}

function off_camera() {
    Webcam.reset();
}

capture_btn.on('click', function (e) {
    Webcam.snap(function (data_uri) {
        captured_image = data_uri;
        document_type = $("#capture_button").attr('picture-type');
        $.ajax({
            type: 'POST',
            url: '/signup/upload_eipv_documents/',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", token);
            },
            data: {
                document_type: document_type,
                image: captured_image
            },
            success: function (response) {
                if (response.result == 'success') {
                    change_document_status(document_type, response.document_url);
                }
            },
            error: function (response) {
                show_alert(
                    'error',
                    '',
                    '<p>Unable to upload <br /> Please try again.<p>'
                );
            }
        });
    });
});

function change_document_status(document_type, download_link) {
    var attached_link = "<span class='child_eipv_span n-padding-r-5 n-span-pink-color'>Attached&nbsp; <a class='' onclick=preview_image('" + download_link + "'); data-toggle='tooltip' data-placement='bottom' title='Preview image' style='margin-right:5px;'><i class='fa fa-eye' aria-hidden='true'></i></a><a class='' onclick=re_upload_document('" + document_type + "'); data-toggle='tooltip' data-placement='bottom' title='Reset/Re upload'><i class='fa fa-trash download_link_color' aria-hidden='true'></i></a></span>";
    if (document_type == 'eipv_face_capture') {
        eipv_face_capture = true;
        $("#attached_div")
            .html(attached_link)
            .removeClass('hide');
    }
    $("#question_div").addClass('hide');
    $("#camera_div").addClass('hide');
    $("#upload_div").addClass('hide');
    $("[name='capture_type_radio']").prop('checked', false);
    off_camera();
    $("#next_btn").removeClass('hide');
    $("input[type='file']").val('');
    if (document_type == 'eipv_face_capture') {
        $(".header-profile-pic").html(
            '<img src="' + download_link + '" class="img-responsive n-user-img header-profile" alt="">'
        );
    }
    $.toast({
        text: 'Uploaded Successfully.',
        textAlign: 'center',
        showHideTransition: 'slide',
        position: 'top-center',
        icon: 'success'
    });
}

// preview image pop up 
function preview_image(url) {
    $("#image_show_body").html('');
    $("#image_show_body").html("<img src='" + url + "' class='img-responsive'></img>");
    $("#show_image_model").modal('show');
}

function re_upload_document(doc_type) {
    $("#attached_div").addClass('hide');
    $("#question_div").removeClass('hide');
    $("#next_btn").addClass('hide');
}

// Uploading the image as file
$("#upload").on('click', function (e) {
    var upload_res = upload_document('upload_form');
    upload_res.success(function (response) {
        document_type = $("#capture_button").attr('picture-type');
        change_document_status(document_type, response.url);
        $('html, body').animate({
            scrollTop: $('#face_capture_id').offset().top-500
        }, 'slow');
    });
    upload_res.error(function (response) {
        $.toast({
            heading: 'Error',
            text: 'Unable to upload the document <br /> Please try again.',
            showHideTransition: 'slide',
            position: 'top-center',
            icon: 'error'
        });
    });
});


// Checks uploading file format is image or not
$("[name='document']").change(function (e) {
    var fileInput = $(this);
    if (fileInput.length && fileInput[0].files && fileInput[0].files.length) {
        var url = window.URL || window.webkitURL;
        var image = new Image();
        image.onerror = function () {
            alert('Please Upload Valid image');
            fileInput.val('');
        };
        image.src = url.createObjectURL(fileInput[0].files[0]);
    }
});