angular.module('reg_user_factories',['reg_user_constants'])

.factory('get_userDetails',['$localStorage','$http','$q','$location','PROFILEDETAILSURL','CHECKADHAAR','ISREGURL','SAVEDIGITALLINK','DELETEDIGITALLINK','GETDIGITALLINK'
	,function($localStorage,$http,$q,$location,PROFILEDETAILSURL,CHECKADHAAR,ISREGURL,SAVEDIGITALLINK, DELETEDIGITALLINK, GETDIGITALLINK, ){
	var result = [];
	var promise = "";
	var domain_url = $location.protocol()+"://"+$location.host()+":"+$location.port();
	$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
	return {
		getDetails : function(){
			 var url = domain_url+PROFILEDETAILSURL;
			 var data = $.param({'req_type':'mobile'})
		    promise = $http({
				method : 'POST',
				url: url,
				data: data,
				headers: {
	                'Content-Type': 'application/x-www-form-urlencoded'
	            },
			})
			.then(function(response){
				result = response.data;
                return result;
			}
			,function(response){
                return $q.reject(response);
			});
			return promise;
		},
		get_digital_link : function(){
			var url = domain_url+GETDIGITALLINK;
			return $http.get(url).then(function(response){
				return response;
			})

		},
		get_regornot : function(){
			$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
			var url = domain_url + ISREGURL;
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
		get_aadhaar : function(){
			$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
			var url = domain_url + CHECKADHAAR;
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
		save_digital_link : function(link){
			$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
			var url = domain_url+SAVEDIGITALLINK;
			var data = $.param({'req_type':'mobile', digital_links:link});
			return $http({
				method:'POST',
				url:url,
				data:data,
 				headers :{
 					'Content-Type': 'application/x-www-form-urlencoded'
 				}
			}).then(function(res){
				return res
			})
		},
		delete_foot_print_verification : function(link){
			$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
			var url = domain_url+DELETEDIGITALLINK;
			var data = $.param({'req_type':'mobile', digital_links:link});
			return $http({
				method:'POST',
				url:url,
				data:data,
				headers : {
					'Content-Type': 'application/x-www-form-urlencoded'
				}
			}).then(function(res){
				return res;
			})
		}
	}
}])

.factory('get_reguserdetails',['$localStorage','$http','$q','$location','USERDETAILS','COUNTRY' ,function($localStorage,$http,$q,$location,USERDETAILS,COUNTRY){
	var result = [],
	    promise = "",
		cpromise = "",
		results = [];
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

.factory('submitProfileData',['$http','$q','$location','REGISTER','USERPROFILE','ADVISORPROFILEANSWER','EDUCATIONDETAILS','Upload','UPEIPV',
				function($http,$q,$location,REGISTER,USERPROFILE,ADVISORPROFILEANSWER,EDUCATIONDETAILS,Upload,UPEIPV){
	var returnpromise = '',parameter=[],json = {}, msg = '';
	$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
	var domain_url = $location.protocol()+"://"+$location.host()+":"+$location.port();
	var profilepromise = {};

	 profilepromise.editprofiledetails1 = function(regdata,dsa,rera){
		 var newdata =  angular.toJson(regdata.Advisory_ins) ;
		 var rera_details;
		 var dsa_details;
		
		//  for(var i=0; i<rera.length; i++){
		// 	if((rera[i].rera_registration_no)){
		// 		rera_details = angular.toJson(rera);
		// 		break;
		// 	} else {
		//    		rera_details = null;
		// 	}
		//  }
		//  for(var i=0; i<dsa.length; i++){
		// 	if((dsa[i].dsa_bank_name)){
		// 		dsa_details = angular.toJson(dsa);
		// 		break;
		// 	} else {
		//    		dsa_details = null;
		// 	}
		//  }
		 if(regdata.scheck =='true'){
			communication_email_id ='secondary';
		  }
		  else{
		  communication_email_id = 'primary';
		  }
         var sebi_expiry= "";
		 var irda_expiry= "";
		 var amfi_expiry= "";
		 var other_expiry= "" ;
		  var sebi_valid= "" ;
		 var amfi_valid= "" ;
		 var irda_valid= "";
		 var birthdate = moment(new Date(regdata.birthday)).format('MM-DD-YYYY');
		 if(regdata.SEBI_valid_from!=null)
		 {
		 sebi_valid =  moment(new Date(regdata.SEBI_valid_from )).format('DD-MM-YYYY');
	     }
		 if(regdata.IRDA_valid_from!=null)
		 {
		  irda_valid =  moment(new Date(regdata.IRDA_valid_from)).format('DD-MM-YYYY');
	     }
		 if(regdata.AMFI_valid_from!=null)
		 {
		 amfi_valid =  moment(new Date(regdata.AMFI_valid_from)).format('DD-MM-YYYY');
	     }
		 if( regdata.SEBI_expire_date !=null)
		    {
		  sebi_expiry = moment(new Date(regdata.SEBI_expire_date)).format('DD-MM-YYYY');
	     	}
			 if(regdata.IRDA_expire_date!=null)
		 	{
		  irda_expiry = moment(new Date(regdata.IRDA_expire_date)).format('DD-MM-YYYY');
	     	}
		 if(regdata.AMFI_expire_date!=null)
		 	{
		 amfi_expiry = moment(new Date(regdata.AMFI_expire_date)).format('DD-MM-YYYY');
	     	}
		 if(regdata.other_expiry_date !=null)
		 	{
		  other_expiry = moment(new Date(regdata.other_expiry_date)).format('DD-MM-YYYY');
			 }

		 var userprof = $.param({
			  first_name : regdata.first_name,
				last_name : regdata.last_name,
				nationality:regdata.nationality,
			  middle_name : regdata.middle_name,
			  mobile : regdata.mobile_number,
			  username : regdata.email_id,
			  secondary_email:regdata.secondary_email,
				suffix :regdata.suffix,
				street_name : regdata.street_name,
				birthdate : birthdate,
				address :regdata.address,
				gender: regdata.gender,
				city:regdata.city,
			 pincode:regdata.pincode,
			 state: regdata.state,
			 country : regdata.country,
			  sebi_registration_no :regdata.SEBI_registration_no,
			  irda_registration_no : regdata.IRDA_registration_no,
			  amfi_registration_no : regdata.AMFI_registration_no,
			  other_organisation : regdata.other_registration_state,
			  other_registration_no :regdata.other_registration_no,
			  sebi_expiry_date : sebi_expiry,
			  sebi_start_date  : sebi_valid,
			  irda_expiry_date : irda_expiry,
			  irda_start_date :irda_valid,
			  amfi_expiry_date : amfi_expiry,
			  amfi_start_date: amfi_valid,
			  other_expiry_date : other_expiry,
			  practice_country : regdata.practice_country,
			  practice_city : regdata.practice_city,
			  practice_location : regdata.practice_location,
			  education_qualification :regdata.education_qualification,
			  my_promise : regdata.my_promise,
			  total_client_served : regdata.total_clients_served,
			  total_advisors_connected : regdata.total_advisors_connected,
			  hidden_input : newdata,
			  hidden_value : rera_details,
			  dsa_hidden_input_field : dsa_details,
				communication_email_secondary :communication_email_id,
				
		      req_type : "mobile"
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

	 profilepromise.editprofiledetails2 = function(regdata,regPracticeDetails){

		 var education =   angular.toJson(regdata.Additional_qualification_list);
		 var birthdate =   moment(new Date(regdata.birthday)).format('MM-DD-YYYY');
		 if(regdata.checkaddress=='true' ){

			primary_communication ="home";
		  }
		  else{

			primary_communication ='office';
		  }

		  if(regdata.scheck =='true'){

			communication_email_id ='secondary';
		  }
		  else{

		  communication_email_id = 'primary';
		  }
		 var userprf = $.param({
			 first_name : regdata.first_name,
			 middle_name : regdata.middle_name,
			 last_name : regdata.last_name,
			 suffix : regdata.suffix,
			 gender :regdata.gender,
			 birthdate :birthdate,
			 marital_status :  regdata.marital_status,
			 nationality : regdata.nationality,
			 father_name : regdata.father_name,
			 mother_name :regdata.mother_name,
			 locality :regdata.locality,
			 street_name : regdata.street_name,
			 address :regdata.address,
			 landmark :regdata.landmark,
			 city:regdata.city,
			 pincode:regdata.pincode,
			 state: regdata.state,
			 country : regdata.country,
			 mobile :regdata.mobile_number,
			 primary_email :regdata.primary_email,
			 secondary_email :regdata.secondary_email,
			 company_name : regdata.company_name,
			 company_city : regdata.company_city,
			 designation : regdata.designation,
			 annual_income : regdata.annual_income,
			 qualification :regdata.qualifications,
			 college_name :regdata.college,
			 language_known :regdata.language_known,
			 languages_known_read_write :regdata.languages_known_read_write,
			 company_website:regdata.company_website,
			 mother_tongue:regdata.mother_tongue,
			year_passout : regdata.year_passout,
			company_address1 : regdata.company_address1,
			company_address2 : regdata.company_address2,
			company_landmark : regdata.company_landmark,
			company_locality : regdata.company_locality,
			company_state : regdata.company_state,
			company_pincode :regdata.company_pincode,
			company_country : regdata.company_country,
			is_submitted_all : "true",
			additional_qualification :education,
			facebook_media : regdata.facebook_media,
			google_media : regdata.google_media,
			linkedin_media : regdata.linkedin_media,
			twitter_media : regdata.twitter_media,
			education_category :regdata.education_category,
			pan_no: regdata.pan_no,
			primary_communication :  primary_communication,
			communication_email : communication_email_id,
			hidden_practice_details_input : regPracticeDetails,
			req_type : "mobile"
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
		 var  dquestion = angular.toJson(question);
		 var url = domain_url +ADVISORPROFILEANSWER;
		 var data = $.param({questions : dquestion ,is_submitted_questions : 'True', req_type:"mobile"});
     var promise = $http({
				method :'POST',
				data : data ,
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
		 

		 profilepromise.postdata = function(data,type){
			if(type =="certificate")
			{
				document_type = "certificate";
			}
			if(type =="educational_doc")
			{
				document_type = "educational_doc";
			}
			$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
			var url = domain_url+UPEIPV;
			var fd = ({document_type : document_type,image:data,req_type : "mobile"});
		var	promise = Upload.upload({
				url:url,
				data:fd
			}).then(function(res){
				console.log(res);
				return res.data;
			},function(error){
				return  error;
			});
			 return promise;
			}
     
		 profilepromise.editprofiledetails5 = function(education_data,cert_data){
			var educational_detail = "";
			var certification_detail = "";
			educational_detail = '{"school":"' + education_data.educational_details.school + '", "qualification":"' + education_data.educational_details.qualification + '","field_of_study":"' + education_data.educational_details.field_of_study + '","activities":"' + education_data.educational_details.activities + '","from_year":"' + education_data.educational_details.from_year + '","to_year":"' + education_data.educational_details.to_year + '","grade":"' + '' + '"}';
	    if(cert_data==undefined){
				certification_detail = '[{"certificate_name":"' + "" + '", "certi_authority":"' + "" + '","licence_number":"' + "" + '","time_period_from":"' + '' + '","certificate_from_year":"' + "" + '","certificate_to_year":"' + "" + '", "certi_credibility":"' + '' + '","certi_url":"' + "" + '", "certificate_expire":"' + false + '"}]';

			}
			else{
				certification_detail = cert_data;

			}
			
			var url = domain_url +EDUCATIONDETAILS;
			var data = $.param({'educational_details': educational_detail,
			'certification_details': certification_detail});
			var promise = $http({
				 method :'POST',
				 data : data ,
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

.factory('adharverify',['$http','$q','CREATEADHARFORM','$location','CHECKMEMBERAADHAAR','SAVEADHAAR',
	 function($http,$q,CREATEADHARFORM,$location,CHECKMEMBERAADHAAR,SAVEADHAAR) {
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
		 },
         save_adhaar : function(data){
			var url = domain_url+SAVEADHAAR;
			var adhaar_number  = $.param({adhaar_number : data});
			var promise = $http({
				method :'POST',
				data : adhaar_number ,
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

	 }
}])

.factory('aadhar_success',['$http','$q','SUCCESS','$location','MEMBERSUCCESS',function($http,$q,SUCCESS,$location,MEMBERSUCCESS) {
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

.factory('aadhar_failure',['$http','$q','FAILURE','$location','MEMBERFAILURE',function($http,$q,FAILURE,$location,MEMBERFAILURE) {
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
