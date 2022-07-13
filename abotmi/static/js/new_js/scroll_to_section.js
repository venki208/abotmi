(function () {
    var delay = false;
    var down = false;
    $(document).on('mousewheel DOMMouseScroll', function (event) {
        if ($(".upwardz-modal.in").length == 0){
            event.preventDefault();
            if (delay) return;

            delay = true;
            setTimeout(function () { delay = false; }, 200);

            var wd = event.originalEvent.wheelDelta || -event.originalEvent.detail;

            var a = document.getElementsByTagName('section');
            if (wd < 0) {
                down = true;
                for (var i = 0; i < a.length; i++) {
                    var t = a[i].getClientRects()[0].top;
                    if (t >= 40) break;
                }
            }
            else {
                down = false;
                for (var i = a.length - 1; i >= 0; i--) {
                    var t = a[i].getClientRects()[0].top;
                    if (t < -20) break;
                }
            }

            if (i >= 0 && i < a.length) {
                if(down){
                    $('html,body').animate({
                        scrollTop: a[i].offsetTop
                    });
                }else{
                    if ($(a[i]).hasClass('third') || $(a[i]).hasClass('second')){
                        top_px = 150;
                    }else{
                        top_px = 110;
                    }
                    $('html,body').animate({
                        scrollTop: $(a[i]).offset().top - top_px
                    }, 'fast');
                }
            }
        }
    });
})();
