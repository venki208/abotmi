var copy_badge_btn = $("#id_cp_badge");
var edit_profile_link_btn = $("#edit_profile_link_btn");
var element = $("#html-content-holder");
var getCanvas;
// binding click functions
edit_profile_link_btn.bind('click', [], change_batch_code);
// Show bootstrap Modal function(pass id or name)
function show_bootstrap_modal(elem) {
    $(elem).modal({
        show:true,
        keyboard:false,
        backdrop:'static'
    });
}

// setting response data into common div
function load_data(response) {
    $("#my_identity_modal").html('');
    $("#my_identity_modal").html(response);
}

// Copying the code of batch card to clip board
copy_badge_btn.on('click', function(e){
    $(this).attr('disabled', true);
    $("#previewImage").removeClass('hide');
    $("#batch_img_div").removeClass('hide');
    $("#your_profile_div").addClass("hide");
    var my_canvas = document.getElementById("myCanvas");
    var canvas_context = my_canvas.getContext("2d");
    var img = document.getElementById("image_a");
    canvas_context.imageSmoothingEnabled = false;
    canvas_context.drawImage(img,0,0,80,80);
    canvas_context.beginPath();
    canvas_context.moveTo(100, 0);
    canvas_context.lineTo(100, 80);
    canvas_context.stroke();
    canvas_context.beginPath();
    canvas_context.moveTo(100, 0);
    canvas_context.lineTo(100, 80);
    canvas_context.stroke();
    canvas_context.font = "21px Source Sans Pro";
    canvas_context.fillText(full_name,70,105,70);
    canvas_context.font = "14px Source Sans Pro";
    canvas_context.fillText(advisor_city,75,118,50);
    var new_canvas_context;
    var canvas;
    var img = new Image();
    img.onload = function(){
        canvas = document.getElementById('myCanvas');
        new_canvas_context = canvas.getContext('2d');
        new_canvas_context.beginPath();
        new_canvas_context.arc(160, 40, 40, 0, 2 * Math.PI);
        new_canvas_context.clip();
        new_canvas_context.stroke();
        new_canvas_context.closePath();
        new_canvas_context.imageSmoothingEnabled = false;
        new_canvas_context.drawImage(img,120,0,80,80);
    };
    img.src = document.getElementById("image_b").src;
    $("#copy_button").removeClass('hide');
    $("#btn_convert_html2image").removeClass('hide');
    $("#id_badge_font").removeClass('hide');
    $("#batch_card_div").addClass('left-border');
    get_binary_attachment();
});


// Copying the image code
$("#copy_button").on('click', function(){
    get_binary_attachment();
    var copyText = document.getElementById("copy_code_input");
    copyText.select();
    document.execCommand("copy");
});

// downloading the batch card after loading as image
$("#btn_convert_html2image").on('click', function () {
    var c = document.getElementById("myCanvas");
    var imgageData = c.toDataURL("image/png");
    var newData = imgageData.replace(/^data:image\/png/, "data:application/octet-stream");
    $("#btn_convert_html2image").attr("download", advisor_name+'.png').attr("href", newData);
});

  
function get_binary_attachment(){
    var final_c = document.getElementById('myCanvas');
    var img_bi_data = final_c.toDataURL("image/png");
    $("#id_card_img").attr('src', img_bi_data);
    $('#copy_code_input')
        .removeClass('hide')
        .val($('.copy_img_code').html());
}