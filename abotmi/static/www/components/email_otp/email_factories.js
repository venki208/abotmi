angular.module('email_factories',['email_constants'])

.factory('EmailOtp',['$http','$q','$location','RESENDOTPEMAIL','VALIDATEOTPEMAIL','AUTHORIZE','ISREGURL','SAVINGEMAILSTATUS','USERSIGNUP','SOCIALSIGNUPDATA',function($http,$q,$location,RESENDOTPEMAIL,VALIDATEOTPEMAIL,AUTHORIZE,ISREGURL,SAVINGEMAILSTATUS,USERSIGNUP,SOCIALSIGNUPDATA) {
	var result = [],
	promise = "",
	document_type="";
	var promise1 = ""
    var domain_url = $location.protocol()+"://"+$location.host()+":"+$location.port();
    return{
        emailotp : function(data){
			var url = domain_url + RESENDOTPEMAIL;
			var promise = $http({
				method :'POST',
				url: url,
				data:data,
				headers :{
					'Content-Type': 'application/x-www-form-urlencoded',
					'Authorization' : null
				}
			}).then(function(result)
				{
					return result.data;
				},function(error){
					return error;
				});
				return promise;
			 },
			 direct_signup : function(data_details){
				var url = domain_url+USERSIGNUP;
				promise =  $http({
								method : 'POST',
								url : url,
								data : data_details,
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
			social_signup : function(social_data){
				var url = domain_url+SOCIALSIGNUPDATA;
				 promise1 =  $http({
								method : 'POST',
								url : url,
								data : social_data,
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
				return promise1;
			},
			 savingemailstatus : function(data){
				var url = domain_url + SAVINGEMAILSTATUS;
				var promise = $http({
					method :'POST',
					url: url,
					data:data,
					headers :{
						'Content-Type': 'application/x-www-form-urlencoded'
					}
				}).then(function(result)
					{
						return result.data;
					},function(error){
						return error;
					});
					return promise;
				 },
		   verifyotpEmail : function(data){
			   //$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
			   var url = domain_url + VALIDATEOTPEMAIL;
			   var promise = $http({
				   method :'POST',
				   url: url,
				   data:data,
				   headers: {
					'Content-Type': 'application/x-www-form-urlencoded',
					'Authorization' : null
				},
			   }).then(function(result)
				   {
					   return result.data;
				   },function(error){
					   return error;
				   });
				   return promise;
               },
               
               login : function(data){
    			var url = domain_url+AUTHORIZE;
    		  promise =  $http({
                            method : 'POST',
                            url : url,
                            data : data,
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
        
        is_reg_user : function(){
            $http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
			var url = domain_url+ISREGURL;
		    promise =  $http({
                            method : 'POST',
							url : url,
							headers: {
								'Content-Type': 'application/x-www-form-urlencoded',
							},
                        })
                        .then(function(response){
                            return response;
                        }
                        ,function(response){
                            return response;
                        });
            return promise;
		},


    }
}])