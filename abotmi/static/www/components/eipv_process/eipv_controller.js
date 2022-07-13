angular.module('eipv_controller',[]) 

.controller('EipvCtrl',function($scope,EipvuploadFactory,$state,$ionicLoading,$timeout, mainServices, $interval,deviceDetector,$ionicPopup){
    var eipvprocess = this;
    
    eipvprocess.devicedetection = deviceDetector;
    eipvprocess.medium ='';
    eipvprocess.user_details ={};
    eipvprocess.outputImage = null;
    eipvprocess.step = 0;
    eipvprocess.verified =0;
    eipvprocess.otpdata=0;
    eipvprocess.country_data=""; 
    eipvprocess.enableSubmit=true;
    eipvprocess.passport_isDisabled =false;
    eipvprocess.driving_licence_isDisabled =false;
    eipvprocess.id_card_isDisabled =false;
    eipvprocess.id_card_url =[];
    eipvprocess.passport =[];
    eipvprocess.driving_licence =[];
    eipvprocess.init = function() {
        var countrypromise =EipvuploadFactory.getcountry();
        countrypromise.then(function(data){
            eipvprocess.country = data.data;
        },function(error){
            swal("Server Error","Try again later");
        });
        
        

      eipvprocess.otpdata=mainServices.resetItem();
      var promise =  EipvuploadFactory.getdata();
      promise.then(function(res) {

      if(res.eipv_face_capture == true)
      {
          eipvprocess.step = 2;
      }
      if(res.eipv_aadhaar_present == true)
      {
          
          eipvprocess.step = 3;
         
      }
    //   if(res.eipv_pancard_present == true)
    //   {
    //       eipvprocess.step = 4;
    //   }
    //   if(res.eipv_signature_present == true)
    //   {
    //       eipvprocess.step = 5;
    //   }
       if(res.ipv_status == true)
       {
           eipvprocess.step=4;
       }
      if(res.person_info_present==1)
      {
          $state.go("app.eKYC");
      }

      eipvprocess.user_details =res;
      var get_data =EipvuploadFactory.get_verification_data();
        get_data.then(function(data_verify){
            eipvprocess.passport=data_verify.passport_data
            eipvprocess.driving_licence=data_verify.driving_licence
            eipvprocess.id_card_url=data_verify.id_card
            eipvprocess.user_details.country = data_verify.country_data
            console.log(eipvprocess.user_details.country);
            if(eipvprocess.driving_licence.length || eipvprocess.id_card_url.length || eipvprocess.passport.length){
                eipvprocess.enableSubmit=false;
            }
           
        },function(error){
            swal("Server Error","Try again later");
        });

  },function(error){
      swal("Server Error","Try Again Later","error");
  })
   }


     eipvprocess.capturedata = function(image,data){
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
           // eipvprocess.step = eipvprocess.step+1;
            if(eipvprocess.step==3){
                //eipvprocess.submit();
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
    eipvprocess.verifySubmit = function(){
       
        var promise = EipvuploadFactory.savecountry(eipvprocess.user_details.country);
       promise.then(function(res){
        

       },function(error){
           swal("Server Error","Try Again Later","error");
        })
        $state.go("app.editprofile");

    }
    $scope.fileNameChangedPassport = function() {
        eipvprocess.myValue1 = false
        eipvprocess.passport_isDisabled =false;
      }
      $scope.fileNameChangedDrivingLicence = function() {
        eipvprocess.myValue2 = false
        eipvprocess.driving_licence_isDisabled =false;
      }
      $scope.fileNameChangedIdCard = function() {
        eipvprocess.myValue3 = false
        eipvprocess.id_card_isDisabled =false;
      }

      eipvprocess.common_function = function(data){
        var promise = EipvuploadFactory.deletedocuments(data);
        promise.then(function(res){
        
        },function(error){
            swal("Server Error","Try Again Later","error");
         })
      }
      eipvprocess.passport_delete = function(data_id,$index){
        var confirmPopup = $ionicPopup.confirm({
            title: 'Delete',
            template: 'Are you sure you want to delete this item?'
          });
       
          confirmPopup.then(function(res) {
            if(res) {
              // Code to be executed on pressing ok or positive response
              // Something like remove item from list
              eipvprocess.common_function(data_id);
              eipvprocess.passport.splice($index, 1); 
       eipvprocess.myValue1 = true
       if(!eipvprocess.driving_licence.length && !eipvprocess.id_card_url.length && !eipvprocess.passport.length){
        eipvprocess.enableSubmit=true;
    }
            } else {
              // Code to be executed on pressing cancel or negative response
            }
          });  
       

      }
      eipvprocess.id_card_delete = function(data_id,$index){
        var confirmPopup = $ionicPopup.confirm({
            title: 'Delete',
            template: 'Are you sure you want to delete this item?'
          });
       
          confirmPopup.then(function(res) {
            if(res) {
              // Code to be executed on pressing ok or positive response
              // Something like remove item from list
              eipvprocess.common_function(data_id);
             // eipvprocess.id_card_url.shift();
              eipvprocess.id_card_url.splice($index, 1); 
              eipvprocess.myValue3 = true
              if(!eipvprocess.driving_licence.length && !eipvprocess.id_card_url.length && !eipvprocess.passport.length){
                  eipvprocess.enableSubmit=true;
              }
            } else {
              // Code to be executed on pressing cancel or negative response
            }
          });  
       
 
       }
       eipvprocess.driving_delete = function(data_id,$index){

        var confirmPopup = $ionicPopup.confirm({
            title: 'Delete',
            template: 'Are you sure you want to delete this item?'
          });
       
          confirmPopup.then(function(res) {
            if(res) {
              // Code to be executed on pressing ok or positive response
              // Something like remove item from list
              eipvprocess.common_function(data_id);
              //eipvprocess.driving_licence.shift();
              //var index2 = eipvprocess.driving_licence.indexOf(data_id);
              eipvprocess.driving_licence.splice($index, 1); 
              eipvprocess.myValue2 = true
              if(!eipvprocess.driving_licence.length && !eipvprocess.id_card_url.length && !eipvprocess.passport.length){
                  eipvprocess.enableSubmit=true;
              }
            } else {
              // Code to be executed on pressing cancel or negative response
            }
          });  

        

 
       }
    eipvprocess.capturedata_verify = function(image,data){
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
              eipvprocess.id_card_url.push({ documents: res.document_url, id: res.id });

        }
        if(res.document_type == "passport"){
            eipvprocess.passport.push({ documents: res.document_url, id: res.id });
            

      }
      if(res.document_type == "driving_licence"){
        eipvprocess.driving_licence.push({ documents: res.document_url, id: res.id });
       

  }
           if(res.result=="success")
           {
           eipvprocess.step = 2;
           eipvprocess.enableSubmit=false;
           if(data=="id_card"){
            eipvprocess.id_card_isDisabled =true;
           }
           if(data=="passport"){
            eipvprocess.passport_isDisabled =true;
           }
           if(data=="driving_licence"){
            eipvprocess.driving_licence_isDisabled =true;

           }
           
          
          
           if(eipvprocess.step==3){
               //eipvprocess.submit();
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
    eipvprocess.submit = function()
   {
        var promise = EipvuploadFactory.submiteipv();
       promise.then(function(res){
        eipvprocess.step = eipvprocess.step+1;

       },function(error){
           swal("Server Error","Try Again Later","error");
        })
    }

    // eipvprocess.showMenu = function(){
    //   $ionicSideMenuDelegate.toggleLeft();

    // };
    // track.showMenu = function(){
    //     $ionicSideMenuDelegate.toggleLeft();
    //   };
  
    //   eipvprocess.isMenuOpen = function() {
    //       return $ionicSideMenuDelegate.isOpen();
    //   };
    eipvprocess.eipv_form_submit = function(){
        var promise = EipvuploadFactory.submitform(eipvprocess.user_details);
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
    eipvprocess.sendotp = function(medium){
        eipvprocess.otpdata=mainServices.resetItem();
        if(medium=="mobile") {
            eipvprocess.user_details.motp='';
            email=null;
            mobile = eipvprocess.user_details.mobile;
            
        } else if(medium =="email") {
            eipvprocess.user_details.eotp='';
            mobile=null;
            email =eipvprocess.user_details.email;
        } else if(medium=="send") {
            mobile = eipvprocess.user_details.mobile;
            email =eipvprocess.user_details.email;
        } else {
            swal("data error");
        }
        var data =$.param({
            name : eipvprocess.user_details.name,
            pincode :eipvprocess.user_details.pincode,
            mobile : mobile,
            email : email,
            req_type :"mobile"})
        var promise = EipvuploadFactory.mobileotp(data);
        promise.then(function(res){
            swal("Thanks for Details","","success");
            eipvprocess.eipv_form_submit();
            //eipvprocess.step=7;
            $state.go("app.eKYC");
            // if(res.data=="pincode error")
            // {
            //     swal("Pincode Invalid","Please enter a valid pincode","error");
            // }
            // else{
            // swal("Thanks for Details","","success");
            // //eipvprocess.step=7;
            // $state.go("app.eKYC");
            // }
        },function(error){
            swal("Server Error","Try Again Later","error");
        })
    }


     eipvprocess.verify = function(otpm){
         if(otpm =="mobile")
         {
             medium="mobile";
         }
         else {
              medium="email";
         }
         var data =$.param({
             otp :eipvprocess.user_details.motp,
             email_otp : eipvprocess.user_details.eotp,
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
              eipvprocess.eipv_form_submit();
              

           }
            else if(res.is_mobile_otp==null && res.is_email_otp==null)
            {
                eipvprocess.user_details.motp='';
                eipvprocess.user_details.eotp='';
                swal("Wrong OTP","Please enter valid OTP","error");

            }
            else if(res.is_mobile_otp==true && res.is_email_otp == null)
            {
                if(eipvprocess.user_details.email_signup_present==true)
                {
                    $ionicLoading.show({
                      content: 'Loading',
                      animation: 'fade-in',
                      showBackdrop: true,
                      maxWidth: 200,
                      showDelay: 0
                    });

                eipvprocess.eipv_form_submit();
                }
                else
                {

                    eipvprocess.user_details.eotp='';
                    swal("Wrong OTP","Please enter valid email OTP","error");
                }

            }
            else if(res.is_mobile_otp==null && res.is_email_otp == true)
            {
                eipvprocess.user_details.motp='';
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
    eipvprocess.init();
    
    $interval(function(){
       
        eipvprocess.otpdata = mainServices.getItem();
        if(eipvprocess.otpdata){
            eipvprocess.user_details.motp= eipvprocess.otpdata
            eipvprocess.otpdata="";
            $interval.cancel();
           
        }
       
    },2000);

})
