angular.module('signup_login_controllers',[])

.controller('RedirectCtrl',function(result,$state,$stateParams,$localStorage){
    
    if(result.data == "Registered"){
			$state.go('app.editprofile');
    }
    else if(result.data == "Confirmed"){
      $state.go('app.myhub');
    }
		if(result.status == 401){
      if(localStorage.getItem('old_user')!='True'){
          localStorage.setItem('old_user','True');
          $state.go('introduction',{'socialapp':$stateParams.socialapp});
      }else{
          $state.go('login',{'socialapp':$stateParams.socialapp});
      }
    }
		if(result.data == "Not Registered"){
      $state.go('start.eipv')
		}
}, function(error){
	$state.go('login',{'socialapp':$stateParams.socialapp});
})

.controller('SignupLoginCtrl', function($scope,$localStorage,$state,$timeout,
  $ionicSideMenuDelegate,SweetAlert,$ionicLoading,$stateParams,SignupLoginFactory){
  var login = this;
  login.showpage = false;
  login.show_question=false;
  login.passwordvalue=false;
  $scope.forms = {};

  login.init = function(){
    login.socialapp = $stateParams.socialapp;
    login.loginaccordion = true;
  };

  login.init();

  
  login.socialsignup = function(type){
      window.location.href = "socialsignupurl://"+type+"/";
      // var isregistered = SignupLoginFactory.social_facebook();
      //      isregistered.then(function(response){
      //        console.log(response);
      //        //{email : "su14@blackbird.ws" , first_name : "first",last_name : "first",source : "facebook",gender : "",birthday:"",next_url:""}
      //        $state.go('start.email-otp',{ 'emailid': "phanisai5b0@gmail.com",'first_name':"first_name",'password':"null",'last_name':"lastName",'source':"facebook",'gender':"",'next_url':"",birthday:""}); 

      //     })

  };
 login.password_details = function(){
   swal("Should contain at-least one uppercase, one lowercase alphabet, one numeric digits. Should contain at-least one special characters, such as @, #, $. Should not contain a blank space")
 };
 login.showPassword = false;
 login.showPassword1 = false;
  login.toggleShowPassword = function() {
    login.showPassword = !login.showPassword;
  }
  login.toggleShowPassword1 = function() {
    login.showPassword1 = !login.showPassword1;
  }
  login.toggle_accordion = function(type){
    
    if(type == 'signup'){
      login.signupaccordion = true;
      login.forgotpwdaccordion = false;
      login.loginaccordion = false;
      login.signup = {};
    }
    else{
      login.forgotpwdaccordion = true;
      login.signupaccordion = false;
      login.loginaccordion = false;
      login.forgot_pwd_user = "";
    }
  };

  login.closeform = function(type){
    if(type == 'signup'){
      login.signupaccordion = false;
      login.loginaccordion = true;
      login.log = {};
    }
    else{
      login.forgotpwdaccordion = false;
      login.loginaccordion = true;
      login.log = {};
    }
  };

  login.show_details = function()
  {
    var password_data = document.getElementById("create_password").value;
    if(password_data){
      login.show_question=true;
      var expr = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$/;
      if (!expr.test(password_data)) {
       login.passwordvalue=true
      }
      else{
       login.passwordvalue=false
      }
    }
    else{
      login.show_question=false;
      login.passwordvalue=false
    }

    if(password_data){
    
    }
    else{
      
    }
  }
  login.loginsubmit = function (){
    if (login.log.username && login.log.username) {
      $ionicLoading.show({
        content: 'Loading',
        animation: 'fade-in',
        showBackdrop: true,
        maxWidth: 200,
        showDelay: 0
      });
    SignupLoginFactory.login(login.log).then(
      function(response){
        $timeout(function () {
          $ionicLoading.hide();
         }, 1000);
         if(response.data){
           if(localStorage.getItem('jwttoken'))
                 localStorage.removeItem('jwttoken');
           localStorage.setItem('jwttoken',response.data.token);
           var isregistered = SignupLoginFactory.is_reg_user();
           isregistered.then(function(response){
            if(response.data.kyc_step1 == "completed" && response.data.kyc_step2== "completed" && response.data.kyc_step3== "completed" && response.data.kyc_step4== "completed" && response.data.kyc_step5== "completed"){
              $state.go('app.myhub') ;
            }
            else if(response.data.kyc_step1 != "completed")
            {
              
              $state.go('start.eipv');
            }
            else if(response.data.kyc_step2 != "completed")
            {
            
              $state.go('app.eipv_verification');
            }
            else if(response.data.kyc_step3 != "completed")
            {
              $state.go('app.editprofile');
            }
            else if(response.data.kyc_step4 != "completed")
            {
              $state.go('app.editprofilebasic');
            }
            else if(response.data.kyc_step5 != "completed")
            {
              $state.go('app.education');
            }
        //      if(response.data == "Registered"){
				// login.showpage = login.showpage == true ? false : false;
        //        $state.go('app.eKYC');
        //     }
        //     else if (response.data =="Confirmed")
        //     {
        //       $state.go('app.myhub') ;
        //     }
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
  }

  login.forgotpassword = function(){
    if (login.forgot_pwd_user) {
    if(localStorage.getItem('jwttoken'))
         localStorage.removeItem('jwttoken');
    var promise = SignupLoginFactory.forgotpassword(login.forgot_pwd_user);
    promise.then(function(res){
      swal("Success","We have sent you an email with instructions on how to reset your password, please check your email.","success");
      login.closeform('pwd');
      login.log={};

    },function(error){
        swal("Forgot Password","User does not exists");
        $scope.forms.forgotpwd.$setPristine();
        $scope.forms.forgotpwd.$setUntouched();
        login.forgot_pwd_user ='';
    });
    }
  }
  login.direct_signup_status = false;
  login.signupsubmit = function(){
    if (login.signup.name || login.signup.email || login.signup.createpassword || login.signup.lastname) {
        login.direct_signup_status = true;
     SignupLoginFactory.check_email(login.signup).then(
      
      function(res){
        login.direct_signup_status = false;
        if(res.status == 204) {
            swal("Success","Please check your email id to enter to OTP code.","success");
            SignupLoginFactory.signup_otp_email(login.signup).then(
              function(res){
                if(res.status == 200) {
                  $state.go('email-otp',{ 'emailid': login.signup.email ,'first_name':login.signup.name,'password':login.signup.createpassword,'last_name':login.signup.lastname}); 
                }else if(res.status != 201){
                    swal("OTP","Please Try Again");
                }else{
                    swal("Try Again");
                }
              },function(error){
            swal("Check Network","Try Again");
          })
              
        }else if(res.status == 200){
            swal("Sign Up","Email already exists");
            login.closeform('signup');
        }else{
            swal("Try Again");
        }
      },function(error){
     swal("Check Network","Try Again");
   }) 

 }

  };
});
