angular.module('video_controller',[]) 
.controller('videoCtrl',function($state,$ionicScrollDelegate,$location,deviceDetector){
	var video_Ctrl = this;
	video_Ctrl.data = deviceDetector;
	if(video_Ctrl.data.os=="ios"){
		video_Ctrl.vid = "/static/video/video1ios.mp4";
	}
	else{
		video_Ctrl.vid = "/static/video/video1.webm";
	}
    video_Ctrl.allData = JSON.stringify(video_Ctrl.data, null, 2);
    video_Ctrl.scrollTo = scrollTo;
    	function scrollTo(target){
       	 	$location.hash(target);
        	var handle = $ionicScrollDelegate.$getByHandle('myPageDelegate');
        	handle.anchorScroll(true);
    	}

	video_Ctrl.register = function(){
		$state.go("start.eipv");
	};

	video_Ctrl.expand1 = function (){
		$('.showMe1').slideToggle('slow');
	};

	video_Ctrl.expand2 = function (){
		$('.showMe2').slideToggle('slow');
	};

	var videoPlayer1 = document.getElementById("myVideo1");
	//var videoPlayer2 = document.getElementById("myVideo2");
	// videoPlayer2.onplay = function() {
	// 	videoPlayer1.pause();
	// };
	videoPlayer1.onplay = function() {
		//videoPlayer2.pause();
	};

  var play_next1 = $("#my_Video1");
	$('#end1').hide();
	$('#my_Video1').hide();

  var play_next2 = $("#my_Video2");
	$('#end2').hide();
	$('#my_Video2').hide();

	videoPlayer1.addEventListener('ended',myHandler1,false);
	function myHandler1(e1) {
		if(!e1) {
			e1= window.event;
		}
		$('#end1').show();
		$('#my_Video1').show();
		document.getElementById("register").disabled = false;
	}

	play_next1.on('click', function(e1){
		$('#my_Video1').hide();
		
		if(video_Ctrl.data.os=="ios"){
			var nextVideo = "/static/video/video1ios.mp4";
		}
		else{
			var nextVideo = "/static/video/video1.webm";
		}
        videoPlayer2.src = nextVideo;
        videoPlayer2.play();
    });

	// videoPlayer2.addEventListener('ended',myHandler2,false);
	// function myHandler2(e2) {
	// 	if(!e2) {
	// 		e2= window.event;
	// 	}
	// 	$('#end2').show();
	// 	document.getElementById("register").disabled = false;
	// }
})
