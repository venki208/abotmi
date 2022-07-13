angular.module('reiaapp.directives',[])

.directive('validFile',function(){
  return {
    require:'ngModel',
    link:function(scope,el,attrs,ngModel){
      //change event is fired when file is selected
      el.bind('change',function(){
        scope.$apply(function(){
          ngModel.$setViewValue(el.val());
          ngModel.$render();
        });
      });
    }
  }
})

.directive('fileChange', function() {
   return {
    require :'ngModel',
    scope : {
        ngModel : '='
    },
    restrict: 'A',
    link: function(scope, el, attrs) {
      if (!attrs.fileChange) {
        return;
      }

      el.on('change', function(e) {
            scope.ngModel = e.target.files[0];
			//Allow only png,jpg,jpeg files
            if(scope.ngModel.name.split(".").pop() == "png" || scope.ngModel.name.split(".").pop() == "jpg" ||
             scope.ngModel.name.split(".").pop() == "jpeg"){
				     var reader = new FileReader();
					   reader.onload = function (e) {
					         // bind new Image to Component
					         scope.$apply(function () {
						       scope.ngModel = e.target.result;
					   });
					}

				reader.readAsDataURL(scope.ngModel);
				scope.$apply(function() {
					scope.$eval(attrs.fileChange, {
					$event: e
					});
				});
			 } else {
				 swal("Error","Only png,jpg,jpeg files are accepted","error");
				 el.val(null);
			 }
        });
      }
    }
})


.directive('selectDate', ['ionicDatePicker',function(ionicDatePicker) {
    return {
        require:'ngModel',
        scope :{
          ngModel : '='
        },
        link: function(scope, element) {
            element.on('click', function() {
                scope.old_date = scope.ngModel;
                if(!scope.old_date){
                    scope.old_date=new Date()
                }
                scope.date = {
                  callback : function(val){
                    scope.ngModel = moment(new Date(val)).format('YYYY-MM-DD');
                  },
                inputDate:new Date(scope.old_date),
                from: new Date(),
                to: new Date(2030, 12, 31),
                };
                ionicDatePicker.openDatePicker(scope.date);
            });
        }
    }
}])

.directive('selectBirthDate', ['ionicDatePicker',function(ionicDatePicker) {
    return {
        require:'ngModel',
        scope :{
          ngModel : '='
        },
        link: function(scope, element) {
            element.on('click', function() {
                scope.old_date = scope.ngModel;
                var today = new Date();
                var fromyear = today.getFullYear() - 100;
                var toyear = today.getFullYear() - 18;
                if(!scope.old_date){
                    scope.old_date = new Date(toyear, 1, 1)
                }
                scope.date = {
                  callback : function(val){
                    scope.ngModel = moment(new Date(val)).format('YYYY-MM-DD');
                  },
                inputDate:new Date(scope.old_date),
                from: new Date(fromyear, 1, 1),
                to: new Date(toyear, 12, 31),
                };
                ionicDatePicker.openDatePicker(scope.date);
            });
        }
    }
}])

.directive('selectDatefrom', ['ionicDatePicker',function(ionicDatePicker) {
    return {
        require:'ngModel',
        scope :{
          ngModel : '='
        },
        link: function(scope, element) {
            var d = new Date();
            d.setFullYear(d.getFullYear() - 5);
            element.on('click', function() {
                scope.old_date = scope.ngModel;
                if(!scope.old_date){
                    scope.old_date=new Date()
                }
                scope.date = {
                  callback : function(val){
                    scope.ngModel = moment(new Date(val)).format('YYYY-MM-DD');
                  },
                inputDate:new Date(scope.old_date),
                from: d,
                to: new Date(),
            };
            ionicDatePicker.openDatePicker(scope.date);
            });
        }
    }
}])

.directive('back', ['$window', function($window) {
    return {
        restrict: 'A',
        link: function (scope, elem, attrs) {
            elem.bind('click', function () {
                $window.history.back();
            });
        }
    };
}])

.directive('upwrdzTabs',function(){
  return{
    templateUrl : 'templates/upwrdztabs.html'
  }
})

.directive('simpleAccordion', function () {
    return {
        restrict: 'A',
        scope: {
            toggleSpeed: '@toggleSpeed',
            slideUpSpeed: '@slideUpSpeed',
            toggleEasing: '@toggleEasing',
            slideUpEasing: '@slideUpEasing'
        },
        link: function (scope, element, attrs) {
            $(element).bind('click',(function () {
                var elem = $(this);
                elem.next().slideToggle(scope.toggleSpeed, scope.toggleEasing);
                $(".accordion-content").not($(this).next()).slideUp(scope.slideUpSpeed, scope.slideUpEasing);
            }));
        }
    }
})
