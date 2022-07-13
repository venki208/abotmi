(function () {
    'use strict'
    if (navigator.userAgent.match(/IEMobile\/10\.0/)) {
        var msViewportStyle = document.createElement('style')
        msViewportStyle.appendChild(
            document.createTextNode(
                '@-ms-viewport{width:auto!important}'
            )
        )
        document.head.appendChild(msViewportStyle)
    }
}())

// How it works animation
var how_it_works_anim = lottie.loadAnimation({
    container: document.getElementById('how_it_w_anim'),
    renderer: 'svg',
    loop: false,
    autoplay: false,
    path: '/static/V2_theme/animations/how_it_works/data.json'
});

// Loading animation once it reached to view point
var waypoint = new Waypoint.Inview({
    element: document.getElementById('how_it_works_section'),
    enter: function () {
        how_it_works_anim.play();
    },
    exited: function (direction) {
        how_it_works_anim.stop()
    }
})

$('body').on('click', '#learnMore', function () {
    location.href = '/advisor_page/';
    return false;
});
$('body').on('click', '#buildMore', function () {
    location.href = '/advisor_page/';
    return false;
});
$('body').on('click', '#earnMore', function () {
    location.href = '/advisor_page/';
    return false;
});