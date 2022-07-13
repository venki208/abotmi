angular.module('eipv_factories_verification',['eipv_constants_verification'])

.factory('EipvuploadFactory',['$http','EIPVDATA','UPEIPV','SUBEIP','EIPVFORM','MOTP',
				'VOTP','Upload','COUNTRY','$q','$location','COUNTRY_SAVE','DELETE_DOCUMENTS','AADHAR_VERIFICATION_DATA',function($http,EIPVDATA,UPEIPV,SUBEIP,EIPVFORM,
				MOTP,VOTP,Upload,COUNTRY,$q,$location,COUNTRY_SAVE,DELETE_DOCUMENTS,AADHAR_VERIFICATION_DATA,) {
	var result = [],
	promise = "",
	document_type="";
	var domain_url = $location.protocol()+"://"+$location.host()+":"+$location.port();
	
	return {
		postdata : function(data,type){
			if(type =="face")
			{
				document_type = "eipv_face_capture";
			}
			else if(type == "passport")
			{
				document_type = "passport";
			}
			else if(type =="id_card")
			{
				document_type ="id_card";
			}
			else if(type == "driving_licence")
			{
				document_type ="driving_licence";

			}
			else
			{
				document_type ="pan_card";
			}
			$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
			var url = domain_url+UPEIPV;
			var fd = ({document_type : document_type,image:data,req_type : "mobile"});
			promise = Upload.upload({
				url:url,
				data:fd
			}).then(function(res){
				console.log(res);
				return res.data;
			},function(error){
				return  error;
			});
			return promise;
		},
		submiteipv : function(){
				var url = domain_url+SUBEIP;
				var fd = $.param({req_type : "mobile"});
				var promise = $http({
   	   				method :'POST',
   	   				url: url,
					data:fd,
   	   				headers :{
   	   					'Content-Type': 'application/x-www-form-urlencoded'
   	   				}
   	   			}).then(function(result){
   	   				return result.data;
   	   			},function(error){
   	   				return error;
   	   			});
   	   			return promise;
			},

			deletedocuments : function(id_delete){
				var url = domain_url+DELETE_DOCUMENTS;
				var fd = $.param({id : id_delete,req_type : "mobile"});
				var promise = $http({
   	   				method :'POST',
   	   				url: url,
					data:fd,
   	   				headers :{
   	   					'Content-Type': 'application/x-www-form-urlencoded'
   	   				}
   	   			}).then(function(result){
   	   				return result.data;
   	   			},function(error){
   	   				return error;
   	   			});
   	   			return promise;
			},

			get_verification_data : function(){
				var url = domain_url+AADHAR_VERIFICATION_DATA;
			   var cpromise_data = $http.post(url)
			   .then(function(response){
				   results = response.data;
				   return results;
			   }
			   ,function(response){
				   return $q.reject(response);
			   });
			   return cpromise_data;
		   },		

			savecountry : function(country_details){
				var url = domain_url+COUNTRY_SAVE;
				var fd = $.param({country : country_details});
				var promise = $http({
   	   				method :'POST',
   	   				url: url,
					data:fd,
   	   				headers :{
   	   					'Content-Type': 'application/x-www-form-urlencoded'
   	   				}
   	   			}).then(function(result){
   	   				return result.data;
   	   			},function(error){
   	   				return error;
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
		   },		
		submitform :function(data){
			var url = domain_url+EIPVFORM;
			
			var fd =$.param({name : data.name,email :data.email,suffix : data.suffix,mobile : data.mobile,address1 : data.address,city : data.city,country : data.country,pincode : data.pincode,req_type : "mobile"});
			var promise = $http({
				method :'POST',
				url: url,
				data:fd,
				headers :{
					'Content-Type': 'application/x-www-form-urlencoded'
				}
			}).then(function(result){
				return result.data;
			},function(error){
				return error;
			});
			return promise;
	        },
	    mobileotp : function(data){
			var url = domain_url + MOTP;
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
		   verifyotp : function(data){
			   var url = domain_url + VOTP;
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

				getdata : function(){
					var url = domain_url + EIPVDATA;
					console.log(url);
					var fd = $.param({req_type : "mobile"});
					 var promise = $http({
						 method :'POST',
						 data :fd,
						url :url,
						headers : {
							'Content-Type': 'application/x-www-form-urlencoded'
						}
					 }).then(function(result)
  					   {
  						   return result.data;
  					   },function(error){
  						   return error;
  					   });
  					   return promise;
				}
         	}

    }])
