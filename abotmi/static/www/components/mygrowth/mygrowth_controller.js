angular.module('mygrowth_controller',[]) 
.filter('trusted', ['$sce', function ($sce) {
    return function(url) {
        return $sce.trustAsResourceUrl(url);
    };
}])
.controller('mygrowthCtrl',function(mygrowth_factory,$location, $sce, $ionicLoading,$ionicScrollDelegate){
    var mygrowth = this;
    var playing_iframe = [];
    var current_playing_iframe = null;
    var player_arr = [];
    var player = "";
    var scroll_position = 0;
    mygrowth.step=0;
    mygrowth.class="btn1 active";
    mygrowth.class1="btn1";
    
    var is_other_video_present,current_video_present, last_current_video_id, last_other_video_id;
    mygrowth.play_next_video = play_next_video;
    mygrowth.toastmsg = toastmsg;
    mygrowth.knowmore = function (description,id){
      pause_paying_videos(id);
      swal(description);
    };
   
    
    mygrowth.expand1 = function (){
        stop_paying_videos()
        $('#intro_video').hide();
        $('#micro_learning').show();
        $('#gaming').show();
        set_youtube_player();
    };
    mygrowth.expand2 = function (){
        stop_paying_videos()
        $('#intro_video').show();
        $('#gaming').show();
        $('#micro_learning').hide();
        set_youtube_player();
    };
    mygrowth.expand3 = function (){
        stop_paying_videos()
        $('#intro_video').show();
        $('#micro_learning').show();
        $('#gaming').hide();
        set_youtube_player();
  };
  mygrowth.expand4 = function (){
    stop_paying_videos()
    $('#intro_video').show();
    $('#micro_learning').show();
    $('#gaming').show();
    set_youtube_player();
};
mygrowth.expand5 = function (){
  stop_paying_videos()
  $('#intro_video').show();
  $('#micro_learning').show();
  $('#gaming').show();
  set_youtube_player();
};
  mygrowth.init = function(){
    mygrowth.webinarevents();
  }
  mygrowth.micro_learning = function(){
    
    mygrowth.step=1;
    if (mygrowth.class === "btn1 active")
    {
      mygrowth.class = "btn1";
      mygrowth.class1="btn1 active"
    }
    
    
  
    

  }
  mygrowth.certification = function(){
    
    mygrowth.step=0;
    if (mygrowth.class1 === "btn1 active")
    {
      mygrowth.class1 = "btn1";
      mygrowth.class="btn1 active"
    }
  }

  mygrowth.webinarevents = function() {
    get_webinar_list_from_factory();
  }

  function get_webinar_list_from_factory(){
      var webinar_viewpromise = mygrowth_factory.get_advisor_list();
      webinar_viewpromise.then(function(response) {
          mygrowth.details = response.data;
          mygrowth.details.total_icore_posts=response.data.total_icore_posts;
          mygrowth.details.topTrending=response.data.top_trending
          console.log(mygrowth.details.topTrending)
          is_other_video_present = response.data.is_other_advisors_videos_present;
          current_video_present = response.data.is_current_advisor_videos_present;
          last_other_video_id = response.data.last_other_video_id;
          last_current_video_id = response.data.last_current_advisor_video_id;
          if(response.data.is_current_advisor_videos_present)
            mygrowth.current_first_video = $sce.trustAsResourceUrl(mygrowth.details.current_advisor_videos[0]['video_link']);
          if(response.data.is_other_advisors_videos_present)
            mygrowth.other_first_video = $sce.trustAsResourceUrl(mygrowth.details.other_advisors_videos[0]['video_link']);
      }, function(error) {
          swal("Failed try again", JSON.stringify(error.data));
      });
  }

  mygrowth.init();

  function set_youtube_player(){
    var el = angular.element(document.querySelectorAll('.iframe_class'));
    var link_id = "";
    for(var i=0; i<el.length; i++){
      link_id = el[i].attributes['link'].value.split("embed/")[1]
      onYouTubeIframeAPIReady(el[i].id,link_id);
    }
  }

  function onYouTubeIframeAPIReady(id, link_id) {
    var is_present = false;
    if(player_arr.length > 0){
      for(var i=0; i<player_arr.length; i++){
        if(player_arr[i].id == id){
          is_present = true;
          break;
        }
      }
    }
    if(!is_present){
      player = new YT.Player(id, {
          videoId: link_id,
          events: {
            'onStateChange': function(event){
              if(event.data === YT.PlayerState.PLAYING){
                $.each(player_arr, function(k,v) {
                  if (this.getIframe().id != event.target.getIframe().id) {
                    if (typeof this.stopVideo == 'function')
                      this.stopVideo();
                  }
                })
              }

              if(playing_iframe.indexOf(event.target.a.id) === -1)
                playing_iframe.push(event.target.a.id);

              if(event.data === 0){
                var lastIndex = event.target.a.id.lastIndexOf('_');
                var current_next_btn= event.target.a.id.substr(lastIndex+1);
                if(is_other_video_present){
                  if(last_other_video_id != current_next_btn){
                    $('#play_next_'+current_next_btn).removeClass('display_none');
                  }
                }
                if(current_video_present){
                  if(last_current_video_id != current_next_btn){
                    $('#play_next_current_'+current_next_btn).removeClass('display_none');
                  }
                }
              }
            }
          },
          playerVars: {rel: 0},
        });
        player_arr.push(player);
    }
  }

  function stop_paying_videos(){
    for(var i=0; i<player_arr.length; i++){
      if (typeof player_arr[i].stopVideo == 'function') {
        player_arr[i].stopVideo();
      }
    }
  }

  function pause_paying_videos(id){
    if(player_arr.length > 0){
      for(var i=0; i<player_arr.length; i++){
        if(player_arr[i].a.id == id){
          if (typeof player_arr[i].pauseVideo == 'function') {
            player_arr[i].pauseVideo();
            break;
          }
        }
      }
    }
  }

  function play_next_video(element,id,scroll){
    var res = scroll.split("_");
    var next_div = parseInt(res[1]);
    next_div=next_div+1;
    var scroll_final=String(res[0]+"_"+next_div);
    $location.hash(scroll_final);
    var handle = $ionicScrollDelegate.$getByHandle('myPageDelegate');
    handle.anchorScroll(true);
    $("#"+element.target.id).addClass('display_none');
    var total_video_ids = mygrowth.details.total_video_ids;
    var lastIndex = element.target.id.lastIndexOf('_');
    var current_next_btn= element.target.id.substr(lastIndex+1);
    var index_current_video_id = total_video_ids.indexOf(parseInt(current_next_btn));
    var index_next_video_id = index_current_video_id + 1;
    if(index_next_video_id < total_video_ids.length){
      if(player_arr.length > 0){
        for(var i=0; i<player_arr.length; i++){
            if(player_arr[i].a.id == "advisors_videos_"+total_video_ids[index_next_video_id]){
              player_arr[i].playVideo();
              break;
            }
        }
      }
    }
  }

  function toastmsg(){
      $ionicLoading.show({
          template: 'Coming soon...',
          noBackdrop: true,
          duration: 1500
      });
  }
})
