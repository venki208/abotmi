angular.module('reiaapp.controllers',[])
.controller('ClientToken',function (get_userRegisterd,$localStorage,$state,SweetAlert,$scope, mainServices) {
  
	$scope.ClientTokenMethod = function (email_Verified_Status,emailid,first_name,pass_word,lastName,source,gender,next_url) {
  
    if(email_Verified_Status=="not verified")
    {
   
     $state.go('email-otp',{ 'emailid': emailid ,'first_name':first_name,'password':pass_word,'last_name':lastName,'source':source,'gender':gender,'next_url':next_url}); 


    }
    else{
    var jwttoken=localStorage.getItem('jwttoken');
		var Registerd = get_userRegisterd.getDetails(jwttoken);
		Registerd.then(function(response){
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
			else {
       
        $state.go('start.eipv');

			}
		},function(error){
			swal("UNAuthorized","Try again later");
    })
     }
   }

  $scope.ReciveOtpMethod = function(otpsms) {
    mainServices.setItem(otpsms);
  }
 })
 .controller('LogoutCtrl',function(get_userRegisterd,$localStorage,$state,$http){
  var log = this;
  log.init = function(){
    var logoutdetails = get_userRegisterd.userLogout();
    logoutdetails.then(function(data){
    },function(error){
      swal("Error",JSON.stringify(error.data));
    });
  if(localStorage.getItem('jwttoken'))
      localStorage.removeItem('jwttoken');
      $http.defaults.headers.common['Authorization']="";
      window.location.href = 'nativeurl://logout';
  };
  log.init();
})

.controller('EkycCtrl',function($localStorage,adharverify,$window,AADHAAR_BRIDGE_API){
  var ekyc = this;
  ekyc.AADHAAR_BRIDGE_API = AADHAAR_BRIDGE_API;
  ekyc.adharnumberverify = function(){
  var promise = adharverify.verify(ekyc.number,"self");
     promise.then(function(res){
        if(res.data == "Aadhaar number is already exist") {
        swal("Your Aadhar Number Already Exist");
      } else {
        ekyc.aadhaar_form = res;
        setTimeout(function() {
          var submitform = $window.document.forms['ekyc.aadhar_form'].submit();
        }, 1500);
      }
    })
 }
})


.controller('eKYCsuccess',function($localStorage,$state,$location,aadhar_success){
      var uuid =$location.search().uuid;
      var reqid =$location.search().requestId;
      var type = $location.search().type?$location.search().type:"web";
      if(type.search("mobile")){
        var promise = aadhar_success.success(uuid,reqid,"member");
          promise.then(function(response) {
            if(response.data.is_kyc_success) {
              var aadhaar_transaction_id = response.data.aadhaar_transaction_id;
              swal("Success","Aadhaar verification is success");
              $state.go('app.myhub.add_client_aadhar',{"trans_id":aadhaar_transaction_id});
            } else {
              swal("Failure","Aadhaar verification failed ");
              $state.go('app.myhub');
            }
        });
      } else {
          var promise = aadhar_success.success(uuid,reqid,"self");
          promise.then(function(response) {
            if(response.data == 'signup_with_email') {
              swal("Success","Aadhaar verification is success");
              $state.go('app.myhub');
            } else {
              swal("Aadhaar verification success ","login credentials are  sent to your email id");
              $state.go('login');
            }
        });
      }
})

.controller('eKYCfailure',function($localStorage,$state,$location,aadhar_failure) {
   var reqid =$location.search().requestId;
   var type = $location.search().type?$location.search().type:"web";
      if(type == "mobile"){
        var promise = aadhar_failure.failure(reqid,"member");
          promise.then(function(response) {
            if(response.data.is_adhaar_no_invalid) {
              swal("Failure","Aadhaar Number is invalid");
            } else {
              swal("Failure","Error happened during verifying ekyc");
              $state.go('app.myhub');
            }
        });
      } else {
      var promise = aadhar_failure.failure(reqid,"self")
      promise.then(function(response)
      {
        if(response.data = 'Aadhar Details Storing unsuccessful')
        {
          swal("Aadhar verification   Failed ","Please try again");
          $state.go('eKYC');
      }
    });
   }
})

.controller('TrackCtrl',function($state,get_userRegisterd,$ionicSideMenuDelegate,mainServices){
    var promise = "";
    var track = this;
    track.showTabs = 1;
    track.init = function (){
    promise = get_userRegisterd.getDetails_menu();
    promise.then(function(results){
    track.data = results;
    mainServices.DataUpdate(track.data);
      

    
  
    track.faq = function(){
    
      $state.go("start.faq",{'status':'non_registered'});
    }

    track.help = function(){
      $state.go("start.help",{'status':'non_registered'});
    }

    track.terms = function(){
      $state.go("start.terms",{'status':'non_registered'});
    }

    track.privacypolicy = function(){
      $state.go("start.privacypolicy",{'status':'non_registered'});
    }

    track.apphelp = function(){
      if(track.data =="Confirmed") {
      $state.go("app.apphelp",{'status':'confirmed'});
      }
     if(track.data =="Registered") {
        $state.go("app.apphelp",{'status':'registered'}); 
      }
    }

    track.appfaq = function(){
      if(track.data =="Confirmed") {
        $state.go("app.appfaq",{'status':'confirmed'});
        }
       if(track.data =="Registered") {
          $state.go("app.appfaq",{'status':'registered'}); 
        }
       
      }
    

    track.appterms = function(){
      var updatedvalueTerms=mainServices.DataUpdateItem();
      
      if(updatedvalueTerms =="Confirmed") {
        $state.go("app.termsandconditions",{'status':'confirmed'});
        }
      if(updatedvalueTerms =="Registered") {
          $state.go("app.termsandconditions",{'status':'registered'}); 
        }
        if(updatedvalueTerms =="Not Registered"){
          swal("Success","User is not registerd terms and conditions cannot be shown");
        }
        
      }
    

    track.appprivacypolicy  = function(){
      var updatedvalueTrack=mainServices.DataUpdateItem();
      if(updatedvalueTrack=="Confirmed") {
        $state.go("app.privacypolicy",{'status':'confirmed'});
        }
      if(updatedvalueTrack=="Registered") {
          $state.go("app.privacypolicy",{'status':'registered'}); 
        }
        if(updatedvalueTrack=="Not Registered") {
          swal("Success","User is not registerd  privacy policy cannot be shown");
        }
        
      }
        
    track.changepass = function(){
      var updatedvalue=mainServices.DataUpdateItem();
      if(updatedvalue =="Confirmed") {
        
        $state.go("app.changepassword",{'status':'confirmed'});
        }
      if(updatedvalue =="Registered") {
          $state.go("app.changepassword",{'status':'registered'}); 
        }
        if(updatedvalue =="Not Registered") {
          swal("Success","User is not registerd  change password cannot be done");
        }
        
      }
    
  }) 
}
    //commented for now , will be removed later
    // track.showModal = function(template){
    //   $ionicModal.fromTemplateUrl('templates/'+template+'.html',{
    //     scope : $scope,
    //     hardwareBackButtonClose: true
    //   }).then(function(modal){
    //               track.modal = modal;
    //               track.modal.show();
    //           });
    // }
    // track.emailshare = {};
    // track.shareThroughEmail = function(){
    //   track.emailshare.template_name = "ABOTMI_16";
    //   track.emailshare.mail_body = 'Please click '+'<a href='+"'"+track.url+"'"+'>here</a>'+ ' to view the profile';
    //   var emailShareResult = sendEmail.sendEmailShare(track.emailshare);
    //   emailShareResult.then(function(msg){
    //     swal("success","Profile shared Successfully","success");
    //   });
    //   track.cancel(track.modal);
    // };

    // track.cancel = function(modal){
    //   modal.hide();
    // };

    track.showMenu = function(){
      $ionicSideMenuDelegate.toggleLeft();
    };

    track.isMenuOpen = function() {
        return $ionicSideMenuDelegate.isOpen();
    };
    track.init();
  })

    // track.init = function(){
    //   var data = [];
    //   track.user_details = [];
    //   track.peerrate = "";
    //   track.rateproperty = [];
    //   track.rateproperty.trust = null;
    //   track.rateproperty.financial = null;
    //   track.rateproperty.comm = null;
    //   track.rateproperty.advisory = null;
    //   track.rateproperty.ccare = null;
    //   track.rateproperty.ethics = null;
    //   track.rateproperty.avgrate = null;
    //   track.user_details.DSA_details =[];
    //   track.user_details.RERA_details = [];
    //   track.question3();
    //   var promise = get_userDetails.getDetails();
    //   promise.then(
    //   function(payload){
    //      $timeout(function () {
    //       $ionicLoading.hide();
    //   }, 1000);
    //     track.user_details = payload;
    //     if(track.user_details.RERA_details!="")
    //    {
    //        track.user_details.rera_checked = 'A';
    //    }
    //    if(track.user_details.DSA_details !="")
    //    {
    //        track.user_details.dsa_checked ='A';

    //    }
    //    if(track.user_details.IRDA_registration_no !="")
    //    {
    //        track.user_details.irda ='A';

    //    }
    //    if(track.user_details.SEBI_registration_no !="")
    //    {
    //        track.user_details.sebi ='A';

    //    }
    //    if(track.user_details.other_registration_no !="")
    //    {
    //        track.user_details.otherregister ='A';

    //    }
    //    if(track.user_details.AMFI_registration_no !="")
    //    {
    //        track.user_details.amfi ='A';

    //    }


    //     track.emailshare.mail_body = track.user_details.name +' has shared profile for your reference. Please click '+'<a href='+"'"+track.url+"'"+'>here</a>'+ ' to view the profile';
    //     switch(track.user_details.crisil_application_status){
    //       case CRISIL_NOT_APPLIED : {
    //                                   track.crisilyearoptions = [{id:1,value :1}, {id:2,value:2}];
    //                                   track.selectedcrisilyear = track.crisilyearoptions[1].value;
    //                                   track.calculate_gross_total();
    //                                   break;
    //       }
    //       case CRISIL_APPLIED : track.crisil_title = "Enter Payment Details";track.crisil_button = true; break;
    //       case CRISIL_PAYMENT_RE_SUBMIT : track.crisil_title = "Re-Enter Payment Details";track.crisil_button = true;break;
    //       case CRISIL_PAYMENT_SUBMITTED : track.crisil_button = false ; break;
    //       case CRISIL_CERTIFICATE_IN_PROCESS : track.crisil_title = "Your CRISIL Certificate is in-process";track.crisil_button = true; break;
    //       case CRISIL_GOT_CERTIFICATE : track.crisil_title = "You are CRISIL Certified";track.crisil_button = true;break;
    //     }
    //   },
    //   function(payloaderror){
    //      $timeout(function () {
    //       $ionicLoading.hide();
    //   }, 100);
    //   swal("Server error,please try again later");
    //   $state.go('login');
//       });

//       track.manageoptions = ["Add","Group","Send Mail","Transaction"];
//       track.crisil = [];
//       track.crisil.paydate = '';
//       track.cirisl_button = 'true';
//       track.value = false;
//     };



//     track.getuserdetails = function(){
//         var promise = get_userDetails.getDetails();
//         promise.then(function(payload){
//           track.user_details = payload;
//       },function(error){
//       });
//     }

//     track.calculate_gross_total = function(){
//         track.crisilgrosstotal = 3 * CRISIL_CERTIFICATE_VALUE;
//         track.crisildiscountedgross = track.selectedcrisilyear * CRISIL_CERTIFICATE_VALUE;
//         track.crisilservicetax = (track.crisildiscountedgross * TAX_PERCENTAGE_CRISIL)/100;
//         track.crisilpayable = track.crisildiscountedgross + track.crisilservicetax;
//     }

//     track.referAdvisorSubmit = function(){
//       var referpromise = submitData.referAdvisor(track.refer);
//       referpromise.then(function(res){
//         if(res == "success"){
//           swal("Success",res,"success");
//           track.user_details = track.getuserdetails();
//           track.cancel(track.modal);
//         }
//         else{
//           swal("Alert",res,"error");
//           track.user_details = track.getuserdetails();
//           track.cancel(track.modal);
//         }
//       },function(payloaderror){
//         swal("Failed",JSON.stringify(payloaderror.data));
//         track.cancel(track.modal);
//       });
//      track.refer = "";
//      track.looplist.$setPristine();
//      track.getuserdetails();
//     };

//     track.viewLoop = function(){
//       if(track.user_details.total_reffered_advisor_count == 0){
//         swal("No Advisors");
//       }else{
//       $ionicLoading.show({
//         content: 'Loading',
//         animation: 'fade-in',
//         showBackdrop: true,
//         maxWidth: 200,
//         showDelay: 0
//       });
//       var viewpromise = dashboardDetails.viewAdvisorLoop();
//       viewpromise.then(function(res){
//        $timeout(function () {
//         $ionicLoading.hide();
//         }, 1000);
//         track.user_details.referred_advisor_details_list = res;
//         $state.go("app.myhub.viewadvisors");
//       },function(error)
//       {
//        $timeout(function () {
//         $ionicLoading.hide();
//       }, 1000);
//       });
//       }
//     }

//   track.viewrank = function(user_type){
//     if (user_type == "advisor" && track.user_details.total_no_invites_to_rate == 0){
//       swal("No Records");
//     }
//     else if(user_type == "member" && track.user_details.total_no_invites_to_rank == 0){
//       swal("No Records");
//     }
//     else{
//     $ionicLoading.show({
//       content: 'Loading',
//       animation: 'fade-in',
//       showBackdrop: true,
//       maxWidth: 200,
//       showDelay: 0
//     });
//     var rankpromise = dashboardDetails.viewRankDetails(user_type);
//     rankpromise.then(function(res){
//       $timeout(function () {
//       $ionicLoading.hide();
//     }, 1000);
//       track.user_details.viewrank = res;
//       if (user_type == "advisor")
//         track.user_details.viewrank.title = "View Peers";
//       else
//         track.user_details.viewrank.title = "View Clients";
//       $state.go("app.myhub.viewraterank");
//       },function(error){
//         $timeout(function () {
//       $ionicLoading.hide();
//     }, 1000);
//       });
//     }
//   }

//   track.inviteRequest = function(type){
//     if (type === "advisor")
//     {
//       track.user_details.invitereqtitle = "Invite Peer To Rate";
//       track.user_details.invitetype = "advisor";
//       track.showRateInvite = true;
//       track.peerrate = '';
//     }
//     else{
//       track.user_details.invitereqtitle = "Invite Client To Rank";
//       track.user_details.invitetype = "member";
//       track.showRankInvite = true;
//       track.peerrate = '';
//     }
//   }

//   track.hideRateInviteDiv = function(){
//   track.showRateInvite = false;
//   };

//   track.hideRankInviteDiv = function(){
//   track.showRankInvite = false;
//   };


//   track.inviterateSubmit = function(){
//     var invitepeerpromise = submitData.inviteRate(track.peerrate,track.user_details.invitetype);
//     invitepeerpromise.then(function(res){
//       if(res == "success"){
//         track.user_details = track.getuserdetails();
//           swal("Invite",res,"success");
//           track.hideRateInviteDiv();
//           track.hideRankInviteDiv();
//       }
//     else{
//         swal("Invite",res,"error");
//         track.user_details = track.getuserdetails();
//         track.hideRateInviteDiv();
//         track.hideRankInviteDiv();
//       }
//       },function(error){
//       swal("Invite Failed","Try Again");
//       track.hideRateInviteDiv();
//       track.hideRankInviteDiv();}
//     );
//   }

//   track.ratePeer = function(key){
//     var ratepromise = dashboardDetails.ratePeer(key);
//   }

//   track.checkPromoCode = function(){
//     var promopromise = submitData.checkPromoCode(track.enteredpromocode);
//     promopromise.then(function(res){
//       track.crisil_taxamount = res.tax;
//       track.crisil_discamount = res.discount_amount;
//       track.crisil_total_amount = res.amount;
//       track.crisil_valid_status = res.promocode_status;
//       if(track.crisil_valid_status == "invalid"){
//         track.enteredpromocode = "";
//     }
//     });
//   }

//   track.confirm_advisor_to_apply_crisil = function(){
//       var crisilpromise = submitData.applyCrisil(track.selectedcrisilyear);
//       crisilpromise.then(function(res){
//         swal("CRISIL","Applied for CRISIL","success");
//         track.getuserdetails();
//         $state.go("app.myhub");
//       });
//   }

//   track.selectDate = function(date){
//     ionicDatePicker.openDatePicker(date);
//   }

//   track.selectPayDate = function(val){
//     track.paydate = {
//       callback : function(val){
//         //track.crisil.paydate = new Date(val);
//         track.crisil.paydate = moment(new Date(val)).format('YYYY-MM-DD');
//       }
//     };
//     track.selectDate(track.paydate);
//   }

//   track.crisil_refdocsubmit = function(){
//     $ionicLoading.show({
//       content: 'Loading',
//       animation: 'fade-in',
//       showBackdrop: true,
//       maxWidth: 200,
//       showDelay: 0
//     });
//     var crisilformprom = submitData.crisilDocSubmit(track.crisil,track.user_details.crisil_amount.amount);
//     crisilformprom.then(function(res){
//         $timeout(function () {
//       $ionicLoading.hide();
//     }, 2000);
//       track.user_details.crisil_amount.bankname = track.crisil.bankname;
//       track.user_details.crisil_amount.cheque_no = track.crisil.refnumber;
//       track.user_details.crisil_amount.cheque_date = track.crisil.paydate;
//       track.crisil_button = false;
//       swal("CRISIL","Form Updated successfully.","success");
//       track.getuserdetails();
//       $state.go("app.myhub");
//     },function(error){
//       swal("CRISIL",JSON.stringify(error));
//     });
//   }

//   track.disown_member = function(mememailid){
//     var disownprom = dashboardDetails.disownMember(mememailid);
//     disownprom.then(function(res){
//       swal("Disown","Member Successfully disowned","success");
//       if(track.user_details.total_clients_added > 0)
//       track.user_details.total_clients_added -= 1;
//       track.cancel(track.modal);
//     },function(error){
//       swal("Disown","Member disown Not Successful");
//       track.cancel(track.modal);
//     });
//   };

//   track.refresh = function(){
//     track.init();
//     $timeout(function(){
//     },2000);
//     $scope.$broadcast('scroll.refreshComplete');
//   };

//   track.crisil_renewalsubmit = function(){
//     $ionicLoading.show({
//       content: 'Loading',
//       animation: 'fade-in',
//       showBackdrop: true,
//       maxWidth: 200,
//       showDelay: 0
//     });
//     var crisilformprom = submitData.crisilRenewSubmit(track.crisil,track.user_details.crisil_pay_amount,track.user_details.crisil_expiry_date);
//     crisilformprom.then(function(res){
//         $timeout(function () {
//       $ionicLoading.hide();
//     }, 2000);
//       swal("CRISIL","Renewal submitted successfully.","success");
//       track.getuserdetails();
//       $state.go("app.myhub");
//     },function(error){
//       swal("CRISIL",JSON.stringify(error));
//     });
//   };

//  track.question3 = function(){

//       track.user_details.answer =[];
//       track.user_details.answer[0]={};
//       track.user_details.answer[0].Question ="1. Are you a Realtor ?";
//       track.user_details.answer[0].Remark =[];
//       track.user_details.answer[0].Remark[0] ={};
//       track.user_details.answer[0].Remark[0].Question ="Experience";
//       track.user_details.answer[0].Remark[1] ={};
//       track.user_details.answer[0].Remark[1].Question ="Total Number of clients so far";
//       track.user_details.answer[0].Remark[2] ={};
//       track.user_details.answer[0].Remark[2].Question = "Average transaction";
//       track.user_details.answer[1] ={};
//       track.user_details.answer[1].Question ="2.Do you have an infrastructure or will you be able to create an infrastructure to handle the members?";
//       track.user_details.answer[2]={};
//       track.user_details.answer[1].Remark=[];
//       track.user_details.answer[2].Question ="3. Are you associated with any Financial Organisation";
//       track.user_details.answer[2].Remark =[];
//       track.user_details.answer[2].Remark[0] ={};
//       track.user_details.answer[2].Remark[0].Question ="institution_name";
//       track.user_details.answer[2].Remark[0].Answer ="";
//       track.user_details.answer[3]={};
//       track.user_details.answer[3].Question ="4. Will you be interested to undergo any training program about real estate investment advisory?";


//   }
//   track.addinstituite = function()
//   {

//           track.user_details.answer[2].Remark[0].Remark.push(
//               {'Question': 'institution_name','Answer':''});
//               track.user_details.answer[2].Remark[0].Remark.push({'Question': 'official_email_id','Answer':''});
//               track.user_details.answer[2].Remark[0].Remark.push({'Question':'registration_id','Answer':''});
//               track.user_details.answer[2].Remark[0].Remark.push({'Question':'year_of_association','Answer':''});
//       }
//       track.delete = function(data,i){
//            data.splice(i,4);
//       }
//       track.append = function(data,i)
//       {
//           if(i%4 == 1 && data!='')
//           {
//           string = "http://:"
//           track.user_details.answer[2].Remark[0].Remark[i].Answer= string.concat(data);


//   }
//   }
// track.init();
.controller('sideMunuCtrl',function($stateParams){
  var sidemenu = this;
  
  sidemenu.status = $stateParams.status;
})

.controller('ICORECtrl',function(get_userDetails,get_blogDetails,socialShare,$stateParams,SweetAlert,$timeout,$ionicLoading){
	var icore = this;
	icore.usericoreid = 0;
  icore.posts = [];
  icore.content = [];
  icore.eachpost = [];
  icore.postid = $stateParams.id;
  icore.init = function(){
    var promise = get_userDetails.getDetails();
    promise.then(function(response){
       $timeout(function () {
    $ionicLoading.hide();
  }, 100);
        icore.usericoreid = response.wordpress_user_id;
        var postpromise = get_blogDetails.getDetails(icore.usericoreid);
     postpromise.then(function(response){
      icore.posts = response;
      icore.totalposts = Object.keys(icore.posts).length;
  },function(error){
     });
     var commentpromise = get_blogDetails.getUserComments(response.email_id);
     commentpromise.then(function(data){
      icore.usercomments = data;
     },function(error){

     });
    },function(error){
       $timeout(function () {
    $ionicLoading.hide();
  }, 100);
    });
 };

icore.getPost = function(postid){
  if(postid){
  var promisepost = get_blogDetails.getPost(postid);
  var postcomments = "";
    promisepost.then(function(res){
        $timeout(function () {
          $ionicLoading.hide();
        }, 100);
        icore.eachpost = res;
        icore.eachpost.postid = postid;
    },function(error){
        $timeout(function () {
          $ionicLoading.hide();
        }, 100);
    });
  }
};

icore.postsocialshare = function(app,url,text){
  switch(app){
  case 'Facebook' : socialShare.fb_share(url); break;
  case 'LinkedIn' : socialShare.LinkedInShare(url); break;
  case 'Google' : socialShare.googleplusbtn(url); break;
  case 'Whatsapp' : socialShare.whatsapp_share(url,text);break;
  case 'Twitter' : socialShare.twitter_share(url);break;
}
};

icore.rate_post = function(){
  var promise = get_blogDetails.ratePost(icore.eachpost.postid,icore.eachpost.rating[3].meta_value);
  promise.then(function(res){
      $timeout(function () {
        $ionicLoading.hide();
      }, 100);
      icore.eachpost.rating = res.data;
      swal("Success","Post rated successfully");
  },function(error){
      $timeout(function () {
        $ionicLoading.hide();
      }, 100);
      swal("Error","Please Try Again");
  });
};

icore.addComment = function(){
  var comment = get_blogDetails.addComment(icore.eachpost.postid,icore.eachpost.addcomment);
  comment.then(function(res){
      $timeout(function () {
        $ionicLoading.hide();
      }, 100);
      swal("Success","Post commented successfully");
      icore.getPost(icore.eachpost.postid);
      icore.eachpost.add_comment = "";
  },function(error){
      $timeout(function () {
        $ionicLoading.hide();
      }, 100);
      swal("Error","Please Try Again");
  });
}


icore.init();
icore.getPost(icore.postid);
})

.controller('ICOREAddPostCtrl',function(get_blogDetails,$window,$state){
  var addpost = this;
  addpost.tinyMceOptions = {
                        setup: function(editor) {
                            $timeout(function () {
                                editor.focus();

                            }, 200);
                        },
                        statusbar: false,
                        menubar: false,
                        resize: false,
                        toolbar: 'formatselect | bold italic underline | bullist numlist | undo redo '
                    };

  addpost.init = function(){
    addpost.show_media_form = false;
    addpost.post = {};
    addpost.post.categories = [];
    addpost.post.content = "";
    var getcategory = get_blogDetails.getCategories();
    getcategory.then(function(res){
      addpost.categories = res.data;
    },function(error){
      swal("Error in getting categories, please try again");
    });
  };

  addpost.goBack = function(){
    $window.history.back();
  };

  addpost.updateHtml = function() {
    ctrl.tinymceHtml = $sce.trustAsHtml(ctrl.tinymce);
  };

  addpost.toggleSelection = function(name) {
    var idx = addpost.post.categories.indexOf(name);

    // Is currently selected
    if (idx > -1) {
      addpost.post.categories.splice(idx, 1);
    }

    // Is newly selected
    else {
      addpost.post.categories.push(name);
    }
  };

  addpost.uploadmedia = function(){
    var post = get_blogDetails.addMedia(addpost.post.media);
    post.then(function(result){
      var res=result.data.split("::");
      if(addpost.post.content){
        addpost.post.content = addpost.post.content + '<img src="'+res[1]+'" width="100" height="100"/><br>';
      }
      else{
        addpost.post.content = '<img src="'+res[1]+'" width="100" height="100"/><br>';
        addpost.post.feature_img = addpost.post.content;
      }
      addpost.show_media_form = false;
    },function(error){
      swal("Try again",JSON.stringify(error.data));
    });
  };

  addpost.submitPost = function(){
    var post = get_blogDetails.addPost(addpost.post);
    post.then(function(result){
      swal("Success","Post added successfully");
      $state.go('app.myhub.post',{id:result.data});
    },function(error){
      swal("Error","Try Again");
    })
  };

addpost.init();

})

.controller('ContactCtrl',function(submitData,$state){
  var contact = this;

  contact.submit = function(){
    var contactpromise = submitData.getintouch(contact.details);
    contactpromise.then(function(data){
      swal("Get In Touch","Details Submitted","success");
      $state.go('app.myhub');
    },function(error){
      swal("Get In Touch",JSON.stringify(error.data));
    });
  }
})


//webinar
.controller('webinarCtrl',function(submitData,$state){
            var webinar = this;
            webinar.submit = function(){
            var webinarpromise = submitData.webinar(webinar.details);
            webinarpromise.then(function(response){
                 if (response.data=="success") {
                   swal("webinar","Details Submitted","success");
                 } else {
                   swal("webinar","You have entered wrong old password please try again");
                   webinar.details='';
                 }
                 },function(error){
                   swal("Get In Touch",JSON.stringify(error.data));
                 });
            }
})

.controller('meetupCtrl',function(submitData,$state){
      var meetup = this;
      meetup.submit = function(){
      var meetuppromise = submitData.meetup(meetup.details);
      meetuppromise.then(function(response) {
        if (response.data=="success") {
          swal("meetup","Details Submitted","success");
          $state.go('login');
        } else {
          swal("meetup","You have entered wrong old password please try again");
          meetup.details='';
        }
        },function(error){
          swal("Get In Touch",JSON.stringify(error.data));
        });
     }
})


//changepassword
.controller('changepasswordCtrl',function(changepasswordfactory,$stateParams,$state,$localStorage){
  var changepassword = this;
  changepassword.status= $stateParams.status;
  changepassword.showPassword1 = false;
  changepassword.showPassword = false;
  changepassword.passwordvalue=false;
  
  changepassword.toggleShowPassword = function() {
   
    changepassword.showPassword = !changepassword.showPassword;
  }
 
  
  changepassword.toggleShowPassword1 = function() {
    
   
    changepassword.showPassword1 = !changepassword.showPassword1;
  }
  changepassword.ValidateEmail1 =function(){
    var email = document.getElementById("newpassword").value;
   if(email){
    var expr = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$/;
    if (!expr.test(email)) {
      changepassword.passwordvalue=true
    }
    else{
      changepassword.passwordvalue=false
    }
  }
  else{
    changepassword.passwordvalue=false
  }
}
  
  changepassword.submit = function(){
    var changepasswordpromise = changepasswordfactory.changepassword(changepassword.details);
    changepasswordpromise.then(function(response){
      if (response.data=="success") {
        swal("Change Password","Success","success");
        localStorage.removeItem('jwttoken');
        $state.go('logout');
      } else {
        swal("Change Password","You have entered wrong old password please try again");
        changepassword.details='';
      }
    },function(error){
      swal("Get In Touch",JSON.stringify(error.data));
    });
  }
})


.controller('CloseCtrl',function(submitData,$state){
  var close = this;
  close.init = function(){
      window.close();
  };
  close.init();
})

.controller('SMSCtrl',function(smsNotification){
  var sms = this;
  sms.init = function(){
    var smspromise = smsNotification.get_status();
    smspromise.then(function(response){
      sms.alertValue = response.data;
    },
    function(error){
      swal("Error","Please try again");
    })
  };

  sms.toggle_status = function(){
    sms.alertValue = !sms.alertValue;
    var change = smsNotification.toggle_status();
    change.then(function(response){
      sms.alertValue = response.data;
    },
    function(error){
      swal("Error","Please try again");
    })
  }

  sms.init();
})

.controller('UpdateProfileCtrl',function(get_userDetails,updateprofiledetails,$state){
  var updateprofile = this;
  updateprofile.init = function(){
      updateprofile.my_belief = ["Service is my motto","Work is worship","Customer first"];
  };

  updateprofile.init();
})

.controller('register',function($state,get_reguserdetails,submitProfileData,$localStorage){
    var reg = this;
    reg.init = function(){
    reg.user_details = {};
    reg.year = [];
    var max  = new Date().getFullYear();
    var min = max - 100 ;
    for (var i = max; i>=min; i--){
         reg.year.push(i);
    }

  var promise = get_reguserdetails.getDetails();
  promise.then(function(payload){
      reg.user_details = payload;
      if(reg.user_details.address!=null) {
            reg.user_details.checkaddress ="true"  ;
      }
  },function(error){
      swal("Server Error","Try again later");
  });
  var countrypromise =get_reguserdetails.getcountry();
  countrypromise.then(function(data){
       reg.country = data.data;
   },function(error){
       swal("Server Error","Try again later");
  });
}

reg.adddata = function(data){
    data.push({});
}
reg.delete = function(data,i){
     data.splice(i,1);
}

reg.editprofile1 = function(data){
var editdetailspromise1 = submitProfileData.editprofiledetails1(data,reg.user_details);
    editdetailspromise1.then(function(res){
        if(res.data == "success") {
            swal("Step 1 Completed")
            $state.go('app.editprofilebasic');
        }
        },function(error) {
            swal("Server  Error","Please try later");
        })
    }
reg.editprofile2 = function(data){
    var editdetailspromise2 = submitProfileData.editprofiledetails2(data,reg.user_details);
    editdetailspromise2.then(function(res){
   if(res =="success") {
       swal("Step 2 Completed");
       $state.go("app.editprofileanswer");
   }
   },function(error) {
     swal("Server Error","Please try later");
   })
}

reg.editprofile3 = function(data){
    var editdetailspromise3 = submitProfileData.editprofiledetails3(data.answer);
    editdetailspromise3.then(function(res){
    if (res.data!=null) {
        swal("Personal Information Completed")
        $state.go('app.eipv');
    }
    },function(error) {
        swal("Server Error","Please try later");
    })
   }
   reg.init();
})
