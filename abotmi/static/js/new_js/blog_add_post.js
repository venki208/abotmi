var selected_chip_ids = "";
var text_category = "";

// on cliking out side of dropdown div hiding dropdown
$(document).mouseup(function (e) {
    var container = $(".total-category");
    value = $('#category').val();
    var value2 = $('#id_item_name' + value).html();
    if (value2 == undefined)
        $('#category').val('');
    if (!container.is(e.target)
        && container.has(e.target).length === 0) {
        $('.search-dropdown').css('display', 'none');
    }
});

// adding chips to the Category div
function add_category_to_input(id, category_div) {
    var value = $('#id_item_name' + id).html();
    $('#' + id).addClass('chip-active');
    var n = selected_chip_ids.search(value);
    if (n == -1)
        $('#' + category_div).append("<a class='chip' id='" + id + "' style='display:inline-block;'>" + value + "<span class='closebtn' onclick='remove_chip(" + id + ");'>&times;</span></a>");
    selected_chip_ids = selected_chip_emails();
    $('#id_total_category_selected').val(selected_chip_ids);
    $('#id_search').val('');
    $('#search-dropdown').css('display', 'block');
    // searching the dropdown
    $('.item').each(function () {
        ids = $(this).attr('id');
        $('#' + ids).removeClass('search-output');
    });
}

// Fetching Selected Chip ids
function selected_chip_emails() {
    var selected_chip_ids = $(".chip-active").map(function () {
        ids = $(this).attr('id');
        name = $(this).attr('name');
        return name;
    }).get().join(',');
    return selected_chip_ids;
}

// remove Chips and showing that block in dropdown
function remove_chip(id) {
    $('#' + id).remove();
    $('#' + id).removeClass('chip-active');
    var selected_chip_ids = selected_chip_emails();
    $('#id_total_category_selected').val(selected_chip_ids);
}

// incresing and decresing the width of textbox
$(".search").on("keyup", function () {
    // searching the dropdown
    $('.search-dropdown').css('display', 'block');
    $('.item').each(function () {
        ids = $(this).attr('data-value');
        if (ids.indexOf($('#category').val()) > -1) {
            ids = $(this).attr('id');
            $('#' + ids).removeClass('search-output');
        } else {
            ids = $(this).attr('id');
            $('#' + ids).addClass('search-output');
        }
    });
});

// Intializing the tinymce editor
tinymce.init({
    selector: '#content_raw',
    height: 500,
    menubar: false,
    plugins: [
        'advlist autolink lists link image charmap print preview anchor textcolor',
        'searchreplace visualblocks code fullscreen',
        'insertdatetime table contextmenu paste code help wordcount'
    ],
    toolbar: 'insert | undo redo |  formatselect | bold italic backcolor  | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | help',
});

// Adding change event to upload button
document.getElementById('up').addEventListener('change', handleFileSelect, false);

// enable the upload image button
function handleFileSelect(e) {
    var files = e.target.files;
    for (var i = 0, f; f = files[i]; i++) {
        var reader = new FileReader();
        reader.onload = (function (theFile) {
            return function (e) {
                $("#binary_document").val(e.target.result);
                $("#upload_image").attr("disabled", false);
            };
        })(f);
        reader.readAsDataURL(f);
    }
}

// Uploading image and appending the image url to tinymce editor
var blog_post_image_arr = [];
function upload_image_ajax() {
    var form_data = new FormData($('#add_media_form')[0]);
    var tinyMCE_image_arr = [];
    $.ajax({
        url: "/blog/icore/add_media/",
        method: "POST",
        data: form_data,
        cache: false,
        processData: false,
        contentType: false,
        success: function (response) {
            var res = response.split("::");
            tinymce.get("content_raw").execCommand(
                'mceInsertContent',
                false,
                '<img src="' + res[1] + '" width="300" height="300"/><br>'
            );
            $(tinyMCE.activeEditor.dom.getRoot()).find('img').each(
                function () {
                    tinyMCE_image_arr.push($(this).attr("src"));
                });
            blog_post_image_arr.push({
                key: res[0],
                value: res[1]
            });
            $('#MediaModel').modal('hide');
            for (var i = 0; i < blog_post_image_arr.length; i++) {
                if (tinyMCE_image_arr[0] == blog_post_image_arr[i].value) {
                    document.getElementById('featured_image').value = blog_post_image_arr[i].key;
                }
            }
        },
    });
}

// The funciton is for onclick of category checkbox, add the value in add category field.
function onClickCategory(id) {
    var all_category = document.getElementById('add_category').value;
    var value;
    if (all_category.indexOf(id + ",") > -1)
        value = id + ",";
    else if (all_category.indexOf("," + id) > -1)
        value = "," + id;
    else if (all_category.indexOf(id) > -1)
        value = id;

    if (document.getElementById(id).checked == true) {
        if (text_category == "")
            text_category = id;
        else
            text_category = text_category + "," + id;
    }
    else if (document.getElementById(id).checked == false)
        text_category = all_category.replace(value, "");
    document.getElementById('add_category').value = text_category;
}

// trimming the input catogery content
function triming(id) {
    var group = document.getElementById(id).value;
    var array = group.split(",");
    var i;
    var value = "";
    for (i = 0; i < array.length; i++) {
        if (!array[i] == "" || !array[i] == " ") {
            var ar_value = array[i].replace(/ /, '');
            value = value + ar_value + ",";
        }
    }
    value = value.substring(0, value.length - 1);
    document.getElementById(id).value = value;
}

// submitting the Blog post
function submitPost() {
    if ($("#title").val() == "") {
        alert("Enter the title");
        return false;
    }
    var post = tinyMCE.get('content_raw').getContent();
    if (post == '') {
        alert("Write on the content box");
        return false;
    }
    $("#icore_add_post").submit();
}