angular.module('reiaapp')

.run(function($state,$rootScope,$ionicLoading,$localStorage,$ionicNavBarDelegate,$interval,jwtHelper,RefreshTokenFactory){

	$rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams){
		if (toState.name == 'app.myhub' || toState.name == 'app.myidentity' || toState.name == 'app.mygrowth') {
			$ionicLoading.show({
				content: 'Loading',
				animation: 'fade-in',
				showBackdrop: true,
				maxWidth: 200,
				showDelay: 0,
				duration: 2000
			});
		}
	})

	$interval(function(){
		if(localStorage.getItem('jwttoken')){
			var istokenexpired = (jwtHelper.getTokenExpirationDate(localStorage.getItem('jwttoken')).getTime() - moment(new Date().getTime()))/(1000*60)%60;
			if(istokenexpired < 60){ ////if expiration time is lesser than threshold (here 1 hr), refresh the token
				//call refresh token
				newtoken = RefreshTokenFactory.getToken();
				newtoken.then(function(response){
					localStorage.removeItem('jwttoken');
					localStorage.setItem('jwttoken',response.token);
				},function(error){
					swal("Error","Try Again");
				});
			}
		}
	},25200*1000) //call refresh token every 7 hours 25200*1000
})

//To place tabs in top
.config(function($ionicConfigProvider){
	$ionicConfigProvider.tabs.position('top');
	$ionicConfigProvider.scrolling.jsScrolling(false);
})

//Ionic Datepicker configuration , cache and javascript scroll
.config(function(ionicDatePickerProvider,$ionicConfigProvider){
	var datePickerObj = {
		inputDate : new Date(),
		titleLabel : 'Select a Date',
		setLabel: 'Set',
        todayLabel: 'Today',
        closeLabel: 'Close',
        templateType: 'popup',
        to: new Date(),
        showTodayButton: true,
        dateFormat: 'yyyy-MM-dd'
	};
	ionicDatePickerProvider.configDatePicker(datePickerObj);
    $ionicConfigProvider.views.maxCache(0);
    $ionicConfigProvider.scrolling.jsScrolling(false);
})

.config(function ( $httpProvider) {
    delete $httpProvider.defaults.headers.common['X-Requested-With'];
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
})

//To allow as trusted urls
.config(function($sceDelegateProvider,AADHAAR_BRIDGE_API) {
 $sceDelegateProvider.resourceUrlWhitelist([
   // Allow same origin resource loads.
   'self',
   // Allow loading from our assets domain.  Notice the difference between * and **.
   AADHAAR_BRIDGE_API]);
 })

//Router Configuration
.config(['$stateProvider','$urlRouterProvider','$compileProvider',function($stateProvider,$urlRouterProvider,$compileProvider){
	$compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|chrome-extension|whatsapp):/);
	$stateProvider

	.state('redirect',{
		url:'/redirect/:socialapp',
		controller : 'RedirectCtrl',
		resolve:{
			result : function(SignupLoginFactory){
				return SignupLoginFactory.is_reg_user_redirect();
			}
		}
	})

	.state('login',{
		url:'/login',
		templateUrl : 'components/signup_login/signup_login.html',
		controller : 'SignupLoginCtrl',
		controllerAs : 'login',
		params:{
			socialapp : null
		}
	})

 	.state('introduction',{
		 url:'/introduction',
		templateUrl : 'components/intro_screens/intro_screens.html',
		controller : 'IntroCtrl',
		controllerAs : 'introCtrl',
		params:{
			socialapp : null
		}
	})

  .state('start',{
        url :'/start',
        templateUrl :'templates/startapp.html',
        controller : 'TrackCtrl',
        controllerAs : 'track',
        abstract : true,
  })

  .state('start.video',{
         url:'/video',
         cache : false,
         views :{
             'content' : {
                  templateUrl : 'components/video_process/video.html',
                  controller : 'videoCtrl',
              	  controllerAs : 'video'
             }
         }
   })


  

   .state('app.mygrowth',{
	     url:'/mygrowth',
	     cache : false,
	     views :{
		        'content' : {
			           templateUrl : 'components/mygrowth/mygrowth.html',
			           controller : 'mygrowthCtrl',
			           controllerAs : 'mygrowth'
		         }
	      }
   })
  .state('start.help',{
      url:'/help',
      views :{
          'content' : {
              templateUrl : 'templates/help.html',
              controller:'sideMunuCtrl',
              controllerAs:'sidemenu'
          }
      },
      params:{
        'status':null
      }
  })

 .state('start.eipv',{
     url :'/eipv',
     views :{
         'content':{
             templateUrl:'components/eipv_process/eipv.html',
             controller :'EipvCtrl',
             controllerAs :'eipvprocess'
         }
     }
 })

 .state('app.eipv_verification',{
	url :'/eipv_verification',
	views :{
			'content':{
					templateUrl:'components/eipv-verification-step2/eipv_verification_step2.html',
					controller :'EipvCtrl_step2',
					controllerAs :'eipvprocess_step2'
			}
	}
})


 .state('email-otp',{
	url:'/email-otp',
	templateUrl:'components/email_otp/email_otp.html',
	controller :'EmailCtrl',
	controllerAs :'emailotpprocess',
 params:{
	'emailid' : null,'first_name':null,'password':null,'last_name':null,'source':null,'gender':null,'next_url':null
 }
})
 
// .state('start.email-otp',{
// 	url:'/email-otp',
// 	views :{
// 		'content':{
// 	templateUrl:'components/email_otp/email_otp.html',
// 	controller :'EmailCtrl',
// 	controllerAs :'emailotpprocess'
// 		}
// 	},
// 	params: {'emailid' : null,'first_name':null,'password':null,'last_name':null,'source':null,'gender':null,'next_url':null}
	
// })

 .state('start.settings',{
     url:'/settings',
     views :{
         'content' : {
             templateUrl : 'templates/settings.html'
         }
     }
   })
 .state('start.terms',{
     url:'/term',
     views :{
         'content' : {
             templateUrl : 'templates/terms.html',
             controller:'sideMunuCtrl',
             controllerAs:'sidemenu'
         }
     },
     params:{
        'status':null
     }
 })
 .state('start.whytoregister',{
     url:'/whytoregister',
     views :{
         'content' : {
             templateUrl : 'templates/whytoregister.html'
         }
     }
 })
 .state('start.faq',{
     url:'/faq ',
     views :{
         'content' : {
             templateUrl:'templates/faq.html',
             controller:'sideMunuCtrl',
             controllerAs:'sidemenu'
         }
     },
     params:{
        'status':null
     }
 })
 .state('start.privacypolicy',{
 	url:'/privacypolicy',
 	views:{
 		'content' : {
 			templateUrl : 'templates/privacypolicy.html',
 	  controller:'sideMunuCtrl',
 	  controllerAs:'sidemenu'
 	}
 	},
   params:{
 	'status':null
   }
 })


.state('app.myhub.why_to_add_client',{
	url:'/why_to_add_client',
	cache : true,
	views:{
		'content@app':{
			templateUrl : 'components/myhub/why_to_add_client.html'
		}
	}
})

.state('app.myhub.how_to_add_client',{
	url:'/how_to_add_client',
	cache : true,
	views:{
		'content@app':{
			templateUrl : 'components/myhub/how_to_add_client.html'
		}
	}
})

.state('app.myhub.benefits_of_add_client',{
	url:'/benefits_of_add_client',
	cache : true,
	views:{
		'content@app':{
				templateUrl : 'components/myhub/benefits_of_add_client.html'
		}
	}
})

.state('app.myhub.add_client_terms_conditions',{
	url:'/add_client_terms_conditions',
	cache : true,
	views:{
		'content@app':{
				templateUrl : 'components/myhub/add_client_terms_conditions.html'
		}
	}
})

  .state('app',{
		url :'/app',
		templateUrl :'templates/tabs.html',
		controller : 'TrackCtrl',
		controllerAs : 'track',
abstract : true,		
	})


	.state('app.myidentity',{
		url :'/myidentity',
		views :{
			'content':{
				templateUrl :'components/myidentity/myidentity.html',
				controller : 'MyIdentityCtrl',
				controllerAs : 'mytrack'
			}
		}
	})
  .state('app.myidentity.edit',{
          url:'/myidentity/edit',
          views :{
              'content@app':{
                  templateUrl :'components/myidentity/editprofile.html',
                  controller :'EditCtrl',
                  controllerAs:'edit'
              }
          },
          params:{
              'editstep':null,
			        'data':null,
              'heading':null
          }
  })
  .state('app.myhub',{
		url:'/myhub',
		views:{
			'content':{
				templateUrl : 'components/myhub/myhub.html',
				controller : 'MyHubCtrl',
				controllerAs : 'myhub'
			}
		}
	})

	.state('app.repute',{
		url:'/repute',
		views:{
			'content':{
				templateUrl : 'templates/repute.html'
			}
		}
	})

	.state('app.myhub.post',{
		url:'/post/:id',
		views:{
			'content@app':{
				templateUrl : 'templates/icorepostview.html',
				controller : 'ICORECtrl',
				controllerAs : 'icore'
			}
		}
	})

	.state('app.myhub.createpost',{
		url:'/createpost',
		views:{
			'content@app':{
				templateUrl : 'templates/addicorepost.html',
				controller : 'ICOREAddPostCtrl',
				controllerAs : 'addpost'
			}
		}
	})

	.state('app.myhub.requestrate',{
		url:'/requestrate',
		views:{
			'content@app':{
				templateUrl : 'components/myhub/requestrate.html',
				controller : 'RatingRankingCtrl',
				controllerAs : 'raterank'
			}
		},
		params :{
			requesttype:null
		}
	})

	.state('app.myhub.makepayment',{
		url:'/makepayment',
		views:{
			'content@app':{
				templateUrl : 'components/myhub/crisilpaymentdetails.html'
			}
		}
	})

	.state('app.myhub.crisiltermsconditions',{
		url:'/crisiltermsconditions',
		views:{
			'content@app':{
				templateUrl : 'components/myhub/crisiltermsconditions.html'
			}
		}
	})

	.state('app.myhub.calendly',{
		url:'/calendly',
		views:{
			'content@app':{
				templateUrl : 'components/myhub/calendly.html',
				controller : 'MyHubCtrl',
				controllerAs : 'myhub'
			}
		}
	})

	

	.state('app.myhub.crisilfaq',{
		url:'/crisilfaq',
		views:{
			'content@app':{
				templateUrl : 'components/myhub/crisilfaq.html'
			}
		}
	})

	.state('app.myhub.microlearninghelp',{
		url:'/microlearninghelp',
		views:{
			'content@app':{
				templateUrl : 'components/myhub/micro_learning_help.html'
			}
		}
	})

	.state('app.myhub.microlearningtc',{
		url:'/microlearningtc',
		views:{
			'content@app':{
				templateUrl : 'components/myhub/micro_learning_termsandconditions.html'
			}
		}
	})

	.state('app.myhub.db_how_it_work',{
		url:'/db_how_it_work',
		views:{
			'content@app':{
				templateUrl : 'components/myhub/db_how_it_work.html'
			}
		}
	})

	.state('app.myhub.calendly_how_it_work',{
		url:'/calendly_how_it_work',
		views:{
			'content@app':{
				templateUrl : 'components/myhub/calendly_how_it_work.html',
				controller : 'MyHubCtrl',
				controllerAs : 'myhub'
			}
		}
	})

	.state('app.myhub.micro_faq',{
		url:'/micro_faq',
		views:{
			'content@app':{
				templateUrl : 'components/myhub/micro_faq.html'
			}
		}
	})

	.state('app.myhub.db_faq',{
		url:'/db_faq',
		views:{
			'content@app':{
				templateUrl : 'components/myhub/db_faq.html'
			}
		}
	})

	.state('app.myhub.microlearninghowitworks',{
		url:'/microlearninghowitworks',
		views:{
			'content@app':{
				templateUrl : 'components/myhub/micro_how_it_works.html'
			}
		}
	})

	.state('app.myhub.wpb_how_it_work',{
		url:'/wpb_how_it_work',
		views:{
			'content@app':{
				templateUrl : 'components/myhub/wpb_how_it_work.html'
			}
		}
	})

	/*to manage client*/
	  .state('app.myhub.add_member',{
		url:'/add_member',
        cache : false,
		views:{
			'content@app':{
				templateUrl : 'components/myhub/add_member.html',
				controller : 'ClientMgmtCtrl',
				controllerAs : 'client'
			}
		}
	})

	.state('app.myhub.add_client_aadhar',{
		url:'/add_client_aadhar/:trans_id',
        cache : false,
		views:{
			'content@app':{
				templateUrl : 'components/myhub/aadhar_add_client.html',
				controller : 'ClientMgmtCtrl',
				controllerAs : 'client'
			}
		}
	})
	/*to view client*/
	.state('app.myhub.viewclients',{
		url:'/viewclients',
        cache : false,
		views:{
			'content@app':{
				templateUrl : 'components/myhub/view_client_modal.html',
				controller : 'ClientMgmtCtrl',
				controllerAs : 'client'
			}
		}
	})
	/*to view uplyf transactions*/
	.state('app.myhub.view_transactions',{
		url:'/viewclient',
		views:{
			'content@app':{
				templateUrl : 'components/myhub/view_uplyf_transactions.html'
			}
		}
	})
		/*to view advisors*/
	.state('app.myhub.viewadvisors',{
		url:'/viewadvisors',
        cache : false,
		views:{
			'content@app':{
				templateUrl : 'components/myhub/view_looped_advisors.html',
				controller : 'AdvisorCtrl',
				controllerAs : 'advisor'
			}
		}
	})
		/*to request advisors*/
	  .state('app.myhub.requestadvisor',{
		url:'/requestadvisor',
        cache : false,
		views:{
			'content@app':{
				templateUrl : 'components/myhub/advisor_refer_modal.html',
				controller : 'AdvisorCtrl',
				controllerAs : 'advisor'
			}
		}
	})

	.state('app.myhub.advisor_loop_tnc',{
		url:'/advisor_loop_termsandconditions',
		cache : true,
		views:{
			'content@app':{
					templateUrl : 'components/myhub/advisor_loop_termsandconditions.html'
			}
		}
	})

	//View Enquiries
	.state('app.myhub.viewenquiries',{
		url:'/viewenquiries',
        cache : false,
		views:{
			'content@app':{
				templateUrl : 'components/myhub/view_enquiries.html',
				controller : 'EnquiryCtrl',
				controllerAs : 'enquiry'
			}
		}
	})
		/*to view to be rated peers*/
	  .state('app.myhub.viewratepeers',{
		url:'/viewratepeers',
        cache : false,
		views:{
			'content@app':{
				templateUrl : 'components/myhub/view_torate_peerlist.html',
				controller : 'RatingRankingCtrl',
				controllerAs : 'raterank'
			}
		},
		params : {
			'is_rated':null
		}
	})
		/*to rate peers*/
	  .state('app.myhub.viewratepeers.ratepeers',{
		url:'/ratepeers',
        cache : false,
		views:{
			'content@app':{
				templateUrl : 'components/myhub/rate_modal.html',
				controller : 'RatingRankingCtrl',
				controllerAs : 'raterank'
			}
		}
	})
		/*to view rate/rank peers/clients*/
	  .state('app.myhub.viewraterank',{
		url:'/viewraterank',
        cache : false,
		views:{
			'content@app':{
				templateUrl : 'components/myhub/view_client_rank.html',
				controller : 'RatingRankingCtrl',
				controllerAs : 'raterank'
			}
		}
	})

	.state('app.myhub.applycrisil',{
		url:'/applycrisil',
		views:{
			'content@app':{
				templateUrl : 'components/myhub/crisilapply.html',
				controller : 'CRISILCtrl',
				controllerAs : 'crisil'
			}
		}
	})
	.state('app.myhub.entercrisilpayment',{
		url:'/entercrisilpayment',
		views:{
			'content@app':{
				templateUrl : 'components/myhub/crisilenterpaymentdetails.html',
				controller : 'CRISILCtrl',
				controllerAs : 'crisil'
			}
		}
	})
  .state('app.myhub.videopublish',{
    url:'/videopublish',
    views: {
      'content@app':{
        templateUrl: 'components/myhub/advisorvideopublish.html',
        controller: 'MyHubCtrl',
        controllerAs: 'myhub'
      }
    }
  })
  .state('app.myhub.videorequest',{
    url:'/videorequest',
    views: {
      'content@app':{
        templateUrl: 'components/myhub/advisorvideorequest.html',
        controller: 'MyHubCtrl',
        controllerAs: 'myhub'
      }
    }
  })
	.state('app.mytrack.crisilrenewal',{
		url:'/crisilrenewal',
		views:{
			'content@app':{
				templateUrl : 'templates/crisil_renewal.html'
			}
		}
	})
	.state('app.myidentity.emailshare',{
		url:'/emailshare',
		views:{
			'content@app':{
				templateUrl : 'components/myidentity/email_share.html',
				controller : 'ProfileShareCtrl',
				controllerAs : 'share'
			}
		},
		params:{
			'shareurl':null
		}
	})
	.state('app.loop',{
		url :'/loop',
		views :{
		'content': {
			templateUrl : 'templates/loop.html'
	               }
	           }
	})
	.state('help',{
		url:'/help',
				templateUrl : 'templates/help.html'
	})
	.state('app.about',{
		url:'/about',
		views :{
			'content' : {
				templateUrl : 'templates/aboutus.html'
			}
		}
	})
	.state('app.getintouch',{
		url:'/getintouch',
		views : {
			'content' : {
				templateUrl : 'templates/getintouch.html',
				controller : 'ContactCtrl',
				controllerAs : 'contact'
			}
		}
	})
   .state('app.advisor',{
        url:'/advisor',
        views :{
          'content'  : {
              templateUrl:'templates/advisorornot.html'
          }
        }
    })
    .state('app.editprofile',{
              url:'/editprofile',
              views :{
                'content'  : {
              templateUrl:'components/registration_process/form1.html',
							controller : 'RegCtrl',
              controllerAs : 'reg'
          }
       }
    })
		.state('app.footprint',{
				url:'/footprint',
				views: {
					'content':{
						templateUrl:'components/registration_process/footprint_form.html',
						controller:'FootPrintCtrl',
						controllerAs:'foot'
					}
				},
				params:{
					'confirm': null
				}
		})

    .state('app.editprofilebasic',{
              url:'/editprofilebasic',
              views :{
                  'content' : {
                      templateUrl:'components/registration_process/form2.html',
                      controller :'RegCtrl',
                      controllerAs :'reg'
                  }
              }
    })
    .state('app.editprofileanswer',{
            url:'/editprofileanswer',
            views : {
                'content': {
                    templateUrl:'components/registration_process/form3.html',
                    controller :'RegCtrl',
                    controllerAs :'reg'
                }
            }
    })
	.state('app.eKYC',{
	  url :'/eKYC',
	  views :{
		  'content' :{
	  templateUrl:'components/registration_process/ekyc.html',
	  controller :'EkycCtrl',
	  controllerAs :'ekyc'
     }
   }
})

.state('app.education',{
	url :'/education',
	views :{
		'content' :{
	templateUrl:'components/registration_process/education.html',
	controller :'RegCtrl',
  controllerAs :'reg'
	 }
 }
})
	.state('eKYCsuccess',{
	  url :'/eKYCsuccess',
	  controller :'eKYCsuccess',
	  controllerAs : 'eKYCs'
	})

	.state('eKYCfailure' ,{
	  url :'/eKYCfailure',
	  controller :'eKYCfailure',
	 controllerAs :'eKYCf'

	})
//Enable/Disable SMS notifications
	.state('app.smsalert',{
		url:'/smsalert',
		views:{
			'content@app':{
				templateUrl : 'templates/smsalert.html',
				controller : 'SMSCtrl',
				controllerAs :'sms'
			}
		}
	})

//Edit myprofile

	.state('app.updateprofile',{
		url:'/updateprofile',
		views:{
			'content':{
				templateUrl : 'templates/updateprofile.html',
				controller : 'UpdateProfileCtrl',
				controllerAs :'updateprofile'
			}
		}
	})

	.state('app.myidentity.changepicture',{
		url:'/changepicture',
		views:{
			'content@app':{
				templateUrl : 'components/myidentity/changeprofilepicture.html',
				controller : 'ChangePictureCtrl',
				controllerAs :'changepicture'
			}
		},
		params:{
			'picture':null
		}
	})

  .state('app.changepassword',{
    url:'/changepassword',
    views : {
      'content@app' : {
        templateUrl : 'templates/changepassword.html',
        controller : 'changepasswordCtrl',
        controllerAs : 'changepassword'
      }
	},
	params:{
		'status':null
	}
  })

  .state('app.termsandconditions',{
		url:'/termsandconditions',
		views :{
			'content@app' : {
				templateUrl : 'templates/terms.html',
			  controller:'sideMunuCtrl',
        controllerAs:'sidemenu'
      }
		},
    params:{
      'status':null
    }
   })

   .state('app.privacypolicy',{
	   url:'/privacypolicy',
	   views:{
		   'content@app':{
			   templateUrl : 'templates/privacypolicy.html',
         controller:'sideMunuCtrl',
         controllerAs:'sidemenu'
       }
	   },
     params:{
       'status':null
     }
   })

    .state('app.appfaq',{
     url:'/appfaq',
     views :{
         'content@app' : {
             templateUrl : 'templates/faq.html',
             controller:'sideMunuCtrl',
             controllerAs:'sidemenu'
         }
     },
     params:{
       'status':null
     }
	})

	.state('app.apphelp',{
		    url:'/apphelp',
		    views :{
  			     'content@app' : {
  				       templateUrl : 'templates/help.html',
                 controller:'sideMunuCtrl',
                 controllerAs:'sidemenu'
  			      }
		     },
         params:{
           'status':null
         }
	})

   .state('app.meetup',{
          url:'/meetup',
          views : {
              'sidemenu' : {
                  templateUrl : 'templates/meetup.html',
                  controller : 'meetupCtrl',
                  controllerAs : 'meetup'
              }
          }
    })

    .state('app.myhub.meetup',{
		    url:'/meetup',
        cache : false,
		    views:{
			       'content@app':{
				           templateUrl : 'components/myhub/meetup.html',
				           controller : 'meetupCtrl',
                   controllerAs : 'meetup'
			        }
		    }
	})

	.state('app.myhub.list_mail_invitation',{
		    url:'/list_mail_invitation',
        cache : false,
		    views:{
			       'content@app':{
            				templateUrl : 'components/myhub/list_mail_invitation.html',
            				controller : 'meetup_listmailCtrl',
                    controllerAs : 'meetuplist'
			       }
		    }
	})

	.state('app.myhub.list_register_webinar',{
		    url:'/:room_id',
        cache : false,
		    views:{
			       'content@app':{
				           templateUrl : 'components/myhub/list_register_webinar.html',
				           controller : 'webinar_listmailCtrl',
                   controllerAs : 'webinarlist'
			       }
		    }
	})

	.state('app.myhub.view_meetup',{
		    url:'/view_meetup',
        cache : false,
		    views:{
			       'content@app':{
				           templateUrl : 'components/myhub/view_meetup.html',
				           controller : 'meetup_viewCtrl',
                   controllerAs : 'meetupview'
			       }
		    }
	})

	.state('app.myhub.view_webinar',{
		    url:'/view_webinar',
        cache : false,
		    views:{
			       'content@app':{
				           templateUrl : 'components/myhub/view_webinar.html',
				           controller : 'webinar_viewCtrl',
                   controllerAs : 'webinarview'
			       }
		    }
	})

  .state('app.webinar',{
        url:'/webinar',
        views : {
              'sidemenu' : {
                    templateUrl : 'templates/webinar.html',
                    controller : 'webinarCtrl',
                    controllerAs : 'webinar'
              }
        }
  })
  .state('app.myhub.webinar',{
		    url:'/webinar',
        cache : false,
		    views:{
			       'content@app':{
				           templateUrl : 'components/myhub/webinar.html',
				           controller : 'webinarCtrl',
                   controllerAs : 'webinar'
			        }
		    }
	})

	.state('logout',{
		    url:'/logout',
        controller : 'LogoutCtrl',
        controllerAs : 'logout'
	});
  $urlRouterProvider.otherwise('/redirect/');
}
]);
