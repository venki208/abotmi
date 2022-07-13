angular.module('eipv_controller_verification',[]) 

.controller('EipvCtrl_step2',function($scope,EipvuploadFactory,$state,$ionicLoading,$timeout,$ionicSideMenuDelegate, mainServices, $interval,deviceDetector,$ionicPopup){
    var eipvprocess_step2 = this;
    
    eipvprocess_step2.devicedetection = deviceDetector;
    eipvprocess_step2.medium ='';
    eipvprocess_step2.user_details ={};
    eipvprocess_step2.outputImage = null;
    eipvprocess_step2.step = 0;
    eipvprocess_step2.verified =0;
    eipvprocess_step2.otpdata=0;
    eipvprocess_step2.enableSubmit=true;
    eipvprocess_step2.passport_isDisabled =false;
    eipvprocess_step2.driving_licence_isDisabled =false;
    eipvprocess_step2.id_card_isDisabled =false;
    eipvprocess_step2.id_card_url =[];
    eipvprocess_step2.passport =[];
    eipvprocess_step2.driving_licence =[];
    eipvprocess_step2.init = function() {
        var countrypromise =EipvuploadFactory.getcountry();
        countrypromise.then(function(data){
            eipvprocess_step2.country = data.data;
        },function(error){
            swal("Server Error","Try again later");
        });
        
        

      eipvprocess_step2.otpdata=mainServices.resetItem();
      var promise =  EipvuploadFactory.getdata();
      promise.then(function(res) {

      if(res.eipv_face_capture == true)
      {
          eipvprocess_step2.step = 2;
      }
      if(res.eipv_aadhaar_present == true)
      {
          
          eipvprocess_step2.step = 3;
         
      }
    //   if(res.eipv_pancard_present == true)
    //   {
    //       eipvprocess_step2.step = 4;
    //   }
    //   if(res.eipv_signature_present == true)
    //   {
    //       eipvprocess_step2.step = 5;
    //   }
       if(res.ipv_status == true)
       {
           eipvprocess_step2.step=4;
       }
      if(res.person_info_present==1)
      {
          $state.go("app.eKYC");
      }

      eipvprocess_step2.user_details =res;
      var get_data =EipvuploadFactory.get_verification_data();
        get_data.then(function(data_verify){
            eipvprocess_step2.passport=data_verify.passport_data
            eipvprocess_step2.driving_licence=data_verify.driving_licence
            eipvprocess_step2.id_card_url=data_verify.id_card
            eipvprocess_step2.user_details.country = data_verify.country_data
            if(!eipvprocess_step2.user_details.country){
                eipvprocess_step2.user_details.country="United States"
            }
            if(eipvprocess_step2.driving_licence.length || eipvprocess_step2.id_card_url.length || eipvprocess_step2.passport.length){
                eipvprocess_step2.enableSubmit=false;
            }
           
        },function(error){
            swal("Server Error","Try again later");
        }); 

  },function(error){
      swal("Server Error","Try Again Later","error");
  })
   }

     eipvprocess_step2.capturedata = function(image,data){
         $ionicLoading.show({
           content: 'Loading',
           animation: 'fade-in',
           showBackdrop: true,
           maxWidth: 200,
           showDelay: 0
         });
        var promise = EipvuploadFactory.postdata(image,data);
        promise.then(function(res){
            
           
           
            if(res.result=="success")
            {
            $state.go("app.eipv_verification");    
            //eipvprocess_step2.step = eipvprocess_step2.step+1;
            if(eipvprocess_step2.step==3){
                //eipvprocess_step2.submit();
                //$state.go("app.editprofile");
            }
            $timeout(function () {
             $ionicLoading.hide();
             }, 1000);
             swal("Uploaded","","success");
         }
         else{
             $ionicLoading.hide();
             swal("Upload failed","Check  internet connection and try again","error");
         }
        }
        ,function(error)
        {
            $timeout(function () {
             $ionicLoading.hide();
           }, 1000);
        swal("Server Error","Try Again Later","error");
        })

    }
    eipvprocess_step2.verifySubmit = function(){
       
        var promise = EipvuploadFactory.savecountry(eipvprocess_step2.user_details.country);
       promise.then(function(res){
        

       },function(error){
           swal("Server Error","Try Again Later","error");
        })
        $state.go("app.editprofile");

    }
    $scope.fileNameChangedPassport = function() {
        eipvprocess_step2.myValue1 = false
        eipvprocess_step2.passport_isDisabled =false;
      }
      $scope.fileNameChangedDrivingLicence = function() {
        eipvprocess_step2.myValue2 = false
        eipvprocess_step2.driving_licence_isDisabled =false;
      }
      $scope.fileNameChangedIdCard = function() {
        eipvprocess_step2.myValue3 = false
        eipvprocess_step2.id_card_isDisabled =false;
      }

      eipvprocess_step2.common_function = function(data){
        var promise = EipvuploadFactory.deletedocuments(data);
        promise.then(function(res){
        
        },function(error){
            swal("Server Error","Try Again Later","error");
         })
      }
      eipvprocess_step2.passport_delete = function(data_id,$index){
        var confirmPopup = $ionicPopup.confirm({
            title: 'Delete',
            template: 'Are you sure you want to delete this item?'
          });
       
          confirmPopup.then(function(res) {
            if(res) {
              // Code to be executed on pressing ok or positive response
              // Something like remove item from list
              eipvprocess_step2.common_function(data_id);
              eipvprocess_step2.passport.splice($index, 1); 
       eipvprocess_step2.myValue1 = true
       if(!eipvprocess_step2.driving_licence.length && !eipvprocess_step2.id_card_url.length && !eipvprocess_step2.passport.length){
        eipvprocess_step2.enableSubmit=true;
    }
            } else {
              // Code to be executed on pressing cancel or negative response
            }
          });  
       

      }
      eipvprocess_step2.id_card_delete = function(data_id,$index){
        var confirmPopup = $ionicPopup.confirm({
            title: 'Delete',
            template: 'Are you sure you want to delete this item?'
          });
       
          confirmPopup.then(function(res) {
            if(res) {
              // Code to be executed on pressing ok or positive response
              // Something like remove item from list
              eipvprocess_step2.common_function(data_id);
             // eipvprocess_step2.id_card_url.shift();
              eipvprocess_step2.id_card_url.splice($index, 1); 
              eipvprocess_step2.myValue3 = true
              if(!eipvprocess_step2.driving_licence.length && !eipvprocess_step2.id_card_url.length && !eipvprocess_step2.passport.length){
                  eipvprocess_step2.enableSubmit=true;
              }
            } else {
              // Code to be executed on pressing cancel or negative response
            }
          });  
       
 
       }
       eipvprocess_step2.driving_delete = function(data_id,$index){

        var confirmPopup = $ionicPopup.confirm({
            title: 'Delete',
            template: 'Are you sure you want to delete this item?'
          });
       
          confirmPopup.then(function(res) {
            if(res) {
              // Code to be executed on pressing ok or positive response
              // Something like remove item from list
              eipvprocess_step2.common_function(data_id);
              //eipvprocess_step2.driving_licence.shift();
              //var index2 = eipvprocess_step2.driving_licence.indexOf(data_id);
              eipvprocess_step2.driving_licence.splice($index, 1); 
              eipvprocess_step2.myValue2 = true
              if(!eipvprocess_step2.driving_licence.length && !eipvprocess_step2.id_card_url.length && !eipvprocess_step2.passport.length){
                  eipvprocess_step2.enableSubmit=true;
              }
            } else {
              // Code to be executed on pressing cancel or negative response
            }
          });  

        

 
       }
    eipvprocess_step2.capturedata_verify = function(image,data){
        $ionicLoading.show({
          content: 'Loading',
          animation: 'fade-in',
          showBackdrop: true,
          maxWidth: 200,
          showDelay: 0
        });
       var promise = EipvuploadFactory.postdata(image,data);
       promise.then(function(res){
        if(res.document_type == "id_card"){
              eipvprocess_step2.id_card_url.push({ documents: res.document_url, id: res.id });

        }
        if(res.document_type == "passport"){
            eipvprocess_step2.passport.push({ documents: res.document_url, id: res.id });
            

      }
      if(res.document_type == "driving_licence"){
        eipvprocess_step2.driving_licence.push({ documents: res.document_url, id: res.id });
       

  }
           if(res.result=="success")
           {
           eipvprocess_step2.step = 2;
           eipvprocess_step2.enableSubmit=false;
           if(data=="id_card"){
            eipvprocess_step2.id_card_isDisabled =true;
           }
           if(data=="passport"){
            eipvprocess_step2.passport_isDisabled =true;
           }
           if(data=="driving_licence"){
            eipvprocess_step2.driving_licence_isDisabled =true;

           }
           
          
          
           if(eipvprocess_step2.step==3){
               //eipvprocess_step2.submit();
               //$state.go("app.editprofile");
           }
           $timeout(function () {
            $ionicLoading.hide();
            }, 1000);
            swal("Uploaded","","success");
        }
        else{
            $ionicLoading.hide();
            swal("Upload failed","Check  internet connection and try again","error");
        }
       }
       ,function(error)
       {
           $timeout(function () {
            $ionicLoading.hide();
          }, 1000);
       swal("Server Error","Try Again Later","error");
       })

   }
    eipvprocess_step2.submit = function()
   {
        var promise = EipvuploadFactory.submiteipv();
       promise.then(function(res){
        eipvprocess_step2.step = eipvprocess_step2.step+1;

       },function(error){
           swal("Server Error","Try Again Later","error");
        })
    }

    eipvprocess_step2.showMenu = function(){
      $ionicSideMenuDelegate.toggleLeft();

    };
    eipvprocess_step2.eipv_form_submit = function(){
        var promise = EipvuploadFactory.submitform(eipvprocess_step2.user_details);
        promise.then(function(res){
            //swal("Success","","success");
            $timeout(function () {
                $ionicLoading.hide();
                }, 1000);
                $state.go("app.eKYC");
        },function(error){
            swal("Server Error","Try Again Later","error");
        })
    }
    eipvprocess_step2.sendotp = function(medium){
        eipvprocess_step2.otpdata=mainServices.resetItem();
        if(medium=="mobile") {
            eipvprocess_step2.user_details.motp='';
            email=null;
            mobile = eipvprocess_step2.user_details.mobile;
            
        } else if(medium =="email") {
            eipvprocess_step2.user_details.eotp='';
            mobile=null;
            email =eipvprocess_step2.user_details.email;
        } else if(medium=="send") {
            mobile = eipvprocess_step2.user_details.mobile;
            email =eipvprocess_step2.user_details.email;
        } else {
            swal("data error");
        }
        var data =$.param({
            name : eipvprocess_step2.user_details.name,
            pincode :eipvprocess_step2.user_details.pincode,
            mobile : mobile,
            email : email,
            req_type :"mobile"})
        var promise = EipvuploadFactory.mobileotp(data);
        promise.then(function(res){
            swal("Thanks for Details","","success");
            eipvprocess_step2.eipv_form_submit();
            //eipvprocess_step2.step=7;
            $state.go("app.eKYC");
            // if(res.data=="pincode error")
            // {
            //     swal("Pincode Invalid","Please enter a valid pincode","error");
            // }
            // else{
            // swal("Thanks for Details","","success");
            // //eipvprocess_step2.step=7;
            // $state.go("app.eKYC");
            // }
        },function(error){
            swal("Server Error","Try Again Later","error");
        })
    }


     eipvprocess_step2.verify = function(otpm){
         if(otpm =="mobile")
         {
             medium="mobile";
         }
         else {
              medium="email";
         }
         var data =$.param({
             otp :eipvprocess_step2.user_details.motp,
             email_otp : eipvprocess_step2.user_details.eotp,
             medium : medium,req_type :"mobile"})
         var promise = EipvuploadFactory.verifyotp(data);
         promise.then(function(res){
           if(res.is_mobile_otp==true && res.is_email_otp==true)
           {
               $ionicLoading.show({
                 content: 'Loading',
                 animation: 'fade-in',
                 showBackdrop: true,
                 maxWidth: 200,
                 showDelay: 0
               });
              eipvprocess_step2.eipv_form_submit();
              

           }
            else if(res.is_mobile_otp==null && res.is_email_otp==null)
            {
                eipvprocess_step2.user_details.motp='';
                eipvprocess_step2.user_details.eotp='';
                swal("Wrong OTP","Please enter valid OTP","error");

            }
            else if(res.is_mobile_otp==true && res.is_email_otp == null)
            {
                if(eipvprocess_step2.user_details.email_signup_present==true)
                {
                    $ionicLoading.show({
                      content: 'Loading',
                      animation: 'fade-in',
                      showBackdrop: true,
                      maxWidth: 200,
                      showDelay: 0
                    });

                eipvprocess_step2.eipv_form_submit();
                }
                else
                {

                    eipvprocess_step2.user_details.eotp='';
                    swal("Wrong OTP","Please enter valid email OTP","error");
                }

            }
            else if(res.is_mobile_otp==null && res.is_email_otp == true)
            {
                eipvprocess_step2.user_details.motp='';
                swal("Wrong OTP","Please enter valid mobile OTP","error");
            }
           else
           {
               swal("error");
           }
       },function(error){
           $timeout(function () {
            $ionicLoading.hide();
          }, 1000);
           swal("Server Error","Try Again Later","error");
      })
  }
    eipvprocess_step2.init();
    
    $interval(function(){
       
        eipvprocess_step2.otpdata = mainServices.getItem();
        if(eipvprocess_step2.otpdata){
            eipvprocess_step2.user_details.motp= eipvprocess_step2.otpdata
            eipvprocess_step2.otpdata="";
            $interval.cancel();
           
        }
       
    },2000);

})
