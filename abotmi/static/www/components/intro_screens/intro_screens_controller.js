angular.module('intro_controller',[])
.controller('IntroCtrl',function($scope,$state,$stateParams,$ionicSlideBoxDelegate){
    var introCtrl = this;
    introCtrl.slide_index = 0;
    introCtrl.skip_continue = function(){
        $state.go('login',{'socialapp':$stateParams.socialapp});
    }
    introCtrl.slideNext= function(){
        $ionicSlideBoxDelegate.next();
        introCtrl.slide_index = $ionicSlideBoxDelegate.currentIndex();
    }
    introCtrl.slideHasChanged= function(){
        introCtrl.slide_index = $ionicSlideBoxDelegate.currentIndex();
    }
});