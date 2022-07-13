// Showing alert onclick of browser back button
history.pushState(null, document.title, location.href);
window.addEventListener('popstate', function (event) {
    var l_url = location.href;
    if (!l_url.endsWith('#step1') && !l_url.endsWith('#step2') && !l_url.endsWith('#step3') && !l_url.endsWith('#')){
        alert('You cannot go back');
        history.pushState(null, document.title, location.href);
    }
});

$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});