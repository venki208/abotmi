angular.module('signup_login_factories',['signup_login_constants'])

.factory('SignupLoginFactory',['$localStorage','$http','$q','signup_face','CHECKEMAIL','USERSIGNUP','AUTHORIZE','ISREGISTER','FORGOTPWD','$location','USERSIGNUPOTP','MENUDETAILS'
         ,function($localStorage,$http,$q,signup_face,CHECKEMAIL,USERSIGNUP,AUTHORIZE,ISREGISTER,FORGOTPWD,$location,USERSIGNUPOTP,MENUDETAILS){
	var result = [];
	var promise = "";
	var domain_url = $location.protocol()+"://"+$location.host()+":"+$location.port();
	return {
		direct_signup : function(data){
			var url = domain_url+USERSIGNUP;
            var signupparam =$.param({first_name : data.name, email : data.email, password : data.createpassword, ref_link :'', last_name :data.lastname});
		    promise =  $http({
                            method : 'POST',
                            url : url,
                            data : signupparam,
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
        },
        
        check_email : function(data){
            var url = domain_url+CHECKEMAIL;
      var logparams = $.param({username : data.email });
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
    },

    signup_otp_email : function(data){
        var url = domain_url+USERSIGNUPOTP;
  var logparams = $.param({email : data.email, first_name : data.name });
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
},

      login : function(data){
    			var url = domain_url+AUTHORIZE;
          var logparams = $.param({username : data.username , password : data.password});
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
        },
        

        social_facebook : function(data){
            var url = domain_url+signup_face;
      var logparams = $.param({email : "phanisai5b0@gmail.com" , first_name : "first",last_name : "first",source : "facebook",gender : "",birthday:"",next_url:""});
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
    },

        is_reg_user : function(data){
            $http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
			var url = domain_url+ISREGISTER;
		    promise =  $http({
                            method : 'POST',
                            url : url
                        })
                        .then(function(response){
                            return response;
                        }
                        ,function(response){
                            return response;
                        });
            return promise;
        },



        is_reg_user_redirect : function(data){
            $http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
			var url = domain_url+MENUDETAILS;
		    promise =  $http({
                            method : 'POST',
                            url : url
                        })
                        .then(function(response){
                            return response;
                        }
                        ,function(response){
                            return response;
                        });
            return promise;
        },
        

        forgotpassword : function(data){
			var url = domain_url+FORGOTPWD;
            var param = $.param({resend_email : data});
		    promise =  $http({
                            method : 'POST',
                            url : url,
                            data : param,
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
