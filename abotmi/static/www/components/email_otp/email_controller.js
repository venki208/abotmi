angular.module('email_controller',[])
.controller('EmailCtrl',function($scope,EmailOtp,$stateParams,$localStorage,$state,$timeout,
    $ionicSideMenuDelegate,SweetAlert,$ionicLoading){
    var emailotpprocess = this;
    emailotpprocess.showpage = false;
    var emailid = $stateParams.emailid;
    var first_name = $stateParams.first_name;
    var last_name = $stateParams.last_name;
    var login_password = $stateParams.password;
    var login_source = $stateParams.source;
    var login_gender = $stateParams.gender;
    var login_next_url = $stateParams.next_url; 
    emailotpprocess.user_details ={};
    emailotpprocess.sendotp = function(medium){
        var data =$.param({
            email : emailid,
            name : first_name
            })
        var promise = EmailOtp.emailotp(data);
        promise.then(function(res){
            swal("Please enter the new otp recieved","","success");
        },function(error){
            swal("Server Error","Try Again Later","error");
        })
    }
    emailotpprocess.verifyotpemail = function(){
       
        var data_login_details =$.param({
            username : emailid,
            password: login_password
            })
        var data =$.param({
            email : emailid,
            email_otp:emailotpprocess.user_details.eotp
            })
        var promise = EmailOtp.verifyotpEmail(data);
        promise.then(function(res){
          if(res.email_verf_stat){
            if(login_password !="null"){
            var data_signup_status =$.param({
                first_name : first_name,
                email:emailid,
                password:login_password,
                ref_link:'',
                last_name:last_name
                })
                EmailOtp.direct_signup(data_signup_status).then(
                    function(res){
                        
                      if(res.status == 201) {
                          swal("Success","Thanks for signing up!","success");
                          if (emailid && login_password) {
                            $ionicLoading.show({
                              content: 'Loading',
                              animation: 'fade-in',
                              showBackdrop: true,
                              maxWidth: 200,
                              showDelay: 0
                            });
                          EmailOtp.login(data_login_details).then(
                            function(response){
                              $timeout(function () {
                                $ionicLoading.hide();
                               }, 1000);
                               if(response.data){
                                 if(localStorage.getItem('jwttoken'))
                                 {
                                       localStorage.removeItem('jwttoken');
                                       
                                 }
                                 localStorage.setItem('jwttoken',response.data.token);
                                 localStorage.removeItem('educational_document');
                                 var isregistered = EmailOtp.is_reg_user();
                                 isregistered.then(function(response){
                                   if(response.data == "Registered"){
                                      emailotpprocess.showpage = emailotpprocess.showpage == true ? false : false;
                                     $state.go('app.editprofile');
                                  }
                                  else if (response.data =="Confirmed")
                                  {
                                    $state.go('app.myhub') ;
                                  }
                                  else{
                                      //$state.go('start.video');
                                      $state.go('start.eipv');
                                  }
                              })
                            }
                          },
                          function(error){
                             $timeout(function () {
                               $ionicLoading.hide();
                              }, 1000);
                              if(error){
                                swal("Credential Alert","Please check your credentials", "error");
                              }
                              else{
                                swal("Alert","Please check your Internet Connection","warning");
                              }
                          })

                        }  
                      }else if(res.status != 201){
                          swal("Sign Up","Please Try Again");
                      }else{
                          swal("Try Again");
                      }
                    },function(error){
                  swal("Check Network","Try Again");
                })
            }
            else{
              var data_signup =$.param({
                  email : emailid,
                  first_name : first_name,
                  last_name : last_name,
                  source: login_source,
                  gender:login_gender,
                  next_url:login_next_url
                  })
               EmailOtp.social_signup(data_signup).then(function(res){
                  swal("Success","Thanks for Social Signup!","success");
                  if(localStorage.getItem('jwttoken'))
                           {
                                 localStorage.removeItem('jwttoken');
                                 
                           }
                      
                            localStorage.setItem('jwttoken',res.data.token);
                            localStorage.removeItem('educational_document');
                              var isregistered = EmailOtp.is_reg_user();
                              isregistered.then(function(response){
                               $timeout(function () {
                                  $ionicLoading.hide();
                                 }, 1000);
                                if(response.data == "Registered"){
                                   emailotpprocess.showpage = emailotpprocess.showpage == true ? false : false;
                                  $state.go('app.eKYC');
                               }
                               else if (response.data =="Confirmed")
                               {
                                 $state.go('app.myhub') ;
                               }
                               else{
                                   //$state.go('start.video');
                                   $state.go('start.eipv');
                               }
                           }),
                           function(error){
                              $timeout(function () {
                                $ionicLoading.hide();
                               }, 1000);
                               if(error){
                                 swal("Credential Alert","Please check your credentials", "error");
                               }
                               else{
                                 swal("Alert","Please check your Internet Connection","warning");
                               }
                           }
                          
                  },function(error){
                  swal("Server Error","Try Again Later","error");
                   })

      }  
          
            }
            else{
              swal("Alert","Wrong Otp","error");
            }
 
        },function(error){
            
            swal("Server Error","Try Again Later","error");
        })
        
    }
    
    
});