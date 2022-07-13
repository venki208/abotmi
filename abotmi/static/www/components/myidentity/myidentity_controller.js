angular.module('myidentity_controllers', [])

  .controller('MyIdentityCtrl', function ($localStorage, $state, SweetAlert,
    $timeout, $location, $stateParams, MyIdentityDetails, CRISIL_GOT_CERTIFICATE, socialShare, GUESTURL, MyidentityShareData, downloadprofile) {

    var mytrack = this;

    mytrack.CRISIL_GOT_CERTIFICATE = CRISIL_GOT_CERTIFICATE;
    mytrack.shareoptions = ["Facebook", "LinkedIn", "Twitter", "Whatsapp", "Email"];
    mytrack.host = $location.protocol() + "://" + $location.host();
    mytrack.value = false;
    mytrack.instruments_limit = 2;
    mytrack.instruments_experience_limit = 2;
    mytrack.see_more = function () {
      mytrack.instruments_limit = mytrack.financial_instruments_length;
    }
    mytrack.init = function () {
      var getDetails = MyIdentityDetails.getDetails();
      getDetails.then(function (res) {
        mytrack.details = res;
        mytrack.financial_instruments_length = mytrack.details.otherdetails.financial_instruments.length;
        mytrack.url = mytrack.host + GUESTURL + mytrack.details.profile.batch_code;
        MyidentityShareData.setdata(res);
      }, function (error) {
        swal("Try Again");
      });
    }
    mytrack.language = function () {
      $state.go("app.myidentity.edit", {
        'editstep': 1,
        'heading': 'LANGUAGES SPOKEN'
      });
    }
    mytrack.education = function () {
      $state.go("app.myidentity.edit", {
        'editstep': 2,
        'heading': 'EDUCATION'
      });
    }
    mytrack.contact = function () {
      $state.go("app.myidentity.edit", {
        'editstep': 3,
        'heading': 'CONTACT DETAILS'
      });
    }
    mytrack.promise = function () {
      $state.go("app.myidentity.edit", {
        'editstep': 4,
        'heading': 'MY PROMISE'
      });
    }
    mytrack.belief = function () {
      $state.go("app.myidentity.edit", {
        'editstep': 5,
        'heading': 'MY BELIEF'
      });
    }
    mytrack.edit_accomplishment = function () {
      $state.go("app.myidentity.edit", {
        'editstep': 6,
        'heading': 'MY SALES ACCOMPLISHMENTS'
      });
    }
    mytrack.edit_skills = function () {
      $state.go("app.myidentity.edit", {
        'editstep': 7,
        'heading': 'SKILLS'
      });
    }
    mytrack.total_adv = function () {
      $state.go("app.myidentity.edit", {
        'editstep': 8,
        'heading': 'Peer Connections'
      });
    }
    mytrack.finacial_instrument = function () {
      $state.go("app.myidentity.edit", {
        'editstep': 9,
        'data': mytrack.details.otherdetails.financial_instruments,
        'heading': 'Experience'
      });
    }
    mytrack.my_sales = function () {
      $state.go("app.myidentity.edit", {
        'editstep': 10,
        'data': mytrack.details.otherdetails,
        'heading': 'Regulatory Certification Registration'
      });
    }
    mytrack.total_clients = function () {
      $state.go("app.myidentity.edit", {
        'editstep': 11,
        'heading': 'Client Connections'
      });
    }

    mytrack.about_me = function () {
      $state.go("app.myidentity.edit", {
        'editstep': 12,
        'heading': 'Professional Statement'
      });
    }
    mytrack.certifications = function () {
      $state.go("app.myidentity.edit", {
        'editstep': 13,
        'heading': 'Certifications'
      });
    }
    mytrack.calendlylink = function () {
      swal("Link can be acessed through web module from app you cannot access", "", "success");

    }

    mytrack.socialshare = function (pageurl) {
      switch (mytrack.selectedoption) {
        case 'Facebook':
          socialShare.fb_share(pageurl, "Hi , Have look on my ABOTMI profile");
          break;
        case 'Twitter':
          socialShare.twitter_share(pageurl, "Hi , Have look on my ABOTMI profile");
          break;
        case 'LinkedIn':
          socialShare.LinkedInShare(pageurl, "Hi , Have look on my ABOTMI profile");
          break;
        case 'Whatsapp':
          socialShare.whatsapp_share(pageurl, "Hi , Have look on my ABOTMI profile");
          break;
        case 'Email':
          $state.go('app.myidentity.emailshare', {
            'shareurl': pageurl
          });
          break;
      }
      mytrack.selectedoption = "";
    };

    mytrack.sharetoggle = function () {
      mytrack.value = !mytrack.value;
    };

    mytrack.downloadprofile = function () {
      var promise = downloadprofile.pdf();
      promise.$promise.then(function (res) {
        file = res.response;
        var fileName = mytrack.details.profile.first_name + "" + mytrack.details.profile.last_name + ".pdf";
        var reader = new window.FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = function () {
          var base64data = reader.result;
          window.location.href = "downloadpdf://" + fileName + "," + base64data;
        }
      });
    };

    mytrack.init();

  })

  .controller('ProfileShareCtrl', function ($stateParams, sendEmail, MyidentityShareData, $state) {

    var share = this;
    share.url = $stateParams.shareurl;
    share.titleoptions = ["Mr", "Ms", "Dr", "Prof"];
    share.emailshare = {};
    share.init = function () {
      share.user_details = MyidentityShareData.getdata();
    }
    share.init();
    share.shareThroughEmail = function () {
      share.emailshare.template_name = "ABOTMI_16";
      share.emailshare.mail_body = 'Please click ' + '<a href=' + "'" + share.url + "'" + '>here</a>' + ' to view the profile';
      var emailShareResult = sendEmail.sendEmailShare(share.emailshare);
      emailShareResult.then(function (msg) {
        swal("success", "Profile shared Successfully", "success");
        $state.go("app.myidentity");
      }, function (error) {
        swal("Error", "Check network and try again");
      });
    }
  })

  .controller('ChangePictureCtrl', function ($scope, updateprofiledetails, $state, $stateParams, $ionicLoading, $timeout, deviceDetector) {
    var changepicture = this;
    changepicture.data = deviceDetector;
    changepicture.outputImage = null;
    changepicture.picture = $stateParams.picture;
    changepicture.filechanged = function (event) {
      changepicture.inputImage = event.target.files[0];
      var reader = new FileReader();
      reader.onload = function (e) {
        // bind new Image to Component
        $scope.$apply(function () {
          changepicture.inputImage = e.target.result;
        });
      }
      reader.readAsDataURL(changepicture.inputImage);
    }

    changepicture.uploadpic = function (picture) {
      $ionicLoading.show({
        content: 'Loading',
        animation: 'fade-in',
        showBackdrop: true,
        maxWidth: 200,
        showDelay: 0
      });
      var promise = updateprofiledetails.postPicture(picture);
      promise.then(function (res) {
        swal("Updated Successfully", "", "success");
        $state.go('app.myidentity');
      }, function (error) {
        $timeout(function () {
          $ionicLoading.hide();
        }, 1000);
        swal("Try again", "", "error");
      });
    };
  })

  .controller('EditCtrl', function ($localStorage, $state, $timeout, $location, $stateParams,
    SweetAlert, MyidentityShareData, MyIdentityDetails, $stateParams, updateprofiledetails, deviceDetector, $ionicLoading, $scope) {
    var edit = this;
    var iti;
    var global_number;
    edit.isDisabled = false;
    edit.boolen_filed = false;
    edit.devicedetection = deviceDetector;
    edit.product_options = [
      "Equity", "Wealth Advisory", "Mutual Fund", "Insurance",
      "Real Estate", "Portfolio Management"
    ];
    edit.additional_qualification_list = [];
    edit.olddata = $stateParams.data;

    edit.heading = $stateParams.heading;
    edit.current_year = new Date().getFullYear();
    edit.years = [];
    for (var i = 1940; i <= edit.current_year; i++) {
      edit.years.push(i);
    }
    edit.init = function () {
      var getDetails = MyIdentityDetails.getDetails();
      getDetails.then(function (res) {
        edit.details = res;
        if(edit.details.otherdetails.educational_details.activities == "undefined"){
           
          edit.details.otherdetails.educational_details.activities=""
        }
        if(edit.details.otherdetails.educational_details.field_of_study == "undefined"){
         
          edit.details.otherdetails.educational_details.field_of_study=""
        }
        $scope.data1 = {
          names1: [{}]
        };
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
        var education_documents = localStorage.getItem('educational_document');
        if (education_documents) {
          edit.details.otherdetails.eipv_face_capture = education_documents;
        }
        if (edit.details.otherdetails.certification_details) {
          $scope.data1.names1 = edit.details.otherdetails.certification_details
          
        }

      }, function (error) {
        swal("Try Again");
      });
      var date = new Date();
      let dateArray = [];
      edit.fromyear = [];
      names = []
      curYear = date.getFullYear();
      for (var j = 0; j < 65; j++) {
        dateArray[j] = (curYear - 65) + j;
        edit.fromyear.push(dateArray[j]);
      }
      edit.step = $stateParams.editstep;
      edit.user_details = MyidentityShareData.getdata();

      if (edit.olddata) {
        for (var i = 0; i < edit.olddata.length; i++) {
          edit.olddata[i]['is_disable'] = true;
        }
      }
      edit.modified = false;
      
    }
    edit.init();
    edit.enableDetails = function () {

      var input = document.querySelector("#phone");


      iti = intlTelInput(input, {
        nationalMode: false,
        //initialCountry: "us",
        separateDialCode: true,
        autoPlaceholder: "off",

        utilsScript: "intl-tel-input/build/js/utils.js"
      });
      iti.setNumber(edit.user_details.profile.mobile);

    }

    edit.additional_qualification_list = []
    edit.webapp_document_upload = function () {
      swal({
        title: "Highest Qualification",
        text: "for Highest Qualification upload please visit www.abotmi.com"
      });
    }
    edit.selectPayDate = function (val) {
      crisil.paydetails.paydate = {
        callback: function (val) {
          crisil.paydetails.dateofpay = moment(new Date(val)).format('YYYY-MM-DD');
        }
      };
      crisil.selectDate(crisil.paydetails.paydate);
    };
    edit.capturedata1 = function (image, data,count_value) {
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
        var promise = MyIdentityDetails.postdata(image, data);
        promise.then(function (res) {
          
          $scope.data1.names1[count_value].certificate_doc=res.document_url;
          $scope.data1.names1[count_value].certificate_doc_id=res.id;
          if (res.result == "success") {

            $timeout(function () {
              $ionicLoading.hide();
            }, 1000);
            swal("Uploaded", "", "success");
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


    edit.skills = [
      'Management', 'Customer Service', 'Project Management',
      'Business Development', 'Research', 'Lead Generation',
      'Customer Research Management', 'Email Marketing', 'Others'
    ];

    edit.selectedSkils = {};

    edit.addRowRera = function (alldata) {
      edit.modified = true;
      var flag = true;
      for (var i = 0; i < alldata.length; i++) {
        if (alldata[i].rera_state == null || alldata[i].rera_expire_date == null || alldata[i].rera_registration_no == null) {
          flag = false;
        }
      }
      if (flag) {
        alldata.push({});
      }
    }

    edit.addRowDsa = function (alldata) {
      edit.modified = true;
      var flag = true;
      for (var i = 0; i < alldata.length; i++) {
        if (alldata[i].dsa_bank_name == null || alldata[i].dsa_code == null || alldata[i].dsa_how_long_associated == null) {
          flag = false;
        }
      }
      if (flag) {
        alldata.push({});
      }
    }
    edit.perData = {};
    edit.addRow = function (alldata) {
      edit.modified = true;
      edit.perData = alldata;

      var flag = false;
      for (var i = 0; i < alldata.length; i++) {
        if (alldata[i].instruments == null || alldata[i].instruments == "select" || alldata[i].experience == null || alldata[i].experience == "") {
          flag = true;
        }
      }
      if (flag == false) {
        alldata.push({
          "is_disable": false
        });
      }
    }

    edit.selectInstrument = function (instruments) {
      for (var i = 0; i < edit.perData.length - 1; i++) {
        if (edit.perData[i].instruments == instruments) {
          var j = edit.perData.length - 1;
          var instruments1 = edit.perData[j]['instruments'] = "";
          if (!instruments1) {
            document.getElementById("finances" + j + '').value = "";
            swal("select other field experience", "", "error")
          }
          break;
        }
      }
    }

    edit.deleteRow = function (alldata, item) {
      edit.modified = true;
      var index = alldata.indexOf(item);
      alldata.splice(index, 1);
    }

    edit.addAdditionalQualification = function (additional_qualification_data) {
      var flag = true;
      for (var i = 0; i < additional_qualification_data.length; i++) {
        if (additional_qualification_data[i].additional_qualification == null || additional_qualification_data[i].year_passout == null || additional_qualification_data[i].university == null) {
          flag = false;
        }
      }
      if (flag) {
        var new_qualification = {
          "additional_qualification": "",
          "university": "",
          "year_passout": "",
          "document_verified": "not_verified",
          "documents_upload": ""
        }
        additional_qualification_data.push(new_qualification);
      }
    }

    edit.deleteAdditionalQualification = function (additional_qualification_data, item) {
      var index = additional_qualification_data.indexOf(item);
      additional_qualification_data.splice(index, 1);
    }

    $scope.fileNameChanged = function () {
      edit.isDisabled = false;
    }

    edit.capturedata = function (image, data) {
      if (image == localStorage.getItem('educational_document')) {
        swal("Please choose new image file", "", "success");
      } else {
        edit.isDisabled = true;
        $ionicLoading.show({
          content: 'Loading',
          animation: 'fade-in',
          showBackdrop: true,
          maxWidth: 200,
          showDelay: 0
        });
        var promise = MyIdentityDetails.postdata(image, data);
        promise.then(function (res) {
          localStorage.removeItem('educational_document');
          localStorage.setItem("educational_document", res.document_url);
          if (res.result == "success") {

            $timeout(function () {
              $ionicLoading.hide();
            }, 1000);
            swal("Uploaded", "", "success");
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

    edit.certification_data = function () {
      var missed_details = 0;
      var cert_length=$scope.data1.names1.length;
      var length_data=$scope.data1.names1.length;
      cert_length=cert_length-1;
      edit.json1 = angular.toJson($scope.data1.names1);
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
          var certificate_vale = edit.validate_certification_year(length_data);
          if ( certificate_vale) {

          if (edit.details.otherdetails.certification_details.is_expired) {
            edit.details.otherdetails.certification_details[0].is_expire = true;
          } else {
            edit.details.otherdetails.certification_details[0].is_expire = false;
          }
          var promise = MyIdentityDetails.saveCertificationalDetails(edit.details.otherdetails,edit.json1);
          promise.then(function (res) {
            swal("Certificational Details Updated successfully", "", "success");
            $state.go('app.myidentity');
          }, function (error) {
            swal("Try again");
          });
        } else {
          swal("Error", "Please enter proper year of completion");
        }
        }

      } else {
        if (missed_details && length_data>1) {
          swal("Error", "Please fill all the details in certification");
        } else{
        var certificate_vale = edit.validate_certification_year(length_data);
        if (certificate_vale) {
        if (edit.details.otherdetails.certification_details.is_expired) {
          edit.details.otherdetails.certification_details[0].is_expire = true;
        } else {
          edit.details.otherdetails.certification_details[0].is_expire = false;
        }
        var promise = MyIdentityDetails.saveCertificationalDetails(edit.details.otherdetails,edit.json1);
        promise.then(function (res) {
          swal("Certificational Details Updated successfully", "", "success");
          $state.go('app.myidentity');
        }, function (error) {
          swal("Try again");
        });
      } else {
        swal("Error", "Please enter proper year of completion");
      }
      }
    }
    }
    edit.validate_education_year = function () {
      var isvalid = false;
      if (edit.details.otherdetails.educational_details.to_year <= edit.details.otherdetails.educational_details.from_year) {
        isvalid = false;
      } else {
        isvalid = true;
      }
      return isvalid;
    }
    edit.validate_certification_year = function (certificate_length) {
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
    edit.educational_details_form = function () {
      var bool_vale = edit.validate_education_year();
      if (bool_vale) {
        var promise = MyIdentityDetails.saveEducationalDetails(edit.details.otherdetails);
        promise.then(function (res) {
          swal("Educational Details Updated successfully", "", "success");
          $state.go('app.myidentity');
        }, function (error) {
          swal("Try again");
        });
      } else {
        swal("Error", "Please enter proper year of completion");
      }
    }

    edit.submitAdditionalQualification = function (AdditionalQualificationdata) {
      AdditionalQualificationdata = angular.toJson(AdditionalQualificationdata);
      var qualification = edit.user_details.profile.qualification;
      var year_passout = edit.user_details.profile.year_passout;
      var college_name = edit.user_details.profile.college_name;
      var data = {
        'qualification': qualification,
        'year_passout': year_passout,
        'college_name': college_name
      }
      var promise = MyIdentityDetails.update_additional_qualification(AdditionalQualificationdata, data);
      promise.then(function (res) {
        swal("Educational Qualifications Updated successfully", "", "success");
        $state.go('app.myidentity');
      }, function (error) {
        swal("Try again");
      });
    }

    edit.submitlanguage = function () {
      var languages_known_speak = edit.user_details.profile.language_known;
      var languages_known_read_write = edit.user_details.profile.languages_known_read_write;
      var data = {
        'languages_known_speak': languages_known_speak,
        'languages_known_read_write': languages_known_read_write
      }
      MyIdentityDetails.saveLanguage(data).then(
        function (response) {
          if (response) {
            $state.go("app.myidentity")
          }
        });
    }

    edit.submitmypromise = function () {
      var my_promise = edit.user_details.otherdetails.my_promise;
      var data = {
        'my_promise': my_promise
      }
      MyIdentityDetails.saveMyPromise(data).then(
        function (response) {
          if (response) {
            $state.go("app.myidentity")
          }
        },
        function (error) {
          swal("unable to process the request try again later");
        });
    }

    edit.submitmybelief = function () {
      var my_belief = edit.user_details.profile.my_belief;
      var data = {
        'my_belief': my_belief
      }
      MyIdentityDetails.saveMyBelief(data).then(
        function (response) {
          if (response) {
            $state.go("app.myidentity");
          }
        },
        function (error) {
          swal("unable to process the request try again later");
        });
    }

    edit.submitcontact = function () {

      var isValid = iti.isValidNumber();

      if (!isValid) {
        swal("please select valid number", "", "error")
      } else {
        var number1 = iti.getNumber();
        var mobile = number1


        var address = edit.user_details.profile.address;
        var city = edit.user_details.profile.city;
        var calendly = edit.user_details.otherdetails.calendly_link;
        var data = {
          'mobile': mobile,
          'address': address,
          'city': city,
          'calendly': calendly
        }
        MyIdentityDetails.saveContectDetails(data).then(
          function (response) {
            if (response) {
              $state.go("app.myidentity");
            }
          },
          function (error) {
            swal("unable to process the request try again later");
          });
      }
    }

    edit.saveSkills = function (data) {

      var data_arr = new Array();
      var data_arr = edit.user_details.otherdetails.skills;
      MyIdentityDetails.saveSkills(data_arr).then(
        function (response) {
          if (response) {
            $state.go("app.myidentity");
          }
        });
    }

    edit.sebi_details = function (value) {
      if (value) {
        edit.sebi_regi = false;
        edit.sebi_validity = false;
        edit.sebi_valid_from = false;
      } else {
        edit.sebi_regi = true;
        edit.sebi_validity = true;
        edit.sebi_valid_from = true;
        edit.sebi_regi_value = "";
        edit.sebi_validity_value = "";
        edit.sebi_valid_from_value = "";
      }
    }
    edit.amfi_details = function (value) {
      if (value) {
        edit.amfi_regi = false;
        edit.amfi_validity = false;
        edit.amfi_valid_from = false;
      } else {
        edit.amfi_regi = true;
        edit.amfi_validity = true;
        edit.amfi_valid_from = true;
        edit.amfi_regi_value = "";
        edit.amfi_validity_value = "";
        edit.amfi_valid_from_value = "";
      }
    }
    edit.irda_details = function (value) {
      if (value) {
        edit.irda_regi = false;
        edit.irda_validity = false;
        edit.irda_valid_from = false;
      } else {
        edit.irda_regi = true;
        edit.irda_validity = true;
        edit.irda_valid_from = true;
        edit.irda_regi_value = "";
        edit.irda_validity_value = "";
        edit.irda_valid_from_value = "";
      }
    }
    edit.other_details = function (value) {
      edit.modified = true;
      if (value) {
        edit.other_authotity = false;
        edit.other_regi = false;
        edit.other_validity = false;
      } else {
        edit.other_authotity = true;
        edit.other_regi = true;
        edit.other_validity = true;
        edit.other_authotity_value = "";
        edit.other_regi_value = "";
        edit.other_validity_value = "";
      }
    }

    edit.rera_details = function (value) {
      edit.modified = true;
      if (value) {
        edit.rera_regi = false;
        edit.rera_state = false;
        edit.rera_validity = false;
        edit.rera_add = false;
      } else {
        edit.rera_regi = true;
        edit.rera_state = true;
        edit.rera_validity = true;
        edit.rera_add = true;
        edit.olddata.rera_values = [{
          "rera_state": "",
          "rera_expire_date": "",
          "rera_registration_no": ""
        }];
      }
    }

    edit.dsa_details = function (value) {
      edit.modified = true;
      if (value) {
        edit.dsa_bank = false;
        edit.dsa_code = false;
        edit.dsa_how_long_associated = false;
        edit.dsa_add = false;
      } else {
        edit.dsa_bank = true;
        edit.dsa_code = true;
        edit.dsa_how_long_associated = true;
        edit.dsa_add = true;
        edit.olddata.dsa_result = [{
          "dsa_bank_name": "",
          "dsa_code": "",
          "dsa_how_long_associated": ""
        }];
      }
    }

    edit.submitAdvisory = function (profiledata) {
      profiledata = angular.toJson(profiledata);
      if (profiledata.search("select") == -1) {
        edit.select_instrument = false;
        var data = profiledata.split("},{");
        var validation_flag = false;
        for (var i = 0; i < data.length; i++) {
          if (!data[i].match("instruments") || !data[i].match("experience")) {
            validation_flag = true;
          }
        }
        var promise = MyIdentityDetails.updateadvisoryspec(profiledata);
        promise.then(function (res) {
          if (res) {
            $state.go('app.myidentity');
          }
        }, function (error) {
          swal("Try again");
        });
      } else {
        edit.select_instrument = true;
      }
    }

    edit.toggleSelection = function toggleSelection(item) {
      var idx = edit.user_details.otherdetails.skills.indexOf(item);

      if (idx > -1) {
        edit.user_details.otherdetails.skills.splice(idx, 1);
      } else {
        if (edit.user_details.otherdetails.skills == "") {
          edit.user_details.otherdetails.skills = [];
        }
        edit.user_details.otherdetails.skills.push(item);

      }
    }

    edit.submitaccomplishment = function (data) {
      var promise = MyIdentityDetails.updatesales(data);
      promise.then(function (res) {
        if (res) {
          $state.go('app.myidentity');
        }
      }, function (error) {
        swal("Try again");
      });
    }

    edit.saveregulatorycertification = function (profiledata) {
      var parameter = {
        sebi_regi: edit.sebi_regi_value,
        sebi_validity: edit.sebi_validity_value,
        sebi_valid_from: edit.sebi_valid_from_value,
        amfi_regi: edit.amfi_regi_value,
        amfi_validity: edit.amfi_validity_value,
        amfi_valid_from: edit.amfi_valid_from_value,
        irda_regi: edit.irda_regi_value,
        irda_validity: edit.irda_validity_value,
        irda_valid_from: edit.irda_valid_from_value,
        rera_values: edit.olddata.rera_values,
        dsa_result: edit.olddata.dsa_result,
        other_authotity: edit.other_authotity_value,
        other_regi: edit.other_regi_value,
        other_validity: edit.other_validity_value
      };

      if (profiledata) {
        var promise = MyIdentityDetails.saveregulatorycertification(parameter);
        promise.then(function (res) {
          if (res) {
            $state.go('app.myidentity');
          }
        }, function (error) {
          swal("Try again");
        });
      } else {
        swal("Please fill the form completely", "", "error");
      }
    }

    edit.submitclient = function (data) {
      var data_arr = edit.user_details.otherdetails.total_clients_served;
      MyIdentityDetails.saveclients(data_arr).then(
        function (response) {
          if (response) {
            $state.go("app.myidentity");
          }
        });
    }

    edit.submitadvisor = function (data) {
      var data_arr = edit.user_details.otherdetails.total_advisors_connected;
      MyIdentityDetails.saveadvisor(data_arr).then(
        function (response) {
          if (response) {
            $state.go("app.myidentity");
          }
        });
    }

    edit.submitaboutme = function () {
      var description = edit.user_details.profile.self_description;
      MyIdentityDetails.saveaboutme(description).then(
        function (response) {
          if (response) {
            $state.go("app.myidentity");
          }
        });
    }

  });
