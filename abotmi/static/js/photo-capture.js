//Global variable declaration
var image;
var token = $('#id_csrf_token').val();
var reset_button = $('.reset');
var upload_button = $(".upload");
var capture_button = $(".capture");
var document_no = 0;
var capture_face_step = $("#step1-completed");
var aadhaar_step = $("#step2-completed");
var personal_information_step = $("#step5-completed");
var personal_information_form = $("#id_form_div");
var camera_started = false;

// Intializing variables
if(eipv_face_capture){
    eipv_face_capture = true;
}else{
    eipv_face_capture = false;
}
if (eipv_idcard){
    eipv_idcard = true;
}else{
    eipv_idcard = false;
}
if (personal_info != 0) {
    personal_information = true;
}else{
    personal_information = false;
}

// intializing camera
Webcam.set({
	width: 420,
	height: 330,
    dest_width: 640,
    dest_height: 480,
	image_format: 'jpeg',
	jpeg_quality: 90
});

// error handling
Webcam.on( 'error', function(err) {
	// an error occurred (see 'err')
    var r = confirm("Unable to start camera...Check Your browser permission to start camera.\nNote: This will not Support in Safari browser. Please use Mozilla Firefox or Chrome browser");
    if (r == true){
        reset_to_start();
    }else{
        reset_to_start();
    }
});

$( document ).ready(function() {
    if(eipv_idcard) {
        aadhaar_step.removeClass('hide');
    }
    if (eipv_face_capture) {
        capture_face_step.removeClass('hide');
    }
    if(personal_information){
        personal_information_step.removeClass('hide');
    }
    $('.stepactive1').addClass('disabled');
});

// starting the camera
function start_camera(){
    var tag_attr = ['.camera-screen', '#id_record_started'];
    for (var i = 0; i < tag_attr.length; i++) {
        $(tag_attr[i]).removeClass('hide');
    }
    $(".start-camera").addClass('hide');
    // $("#id_eipv_points").addClass('hide');
    $(".show-content").removeClass('hide');
    Webcam.attach( '#my_camera' );
    $(".stepactive1")
        .addClass('active')
        .removeClass('disabled');
    enable_eipv_submit('1');
    $('#my_camera').addClass('my-camera-eipv');
    camera_started = true;
    $("#id_card_step").removeClass('hide');
    update_steps_icons();
}

// Taking the snapshot picture
function capture_image(id) {
    var tag_attr = ['.reset', '.upload', id];
    for (var i = 0; i < tag_attr.length; i++) {
        $(tag_attr[i]).removeClass('hide');
        if(id == tag_attr[i]){
            $('#'+tag_attr[i]).addClass('hide');
        }
    }
    Webcam.freeze();
}

// submitting the image
upload_button.click(function() {
    // snap image data in data_uri
    Webcam.snap( function(data_uri) {
        image = data_uri;
    });
    upload_eipv_documents();
});

// reset the camera
reset_button.click(function() {
    // player.recorder.retrySnapshot();
    Webcam.unfreeze();
    var tag_attr = ['.reset', '.upload'];
    for (var i = 0; i < tag_attr.length; i++) {
        $(tag_attr[i]).addClass('hide');
    }
    $('.capture').removeClass('hide');
});

// stop the camera
function stop_camera(){
    // player.recorder.stopDevice();
    Webcam.off();
}

// Uploads the eipv documents
function upload_eipv_documents(){
    var document_type = $("#capture_button").attr('picture-type');
    var captured_image = image;
    upload_button.button('loading');
    $.ajax({
        type: 'POST',
        url: '/signup/upload_eipv_documents/',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token );
        },
        data: {
            document_type : document_type,
            image : captured_image
        },
        success: function (response) {
            if (response.result == 'success') {
                if (document_type == 'eipv_face_capture'){
                    $(".header-profile-pic").html(
                        '<img src="' + captured_image + '" class="img-responsive n-user-img header-profile" alt="">'
                    )
                }
                change_document_status(document_type, response.document_url);
            }
        },
        error: function (response) {
            alert('unable to upload');
        }
    });
}

// changes the document status
function change_document_status(document_type, download_link) {
    var attached_link = "<span class='child_eipv_span n-padding-r-5 n-span-pink-color'>Attached&nbsp; <a class='n-padding-r-5 preview_image' onclick=preview_image('"+download_link+"'); data-toggle='tooltip' data-placement='bottom' title='Preivew image'><i class='fa fa-eye' aria-hidden='true'></i></a><a class='' onclick=re_upload_document('"+document_type+"'); data-toggle='tooltip' data-placement='bottom' title='Reset/Re upload'><i class='glyphicon glyphicon-repeat download_link_color' aria-hidden='true'></i></a></span>";
    if(document_type == 'eipv_face_capture'){
        eipv_face_capture = true;
        capture_face_step.parent().append(attached_link);
        reset_button.click();
        $("#id_card_step").click();
    }
    if(document_type == 'eipv_idcard'){
        eipv_idcard = true;
        aadhaar_step.parent().append(attached_link);
        reset_button.click();
        $("#personal_step").click();
    }
    enable_eipv_submit();
}

// Function makes appear the capture button
function change_capture_button(document_type) {
    upload_button.button('reset');
    if (document_type == 'eipv_idcard') {
        capture_button.html('Capture ID Card');
        capture_button.attr('picture-type','eipv_idcard');
    }
    if (document_type == 'eipv_face_capture') {
        capture_button.html('Capture Face');
        capture_button.attr('picture-type','eipv_face_capture');
    }
}

// reset button to reupload the document
function re_upload_document(document_type){
    if(document_type == 'eipv_face_capture'){
        eipv_face_capture = false;
        capture_face_step.parent().find('.child_eipv_span').remove();
        reset_button.click();
    }
    if(document_type == 'eipv_idcard'){
        eipv_idcard = false;
        aadhaar_step.parent().find('.child_eipv_span').remove();
        reset_button.click();
        $("#capture_div").removeClass('hide');
    }
    enable_eipv_submit();
}

// Enables eipv submit
function enable_eipv_submit(active_step) {
    var step_no;
    if(active_step){
        step_no = active_step;
    }else{
        step_no = $.trim($(".active").find('.round-tab').attr('step-no'));
    }
    if (step_no == "1" && !$('.stepactive1').hasClass('disabled')) {
        $("#my_camera")
            .show()
            .parent().addClass('abotmi-eIPV-camera-section');
        if (eipv_face_capture){
            $('#id_eipv_submit_button').removeClass('hide');
            reset_button.addClass('hide');
            capture_button.addClass('hide');
            upload_button.addClass('hide');
            $("#id_card_step").show();
        }else{
            change_capture_button('eipv_face_capture');
            capture_button.removeClass('hide');
            $("#id_card_step").hide();
            $(".stepactive2").addClass('disabled');
        }
    }
    if (step_no == "2" && !$('.stepactive2').hasClass('disabled')){
        $("#my_camera")
            .show()
            .parent().addClass('abotmi-eIPV-camera-section');
        if (eipv_idcard){
            $('#id_eipv_submit_button').removeClass('hide');
            reset_button.addClass('hide');
            capture_button.addClass('hide');
            upload_button.addClass('hide');
            $("#personal_step").show();
        }else{
            change_capture_button('eipv_idcard');
            capture_button.removeClass('hide');
            $("#personal_step").hide();
            $(".stepactive3").addClass('disabled');
        }
    }
    if (step_no == "3" && !$('.stepactive3').hasClass('disabled')) {
        $("#my_camera")
            .hide()
            .parent().removeClass('abotmi-eIPV-camera-section');
        $(".capture").addClass('hide');
    }
    update_steps_icons();
}

// preview image pop up 
function preview_image(url){
    $("#image_show_body").html('');
    $("#image_show_body").html("<img src='"+url+"' class='img-responsive'></img>");
    $("#show_image_model").modal('show');
}

// reset permission to start the camera
function reset_to_start(){
    var tag_attr = ['.camera-screen', '#id_record_started'];
    for (var i = 0; i < tag_attr.length; i++) {
        $(tag_attr[i]).addClass('hide');
    }
    $(".start-camera").removeClass('hide');
    $("#id_eipv_points").removeClass('hide');
    capture_button.addClass('hide');
    $("#myImage").removeClass('hide');
    reset_button.addClass('hide');
    upload_button.addClass('hide');
    $('.my-camera-eipv').removeClass('my-camera-eipv');
}

// Showing file uploader 
$("#id_upload_card").on('click', function(e){
    $("#file_upload_idcard").click();
});

// uploading the id card document
$("#file_upload_idcard").change(function(e){
    var upload_res = upload_document('upload_id_card_form');
    upload_res.success(function(response){
        document_type = $("#capture_button").attr('picture-type');
        aadhaar_step.parent().find('.child_eipv_span').remove();
        reset_button.click();
        change_document_status(document_type, response.url);
        $("#id_capture_card").prop('checked', true);
        $("#capture_div").addClass('hide');
    });
    upload_res.error(function(response){
        $("#id_capture_card").prop('checked', true);
        alert('Unable to upload the ID Card \n Please try again after some time');
    });
});

// onclick of icons show/hide the capture button
$('.round-tab').on('click', function (e) {
    enable_eipv_submit($.trim($(this).attr('step-no')));
});

// Adding on click to dynamic right icon to navigate to the step
$(document).on('click', '.fa-check', function(){
    var attr_vl = $(this).attr('step-i-no');
    $("span[step-no="+attr_vl+"]").closest('a').click();
});

// Changes the steps icons
function update_steps_icons(){
    if (eipv_face_capture && camera_started) {
        $(".stepactive1")
            .find('span')
            .html('<i class="fa fa-check" aria-hidden="true" step-i-no="1"></i>')
            .addClass('completed');
    }else{
        $(".stepactive1")
            .find('span')
            .html('1')
            .removeClass('completed');
    }
    if (eipv_idcard && camera_started) {
        $(".stepactive2")
            .find('span')
            .html('<i class="fa fa-check" aria-hidden="true" step-i-no="2"></i>')
            .addClass('completed');
    }else{
        $(".stepactive2")
            .find('span')
            .html('2')
            .removeClass('completed');
    }
}