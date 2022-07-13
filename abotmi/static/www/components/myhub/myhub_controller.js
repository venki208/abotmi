angular.module('myhub_controllers',[])

.controller('MyHubCtrl', function($localStorage,$state,$ionicSideMenuDelegate,SweetAlert,$ionicLoading,
    $timeout,$stateParams,MyHubDetails,$ionicLoading,CRISIL_NOT_APPLIED,CRISIL_EXPIRED,
    CRISIL_EXPIRED_BY_USER,CRISIL_APPLIED,TAX_PERCENTAGE_CRISIL,CRISIL_PAYMENT_SUBMITTED,
    CRISIL_RENEWAL_PAYMENT_SUBMITTED,CRISIL_PAYMENT_RE_SUBMIT, CRISIL_VERIFICATION_FAILED,
    CRISIL_RENEWAL_PAYMENT_RE_SUBMIT, CRISIL_CERTIFICATE_VALUE,CRISIL_CERTIFICATE_IN_PROCESS,
    CRISIL_RENEWAL_CERTIFICATE_IN_PROCESS,CRISIL_GOT_CERTIFICATE,DashboardDetailsFactory,MyHubShareData,$location,GUESTURL,socialShare){

    var myhub = this;
    myhub.host = $location.protocol()+"://"+$location.host();
    

    myhub.CRISIL_NOT_APPLIED = CRISIL_NOT_APPLIED;
    myhub.CRISIL_EXPIRED = CRISIL_EXPIRED;
    myhub.CRISIL_EXPIRED_BY_USER = CRISIL_EXPIRED_BY_USER;
    myhub.CRISIL_APPLIED = CRISIL_APPLIED;
    myhub.CRISIL_PAYMENT_SUBMITTED = CRISIL_PAYMENT_SUBMITTED;
    myhub.CRISIL_RENEWAL_PAYMENT_SUBMITTED = CRISIL_RENEWAL_PAYMENT_SUBMITTED;
    myhub.CRISIL_PAYMENT_RE_SUBMIT = CRISIL_PAYMENT_RE_SUBMIT;
    myhub.CRISIL_VERIFICATION_FAILED = CRISIL_VERIFICATION_FAILED;
    myhub.CRISIL_RENEWAL_PAYMENT_RE_SUBMIT = CRISIL_RENEWAL_PAYMENT_RE_SUBMIT;
    myhub.CRISIL_CERTIFICATE_IN_PROCESS = CRISIL_CERTIFICATE_IN_PROCESS;
    myhub.CRISIL_RENEWAL_CERTIFICATE_IN_PROCESS = CRISIL_RENEWAL_CERTIFICATE_IN_PROCESS;
    myhub.CRISIL_GOT_CERTIFICATE = CRISIL_GOT_CERTIFICATE;
    myhub.manageoptions = ["Add","View"];

    myhub.init = function(){
        myhub.now = new Date();
        var getDetails = MyHubDetails.getDetails();
        getDetails.then(function(res){
            myhub.details = res;
            myhub.url = myhub.host + GUESTURL + myhub.details.profile.batch_code;
            MyHubShareData.setDashboardDetails(myhub.details);
            if(myhub.details.advisor.crisil_application_status == CRISIL_NOT_APPLIED){
                myhub.crisilapply = {};
                myhub.crisilapply.crisilyearoptions = [{id:1,value :1}, {id:2,value:2}];
                myhub.crisilapply.selectedcrisilyear = myhub.crisilapply.crisilyearoptions[1].value;
                myhub.crisil_apply_calculate_gross_total();
            }
            else if(myhub.details.advisor.crisil_application_status == CRISIL_APPLIED ||
                    myhub.details.advisor.crisil_application_status == CRISIL_PAYMENT_RE_SUBMIT ||
                    myhub.details.advisor.crisil_application_status == CRISIL_RENEWAL_PAYMENT_RE_SUBMIT ||
                    myhub.details.advisor.crisil_application_status == CRISIL_VERIFICATION_FAILED){
                MyHubShareData.setPayCrisil(myhub.details.advisor.user_profile);
            }
        },function(error){
            swal("Try Again");
        });
    };

    myhub.crisil_apply_calculate_gross_total = function(){
        myhub.crisilapply.crisilgrosstotal = (myhub.crisilapply.selectedcrisilyear == 1) ? CRISIL_CERTIFICATE_VALUE : 3 * CRISIL_CERTIFICATE_VALUE;
        myhub.crisilapply.crisildiscountedgross = myhub.crisilapply.selectedcrisilyear * CRISIL_CERTIFICATE_VALUE;
        myhub.crisilapply.crisilservicetax = (myhub.crisilapply.crisildiscountedgross * TAX_PERCENTAGE_CRISIL)/100;
        myhub.crisilapply.crisilpayable = myhub.crisilapply.crisildiscountedgross + myhub.crisilapply.crisilservicetax;
        MyHubShareData.setApplyCrisil(myhub.crisilapply);
    };

    myhub.init();

    myhub.viewraterank = function(user_type){
        if(myhub.details.otherdetails.total_advisor_rates == 0 && user_type == "advisor"){
            swal("No Advisors Found")
        }else if(myhub.details.otherdetails.total_member_ranks == 0 && user_type == "member"){
            swal("No Clients Found")
        }
        else{
            $ionicLoading.show({
                content: 'Loading',
                animation: 'fade-in',
                showBackdrop: true,
                maxWidth: 200,
                showDelay: 0
            });
            var rankpromise = DashboardDetailsFactory.viewRankDetails(user_type);
            rankpromise.then(function(res){
                $timeout(function () {
                    $ionicLoading.hide();
                }, 1000);
                MyHubShareData.setViewRateRankDetails(res.data,user_type);
                $state.go("app.myhub.viewraterank");
            },function(error){
                $timeout(function () {
                    $ionicLoading.hide();
                }, 1000);
            });
        }
    };
    
    myhub.getStars = function(rating){
       
       
    var val = parseFloat(rating);
    // Turn value into number/100
    var size = val/5*100;
    return size + '%';
    }
    myhub.getStars1 = function(rating1){
       
       
        var val = parseFloat(rating1);
        // Turn value into number/100
        var size = val/5*100;
        return size + '%';
        }
    myhub.viewLoop = function(){
        if(myhub.details.otherdetails.total_reffered_advisor_count == 0){
            swal("No Advisors looped");
        }else{
            $ionicLoading.show({
                content: 'Loading',
                animation: 'fade-in',
                showBackdrop: true,
                maxWidth: 200,
                showDelay: 0
            });
            var viewpromise = DashboardDetailsFactory.viewAdvisorLoop();
            viewpromise.then(function(res){
                $timeout(function () {
                    $ionicLoading.hide();
                }, 1000);
                MyHubShareData.setLoopedAdvisors(res.data);
                $state.go("app.myhub.viewadvisors");
            },function(error)
            {
                $timeout(function () {
                    $ionicLoading.hide();
                }, 1000);
            });
      }
    };

    myhub.viewenquiries = function(type){
        if(myhub.details.otherdetails.total_enquiries == 0 && type == "client") {
            swal("Alert","No Enquiry Found");
        } else if(myhub.details.otherdetails.enquired_members_data_present == 0 && type == "other"){
            swal("Alert","No Enquiry Found");
        } else {
            var viewenquiries = DashboardDetailsFactory.viewEnquiries(type);
            viewenquiries.then(function(res){
                $timeout(function () {
                    $ionicLoading.hide();
                }, 1000);
                MyHubShareData.setViewEnquiries(res.data);
                $state.go("app.myhub.viewenquiries");
            },function(error) {
                $timeout(function () {
                    $ionicLoading.hide();
                }, 1000);
            });
        }
    };

    myhub.manageclients = function(){
        switch(myhub.manageselected){
            case 'Add' : $state.go('app.myhub.add_member'); break;
            case 'View' : myhub.viewClientDetails();break;
            case 'Group' : socialShare.LinkedInShare(url); break;
            case 'Send Mail' : socialShare.googleplusbtn(url); break;
            case 'Transaction' : myhub.showUplyfTransactions();break;
        }
    };
    myhub.socialsharefacebook = function(pageurl){
        socialShare.fb_share(pageurl,"Hi , Have look on my ABOTMI profile");
    }
    myhub.socialsharelinkdeln = function(pageurl){
        socialShare.LinkedInShare(pageurl,"Hi , Have look on my ABOTMI profile");
    }

    myhub.showUplyfTransactions = function(){
        var trans = DashboardDetailsFactory.getTransactions();
        trans.then(function(res){
        if(res.data != ''){
            MyHubShareData.setViewTransactions(res.data);
            $state.go("app.myhub.view_transactions");
        }
        else{
            swal("UPLYF Transactions","No Transactions Found");
        }
        },function(error){
            swal("Error","Try Again");
        });
    };

    myhub.viewClientDetails = function(){
        if (myhub.details.otherdetails.total_members_count == 0 && myhub.details.total_invited_members == 0){
            swal("No Clients");
        }else{
            $ionicLoading.show({
                content: 'Loading',
                animation: 'fade-in',
                showBackdrop: true,
                maxWidth: 200,
                showDelay: 0
            });
            var clientpromise = DashboardDetailsFactory.viewClientDetails();
            clientpromise.then(function(res){
                $timeout(function () {
                    $ionicLoading.hide();
                }, 1000);
                MyHubShareData.setViewMembers(res.member_list);
                MyHubShareData.setViewInvitedMembers(res.invited_member_list);
                $state.go("app.myhub.viewclients");
            },function(error){
                $timeout(function () {
                $ionicLoading.hide();
            }, 1000);
            });
        }
    };

    myhub.getToRatePeersList = function(){
        $ionicLoading.show({
            content: 'Loading',
            animation: 'fade-in',
            showBackdrop: true,
            maxWidth: 200,
            showDelay: 0
        });
        var peerlist = DashboardDetailsFactory.getPeersRateList();
        peerlist.then(function(res){
            $timeout(function () {
                $ionicLoading.hide();
            }, 100);
            if(res.length == 0) {
                swal("Rate Peers","No Records");
            } else{
                MyHubShareData.setRatePeerList(res);
                $state.go("app.myhub.viewratepeers");
            }
        },function(error){
            swal("Error","Try Again");
        });
    };
    myhub.calendlylinkmodule = function(){
        swal("Link can be accessed through web module from app you cannot access","","success");
  
      }

    myhub.add_calendly = function(calendly_saving){
        var save_list = DashboardDetailsFactory.save_calendly_link(calendly_saving);
            save_list.then(function(res){
            swal("Calendly","calendly link saved","success");
            $state.go("app.myhub");
            },function(error){
                swal("Error","Try Again");
            });
    }

    myhub.advisor_video_request = function(){
      var title = myhub.video_title;
      var description = myhub.video_description;
      var location = myhub.location;
      var animation_required = myhub.animation_required;
      var preffered_date_of_shoot = myhub.preffered_date_of_shoot;
      var datetime = new Date(preffered_date_of_shoot);
      var curr_date = datetime.getDate();
      var curr_month = datetime.getMonth()+1;
      var curr_year = datetime.getFullYear();
      var curr_hours = datetime.getHours();
      var curr_minute = datetime.getMinutes();
      var formated_datetime = curr_year+"-"+curr_month+"-"+curr_date+" "+curr_hours+":"+curr_minute;

      var form_date = {
        'title':title,
        'description':description,
        'location':location,
        'preffered_date_of_shoot':formated_datetime,
        'animation_required':animation_required
      }
      MyHubDetails.getvideorequest(form_date).then(function(data){
        if (data) {
            swal({
                 title:'Requested',
                 type:'success',
                 html:'Successfully requested for video shoot'
            },function(response){
                $state.go('app.myhub');
            }, function(error){
                swal('Requested','Unable to reach try some time later!','error')
            });
        }
      });
    }

    myhub.validate_url = true;
    myhub.url_validation = function(url) {
      var p = /^(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?(?=.*v=((\w|-){11}))(?:\S+)?$/;
      return (url.match(p)) ? RegExp.$1 : false;
    }

    myhub.youtube_url_validate = function(url){
      var res_url = myhub.url_validation(url);
      if (res_url != false) {
        myhub.validate_url = false;
      }else{
        myhub.validate_url = true;
      }
    }
    myhub.advisor_video_publish = function(){
      myhub.youtube_url_validate(myhub.video_link)
      if(!myhub.validate_url){
      var video_title = myhub.video_title;
      var video_description = myhub.video_description;
      var video_link = myhub.video_link;
      $ionicLoading.show({
        content: 'Loading',
        animation: 'fade-in',
        showBackdrop: true,
        maxWidth: 200,
        showDelay: 0
    });
      var pattern2 = /(?:http?s?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.+)/g;
      video_url = video_link.replace(pattern2, "https://www.youtube.com/embed/$1");
      MyHubDetails.sendvideopublish(video_title, video_description, video_url).then(
        function(response){
          if (response == 200) {
            $ionicLoading.hide();
            swal({
              title:"success",
              type:'success',
              html:'ok sone is done'
            },function(response){
                $state.go('app.myhub');
            }, function(error){
                $ionicLoading.hide();
                alert("error");
            });
          }
      });
    }
    else{
        
        swal("Error","Please enter valid youtube url"); 
        
    }
    };

})

.controller('CRISILCtrl',function(MyHubShareData,submitData,$state,ionicDatePicker,
  $ionicLoading,$timeout,CRISIL_CERTIFICATE_VALUE,TAX_PERCENTAGE_CRISIL){
    var crisil = this;
    crisil.init = function(){
        crisil.apply = MyHubShareData.getApplyCrisil();
        crisil.paydetails = MyHubShareData.getPayCrisil();
        if(!angular.equals(crisil.paydetails,{})){
            var description = angular.fromJson(crisil.paydetails.payment[4]);
            crisil.paydetails.no_of_years_selected = parseInt(description.no_of_years_selected)+parseInt(description.offered_years);
        }
    };

    crisil.crisil_apply_calculate_gross_total = function(){
        crisil.apply.crisilgrosstotal = (crisil.apply.selectedcrisilyear == 1) ? CRISIL_CERTIFICATE_VALUE : 3 * CRISIL_CERTIFICATE_VALUE;
        crisil.apply.crisildiscountedgross = crisil.apply.selectedcrisilyear * CRISIL_CERTIFICATE_VALUE;
        crisil.apply.crisilservicetax = (crisil.apply.crisildiscountedgross * TAX_PERCENTAGE_CRISIL)/100;
        crisil.apply.crisilpayable = crisil.apply.crisildiscountedgross + crisil.apply.crisilservicetax;
    };

    crisil.confirm_advisor_to_apply_crisil = function(){
        var crisilpromise = submitData.applyCrisil(crisil.apply.selectedcrisilyear);
        crisilpromise.then(function(res){
            swal("CRISIL","Applied for CRISIL","success");
            $state.go("app.myhub");
        });
    };

    crisil.selectDate = function(date){
        ionicDatePicker.openDatePicker(date);
    };

    crisil.selectPayDate = function(val){
        crisil.paydetails.paydate = {
            callback : function(val){
                crisil.paydetails.dateofpay = moment(new Date(val)).format('YYYY-MM-DD');
            }
        };
        crisil.selectDate(crisil.paydetails.paydate);
    };

    crisil.crisil_refdocsubmit = function(){
        $ionicLoading.show({
            content: 'Loading',
            animation: 'fade-in',
            showBackdrop: true,
            maxWidth: 200,
            showDelay: 0
        });
        var crisilformprom = submitData.crisilDocSubmit(crisil.paydetails);
        crisilformprom.then(function(res){
            $timeout(function () {
                $ionicLoading.hide();
                }, 2000);
            crisil.crisil_button = false;
            swal("CRISIL","Payment added successfully.","success");
            $state.go("app.myhub");
            },function(error){
                swal("CRISIL",JSON.stringify(error));
        });
  };

  crisil.downloadprofile = function(){
    var promise = downloadprofile.pdf();
    promise.$promise.then(function(res){
        file = res.response;
        var fileName = "crisil_certificate.pdf";
        var reader = new window.FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = function() {
            var base64data = reader.result;
            window.location.href = "downloadpdf://"+fileName+","+base64data;
        }
    });
  };

    crisil.init();
})

.controller('RatingRankingCtrl',function(submitData,$stateParams,$state,$window,
    DashboardDetailsFactory,MyHubShareData,$ionicLoading,$timeout){
    var raterank = this;
    var iti;
    raterank.request = {};
    raterank.rateproperty = {};
    var refresh = $stateParams.is_rated;

    raterank.init = function(){
        raterank.viewdetails = MyHubShareData.getViewRateRankDetails();
        raterank.ratepeerlist = MyHubShareData.getRatePeerList();
        raterank.rateproperty = MyHubShareData.getRatePeer();
        if(refresh == "rated"){
            $ionicLoading.show({
                content: 'Loading',
                animation: 'fade-in',
                showBackdrop: true,
                maxWidth: 200,
                showDelay: 0
            });
            var peerlist = DashboardDetailsFactory.getPeersRateList();
            peerlist.then(function(res){
                $timeout(function () {
                    $ionicLoading.hide();
                }, 1000);
                if(res == " ")
                {
                    swal("Rate Peers","No Records");
                }
                else{
                    raterank.ratepeerlist = res;
                }
            },function(error){
                swal("Error","Try Again");
            });
        }
    };

    raterank.enableDetails =function()
            {
              var input = document.querySelector("#phone");
        

      iti=intlTelInput(input, {
            nationalMode: false,
            initialCountry: "us",
            separateDialCode: true,
            autoPlaceholder: "off",
            
            utilsScript: "intl-tel-input/build/js/utils.js"
        });
        
            }

    raterank.init();

    raterank.requesttype = $stateParams.requesttype;
    if(raterank.requesttype == "advisor"){
        raterank.title = "INVITE PEER TO RATE";
    } else {
        raterank.title = "INVITE CLIENT TO RANK";
    }

    raterank.goBack = function(){
        $window.history.back();
    }

    raterank.inviterateSubmit = function(inviteform){
        var isValid = iti.isValidNumber();
           if(!isValid){
            swal("please select valid number","","error")
           }
           
    
           else{
            var number = iti.getNumber();
            raterank.request.mobile = number
        var invitepeerpromise = submitData.inviteRate(raterank.request,raterank.requesttype);
        invitepeerpromise.then(function(res){
            if(res.data == "success"){
                swal("Invite",res.data,"success");
                $state.go('app.myhub');
            } else {
                swal("Invite",res.data,"error");
                raterank.request="";
                inviteform.$setPristine();
                inviteform.$setUntouched();
            }
        },function(error){
            swal("Invite Failed","Try Again");
            $state.go('app.myhub');
        });
    }
    };

    raterank.avgcal = function(){
      raterank.rateproperty.avgrate =  (raterank.rateproperty.trust+raterank.rateproperty.financial+raterank.rateproperty.comm+raterank.rateproperty.ethics+raterank.rateproperty.advisory+raterank.rateproperty.ccare)/6;
    };

    raterank.rateModalSubmit = function(activationkey){
      raterank.rateproperty.trust = null;
      raterank.rateproperty.financial = null;
      raterank.rateproperty.comm = null;
      raterank.rateproperty.advisory = null;
      raterank.rateproperty.ccare = null;
      raterank.rateproperty.ethics = null;
      raterank.rateproperty.avgrate = 0;
      raterank.rateproperty.activationkey = activationkey;
      MyHubShareData.setRatePeer(raterank.rateproperty);
      $state.go("app.myhub.viewratepeers.ratepeers");
    };

    raterank.submitRating = function(data){
      var avgratepromise = submitData.submitRating(data);
      avgratepromise.then(function(res){
            raterank.rateproperty.activationkey = "";
            swal("Advisor Rate","Rated successfully");
            $state.go("app.myhub.viewratepeers",{'is_rated':'rated'});
      },function(error){
          swal("Rate","Rate Failed","error");
      });
    };
})

.controller('AdvisorCtrl',function(submitData,$state,DashboardDetailsFactory,
  MyHubShareData,$ionicLoading,$timeout){
    var advisor = this;
    var iti;
    advisor.advisor_boolen = false;
    advisor.refer = {};
    advisor.refer.products = "";
    advisor.refer.is_registered = -1;
    advisor.refer.sebi = "";
    advisor.refer.amfi = "";
    advisor.refer.irda = "";
    advisor.refer.crisilnumber = "";
    advisor.refer.knownduration;
    advisor.refer.justify = "";

    advisor.init = function(){
        advisor.referred_advisor_details_list = MyHubShareData.getLoopedAdvisors();
    };
    advisor.init();

    advisor.enableDetails =function()
    {
      var input = document.querySelector("#phone");


iti=intlTelInput(input, {
    nationalMode: false,
    initialCountry: "us",
    separateDialCode: true,
    autoPlaceholder: "off",
    
    utilsScript: "intl-tel-input/build/js/utils.js"
});

    }
    advisor.referAdvisorSubmit = function(){
        var isValid = iti.isValidNumber();
           console.log(isValid);
           if(!isValid){
            swal("please select valid number","","error")
           }
           
    
           else{
            var number = iti.getNumber();
            advisor.refer.mobile = number
        $ionicLoading.show({
            content: 'Loading',
            animation: 'fade-in',
            showBackdrop: true,
            maxWidth: 200,
            showDelay: 0
        });
        var referpromise = submitData.referAdvisor(advisor.refer);
        referpromise.then(function(res){
            $timeout(function () {
                $ionicLoading.hide();
            }, 1000);
            if(res.data == "success"){
                swal("Success","Advisor Referred", "success");
                $state.go('app.myhub');
            }
            else{
                swal("Alert","You cannot loop/refer yourself","error");
                advisor.refer = "";
                advisor.looplist.$setPristine();
            }
        },function(payloaderror){
            $timeout(function () {
                $ionicLoading.hide();
            }, 1000);
            swal("Failed","Try Again","error");
            $state.go('app.myhub');
        });
    }
    };

    advisor.check_refer_email = function(data){
        var checkemail = DashboardDetailsFactory.check_refer_email(data);
        checkemail.then(function(res){
            if(res.data != "success"){
                swal("Error",res.data,"error");
                advisor.advisor_boolen = true;
                
            }
            else{
                advisor.advisor_boolen = false;
            }
        },function(error){

        });
    };
})

.controller('meetup_viewCtrl',function(meetup_factory,$state,$ionicLoading,$timeout,$ionicPopup){
        var meetupview = this;
        meetupview.delete_meetup_event = function(res_event) {
            var confirmPopup = $ionicPopup.confirm({
                cssClass: 'my-custom-popup',
                title: 'Are you sure ?'
            });

            confirmPopup.then(function(res) {
                if (res) {
                    $ionicLoading.show({
                        content: 'Loading',
                        animation: 'fade-in',
                        showBackdrop: true,
                        maxWidth: 200,
                        showDelay: 0
                    });
                    var meetup_viewpromise = meetup_factory.meetup_delete(res_event);
                    meetup_viewpromise.then(function(response) {
                        if (response.data.status = true) {
                            $timeout(function() {
                                $ionicLoading.hide();
                            }, 1000);
                            swal("Deleted the event successfully", "", "success");
                            meetupview.meetupevents();
                        } else {
                            $timeout(function() {
                                $ionicLoading.hide();
                            }, 1000);
                            swal("meetup", "Deleted the event unsuccessfull");
                        }

                    }, function(error) {
                        $timeout(function() {
                            $ionicLoading.hide();
                        }, 1000);
                        swal("Failed try again", JSON.stringify(error.data));
                    });
                }
            });
        };
        meetupview.update_meetup_event = function(data){
            $state.go('app.myhub.meetup',{'data':data});
        }
        meetupview.meetupevents = function(){
            $ionicLoading.show({
                content: 'Loading',
                animation: 'fade-in',
                showBackdrop: true,
                maxWidth: 200,
                showDelay: 0
              });
            var meetup_viewpromise = meetup_factory.get_meetup_list();
            meetup_viewpromise.then(function(response){
                $timeout(function () {
                    $ionicLoading.hide();
                    }, 1000);
                meetupview.details=response.data;

            },function(error){
                $timeout(function () {
                    $ionicLoading.hide();
                    }, 1000);
                swal("Failed try again",JSON.stringify(error.data));
            });
        };
        meetupview.meetupevents();
})

.controller('webinar_viewCtrl', function(webinar_factory, $state,$ionicLoading,
  $timeout,$ionicPopup,$ionicLoading) {
    var webinarview = this;
    webinarview.init = function(){
        webinarview.webinarevents();
    };
    webinarview.toast_message = function(){
        $ionicLoading.show({
            template: 'Coming soon...',
            noBackdrop: true,
            duration: 1500
        });
    }

    webinarview.delete_webinar_event = function(id) {
        var confirmPopup = $ionicPopup.confirm({
            cssClass: 'my-custom-popup',
            title: 'Are you sure ?'
         });
         confirmPopup.then(function(res) {
            if(res) {
                $ionicLoading.show({
                    content: 'Loading',
                    animation: 'fade-in',
                    showBackdrop: true,
                    maxWidth: 200,
                    showDelay: 0
                });
                var webinar_viewpromise = webinar_factory.webinar_delete(id);
                webinar_viewpromise.then(function(res) {
                    webinar_viewpromise.details = res.data;
                    if (res.data == "success") {
                        $timeout(function () {
                            $ionicLoading.hide();
                            }, 1000);
                        swal("Deleted the event successfully", "", "success");
                        get_webinar_list_from_factory();
                    } else {
                        $timeout(function () {
                            $ionicLoading.hide();
                            }, 1000);
                        swal("Deleted the event unsuccessfull", "");
                    }
                }, function(error) {
                    $timeout(function () {
                        $ionicLoading.hide();
                        }, 1000);
                    swal("Failed try again","","error");
                });
            }
        });
    }

    webinarview.webinarevents = function() {
        $ionicLoading.show({
            content: 'Loading',
            animation: 'fade-in',
            showBackdrop: true,
            maxWidth: 200,
            showDelay: 0
          });
        get_webinar_list_from_factory();
    }

    webinarview.init();
    function get_webinar_list_from_factory(){
        var webinar_viewpromise = webinar_factory.get_webinar_list();
        webinar_viewpromise.then(function(response) {
            $timeout(function () {
                $ionicLoading.hide();
                }, 1000);
            if (response.data.length> 0) {
              webinarview.details = response.data;
              webinarview.details_data = true;
            }else {
              webinarview.details_data = false;
            }
        }, function(error) {
            swal("Failed try again", JSON.stringify(error.data));
        });
    }
})

.controller('meetup_listmailCtrl', function($state,meetup_factory,$ionicLoading,$timeout) {
    var meetuplist = this;
    meetuplist.obj_data = {};
    meetuplist.selected = [];
    meetuplist.toggle = function(item, list) {
    var checkboxs=document.getElementsByName("email_list");
    var validation_checkbox=false;
    for(var i=0,l=checkboxs.length;i<l;i++) {
        if(checkboxs[i].checked) {
            validation_checkbox=true;
            break;
        }
    }
    if(validation_checkbox) {
        document.getElementById('btn').disabled = false;
    } else {
        document.getElementById('btn').disabled = true;
    }
        var idx = list.indexOf(item);
        if (idx > -1) {
            list.splice(idx, 1);
        } else {
            var cr_text = item.first_name + "," + item.email + "," + item.mobile;
            list.push(cr_text);
        }
    };

    meetuplist.exists = function(item, list) {
          return list.indexOf(item) > -1;
    };
    meetuplist.submit = function() {
        $ionicLoading.show({
            content: 'Loading',
            animation: 'fade-in',
            showBackdrop: true,
            maxWidth: 200,
            showDelay: 0
          });
        var meetuppromiseinvitation = meetup_factory.sendinvitationmail(meetuplist.selected);
        meetuppromiseinvitation.then(function(res) {
            if (res.response == "success") {
                $timeout(function () {
                    $ionicLoading.hide();
                    }, 1000);
                swal("meetup invitation sent", "", "success");
                $state.go('app.myhub.view_meetup');
            } else {
                $timeout(function () {
                    $ionicLoading.hide();
                    }, 1000);
                swal("meetup", "You have entered wrong email id please try again");
            }
        }, function(error) {
            $timeout(function () {
                $ionicLoading.hide();
                }, 1000);
        });
    }
    meetuplist.meetuplistmail = function() {
        $ionicLoading.show({
            content: 'Loading',
            animation: 'fade-in',
            showBackdrop: true,
            maxWidth: 200,
            showDelay: 0
          });
        var meetup_viewpromise = meetup_factory.get_email_list();
        meetup_viewpromise.then(function(response) {
            $timeout(function () {
                $ionicLoading.hide();
                }, 1000);
            meetuplist.details = response.data;
        }, function(error) {
            $timeout(function () {
                $ionicLoading.hide();
                }, 1000);
            swal("Failed try again", JSON.stringify(error.data));
        });
    };
    meetuplist.meetuplistmail();
})

.controller('webinar_listmailCtrl', function($state,webinar_factory,$stateParams,$ionicLoading,$timeout) {
   var webinarlist = this;
   webinarlist.register_member = function(index_val,name,email,room_id) {
    $ionicLoading.show({
        content: 'Loading',
        animation: 'fade-in',
        showBackdrop: true,
        maxWidth: 200,
        showDelay: 0
      });
        var mem_details = name + ','+email+ ','+room_id;
        var webinar_data = webinarlist.details.advisor_data[index_val];
        var webinarpromiseinvitation = webinar_factory.register_invitation(mem_details);
       webinarpromiseinvitation.then(function(res) {
            if (res.data =="success") {
                $timeout(function () {
                    $ionicLoading.hide();
                    }, 1000);
                swal("webinar invitation sent ", "", "success");
                webinar_data.disabled = true;
                webinar_data.reg_status = "Registered";
            } else {
                swal("Event has been Expired","","danger");
                $timeout(function () {
                    $ionicLoading.hide();
                    }, 1000);
            }
        }, function(error) {
            $timeout(function () {
                $ionicLoading.hide();
                }, 1000);
        });
    }

    webinarlist.register_member_data = function(index_val,name,email,room_id) {
     $ionicLoading.show({
         content: 'Loading',
         animation: 'fade-in',
         showBackdrop: true,
         maxWidth: 200,
         showDelay: 0
       });
         var mem_details = name + ','+email+ ','+room_id;
         var webinar_data_member = webinarlist.details.member_data[index_val];
         var webinarpromiseinvitation = webinar_factory.register_invitation(mem_details);
        webinarpromiseinvitation.then(function(res) {
             if (res.data =="success") {
                 $timeout(function () {
                     $ionicLoading.hide();
                     }, 1000);
                 swal("webinar invitation sent ", "", "success");
                 webinar_data_member.disabled = true;
                 webinar_data_member.reg_status = "Registered";

             } else {
                 swal("Event has been Expired","","danger");
                 $timeout(function () {
                     $ionicLoading.hide();
                     }, 1000);
             }
         }, function(error) {
             $timeout(function () {
                 $ionicLoading.hide();
                 }, 1000);
         });
     }

    webinarlist.webinarlistmail = function() {
        $ionicLoading.show({
            content: 'Loading',
            animation: 'fade-in',
            showBackdrop: true,
            maxWidth: 200,
            showDelay: 0
          });
        var room_id = $stateParams.room_id;
        var webinar_viewpromise = webinar_factory.list_webinar(room_id);
        webinar_viewpromise.then(function(response) {
            $timeout(function () {
                $ionicLoading.hide();
                }, 1000);
            webinarlist.details = response.data;
        }, function(error) {
            swal("Failed try again", JSON.stringify(error.data));
            $timeout(function () {
                $ionicLoading.hide();
                }, 1000);
        });
    };
    webinarlist.webinarlistmail();
})


.controller('webinarCtrl', function(submitData,Project_Details_Uplyf,webinar_factory,
    $state,$filter,$ionicLoading,$timeout) {
    var webinar = this;
    var today = new Date();
    webinar.now = new Date(today.setHours(today.getHours()+1));
    webinar.getprojectdetails = function() {
        var webinarpromise = Project_Details_Uplyf;
        var data1 = []
        webinarpromise.then(function(response) {
            webinar.details = response.data;
            for(var i = 0; i<response.data.length; i++){
                data1.push(response.data[i].project_name +"-"+ response.data[i].project_id);
            }
            webinar.details = data1
        }, function(error) {
            swal("Failed try again", JSON.stringify(error.data));
        });

    };

    webinar.get_room_name = function() {
        $ionicLoading.show({
            content: 'Loading',
            animation: 'fade-in',
            showBackdrop: true,
            maxWidth: 200,
            showDelay: 0
          });

        webinar_factory.get_room_name(webinar.details.name).then(
            function(res_data) {
                webinar.details.room_name=res_data.data;
            if ( res_data.data == "true") {
                $timeout(function () {
                    $ionicLoading.hide();
                    }, 1000);
                    webinar.details.room_name=res_data.data;
            } else {
                $timeout(function () {
                    $ionicLoading.hide();
                    }, 1000);
            }
        }, function(error) {
            swal("Failed try again", JSON.stringify(error.data));
            $timeout(function () {
                $ionicLoading.hide();
                }, 1000);
        });
    }

    webinar.submit = function() {
        $ionicLoading.show({
            content: 'Loading',
            animation: 'fade-in',
            showBackdrop: true,
            maxWidth: 200,
            showDelay: 0
          });

        var newDate = new Date(webinar.details.datetimeValue);
        if (!webinar.details.uplyf_project) {
            webinar.details.uplyf_project="";
        }

        webinar.details.formatted_date = $filter('date')(newDate, "yyyy-MM-dd HH:mm:ss");
        var webinarpromise = submitData.webinar(webinar.details);
        webinarpromise.then(function(res) {
            if (res.data == "success") {
                $timeout(function () {
                    $ionicLoading.hide();
                    }, 1000);
                swal({
                    title:"Webinar event created successfully",
                    html:"Webinar event created successfully",
                    type:"success"
                },function(response){
                    $state.go('app.myhub.view_webinar');
                });
            } else {
                $timeout(function () {
                    $ionicLoading.hide();
                    }, 1000);
                swal("Webinar event not created successfully", "");
                webinar.details = '';
            }
        }, function(error) {
            $timeout(function () {
                $ionicLoading.hide();
                }, 1000);
            swal("Failed try again", JSON.stringify(error.data));
        });
    }
    webinar.getprojectdetails();
})

.controller('meetupCtrl', function(submitData,Project_Details_Uplyf,$state,$stateParams,$filter,$ionicLoading,$timeout) {
    var meetup = this;
    var index = $stateParams.data;
    meetup.details="";
    meetup.update = false;
    meetup.convertMS = function(milliseconds) {
        var day, hour, minute, seconds;
        seconds = Math.floor(milliseconds / 1000);
        minute = Math.floor(seconds / 60);
        seconds = seconds % 60;
        hour = Math.floor(minute / 60);
        minute = minute % 60;
        day = Math.floor(hour / 24);
        hour = hour % 24;
        hour = hour.toString();
        minute = minute.toString();
        meetup.details.hours=hour;
        meetup.details.minutes=minute; 
    }
    if(index){
    meetup.update = true;    
    meetup.details = JSON.parse(index);
    meetup.details.landmark=meetup.details.meetup_landmark;
    meetup.details.location = meetup.details.meetup_location;
    meetup.details.datetimeValue = meetup.details.scheduled;
    meetup.convertMS(meetup.details.duration);
    }
    meetup.getprojectdetails = function() {
        var meetuppromise = Project_Details_Uplyf;
        var data1 = []
        var hours = []
        var minutes=[]
        meetup.projdata="";
        var today = new Date();
        meetup.now = new Date(today.setHours(today.getHours()+1));
        meetuppromise.then(function(response) {
            meetup.details.projdata = response.data;
            for(var i = 0; i<response.data.length; i++){
                data1.push(response.data[i].project_name +"-"+ response.data[i].project_id);
            }
            meetup.projdata = data1;
            meetup.hours = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24"];
            meetup.minutes = ["5","10","15","20","25","30","35","40","45","50","55","60"];

        }, function(error) {
            swal("Failed try again", JSON.stringify(error.data));
        });
    };

    meetup.submit = function() {
        $ionicLoading.show({
            content: 'Loading',
            animation: 'fade-in',
            showBackdrop: true,
            maxWidth: 200,
            showDelay: 0
          });
         
        var newDate = new Date(meetup.details.datetimeValue);
        meetup.details.formatted_date = $filter('date')(newDate, "yyyy-MM-dd HH:mm:ss");
        if(meetup.update){
            var meetupupdateppromise = submitData.updatemeetup(meetup.details);
            meetupupdateppromise.then(function(response) {
                if (response.data == "success") {
                    $timeout(function () {
                        $ionicLoading.hide();
                        }, 1000);
                    swal("Meetup event updated successfully", "", "success");
                    $state.go('app.myhub.view_meetup');
                } else {
                    $timeout(function () {
                        $ionicLoading.hide();
                        }, 1000);
                    swal("meetup", "Geeting Details Failed");
                    meetup.details = '';
                }
            }, function(error) {
                $timeout(function () {
                    $ionicLoading.hide();
                    }, 1000);
                swal("Failed try again", "", "error");
            });
            
        }else{
            var meetuppromise = submitData.meetup(meetup.details);
        meetuppromise.then(function(response) {
            if (response.data == "success") {
                $timeout(function () {
                    $ionicLoading.hide();
                    }, 1000);
                swal("Meetup event created successfully", "", "success");
                $state.go('app.myhub.view_meetup');
            } else {
                $timeout(function () {
                    $ionicLoading.hide();
                    }, 1000);
                swal("meetup", "Geeting Details Failed");
                meetup.details = '';
            }
        }, function(error) {
            $timeout(function () {
                $ionicLoading.hide();
                }, 1000);
            swal("Failed try again", "", "error");
        });
    }

        }
        
    meetup.getprojectdetails();
})

.controller('EnquiryCtrl',function(MyHubShareData){
    var enquiry = this;
    enquiry.init = function(){
        enquiry.details = MyHubShareData.getViewEnquiries();
    };
    enquiry.init();
})

.controller('ClientMgmtCtrl',function(MyHubShareData,submitData,adharverify,AADHAAR_BRIDGE_API,$state,$window){
    var client = this;
    client.AADHAAR_BRIDGE_API = AADHAAR_BRIDGE_API;
    client.init = function(){
        client.details = MyHubShareData.getDashboardDetails();
        client.transaction_details = MyHubShareData.getViewTransactions();
        client.member_list = MyHubShareData.getViewMembers();
        client.invited_member_list = MyHubShareData.getViewInvitedMembers();
    };
    client.init();

    client.clearMemberForm = function(form){
        client.addmember_form="";
        form.$setPristine();
        form.$setUntouched();
    }

    client.addClientThroughForm = function(addmember_form){
        if(client.addmember_form.email == client.details.advisor.user_profile.email){
            swal("Error","You cannot add yourself");
            client.clearMemberForm(addmember_form);
        }
        else {
            var add = submitData.addClient(client.addmember_form,"form");
            add.then(function(res){
                if(res.status==201){
                    swal("Client got added successfully","","success");
                    $state.go('app.myhub');
                }
                else if (res.status == 200){
                    swal("Client already exists","","error");
                }
                else  if(res.status == 202){
                    swal("The advisor is already looped and registered in ABOTMI","","error");
                }
                else if(res.status == 203 ) {
                    swal("Client is already registered in UPLYF","","error");
                }
                else{
                    swal("Error",res.data);
                    client.clearMemberForm(addmember_form);
                }
            },function(error){
                swal("Error","Please try again");
                client.clearMemberForm(addmember_form);
            });
        }
    };
    client.reset_add_client = false;
    client.reset_emailform = function(data){
        if (data) {
            client.reset_add_client = true;
            client.addmember_form.first_name = '';
            client.addmember_form.last_name = '';
            client.addmember_form.mobile = '';
            client.addmember_form.email = '';
            client.addmember_form.add_agree = '';
        }
    }

    client.addmember_thruaadhaar = function(addmember_aadhaar){
        var promise = adharverify.verify(client.aadhar_no,"member");
        promise.then(function(res){
            if(res.aadhaar_no) {
                swal("Aadhar Number Already Exist in UPLYF");
            } else {
                client.aadhaar_form = res;
                setTimeout(function() {
                var submitform = $window.document.forms['client.aadhar_form'].submit();
                }, 1500);
            }
        },function(error){
            if(error.status == 400){
                swal('Error',error.data.data);
                client.aadhar_no="";
                addmember_aadhaar.$setPristine();
                addmember_aadhaar.$setUntouched();
            }
        });
    };

    client.create_member_through_aadhar = function(){
        client.add_aadhaar.aadhaar_transaction_id = $stateParams.trans_id;
        var create = submitData.addClient(client.add_aadhaar,"aadhaar");
        create.then(function(res){
            if(res.status==200 || res.status==201){
                swal("Success",res.data);
            } else{
                swal("Error",res.data);
            }
        },function(error){
            swal("Error","Please try again");
        });
    };

    client.set_alternative_email = function(){
        if(client.add_aadhaar.checbox_value){
            client.add_aadhaar.alternate_email = client.add_aadhaar.email;
        } else{
            client.add_aadhaar.alternate_email = "";
        }
    };
})
