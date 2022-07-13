angular.module('reiaapp.factories',['reiaapp.constants'])
.factory('get_userDetails',['$localStorage','$http','$q','$location','PROFILEDETAILSURL' ,function($localStorage,$http,$q,$location,PROFILEDETAILSURL){
	var result = [];
	var promise = "";
	var domain_url = $location.protocol()+"://"+$location.host()+":"+$location.port();
	return {
		getDetails : function(){
      $http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
			 var url = domain_url+PROFILEDETAILSURL;
		    promise = $http.post(url)
        .then(function(response){
				      result = response.data;
              return result;
			  }
			  ,function(response){
              return $q.reject(response);
			  });
			return promise;
		}
	}
}])

.factory('RefreshTokenFactory',['$localStorage','$http','$q','$location','REFRESHTOKEN' ,function($localStorage,$http,$q,$location,REFRESHTOKEN){
	var result = [];
	var promise = "";
	var domain_url = $location.protocol()+"://"+$location.host()+":"+$location.port();
	return {
		getToken : function(){
      	$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
			  var url = domain_url+REFRESHTOKEN;
			  var data = $.param({"token":localStorage.getItem('jwttoken')});
			  promise = $http({
					method : "POST",
					url:url,
					data: data,
					headers:{
						'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
					}
       })
			.then(function(response){
				result = response.data;
				return result;
			}
			,function(response){
				return $q.reject(response);
			});
			return promise;
		}
	}
}])

.factory('get_reguserdetails',['$localStorage','$http','$q','$location','USERDETAILS','COUNTRY' ,function($localStorage,$http,$q,$location,USERDETAILS,COUNTRY){
  	var result = [];
  	var promise = "";
  	var cpromise = "";
  	var results = [];
		$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
	  var domain_url = $location.protocol()+"://"+$location.host()+":"+$location.port();
	  return {
      getDetails : function(){
             var url = domain_url+USERDETAILS;
		         promise = $http.post(url)
			       .then(function(response){
				           result = response.data;
                   return result;
			       }
			       ,function(response){
                return $q.reject(response);
			       });
			  return promise;
		    },
		    getcountry : function(){
	         var url = domain_url+COUNTRY;
	  		   cpromise = $http.post(url)
	  			.then(function(response){
	  				    results = response.data;
	              return results;
	  			}
	  			,function(response){
	              return $q.reject(response);
	  			});
	  			return cpromise;
	  		}
		}
}])

.factory('updateprofiledetails',['$localStorage','$http','$q','EDITPROFILEPIC','$location','Upload','EDITPROFILEDETAILS',
		function($localStorage,$http,$q,EDITPROFILEPIC,$location,Upload,EDITPROFILEDETAILS){
	var result = [];
	var promise = "";
	var domain_url = $location.protocol()+"://"+$location.host()+":"+$location.port();
	return {
		postPicture : function(data){
			$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
			var url = domain_url+EDITPROFILEPIC;
			var fd = ({documents_type : "Profile Picture",profile_pic:data});
			promise = Upload.upload({
				url:url,
				data:fd
			}).then(function(res){
				return res.data;
			},function(error){
				return $q.reject(res);
			});
			return promise;
		}
	}
}])

	.factory('changepasswordfactory', function($http, $location, $q, CHANGEPASSWORD) {
		var domain_url = $location.protocol() + "://" + $location.host() + ":" + $location.port();
		return {
			changepassword: function(recived, $location) {
				var touchpromise;
				var url = domain_url + CHANGEPASSWORD;
				touchpromise = $http({
					url: url,
					method: "POST",
					data: "oldpassword=" + recived.old_password + "&newpassword=" + recived.new_password + "&confirmpassword=" + recived.confirm_password,
					headers: { 
						'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
					}
				}).
				then(function(result) {
					msg = result.data;
					return msg;
				}, function(result) {
					return $q.reject(result);
				});
				return touchpromise;
			}
		}
	})

.factory('get_userRegisterd',['$localStorage','$http','$q','$location','ISREGURLS','CHECKEMAIL','MENUDETAILS','LOGOUTUSER' ,function($localStorage,$http,$q,$location,ISREGURLS,CHECKEMAIL,MENUDETAILS,LOGOUTUSER){
      var result_user = [];
      var promise = "";
      var domain_url = $location.protocol()+"://"+$location.host()+":"+$location.port();
      return {
          getDetails : function(){
              $http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
							var url = domain_url+ISREGURLS;
              promise = $http.post(url)
              .then(function(response){
										
                    return response;
              }
              ,function(response){
                    return $q.reject(response);
              });
              return promise;
			},
			userLogout : function(){
				$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
				var url = domain_url+LOGOUTUSER;
				promise = $http.post(url)
				.then(function(response){
							
							return response.data;
				}
				,function(response){
							return $q.reject(response.data);
				});
				return promise;
},
			getDetails_menu : function(){
				$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
				var url = domain_url+MENUDETAILS;
				promise = $http.post(url)
				.then(function(response){
							result_user = response.data;
							return result_user;
				}
				,function(response){
							return $q.reject(response);
				});
				return promise;
},
			check_email : function(data){
				var url = domain_url+CHECKEMAIL;
		  var logparams = $.param({username : data.email});
			  promise =  $http({
							method : 'POST',
							url : url,
							data : logparams,
							headers: {
								'Content-Type': 'application/x-www-form-urlencoded',
								'Authorization' : null
							},
						})
						.then(function(response){
							return response;
						}
						,function(response){
							return $q.reject(response);
						});
			return promise;
		}
      }
}])

.factory('get_blogDetails',['$http','$q','$location','ICOREPOSTURL','EACHPOSTURL','USERCOMMENTURL',
					'RATEICOREPOST','GETICORECATEGORY','Upload','ICOREADDMEDIA','ICOREADDPOST','ICOREADDCOMMENT',
					function($http,$q,$location,ICOREPOSTURL,EACHPOSTURL,USERCOMMENTURL, RATEICOREPOST,
						GETICORECATEGORY,Upload,ICOREADDMEDIA,ICOREADDPOST,ICOREADDCOMMENT){
	    var userresult = [];
	    var postresult = "";
	    var userpostpromise = "";
	    var eachpostpromise = "";
	    var postcommetpromise = "";
	    var lastreqfailed = true;
	    var lasteachpostfailed = true;
	    lastpostcommentfailed = true;
	    $http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
		var domain_url = $location.protocol()+"://"+$location.host()+":"+$location.port();
	return {
		getDetails : function(id,$location){
				var url = domain_url+ICOREPOSTURL+id;
				userpostpromise = $http.get(url).
				then(function(response){
          userresult = response.data;
          return userresult;
				},function(response){
					return $q.reject(response);
				});
			return userpostpromise;
		},

		getPost : function(postid,$location){
			  var dataid = $.param({id : postid});
				var url = domain_url+EACHPOSTURL;
				$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
				eachpostpromise = $http({
					method : "POST",
					url:url,
					data: dataid,
					headers:{
						'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
					}
        }).
				then(function(res){
           postresult = res.data;
           return postresult;
				},function(res){
					 return $q.reject(res);
				});
           return eachpostpromise;
		},

		getUserComments : function(email,$location){
			var url = domain_url+USERCOMMENTURL+email;
			var eachusercomment = $http.get(url).
			then(function(res){
				commentresult = res.data;
				return commentresult;
			},function(error){
				return $q.reject(error);
			});
			return eachusercomment;
		},

		ratePost : function(postid,value){
			var postid = $.param({post_id : postid,star_sum: value});
			var url = domain_url+RATEICOREPOST;
			var rate = $http({
				method : "POST",
				url : url,
				data : postid,
				headers:{
					'Content-Type': 'application/x-www-form-urlencoded;charser=utf-8;'
				}
			}).then(function(res){
				return res.data;
			},function(error){
				return $q.reject(res);
			});
			return rate;
		},

		getCategories : function(){
			var url = domain_url+GETICORECATEGORY;
			var category = $http({
				method:"GET",
				url:url
			}).then(function(res){
				return res.data;
			},function(error){
				return $q.reject(res);
			});
			return category;
		},

		addMedia : function(mediafile){
			var url = domain_url+ICOREADDMEDIA;
			var fd = ({media:mediafile});
			var result = Upload.upload({
				url:url,
				data:fd
			}).then(function(res){
				return res.data;
			},function(error){
				return $q.reject(res);
			});
			return result;
		},

		addPost : function(details){
			var url = domain_url+ICOREADDPOST;
			var data = $.param({add_tag:details.tags,add_category:details.toString().categories,title:details.title,content_raw:details.content,featured_image:details.featured_image});
			var result = $http({
				method:'POST',
				url:url,
				data:data,
				headers:{
					'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
				}
			}).then(function(res){
				return res.data;
			},function(error){
				return $q.reject(res);
			});
			return result;
		},

		addComment : function(postid,comment){
			var url = domain_url+ICOREADDCOMMENT;
			var data = $.param({'post_id':postid,'comment':comment});
			var result = $http({
				method:'POST',
				url:url,
				data:data,
				headers:{
					'Content-Type':'application/x-www-form-urlencoded;charset=utf-8;'
				}
			}).then(function(res){
				return res.data;
			},function(error){
				return $q.reject(res);
			});
			return result;
		}
	}
}])

.factory('socialsignup',['$http','$q','$location','SOCIALSIGNUP',function($http,$q,$location,SOCIALSIGNUP){
	    var returnpromise = '';
	    var msg = '';
			var domain_url = $location.protocol()+"://"+$location.host()+":"+$location.port();
			return {
			signup :function(signupdetails){
				signupdetails = angular.fromJson(signupdetails);
				var user_details = $.param({email : signupdetails.email,first_name : signupdetails.first_name,last_name : signupdetails.last_name,gender : signupdetails.gender,birthday : signupdetails.birthday,ref_link : '',next_url :$location.host(),source : signupdetails.source })
				var url = domain_url+SOCIALSIGNUP;
				returnpromise = $http({
        url : url,
        method : "POST",
				data  : user_details,
				headers : {
					 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
					 'Authorization' : null
				}
			}).
			then(function(result){
				msg = result.data;
                return msg;
			},function(result){
				return $q.reject(result);
			});
			return returnpromise;
			}
		}
}])

.factory('adharverify',['$http','$q','CREATEADHARFORM','$location','CHECKMEMBERAADHAAR',
	 function($http,$q,CREATEADHARFORM,$location,CHECKMEMBERAADHAAR) {
	 var returnpromise ='';
	 var msg = '';
	 $http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
	 var domain_url = $location.protocol()+"://"+$location.host()+":"+$location.port();
	 return {
		 verify : function(number,type){
     	 var adhar_number  = $.param({aadhaar_no : number});
  		 if(type=="self"){
  		 	   var url = domain_url + CREATEADHARFORM;
       } else {
  		 	   var url = domain_url + CHECKMEMBERAADHAAR;
       }
		   returnpromise = $http({
    			 url : url,
    			 method :"POST",
    			 data : adhar_number,
    			 headers : {
             'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
    			 }
		   }).then(function(result){
			      msg = result.data;
			      return msg;
		 },function(result){
			 return $q.reject(result);
		 });
		 return returnpromise;
		 }
	 }
}])

.factory('aadhar_success',['$http','$q','$location','SUCCESS','MEMBERSUCCESS',function($http,$q,$location,SUCCESS,MEMBERSUCCESS) {
	var returnpromise ='';
	var msg = '';
	$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
	var domain_url = $location.protocol()+"://"+$location.host()+":"+$location.port();
	return {
		success : function(uuid,reqid,type){
		var details = $.param({uuid :uuid ,reqid : reqid});
		if(type=="self"){
			var url = domain_url + SUCCESS;
		}else{
			var url = domain_url + MEMBERSUCCESS;
    }
		returnpromise = $http({
			url : url,
			method :"POST",
			data : details,
			headers : {
				 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
			}
		}).
		then(function(result){
			msg = result.data;
			return msg;
		},function(result){
			return $q.reject(result);
		});
		return returnpromise;
	}
	}
}])

.factory('aadhar_failure',['$http','$q','$location','FAILURE','MEMBERFAILURE',function($http,$q,$location,FAILURE,MEMBERFAILURE) {
	var returnpromise ='';
	var msg = '';
	$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
	var domain_url = $location.protocol()+"://"+$location.host()+":"+$location.port();
	return {
		failure : function(reqid,type){
		var details = $.param({reqid : reqid});
		if(type == "self")
			var url = domain_url + FAILURE;
		else
			var url = domain_url + MEMBERFAILURE;
		returnpromise = $http({
			url : url,
			method :"POST",
			data : details,
			headers : {
				 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
			}
		}).
		then(function(result){
			msg = result.data;
							return msg;
		},function(result){
			return $q.reject(result);
		});
		return returnpromise;
	}
	}
}])

.factory('submitData',['$http','$q','$timeout','$location','REFERADVISORURL','INVITERATEURL',
				'SUBMITRATEURL','CHECKPROMOCODEURL','APPLYCRISILURL','CRISILREFDOCURL','GETINTOUCH',
				'CRISILRENEWAL','Upload','CHANGEPASSWORD','WEBINAR','MEETUP',
				function($http,$q,$timeout,$location,REFERADVISORURL,INVITERATEURL,SUBMITRATEURL,
					CHECKPROMOCODEURL,APPLYCRISILURL,CRISILREFDOCURL,GETINTOUCH, CRISILRENEWAL,Upload,
					CHANGEPASSWORD,WEBINAR,MEETUP){
	     var returnpromise = '';
       var parameter=[];
       var json = {};
	     var msg = '';
	     $http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
	     var domain_url = $location.protocol()+"://"+$location.host()+":"+$location.port();
	     return{
	     	referAdvisor : function(data,$location){
				var url = domain_url+REFERADVISORURL;
	     		json = '{'+'"0":["'+data.name+'","'+data.email+'","'+data.mobile+'","'+data.location+'"]}';
	     		parameter = $.param({jsondata : json});
	     		returnpromise = $http({
	     			url : url,
	     			method : "POST",
	     			data : parameter,
	     			headers: {
				   'Content-Type': 'application/x-www-form-urlencoded'
				}
	     		}).
	     		then(function(result){
					return result.data;
	     		},function(result){
	     			return $q.reject(result.data);
	     		});
	     		return returnpromise;
	     	},

	inviteRate : function(data,type,$location){
		var invitejson = '{'+'"0":["'+data.name+'","'+data.email+'","'+data.mobile+'","'+type+'"]}';
		var peerparameter = $.param({invite_advisor_to_rate_form_data : invitejson});
		var url = domain_url+INVITERATEURL;
		var invitepeerpromise = $http({
			method : "POST",
			url : url,
			data : peerparameter,
			headers: {
				   'Content-Type': 'application/x-www-form-urlencoded'
				}
		}).then(function(res){
             return res.data;
	     		},function(result){
	     			return $q.reject(result.data);
		});
		return invitepeerpromise;
	},

	getintouch : function(recived,$location){
		var touchpromise;
		var url = domain_url+GETINTOUCH;
		touchpromise = $http({
				url : url,
       	method : "POST",
        data :"name="+recived.name+"&mobile_number="+recived.mobile+"&email="+recived.emailid+"&location="+recived.location+"&content_msg="+recived.message,
        headers : {
       	  'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
        }
			}).
			then(function(result){
				msg = result.data;
                return msg;
			},function(result){
				return $q.reject(result);
			});
			return touchpromise;
	},

	checkPromoCode : function(data,$location){
		var promoparam = $.param({code : data});
		var url = domain_url+CHECKPROMOCODEURL;
		var promosubmit = $http({
			method : "POST",
			url : url,
      data : promoparam,
      headers : {
      	'Content-Type' : 'application/x-www-form-urlencoded'
      }
		}).then(function(res){
			promosubmit = " ";
			return res.data;
		},function(error){
			promosubmit = " ";
			return $q.reject(error);
		});
		return promosubmit;
	},

	applyCrisil : function(year,$location){
      var promocodeparam = $.param({crisil_selected_years:year,promocode : "not applied",promocode_status :"not applied"});
		  var url = domain_url+APPLYCRISILURL;
      var applypromise = $http({
        	method : "POST",
        	url : url,
        	data : promocodeparam,
        	headers : {
        		'Content-Type' : 'application/x-www-form-urlencoded;charset=utf-8;'
        	}
        }).then(function(res){
        	return res.data;
        },function(error){
        	return $q.reject(error);
        });
        return applypromise;
	},

	crisilDocSubmit : function(data,amount,$location){
		var fd = ({cheque_dd_no : data.refnumber,cheque_date:data.paydate,bankname:data.bankname,scaned_doc:data.refdoc});
		var url = domain_url+CRISILREFDOCURL;
		var docprom = Upload.upload({
			url : url,
			data : fd
		}).then(function(res){
		return res.data;
		},function(error){
			return $q.reject(error);
		})
		return docprom;
	},

	crisilRenewSubmit : function(data,amount,expiry_date,$location){
		var fd = ({reference_number : data.refnumber,payment_date:data.paydate,bank_name:data.bankname,renewal_reference_doc:data.refdoc,amount:amount,years_selected:expiry_date});
		var url = domain_url+CRISILRENEWAL;
		var docprom = Upload.upload({
			url : url,
			data : fd
		}).then(function(res){
			return res.data;
		},function(error){
			return $q.reject(error);
		})
		return docprom;
	},

	submitRating : function(data,$location){
		var submitparam = $.param({
      activation_key : data.activationkey,
      trust:data.trust,
      financial : data.financial,
      communication : data.comm ,
      advisory : data.advisory ,
      ethics : data.ethics ,
      customer : data.ccare ,
      average : data.avgrate
    });
		var url = domain_url+SUBMITRATEURL;
		var ratedpromise = $http({
				url : url,
       	method : "POST",
        data : submitparam,
        headers : {
       	  'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
        }
			}).then(function(result){
				msg = result.data;
        return msg;
			},function(result){
				return $q.reject(result);
			});
			return ratedpromise;
	}
	     }
}])

.factory('socialShare',function(FBSHAREURL,GPLUSSHAREURL,LINKEDINSHAREURL,TWITTERSHAREURL,SweetAlert){
	var share = {};
	 share.fb_share = function(shareurl,text){
        window.location.href = "socialshareurl://facebook://send?text="+shareurl;
   }
   share.LinkedInShare = function(shareurl,text) {
        window.location.href = "socialshareurl://linkedin://send?text="+shareurl;
   }
   share.googleplusbtn = function(shareurl,text) {
			  window.location.href = "socialshareurl://googleplus://send?text="+shareurl;
	 }
	 share.twitter_share = function(shareurl,text){
		   window.location.href = "socialshareurl://twitter://send?text="+shareurl;
	 }
	 share.whatsapp_share = function(shareurl,text){
		   window.location.href = "socialshareurl://whatsapp://send?text="+shareurl;
	 }
   return share;
})

.factory('smsNotification',function(GETSMSSTATUS,MODIFYSMSSTATUS,$http,$location){
	var notify = {};

	notify.get_status = function(){
		$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
		var url = $location.protocol()+"://"+$location.host()+":"+$location.port()+GETSMSSTATUS;
		var promise = $http({
			method:'POST',
			url:url,
			headers:{
                'Content-Type': 'application/x-www-form-urlencoded'
			}
		}).then(function(result){
			return result.data;
		},function(error){
			return error;
		});
		return promise;
	}

	notify.toggle_status = function(){
		$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
		var url = $location.protocol()+"://"+$location.host()+":"+$location.port()+MODIFYSMSSTATUS;
		var promise = $http({
			method:'POST',
			url:url,
			headers:{
                'Content-Type': 'application/x-www-form-urlencoded'
			}
		}).then(function(result){
			return result.data;
		},function(error){
			return error;
		});
		return promise;
	}

	return notify;
})
.factory('submitProfileData',['$http','$q','$location','REGISTER','USERPROFILE','USERANSWER',
		function($http,$q,$location,REGISTER,USERPROFILE,USERANSWER){
	var returnpromise = '';
  var parameter = [];
  var json = {};
  var msg = '';
	$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
	var domain_url = $location.protocol()+"://"+$location.host()+":"+$location.port();
	var profilepromise = {};

	 profilepromise.editprofiledetails1 = function(trackdata,regdata){
		 var newdata =  angular.toJson(trackdata.Advisory_ins) ;
		 var rera = angular.toJson(trackdata.RERA_details);
		 var  dsa =  angular.toJson(trackdata.DSA_details);
		 var userprof = $.param({
       first_name : regdata.first_name,
       last_name : regdata.last_name,
       middle_name : regdata.middle_name,
       mobile : regdata.mobile,
       username : regdata.email,
		   secondary_email:trackdata.secondemail,
       suffix :trackdata.suffix,
       birthdate : regdata.birthday,
       gender: regdata.gender,
       sebi_registration_no :trackdata.SEBI_registration_no,
       irda_registration_no : trackdata.IRDA_registration_no,
       amfi_registration_no : trackdata.AMFI_registration_no,
       other_organisation : trackdata.other_registration_state,
       other_registration_no :trackdata.other_registration_no,
       sebi_expiry_date : trackdata.SEBI_expire_date,
       irda_expiry_date : trackdata.IRDA_expire_date,
			 amfi_expiry_date : trackdata.AMFI_expire_date,
       other_expiry_date : trackdata.other_expiry_date,
       practice_country : trackdata.practice_country,
       practice_city : trackdata.practice_city,
       practice_location : trackdata.practice_location,
       education_qualification :trackdata.education_qualification,
       my_promise : trackdata.my_promise,
       total_clients_served : trackdata.total_clients_served,
       total_advisors_connected : trackdata.total_advisors_connected,
       hidden_input : newdata,
       hidden_value : rera,dsa_hidden_input_field : dsa
     });
		 var url = domain_url +REGISTER;
      var promise = $http({
				method :'POST',
				data :userprof,
				url: url,
				headers :{
					'Content-Type': 'application/x-www-form-urlencoded'
				}
			}).then(function(result){
				return result.data;
			},function(error){
				return error;
			});
			return promise;
	 }

	 profilepromise.editprofiledetails2 = function(trackdata,regdata){
		 var education =   angular.toJson(trackdata.Additional_qualification_list);
		 var userprf = $.param({
        first_name : regdata.first_name,
        middle_name : regdata.middle_name,
        last_name : regdata.last_name,
        suffix : trackdata.suffix,
        gender :regdata.gender,
        birthdate :regdata.birthday,
        marital_status :  trackdata.marital_status,
        nationality : trackdata.nationality,
        father_name : trackdata.father_name,
        mother_name :trackdata.mother_name,
        locality :regdata.locality,
        street_name : regdata.street_name,address :regdata.address,
			  landmark :regdata.landmark,city:regdata.city,
        pincode:regdata.pincode,
        state: regdata.state,
        country : regdata.country,
        mobile :regdata.mobile,
        primary_email :regdata.primary_email,
        secondary_email :trackdata.secondary_email,
        company_name : trackdata.company_name,
        company_city : trackdata.company_website,
        designation : trackdata.designation,
        annual_income : trackdata.annual_income,
        qualification :trackdata.qualification,
        college_name :trackdata.college_name,
        language_known :trackdata.language_known,
        languages_known_read_write :trackdata.languages_known_read_write,
			  company_website:trackdata.company_website,
			  mother_tongue:trackdata.mother_tongue,
		    year_passout : trackdata.year_passout,
        company_address1 : trackdata.company_address1,
        company_address2 : trackdata.company_address2,
        company_landmark :trackdata.company_lankmark,
        company_locality : trackdata.company_locality,
        company_state : trackdata.company_state,
        company_country : trackdata.company_country,
        is_submitted_all : "true",
        additional_qualification :education,
        facebook_media : trackdata.facebook_media,
        google_media : trackdata.google_media,
        linkedin_media : trackdata.linkedin_media,
        twitter_media : trackdata.twitter_media
    });
	 	var url = domain_url +USERPROFILE;
	 	var promise = $http({
	 		 method :'POST',
			 data :userprf,
	 		 url: url,
	 		 headers :{
	 			 'Content-Type': 'application/x-www-form-urlencoded'
	 		 }
	 	 }).then(function(result){
	 		 return result.data;
	 	 },function(error){
	 		 return error;
	 	 });
	 	 return promise;
   }

	 profilepromise.editprofiledetails3 = function(question,$location){
		 var  dquestion =   angular.toJson(question);
		 var url = domain_url +USERANSWER;
		 var datae = $.param({questions : dquestion ,is_submitted_questions : 'True'});
     var promise = $http({
				method :'POST',
				data : datae  ,
				url: url,
				headers :{
					'Content-Type': 'application/x-www-form-urlencoded'
				}
			}).then(function(result){
				return result.data;
			},function(error){
				return error;
			});
			return promise;
 		}

		return profilepromise;
}])
