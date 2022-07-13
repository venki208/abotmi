angular.module('myhub_factories',['myhub_constants'])

.factory('MyHubDetails',['$localStorage','$http','$q','$location','MYHUBDETAILS',
        'VIDEOREQUEST','VIDEOPUBLISH', function($localStorage,$http,$q,$location,
        MYHUBDETAILS,VIDEOREQUEST,VIDEOPUBLISH){
	var result = [],promise = "";
	var domain_url = $location.protocol()+"://"+$location.host()+":"+$location.port();
	return {
		getDetails : function(){
      $http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
			var url = domain_url+MYHUBDETAILS;
           promise =  $http({
                method : 'POST',
                url : url,
                data : $.param({'req_type':'mobile'}),
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
            })
            .then(function(response){
                return response.data;
            }
            ,function(response){
                return $q.reject(response);
            });
            return promise;
		},
    getvideorequest : function(form_data){
        $http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
  			var url = domain_url+VIDEOREQUEST;
        promise = $http({
          method:"POST",
          url:url,
          data: $.param({
            'req_type':'mobile',
            'microlearning_tittle':form_data.title,
            'descrition_of_the_topic':form_data.description,
            'microlearning_location':form_data.location,
            'preffered_date_of_shoot':form_data.preffered_date_of_shoot,
            'animation_required':form_data.animation_required
          }),
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
          }
      })
      .then(function(response){
          return response.status;
      }
      ,function(response){
          return $q.reject(response);
      });
      return promise;
    },
    sendvideopublish: function(video_title, video_description, video_link){
        $http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
        var url = domain_url+VIDEOPUBLISH;
        promise = $http({
          url : url,
          method : "POST",
          data : $.param({
              'req_type':'mobile',
              'video_title':video_title,
              'video_description':video_description,
              'video_url':video_link
          }),
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
          }
        })
        .then(function(response){
            return response.status;
        }
        ,function(response){
            return $q.reject(response);
        });
      return promise;
    }
	}
}])

.factory('submitData', ['$http','$q','$timeout','$location','REFERADVISORURL','INVITERATEURL',
        'SUBMITRATEURL','CHECKPROMOCODEURL','APPLYCRISILURL','CRISILREFDOCURL','GETINTOUCH',
				'CRISILRENEWAL','Upload','CHANGEPASSWORD','WEBINAR','MEETUP','MEETUPUPDATE','ADDCLIENTFORMUPWRDZ',
        'ADDCLIENTAADHAAR', function($http,$q,$timeout,$location,REFERADVISORURL,INVITERATEURL,
          SUBMITRATEURL, CHECKPROMOCODEURL,APPLYCRISILURL,CRISILREFDOCURL,GETINTOUCH,CRISILRENEWAL,
            Upload,CHANGEPASSWORD,WEBINAR,MEETUP,MEETUPUPDATE,ADDCLIENTFORMUPWRDZ,ADDCLIENTAADHAAR){
      	var returnpromise = '',parameter=[],json = {},msg = '';

      	$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
      	var domain_url = $location.protocol()+"://"+$location.host()+":"+$location.port();

        return{
          referAdvisor : function(data){
            var url = domain_url+REFERADVISORURL;
            json = '{"0":["'+data.name+'","'+data.email+'","'+data.mobile+'","'+data.location+'","'+data.products+'","'+data.is_registered+
                    '","'+data.sebi+'","'+data.amfi+'","'+data.irda+'","'+data.crisilnumber+'","'+data.knownduration+'","'+data.justify+'","mobile"]}';
            parameter = $.param({jsondata : json,req_type:"mobile"});
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

        inviteRate : function(data,type){
            var invitejson = '{"name":"'+data.name+'","email":"'+data.email+'","mobile":"'+data.mobile+'","user_type":"'+type+'","req_type":"mobile"}';
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

        checkPromoCode : function(data){
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
        updatemeetup:function(recived){
            console.log("hiii",MEETUPUPDATE);
            var touchpromise;
                      var url = domain_url+MEETUPUPDATE;
            touchpromise = $http({
               url : url,
               method : "POST",
               data :"event_id="+recived.meetup_event_id+"&name="+recived.name+"&description="+recived.description+"&scheduled="+recived.formatted_date+"&landmark="+recived.landmark+"&hours="+recived.hours+"&project="+recived.uplyf_project+"&minutes="+recived.minutes+"&address="+recived.address+"&location="+recived.location+"&req_type=" +"mobile",
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
        meetup : function(recived){
             var touchpromise;
					   var url = domain_url+MEETUP;
             touchpromise = $http({
                url : url,
                method : "POST",
                data :"name="+recived.name+"&description="+recived.description+"&scheduled="+recived.formatted_date+"&landmark="+recived.landmark+"&hours="+recived.hours+"&project="+recived.uplyf_project+"&minutes="+recived.minutes+"&address="+recived.address+"&location="+recived.location+"&req_type=" +"mobile",
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

        webinar : function(recived){
             var touchpromise;
             var url = domain_url+WEBINAR;
             var strDateTime = recived.datetimeValue;
             var myDate = new Date(strDateTime);
             recived.datetimeValue=myDate.toLocaleString();
             var res =  recived.datetimeValue.split(",");
             var str1=res[0];
             var str2=res[1];
             recived.datetimeValue = str1.concat(str2);
             touchpromise = $http({
                  method : "POST",
                  url : url,
                  data :"name="+recived.name+"&lobby_description="+recived.lobby_description+"&starts_at="+recived.formatted_date+"&duration="+recived.duration+"&uplyf_project="+recived.uplyf_project+"&req_type=" +"mobile",
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

        applyCrisil : function(year){
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

        crisilDocSubmit : function(data){
            var fd = ({cheque_dd_no : data.payment[1],cheque_date:data.dateofpay,bankname:data.payment[0],scaned_doc:data.refdoc});
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

        crisilRenewSubmit : function(data,amount,expiry_date){
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

        submitRating : function(data){
            var submitparam = $.param({activation_key : data.activationkey,trust:data.trust,financial : data.financial,communication : data.comm , advisory : data.advisory , ethics : data.ethics , customer : data.ccare , average : data.avgrate,req_type:"mobile"});
            var url = domain_url+SUBMITRATEURL;
            var ratedpromise = $http({
                    url : url,
                    method : "POST",
                data : submitparam,
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
                return ratedpromise;
        },

        addClient : function(data,type){
      		$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
          data["req_type"] = "mobile";
			    var formdata = $.param(data);
    			if (type == "form"){
            var url = domain_url+ADDCLIENTFORMUPWRDZ;
          }else{
            var url = domain_url+ADDCLIENTAADHAAR;
          }
		      promise = $http({
						method : "POST",
						url:url,
						data: formdata,
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

.factory('DownloadCertificateFactory',['$resource','DOWNLOADCERTIFICATE',function($resource,DOWNLOADPROFILE){
	return $resource(DOWNLOADPROFILE, {}, {
      pdf: {
        method: 'POST',
        responseType: 'arraybuffer',
        cache: true,
        transformResponse: function(data) {
          var pdf;
          if (data) {
            pdf = new Blob([data], {
              type: 'application/pdf'
            });
          }
          return {
            response: pdf
          };
        }
      }
    });
}])

.factory('webinar_factory', function($http, $location, WEBINAR_LIST, REGISTER_INVITATION_WEBINAR, DELETEWEBINAREVENT, LISTMEMBERINVITATION,WEBINAR_GET_ROOM_NAME_MOBILE, $q) {
    var domain_url = $location.protocol() + "://" + $location.host() + ":" + $location.port();
    return {
        webinar_delete : webinar_delete,
        list_webinar : list_webinar,
        register_invitation : register_invitation,
        get_webinar_list : get_webinar_list,
        get_room_name : get_room_name
    }

    function get_room_name(room_name){
        var url = domain_url+WEBINAR_GET_ROOM_NAME_MOBILE;
        var trans = $http({
            method : "POST",
            url:url,
            data: $.param({'req_type':'mobile', 'room_name':room_name}),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).then(function(res){
            return res.data;
        },function(error){
            return $q.reject(error);
        });
        return trans;
    }

    function get_webinar_list(){
        var touchpromise="";
        var url = domain_url+WEBINAR_LIST;
        var config = {
            params: {
                req_type: "mobile"
            }
        }
        touchpromise = $http.get(url,config).
        then(function(result){
                msg = result.data;
                return msg;
                },function(result){
                return $q.reject(result);
                });
        return touchpromise;
    }

    function register_invitation(reg_invite){
        var url = domain_url+REGISTER_INVITATION_WEBINAR;
        var trans = $http({
            method : "POST",
            url : url,
            data : $.param({ 'member_details' : reg_invite,'req_type': "mobile" }),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).then(function(res){
            return res.data;
        },function(error){
            return $q.reject(error);
        });
        return trans;
    }

    function list_webinar(webinarlist){
        var touchpromise;
        var url = domain_url + LISTMEMBERINVITATION;
        var config = {
            params: {
                req_type: "mobile",room_id: webinarlist
            }
        }

        touchpromise = $http.get(url,config)
        .then(function(result){
             msg = result.data;
             return msg;
             },function(result){
             return $q.reject(result);
             });

        return touchpromise;
    }

    function webinar_delete(recived){
        var touchpromise;
        var url = domain_url + DELETEWEBINAREVENT;
        touchpromise = $http({
            url: url,
            method: "POST",
            data: "room_id=" + recived +"&req_type=" + "mobile",
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
})

.factory('meetup_factory', function($http, $location, MEETUP_LIST, SEND_MEETUP_INVITATION_MAIL, DELETEMEETUPEVENT, LISTMAILINVITATION, $q) {
    var domain_url = $location.protocol() + "://" + $location.host() + ":" + $location.port();
    return {
        meetup_delete : meetup_delete,
        get_email_list : get_email_list,
        sendinvitationmail : sendinvitationmail,
        get_meetup_list : get_meetup_list
    }

    function get_meetup_list(){
        var touchpromise;
        var url = domain_url+MEETUP_LIST;
        var config = {
            params: {
                req_type: "mobile"
            }
        }
        touchpromise = $http.get(url,config).
        then(function(result){
             msg = result.data;
             return msg;
             },function(result){
             return $q.reject(result);
             });
        return touchpromise;
    }

    function sendinvitationmail(meetuplist){
        var url = domain_url+SEND_MEETUP_INVITATION_MAIL;
        var trans = $http({
            method : "POST",
            url : url,
            data : $.param({ 'email_list' : meetuplist,'req_type': "mobile" }),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).then(function(res){
            return res.data;
        },function(error){
            return $q.reject(error);
        });
        return trans;
    }

    function get_email_list(){
        var touchpromise;
        var url = domain_url + LISTMAILINVITATION;
        var config = {
            params: {
                req_type: "mobile"
            }
        }
        touchpromise = $http.get(url,config).
        then(function(result){
             msg = result.data;
             return msg;
             },function(result){
             return $q.reject(result);
             });

        return touchpromise;
    }

    function meetup_delete(recived) {
        var touchpromise;
        var url = domain_url + DELETEMEETUPEVENT;
        touchpromise = $http({
            url: url,
            method: "POST",
            data: "event_id=" + recived +"&req_type=" + "mobile",
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

})
.factory('Project_Details_Uplyf',function($http,$location,GET_UPLYF_PROJECT_DETAILS,$q){
	var domain_url = $location.protocol()+"://"+$location.host()+":"+$location.port();
	var touchpromise;
	var url = domain_url+GET_UPLYF_PROJECT_DETAILS;
	var config = {
		params: {
			req_type: "mobile"

		}
	}
	touchpromise = $http.get(url,config).
	then(function(result){
		 msg = result.data;
		 return msg;
		 },function(result){
		 return $q.reject(result);
		 });
	return touchpromise;
	})

.factory('DashboardDetailsFactory',['$localStorage','$http','VIEWRANKDETAILSURL','$q','TORATEPEERURL','VIEWCLIENTSURL',
	'VIEWLOOPURL','DISOWNMEMBERURL','$location','GETUPLYFTRANSACTIONS','CHECKREFERADVISOREMAIL','LISTENQUIRY','LISTCLIENTENQUIRY', 'SAVE_CALENDLY_LINK',
    function($localStorage,$http,VIEWRANKDETAILSURL,$q,TORATEPEERURL,VIEWCLIENTSURL,VIEWLOOPURL,DISOWNMEMBERURL,$location,
    GETUPLYFTRANSACTIONS,CHECKREFERADVISOREMAIL,LISTENQUIRY,LISTCLIENTENQUIRY,SAVE_CALENDLY_LINK){
	var detailresult = [],promise = '',parameter = {};
	var loopresult = [],promise = "",viewclientres = [],clientpromise = "",calendly = "";
	$http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
	var domain_url = $location.protocol()+"://"+$location.host()+":"+$location.port();

	return {
		viewClientDetails:function(){
		    var url = domain_url+VIEWCLIENTSURL;
            clientpromise = $http.post(url).
            then(function(res){
                viewclientres = res.data;
                return viewclientres;
            },function(error){
                return $q.reject(error);
            });
            return clientpromise;
        },
        
        save_calendly_link:function(calendlyUrl){
            var url = domain_url+SAVE_CALENDLY_LINK;
            $http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
            var req = {
				method: 'POST',
				url: url,
                data: $.param({'link': calendlyUrl}),
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization' : 'JWT '+localStorage.getItem('jwttoken')
                 },
			}
            calendly = $http(req).
            then(function(res){
                calendly = res.data;
                return calendly;
            },function(error){
                return $q.reject(error);
            });
            return calendly;
		},

		viewAdvisorLoop : function(){
			var url = domain_url+VIEWLOOPURL;
            var req = {
				method: 'POST',
				url: url,
				headers: {
				   'Content-Type': 'application/x-www-form-urlencoded'
				},
				data: $.param({'req_type':'mobile'})
			}
			promise = $http(req).
			then(function(res){
				loopresult = res.data;
				return loopresult;
			},function(error){
				return $q.reject(error);
			});
			return promise;
		},

		viewRankDetails : function(type){
			parameter = $.param({'user_type' : type,'req_type':'mobile'});
			var url = domain_url+VIEWRANKDETAILSURL;
			var req = {
				method: 'POST',
				url: url,
				headers: {
				   'Content-Type': 'application/x-www-form-urlencoded'
				},
				data: parameter
			}
			rankpromise = $http(req)
			.then(function(res){
				detailresult = res.data;
				return detailresult;
			},function(error){
				return $q.reject(error);
			});
		    return rankpromise;
	    },

        getPeersRateList : function(){
            var ratelist = [];
            $http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
            var url = domain_url+TORATEPEERURL;
            var ratepromise = $http.get(url).
            then(function(res){
                ratelist = res.data;
                return ratelist;
            },function(error){
                return $q.reject(error);
            });
            return ratepromise;
        },

        disownMember : function(emailid){
            var emailparam = $.param({member_email : emailid});
            var url = domain_url+DISOWNMEMBERURL;
            var disownprom = $http({
                method : "POST",
                url : url,
                data : emailparam,
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).then(function(res){
                return res.data;
            },function(error){
                return $q.reject(error);
            });
            return disownprom;
        },

        ratePeer : function(key){
            var peerrate = [];
            $http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
            var promise = $http.post().
            then(function(res){
                peerrate = res.data;
                return peerrate;
            },function(error){
                return $q.reject(error);
            });
            return promise;
        },

        getTransactions : function(){
            $http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
            var url = domain_url+GETUPLYFTRANSACTIONS;
            var trans = $http({
                method : "POST",
                url : url,
                data : $.param({req_type : "mobile"}),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).then(function(res){
                return res.data;
            },function(error){
                return $q.reject(error);
            });
            return trans;
        },

        check_refer_email : function(data){
            $http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
            var url = domain_url+CHECKREFERADVISOREMAIL;
            var trans = $http({
                method : "POST",
                url : url,
                data : $.param({req_type : "mobile",email_id:data}),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).then(function(res){
                return res.data;
            },function(error){
                return $q.reject(error);
            });
            return trans;
        },

        viewEnquiries : function(type){
            $http.defaults.headers.common['Authorization'] = 'JWT '+localStorage.getItem('jwttoken');
            if(type == "client"){
                var url = domain_url+LISTCLIENTENQUIRY;
            }else{
                var url = domain_url+LISTENQUIRY;
            }
            var trans = $http({
                method : "POST",
                url : url,
                data : $.param({req_type : "mobile"}),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).then(function(res){
                return res.data;
            },function(error){
                return $q.reject(error);
            });
            return trans;
        }
	}
}])
