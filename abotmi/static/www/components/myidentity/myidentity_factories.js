angular.module('myidentity_factories', ['myidentity_constants'])

    .factory('MyIdentityDetails', ['$localStorage', '$http', '$q', '$location', 'MYIDENTITYDETAILS', 'SAVE_EDUCATION',
        'SAVE_LANGUAGE', 'SAVE_MYPROMISE', 'SAVE_MYBELIEF', 'SAVE_CONTECTDETAILS', 'SAVE_SKILLS', 'SAVE_CLIENTS',
        'SAVE_ADVISOR', 'SAVE_ADVISORY_SPEC', 'SAVE_SALE_ACCOMPLISHMENTS', 'SAVE_REGULATORY_CERTIFICATION',
        'SAVE_ADDITIONAL_QUALIFICATION', 'SAVE_ABOUTME', 'EDUCATIONSAVE', 'UPEIPV', 'Upload', 'CERTIFICATIONSAVE',
        function ($localStorage, $http, $q, $location, MYIDENTITYDETAILS, SAVE_EDUCATION, SAVE_LANGUAGE, SAVE_MYPROMISE,
            SAVE_MYBELIEF, SAVE_CONTECTDETAILS, SAVE_SKILLS, SAVE_CLIENTS, SAVE_ADVISOR, SAVE_ADVISORY_SPEC,
            SAVE_SALE_ACCOMPLISHMENTS, SAVE_REGULATORY_CERTIFICATION, SAVE_ADDITIONAL_QUALIFICATION, SAVE_ABOUTME, EDUCATIONSAVE, UPEIPV, Upload, CERTIFICATIONSAVE) {
            var result = [];
            var promise = "";
            var domain_url = $location.protocol() + "://" + $location.host() + ":" + $location.port();
            return {
                getDetails: function () {
                    $http.defaults.headers.common['Authorization'] = 'JWT ' + localStorage.getItem('jwttoken');
                    var url = domain_url + MYIDENTITYDETAILS;
                    promise = $http({
                            method: 'POST',
                            url: url,
                            data: $.param({
                                'req_type': 'mobile'
                            }),
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded'
                            },
                        })
                        .then(function (response) {
                            return response.data;
                        }, function (response) {
                            return $q.reject(response);
                        });
                    return promise;
                },

                saveLanguage: function (data) {
                    $http.defaults.headers.common['Authorization'] = 'JWT ' + localStorage.getItem('jwttoken');
                    var url = domain_url + SAVE_LANGUAGE;
                    promise = $http({
                            method: 'POST',
                            url: url,
                            data: $.param({
                                'languages_known_speak': data.languages_known_speak,
                                'languages_known_read_write': data.languages_known_read_write
                            }),
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded'
                            },
                        })
                        .then(function (response) {
                            return response.data;
                        }, function (response) {
                            return $q.reject(response);
                        });
                    return promise;
                },

                saveMyPromise: function (data) {
                    $http.defaults.headers.common['Authorization'] = 'JWT ' + localStorage.getItem('jwttoken');
                    var url = domain_url + SAVE_MYPROMISE;
                    promise = $http({
                            method: 'POST',
                            url: url,
                            data: $.param({
                                'my_promise': data.my_promise
                            }),
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded'
                            },
                        })
                        .then(function (response) {
                            return response.data;
                        }, function (response) {
                            return $q.reject(response);
                        });
                    return promise;
                },

                saveMyBelief: function (data) {
                    $http.defaults.headers.common['Authorization'] = 'JWT ' + localStorage.getItem('jwttoken');
                    var url = domain_url + SAVE_MYBELIEF;
                    promise = $http({
                            method: 'POST',
                            url: url,
                            data: $.param({
                                'my_belief': data.my_belief
                            }),
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded'
                            },
                        })
                        .then(function (response) {
                            return response.data;
                        }, function (response) {
                            return $q.reject(response);
                        });
                    return promise;
                },

                saveContectDetails: function (data) {
                    $http.defaults.headers.common['Authorization'] = 'JWT ' + localStorage.getItem('jwttoken');
                    var url = domain_url + SAVE_CONTECTDETAILS;
                    promise = $http({
                            method: 'POST',
                            url: url,
                            data: $.param({
                                'req_type': 'mobile',
                                'mobile': data.mobile,
                                'address': data.address,
                                'city': data.city,
                                'calendly': data.calendly
                            }),
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded'
                            },
                        })
                        .then(function (response) {
                            return response.data;
                        }, function (response) {
                            return $q.reject(response);
                        });
                    return promise;
                },
                saveSkills: function (data_arr) {
                    $http.defaults.headers.common['Authorization'] = 'JWT ' + localStorage.getItem('jwttoken');
                    var url = domain_url + SAVE_SKILLS;
                    promise = $http({
                            method: 'POST',
                            url: url,
                            data: $.param({
                                'req_type': 'mobile',
                                'skills_content': data_arr
                            }),
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded'
                            },
                        })
                        .then(function (response) {
                            return response.data;
                        }, function (response) {
                            return $q.reject(response);
                        });
                    return promise;
                },

                updateadvisoryspec: function (data) {
                    var dataid = $.param({
                        'financial_instruments': data
                    });
                    var url = domain_url + SAVE_ADVISORY_SPEC;
                    $http.defaults.headers.common['Authorization'] = 'JWT ' + localStorage.getItem('jwttoken');
                    promise = $http({
                        method: "POST",
                        url: url,
                        data: dataid,
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
                        }
                    }).
                    then(function (res) {
                        postresult = res.data;
                        return postresult;
                    }, function (res) {
                        return $q.reject(res);
                    });
                    return promise;
                },

                postdata: function (data, type) {
                    if(type =="certificate")
                    {
                        document_type = "certificate";
                    }
                    if(type =="educational_doc")
                    {
                        document_type = "educational_doc";
                    }
                    $http.defaults.headers.common['Authorization'] = 'JWT ' + localStorage.getItem('jwttoken');
                    var url = domain_url + UPEIPV;
                    var fd = ({
                        document_type: document_type,
                        image: data,
                        req_type: "mobile"
                    });
                    var promise = Upload.upload({
                        url: url,
                        data: fd
                    }).then(function (res) {
                        return res.data;
                    }, function (error) {
                        return error;
                    });
                    return promise;
                },
                saveEducationalDetails: function (education_data) {
                    var educational_detail = "";
                    //var certification_detail = "";
                    if (education_data.educational_details.field_of_study == undefined) {
                        education_data.educational_details.field_of_study = ''
                    }
                    if (education_data.educational_details.activities == undefined) {
                        education_data.educational_details.activities = ''
                    }

                    educational_detail = '{"school":"' + education_data.educational_details.school + '", "qualification":"' + education_data.educational_details.qualification + '","field_of_study":"' + education_data.educational_details.field_of_study + '","activities":"' + education_data.educational_details.activities + '","from_year":"' + education_data.educational_details.from_year + '","to_year":"' + education_data.educational_details.to_year + '","grade":"' + '' + '"}';
                    var url = domain_url + EDUCATIONSAVE;
                    $http.defaults.headers.common['Authorization'] = 'JWT ' + localStorage.getItem('jwttoken');
                    var data = $.param({
                        'educational_details': educational_detail
                    });
                    var promise = $http({
                        method: 'POST',
                        data: data,
                        url: url,
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded'
                        }
                    }).then(function (result) {
                        return result.data;
                    }, function (error) {
                        return error;
                    });
                    return promise;
                },


                saveCertificationalDetails: function (education_data,cert_data) {
                    var certification_detail = "";
                    certification_detail = cert_data;
                    var url = domain_url + CERTIFICATIONSAVE;
                    $http.defaults.headers.common['Authorization'] = 'JWT ' + localStorage.getItem('jwttoken');
                    var data = $.param({
                        'certification_data': certification_detail
                    });
                    var promise = $http({
                        method: 'POST',
                        data: data,
                        url: url,
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded'
                        }
                    }).then(function (result) {
                        return result.data;
                    }, function (error) {
                        return error;
                    });
                    return promise;
                },


                update_additional_qualification: function (data, edudata) {
                    var data = $.param({
                        'additional_qualification': data,
                        'qualification': edudata.qualification,
                        'year_of_passout': edudata.year_passout,
                        'college_name': edudata.college_name
                    });
                    var url = domain_url + SAVE_ADDITIONAL_QUALIFICATION;
                    $http.defaults.headers.common['Authorization'] = 'JWT ' + localStorage.getItem('jwttoken');
                    promise = $http({
                        method: "POST",
                        url: url,
                        data: data,
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
                        }
                    }).
                    then(function (res) {
                        postresult = res.data;
                        return postresult;
                    }, function (res) {
                        return $q.reject(res);
                    });
                    return promise;
                },

                updatesales: function (data) {
                    var dataid = $.param({
                        'sale_content': data
                    });
                    var url = domain_url + SAVE_SALE_ACCOMPLISHMENTS;
                    $http.defaults.headers.common['Authorization'] = 'JWT ' + localStorage.getItem('jwttoken');
                    promise = $http({
                        method: "POST",
                        url: url,
                        data: dataid,
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
                        }
                    }).
                    then(function (res) {
                        postresult = res.data;
                        return postresult;
                    }, function (res) {
                        return $q.reject(res);
                    });
                    return promise;
                },

                saveregulatorycertification: function (data_to_send) {
                    var url = domain_url + SAVE_REGULATORY_CERTIFICATION;
                    $http.defaults.headers.common['Authorization'] = 'JWT ' + localStorage.getItem('jwttoken');
                    promise = $http({
                        method: "POST",
                        url: url,
                        data: data_to_send,
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
                        }
                    }).
                    then(function (res) {
                        postresult = res.data;
                        return postresult;
                    }, function (res) {
                        return $q.reject(res);
                    });
                    return promise;
                },

                saveclients: function (data) {
                    $http.defaults.headers.common['Authorization'] = 'JWT ' + localStorage.getItem('jwttoken');
                    var url = domain_url + SAVE_CLIENTS;
                    promise = $http({
                            method: 'POST',
                            url: url,
                            data: $.param({
                                'total_client_serverd_count': data,
                                'req_type': 'mobile'
                            }),
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded'
                            },
                        })
                        .then(function (response) {
                            return response.data;
                        }, function (response) {
                            return $q.reject(response);
                        });
                    return promise;
                },

                saveadvisor: function (data) {
                    $http.defaults.headers.common['Authorization'] = 'JWT ' + localStorage.getItem('jwttoken');
                    var url = domain_url + SAVE_ADVISOR;
                    promise = $http({
                            method: 'POST',
                            url: url,
                            data: $.param({
                                'total_advisors_connected': data,
                                'req_type': 'mobile'
                            }),
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded'
                            },
                        })
                        .then(function (response) {
                            return response.data;
                        }, function (response) {
                            return $q.reject(response);
                        });
                    return promise;
                },

                saveaboutme: function (data) {
                    $http.defaults.headers.common['Authorization'] = 'JWT ' + localStorage.getItem('jwttoken');
                    var url = domain_url + SAVE_ABOUTME;
                    promise = $http({
                            method: 'POST',
                            url: url,
                            data: $.param({
                                'self_declaration_content': data,
                                'req_type': 'mobile'
                            }),
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded'
                            },
                        })
                        .then(function (response) {
                            return response.data;
                        }, function (response) {
                            return $q.reject(response);
                        });
                    return promise;
                }
            }
        }
    ])


    .factory('sendEmail', ['$http', '$q', 'ADMINMAILURL', '$location', function ($http, $q, ADMINMAILURL, $location) {
        var returnpromise = '';
        var msg = '';
        $http.defaults.headers.common['Authorization'] = 'JWT ' + localStorage.getItem('jwttoken');
        var domain_url = $location.protocol() + "://" + $location.host() + ":" + $location.port();
        return {
            sendEmailShare: function (recived) {
                var url = domain_url + ADMINMAILURL;
                returnpromise = $http({
                        url: url,
                        method: "POST",
                        data: "title=" + recived.title + "&name=" + recived.name + "&email_to=" + recived.email_to + "&mail_body=" + recived.mail_body + "&template_name=" + recived.template_name + "&subject=" + recived.subject,
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
                        }
                    })
                    .then(function (result) {
                        msg = result.data;
                        return msg;
                    }, function (result) {
                        return $q.reject(result);
                    });
                return returnpromise;
            }
        }
    }])

    .factory('downloadprofile', ['$resource', 'DOWNLOADPROFILE', function ($resource, DOWNLOADPROFILE) {
        return $resource(DOWNLOADPROFILE, {}, {
            pdf: {
                method: 'POST',
                responseType: 'arraybuffer',
                cache: true,
                transformResponse: function (data) {
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
