angular.module('reg_user_controllers', [])

  .controller('RegCtrl', function ($state, $ionicSideMenuDelegate, $scope, $ionicPopup, get_userDetails, $timeout, $ionicLoading, submitProfileData, get_reguserdetails, deviceDetector, $controller, $rootScope) {
    var reg = this;
    var iti;
    var global_number;
    reg.isDisabled = false;
    
    reg.devicedetection = deviceDetector;




    reg.init = function () {

      $ionicLoading.show({
        content: 'Loading',
        animation: 'fade-in',
        showBackdrop: true,
        maxWidth: 200,
        showDelay: 0
      });
      // Adding year options to certification and eductation year fields
      var date = new Date();
      let dateArray = [];
      reg.fromyear = [];
      names = []
      curYear = date.getFullYear();
      for (var j = 0; j < 65; j++) {
        dateArray[j] = (curYear - 64) + j;
        reg.fromyear.push(dateArray[j]);
      }



      $scope.data = {
        names: [{}]
      };
      $scope.data1 = {
        names1: [{}]
      };

      $scope.addRow = function (index) {
        if ($scope.data.names[index].practice_country != undefined && $scope.data.names[index].practice_city != undefined && $scope.data.names[index].pincode != undefined) {
          var name = {};
          if ($scope.data.names.length <= index + 1) {
            $scope.data.names.splice(index + 1, 0, name);
          }
        }
      };


      $scope.deleteRow = function ($event, name) {
        var index = $scope.data.names.indexOf(name);
        if ($event.which == 1)
          $scope.data.names.splice(index, 1);
      }


      $scope.addRow1 = function (index) {
         if ($scope.data1.names1[index].certification_name !=undefined &&  $scope.data1.names1[index].certi_authority !=undefined && $scope.data1.names1[index].licence_number !=undefined && $scope.data1.names1[index].certi_url !=undefined && $scope.data1.names1[index].from_year !=undefined && $scope.data1.names1[index].to_year) {
          var name = {}; 
          if ($scope.data1.names1.length <= index + 1) {
            $scope.data1.names1.splice(index + 1, 0, name);
          }
        }
      };


      $scope.deleteRow1 = function ($event, name) {
        var index = $scope.data1.names1.indexOf(name);
        if ($event.which == 1)
          $scope.data1.names1.splice(index, 1);
      }

      reg.year = [];

      var max = new Date().getFullYear();
      var min = max - 100;
      for (var i = max; i >= min; i--) {
        reg.year.push(i.toString());

      }

      var countrypromise = get_reguserdetails.getcountry();
      countrypromise.then(function (data) {
        reg.country = data.data;
      }, function (error) {
        swal("Server Error", "Try again later");
      });

      var digital_footprint = get_userDetails.get_digital_link();
      digital_footprint.then(function (results_get) {
        reg.results = results_get.data;

      }, function (error) {
        swal("Server Error", "Try again later");
      });


      var promise = get_userDetails.getDetails();
      promise.then(
        function (payload) {
          $timeout(function () {
            $ionicLoading.hide();
          }, 1000);

          reg.user_details = payload;
          if(!reg.user_details.country){

            reg.user_details.country="United States"
          }
          
          if(!reg.user_details.company_country){

            reg.user_details.company_country="United States"
          }
          if(reg.user_details.educational_details){
          if(reg.user_details.educational_details.activities == "undefined"){
           
            reg.user_details.educational_details.activities=""
          }
          if(reg.user_details.educational_details.field_of_study == "undefined"){
           
            reg.user_details.educational_details.field_of_study=""
          }
        }
          global_number = reg.user_details.mobile_number;
          if (iti) {
            if (global_number) {
              iti.setNumber(global_number);
            }
          }
          // window.intlTelInput(input);
          var education_document = localStorage.getItem('educational_document');
          if (education_document) {
            reg.user_details.eipv_face_capture = education_document;
          }

          if (reg.user_details.certification_details == null) {
            reg.user_details.certification_details = '';

          }
          if (reg.user_details.certification_details.certification_name == undefined) {
            reg.user_details.certification_details.certification_name = "";
          }
          if (reg.user_details.practice_details) {
            $scope.data.names = JSON.parse(reg.user_details.practice_details)
          }
          if (reg.user_details.certification_details) {
            $scope.data1.names1 = reg.user_details.certification_details
          }
          reg.dsa_details = reg.user_details.DSA_details;
          reg.rera_details = reg.user_details.RERA_details;
          reg.disable_add = false;
          reg.answer4 = false;

          if (reg.user_details.answer[2]) {
            reg.disable_add = true;
          }
          if (reg.user_details.answer == "") {
            reg.question3();
            reg.user_details.answer[2].Remark[0].Remark = [];
          }

          if (reg.user_details.Additional_qualification_list.length != 0) {
            if (reg.user_details.Additional_qualification_list[0].additional_qualification != "") {
              reg.addbutton = 'true';
            }
          }
          if (reg.user_details.RERA_details[0].rera_state == "") {
            reg.user_details.rera_checked = 'B';
          } else {
            reg.user_details.rera_checked = 'A';
          }
          if (reg.user_details.DSA_details[0].dsa_bank_name == "") {
            reg.user_details.dsa_checked = 'B';
          } else {
            reg.user_details.dsa_checked = 'A';
          }
          if (reg.user_details.IRDA_registration_no == "" || reg.user_details.IRDA_registration_no == null) {
            reg.user_details.irda = 'B';
          } else {
            reg.user_details.irda = 'A';
          }
          if (reg.user_details.SEBI_registration_no == "" || reg.user_details.SEBI_registration_no == null) {
            reg.user_details.sebi = 'B';
          } else {
            reg.user_details.sebi = 'A';
          }
          if (reg.user_details.other_registration_no == "" || reg.user_details.other_registration_no == null) {
            reg.user_details.otherregister = 'B';
          } else {
            reg.user_details.otherregister = 'A';
          }
          if (reg.user_details.AMFI_registration_no == "" || reg.user_details.AMFI_registration_no == null) {
            reg.user_details.amfi = 'B';
          } else {
            reg.user_details.amfi = 'A';
          }
          if (reg.user_details.primary_communication == "office") {
            reg.user_details.off_address = "true";
          } else if (reg.user_details.primary_communication == "home") {
            reg.user_details.checkaddress = "true";
          } else {
            reg.user_details.checkaddress = "true"
          }
          if (reg.user_details.communication_email_id == 'primary') {
            reg.user_details.check = 'true';
          } else if (reg.user_details.communication_email_id == 'secondary') {
            reg.user_details.scheck = 'true';
          } else {
            reg.user_details.check = 'true';
          }
          reg.user_details.answer[0].Remark[3].Answer = reg.user_details.total_advisors_connected;
          reg.user_details.answer[0].Remark[1].Answer = reg.user_details.total_clients_served;
        },
        function (error) {
          $timeout(function () {
            $ionicLoading.hide();
          }, 1000);
        });

    }
    reg.enableDetails = function () {
      var input = document.querySelector("#phone");


      iti = intlTelInput(input, {
        nationalMode: false,
        initialCountry: "us",
        separateDialCode: true,
        autoPlaceholder: "off",

        utilsScript: "intl-tel-input/build/js/utils.js"
      });

    }

    reg.question3 = function () {
      reg.user_details.answer = [];
      reg.user_details.answer[0] = {};
      reg.user_details.answer[0].Question = "1.Are you a Certified Financial Advisor or digital asset advisor ?";
      reg.user_details.answer[0].Remark = [];
      reg.user_details.answer[0].Remark[0] = {};
      reg.user_details.answer[0].Remark[0].Question = "Experience";
      reg.user_details.answer[0].Remark[1] = {};
      reg.user_details.answer[0].Remark[1].Question = "Total Number of clients so far";
      reg.user_details.answer[0].Remark[2] = {};
      reg.user_details.answer[0].Remark[2].Question = "Average transaction";
      reg.user_details.answer[0].Remark[3] = {};
      reg.user_details.answer[0].Remark[3].Question = "Total Advisors connected";
      reg.user_details.answer[1] = {};
      reg.user_details.answer[1].Question = "2) Do you have an infrastructure or will you be able to create an infrastructure to handle the clients ?";
      reg.user_details.answer[2] = {};
      reg.user_details.answer[1].Remark = [];
      reg.user_details.answer[2].Question = "3) Are you associated with any financial organization ?";
      reg.user_details.answer[2].Remark = [];
      reg.user_details.answer[2].Remark[0] = {};
      reg.user_details.answer[3] = {};
      reg.user_details.answer[2].Remark[0].Question = "Number of Institutions";
      reg.user_details.answer[2].Remark[0].Answer = "1";
      reg.user_details.answer[3].Question = "4) Will you be interested to undergo any training program about digital asset investments and advisory ?";
    }


    reg.finances_org_yes = function () {
      reg.disable_add = true;
      reg.user_details.answer[2].Remark[0].Remark = [];
      reg.user_details.answer[2].Remark[0].Remark[0] = {
        'Question': 'institution_name'
      };
      reg.user_details.answer[2].Remark[0].Remark[1] = {
        'Question': 'official_email_id'
      };
      reg.user_details.answer[2].Remark[0].Remark[2] = {
        'Question': 'registration_id'
      };
      reg.user_details.answer[2].Remark[0].Remark[3] = {
        'Question': 'year_of_association'
      };
    }
    reg.infrastructure = function () {


      var office_full_address = '';


      if ($.trim($("#office_ad1").val())) {
        office_full_address += $.trim($("#office_ad1").val());
      }
      if ($.trim($("#office_ad2").val())) {
        if (office_full_address) {
          office_full_address += " " + $.trim($("#office_ad2").val());
        } else {
          office_full_address += $.trim($("#office_ad2").val())
        }
      }
      if ($.trim($('#company_city').val())) {
        if (office_full_address) {
          office_full_address += " " + "\n" + $.trim($('#company_city').val());
        } else {
          office_full_address += $.trim($('#company_city').val());
        }
      }
      if ($.trim($('#office_state').val())) {
        if (office_full_address) {
          office_full_address += ", " + $.trim($('#office_state').val());
        } else {
          office_full_address += $.trim($('#office_state').val());
        }
      }
      if ($.trim($('#company_pincode').val())) {
        if (office_full_address) {
          office_full_address += " " + $.trim($('#company_pincode').val());
        } else {
          office_full_address += $.trim($('#company_pincode').val());
        }
      }
      if ($.trim($('#company_country').val())) {
        if (office_full_address) {
          office_full_address += " " + "\n" + $.trim($('#company_country').val());
        } else {
          office_full_address += $.trim($('#company_country').val());
        }
      }
      reg.user_details.answer[1].Remark = office_full_address;

    }

    reg.finances_org_no = function () {
      reg.user_details.answer[2].Remark[0].Remark = [];
      reg.disable_add = false;
    }

    reg.delete = function (data, i) {
      reg.disable_add = false;
      data.splice(i, 4);
    }

    reg.deletedu = function (data, i) {
      data.splice(i, 1);
    }

    reg.userAnswer4 = function (option) {
      if (option == 'no') {
        reg.answer4 = true;
      } else {
        reg.answer4 = false;
      }
    }

    reg.append = function (data, i) {
      var str = data;
      reg.user_details.answer[2].Remark[0].Remark[i].Answer = [];
      if (str.indexOf("https://www") == 0 || str.indexOf("http://www") == 0) {
        reg.user_details.answer[2].Remark[0].Remark[i].Answer = data;
      } else if (str.indexOf("www.") == 0) {
        string = "https://"
        reg.user_details.answer[2].Remark[0].Remark[i].Answer = string + data;
      } else {
        string = "https://www."
        reg.user_details.answer[2].Remark[0].Remark[i].Answer = string + data;
      }
    }

    reg.clear = function (data) {

      if (reg.user_details.sebi == 'B' && data == "sebi") {
        reg.user_details.SEBI_registration_no = "";
        reg.user_details.SEBI_expire_date = null;
        reg.user_details.SEBI_valid_from = null;
      }
      if (reg.user_details.irda == 'B' && data == "irda") {
        reg.user_details.IRDA_registration_no = "";
        reg.user_details.IRDA_expire_date = null;
        reg.user_details.IRDA_valid_from = null;
      }
      if (reg.user_details.amfi == 'B' && data == "amfi") {
        reg.user_details.AMFI_registration_no = "";
        reg.user_details.AMFI_expire_date = null;
        reg.user_details.AMFI_valid_from = null;
      }
      if (reg.user_details.otherregister == 'B' && data == "other") {
        reg.user_details.other_registration_no = "";
        reg.user_details.other_expiry_date = null;
        reg.user_details.other_registration_state = "";
      }
      if (reg.user_details.rera_checked == 'B' && data == "rera") {
        reg.rera_details = [{
          "rera_registration_no": "",
          "rera_state": "",
          "rera_expire_date": ""
        }];
      }
      if (reg.user_details.dsa_checked == 'B' && data == "dsa") {
        reg.dsa_details = [{
          "dsa_bank_name": "",
          "dsa_code": "",
          "dsa_how_long_associated": ""
        }];

      }
    }
    reg.confirmed = function (confirmed) {
      $state.go('app.footprint', {
        'confirmed': confirmed
      });
    }
    reg.adddata = function (data) {
      data.push({});
    }
    reg.addfin = function (data) {
      var new_qualification = {
        "additional_qualification": "",
        "university": "",
        "year_passout": "",
        "document_verified": "not_verified",
        "documents_upload": ""
      }
      data.push(new_qualification);
      reg.addbutton = 'true';
    }

    reg.cleardata = function () {
      reg.user_details.college = '';
      reg.user_details.year_passout = '';
      reg.user_details.qualifications = '';
    }
    reg.selectInstrument = function (instruments) {
      for (var i = 0; i < reg.user_details.Advisory_ins.length - 1; i++) {
        if (reg.user_details.Advisory_ins[i].instruments == instruments) {
          var j = reg.user_details.Advisory_ins.length - 1;
          var instruments1 = reg.user_details.Advisory_ins[j]['instruments'] = "";
          if (!instruments1) {
            document.getElementById("finances" + j + '').value = "";
            swal("select other field experience", "", "error")
          }
          break;
        }
      }
    }

    reg.editprofile1 = function (dsa, rera) {

      var isValid = iti.isValidNumber();

      if (!isValid) {
        swal("please select valid number", "", "error")
      } else {
        var number = iti.getNumber();
        reg.user_details.mobile_number = number
       
        var editdetailspromise1 = submitProfileData.editprofiledetails1(reg.user_details, dsa, rera);
        editdetailspromise1.then(function (res) {
          if (res.data == "success") {
            swal("Personal Information", "Completed", "success")
            $state.go('app.editprofilebasic');
          }

        }, function (error) {
          swal("Server  Error", "Please try later");
        })
      }
    }

    reg.editprofile2 = function () {
      reg.json = angular.toJson($scope.data.names);
      var editdetailspromise2 = submitProfileData.editprofiledetails2(reg.user_details,reg.json);
      editdetailspromise2.then(function (res_profile2) {

        if (res_profile2.data == "success") {
          swal("Business Information", "Completed", "success");
          reg.editprofile3();
          $state.go("app.education");
        }
      }, function (error) {
        swal("Server Error", "Please try later");
      })
    }
    reg.save_digital_link = function () {
      get_userDetails.save_digital_link(reg.user_details.link_url)
        .then(function (res2) {
          get_userDetails.get_digital_link().then(function (results_save) {
            reg.results = results_save.data;
            reg.user_details.link_url = "";

          })
        }, function (error) {})
    }
    reg.delete_digital_link_data = function (link) {
      get_userDetails.delete_foot_print_verification(link)
        .then(function (res1) {
          get_userDetails.get_digital_link().then(function (results_delete) {
            reg.results = results_delete.data;
            reg.user_details.link_url = "";

          })
        })
    }
    reg.validate_education_year = function () {
      var isvalid = false;

      if (reg.user_details.educational_details.to_year <= reg.user_details.educational_details.from_year) {
        isvalid = false;

      } else {
        isvalid = true;
      }
      return isvalid;
    }
    reg.validate_certification_year = function (certificate_length) {
      var isvalid = false;
      for(var i=0;i<certificate_length;i++){
      if ( $scope.data1.names1[i].to_year <= $scope.data1.names1[i].from_year) {
        if ($scope.data1.names1[i].to_year == '' && $scope.data1.names1[i].from_year == '') {
          isvalid = true;
        } else {
          isvalid = false;
        }

      } else {
        isvalid = true;
      }
    }
      return isvalid;
    }

    $scope.fileNameChanged = function () {
      reg.isDisabled = false;
    }
    
    reg.capturedata = function (image, data) {
      if (image == localStorage.getItem('educational_document')) {
        swal("Please choose new image file", "", "success");
      } else {
        reg.isDisabled = true;
        $ionicLoading.show({
          content: 'Loading',
          animation: 'fade-in',
          showBackdrop: true,
          maxWidth: 200,
          showDelay: 0
        });
        var promise = submitProfileData.postdata(image, data);
        promise.then(function (res) {
          localStorage.removeItem('educational_document');
          localStorage.setItem("educational_document", res.document_url);
          if (res.result == "success") {

            $timeout(function () {
              $ionicLoading.hide();
            }, 1000);
            swal("Uploaded", "", "success");
            reg.hide = true;
          } else {
            $ionicLoading.hide();
            swal("Upload failed", "Check  internet connection and try again", "error");
          }
        }, function (error) {
          $timeout(function () {
            $ionicLoading.hide();
          }, 1000);
          swal("Server Error", "Try Again Later", "error");
        })

      }

    }

    reg.capturedata1 = function (image, data,count_value) {
      var str = image;
      var n = str.includes("/media/reia/");
    if(n){
      swal("Please choose new image file", "", "success");
    } else {
        $ionicLoading.show({
          content: 'Loading',
          animation: 'fade-in',
          showBackdrop: true,
          maxWidth: 200,
          showDelay: 0
        });
        var promise = submitProfileData.postdata(image, data);
        promise.then(function (res) {
          
          $scope.data1.names1[count_value].certificate_doc=res.document_url;
          $scope.data1.names1[count_value].certificate_doc_id=res.id;
          if (res.result == "success") {

            $timeout(function () {
              $ionicLoading.hide();
            }, 1000);
            swal("Uploaded", "", "success");
            reg.hide = true;
          } else {
            $ionicLoading.hide();
            swal("Upload failed", "Check  internet connection and try again", "error");
          }
        }, function (error) {
          $timeout(function () {
            $ionicLoading.hide();
          }, 1000);
          swal("Server Error", "Try Again Later", "error");
        })
    }
      }

  


    reg.editprofile5 = function () {
      var missed_details = 0;

      var cert_length=$scope.data1.names1.length;
      var length_data=$scope.data1.names1.length;
      cert_length=cert_length-1;
      reg.json1 = angular.toJson($scope.data1.names1);
      for(var i=0;i<length_data;i++){
        if (!$scope.data1.names1[i].certification_name) {
          missed_details = 1;
        }
        if (!$scope.data1.names1[i].certi_authority) {
          missed_details = 1;
        }
        if (!$scope.data1.names1[i].licence_number) {
          missed_details = 1;
        }
        if (!$scope.data1.names1[i].certi_url) {
          missed_details = 1;
        }
        if (!$scope.data1.names1[i].from_year) {
          missed_details = 1;
        }
        if (!$scope.data1.names1[i].to_year) {
          missed_details = 1;
        }

      }
    
      
      if ($scope.data1.names1[cert_length].certification_name || $scope.data1.names1[cert_length].certi_authority || $scope.data1.names1[cert_length].licence_number || $scope.data1.names1[cert_length].certi_url || $scope.data1.names1[cert_length].from_year || $scope.data1.names1[cert_length].to_year ) {
           
        if (!$scope.data1.names1[cert_length].certification_name) {
          missed_details = 1;
        }
        if (!$scope.data1.names1[cert_length].certi_authority) {
          missed_details = 1;
        }
        if (!$scope.data1.names1[cert_length].licence_number) {
          missed_details = 1;
        }
        if (!$scope.data1.names1[cert_length].certi_url) {
          missed_details = 1;
        }
        if (!$scope.data1.names1[cert_length].from_year) {
          missed_details = 1;
        }
        if (!$scope.data1.names1[cert_length].to_year) {
          missed_details = 1;
        }
        
        if (missed_details) {
          swal("Error", "Please fill all the details in certification");
        } else {
          var bool_vale = reg.validate_education_year();
          var certificate_vale = reg.validate_certification_year(length_data);
          if (bool_vale && certificate_vale) {
            if (reg.user_details.certification_details.is_expired) {
              reg.user_details.certification_details.is_expire = true;
            } else {
              reg.user_details.certification_details.is_expire = false;
            }
            var editdetailspromise5 = submitProfileData.editprofiledetails5(reg.user_details,reg.json1);
            editdetailspromise5.then(function (res) {
              if (res.data == "success") {
                swal("THANK YOU !", "Congratulations!", "success");
                var testCtrl2 = $controller('TrackCtrl');
                console.log(testCtrl2);
                $state.go("app.myhub");

              }
            }, function (error) {
              swal("Server Error", "Please try later");
            })
          } else {
            swal("Error", "Please enter proper year of completion");
          }

        }

      } else {
        if (missed_details && length_data>1) {
          swal("Error", "Please fill all the details in certification");
        } else {
        var bool_vale = reg.validate_education_year();
        var certificate_vale = reg.validate_certification_year(length_data);
        if (bool_vale && certificate_vale) {
          if (reg.user_details.certification_details.is_expired) {
            reg.user_details.certification_details.is_expire = true;
          } else {
            reg.user_details.certification_details.is_expire = false;
          }
          var editdetailspromise5 = submitProfileData.editprofiledetails5(reg.user_details,reg.json1);
          editdetailspromise5.then(function (res) {
            if (res.data == "success") {
              swal("THANK YOU !", "Congratulations!", "success");
              var testCtrl2 = $controller('TrackCtrl');
              console.log(testCtrl2);
              $state.go("app.myhub");

            }
          }, function (error) {
            swal("Server Error", "Please try later");
          })
        } else {
          swal("Error", "Please enter proper year of completion");
        }
      }
    }
    }

    reg.editprofile3 = function () {
      var editdetailspromise3 = submitProfileData.editprofiledetails3(reg.user_details.answer);
      editdetailspromise3.then(function (res) {
        if (res == "success") {

        }
      }, function (error) {
        swal("Server Error", "Please try later");
      })
    }

    reg.webapp_document_upload = function (type) {
      swal({
        html: true,
        title: type + ' Document upload',
        text: 'for ' + type + ' Document upload please visit <a>www.abotmi.com</a>'
      })
    }
    reg.answerclear = function () {
      reg.user_details.answer[0].Remark[0].Answer = "";
      reg.user_details.answer[0].Remark[1].Answer = "";
      reg.user_details.answer[0].Remark[2].Answer = "";
      reg.user_details.answer[0].Remark[3] = "";
    }
    reg.init();
  })


  .controller('EkycCtrl', function ($localStorage, $state, get_userDetails, $http, adharverify, $window, AADHAAR_BRIDGE_API) {
    var ekyc = this;
    ekyc.AADHAAR_BRIDGE_API = AADHAAR_BRIDGE_API;
    ekyc.init = function () {
      var promise = get_userDetails.get_regornot();
      promise.then(function (results) {

        ekyc.data = results.data;
        if (ekyc.data == 'Confirmed') {
          ekyc.confirmed = 'true';
        }

      })
      var aadhaarpromise = get_userDetails.get_aadhaar();
      aadhaarpromise.then(function (results) {

        ekyc.check = results.data;

        if (ekyc.check == 'Aadhaar') {
          ekyc.aadhaar = 'true';

        }

      })

    }
    ekyc.adharnumberverify = function () {
      var promise = adharverify.verify(ekyc.number, "self");
      promise.then(function (res) {
        if (res.data == "Aadhaar number is already exist") {
          swal("Your Passport Number Already Exist");
          ekyc.number = "";
        } else {
          ekyc.saveadhar();
        }
      })
    }
    ekyc.saveadhar = function () {
      var savepromise = adharverify.save_adhaar(ekyc.number);
      savepromise.then(function (results) {
        if (results.status == 200) {
          swal("Success", "Passport number added successfully", "success");
          $state.go('app.editprofile');
        }
      })
    }
    ekyc.init();
  })
  .controller('eKYCsuccess', function ($localStorage, $state, $http, $location, aadhar_success) {


    var uuid = $location.search().uuid;
    var reqid = $location.search().requestId;
    var type = $location.search().type ? $location.search().type : "web";

    var promise = aadhar_success.success(uuid, reqid, "self");
    promise.then(function (response) {
      if (response.data == 'signup_with_email') {
        swal("Success", "Aadhaar verification is success");
        $state.go('app.editprofile');
      } else {
        swal("Aadhaar verification success ", "login credentials are  sent to your email id");
        $state.go('app.editprofile');
      }

    });

  })
  .controller('eKYCfailure', function ($localStorage, $state, $http, $location, aadhar_failure) {
    var reqid = $location.search().requestId;
    var type = $location.search().type ? $location.search().type : "web";
    var promise = aadhar_failure.failure(reqid, "self")
    promise.then(function (response) {
      if (response.data = 'Aadhar Details Storing unsuccessful') {
        swal("Aadhar verification   Failed ", "Please try again");
        $state.go('app.eKYC');
      }
    });
  })

  .controller("FootPrintCtrl", function ($localStorage, $state, get_userDetails, MyHubDetails, $ionicSideMenuDelegate, $stateParams) {
    var foot = this;
    foot.confirmed = $stateParams.confirm;
    foot.init = function () {
      get_userDetails.get_digital_link().then(function (results) {
        foot.results = results.data;
        foot.results;
      })
      var promise = get_userDetails.get_regornot();
      promise.then(function (results) {
        foot.data = results.data;
        if (foot.data == 'Confirmed') {
          foot.confirmed = 'true'
        }
      })
    }

    foot.save_digital_link = function () {
      get_userDetails.save_digital_link(foot.link_url)
        .then(function (res) {
          $state.reload();
        }, function (error) {})
    }

    foot.delete_digital_link_data = function (link) {
      get_userDetails.delete_foot_print_verification(link)
        .then(function (res_foot) {
          $state.reload();
        })
    }

    foot.show_upload = false;
    foot.upload_show = function () {
      foot.video_title = null;
      foot.video_description = null;
      foot.video_link = null;
      foot.show_upload = true;
    }

    foot.upload_hide = function () {
      foot.show_upload = false;
    }
    foot.validate_url = true;
    foot.url_validation = function (url) {
      var p = /^(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?(?=.*v=((\w|-){11}))(?:\S+)?$/;
      return (url.match(p)) ? RegExp.$1 : false;
    }

    foot.youtube_url_validate = function (url) {
      var res_url = foot.url_validation(url);
      if (res_url != false) {
        foot.validate_url = false;
      } else {
        foot.validate_url = true;
      }
    }

    foot.advisor_video_publish = function () {
      var video_title = foot.video_title;
      var video_description = foot.video_description;
      var video_link = foot.video_link;
      var pattern2 = /(?:http?s?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.+)/g;
      video_url = video_link.replace(pattern2, "https://www.youtube.com/embed/$1");
      MyHubDetails.sendvideopublish(video_title, video_description, video_url).then(
        function (response) {
          if (response == 200) {
            swal('success', "video uploaded successfully ", 'success');
            foot.show_upload = false;
          }
        });
    };

    foot.init();

  })
