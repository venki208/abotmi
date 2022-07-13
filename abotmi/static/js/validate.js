// Student Form Validation
$(document).ready(function(){

function emailvalidate(){
  $.validator.addMethod("email_format",function(value){
  return /^[\w\-\.\+]+\@[a-zA-Z0-9\.\-]+\.[a-zA-z0-9]{2,4}$/.test(value);
},"Please Enter Valid email id ");
}

// Adding New Rule : New Password and Confirm Password Should Be Same
$.validator.addMethod("isPassword_Same", function(value, element) {
  return $('#password').val() == $('#confirmpassword').val();
}, "*New Password and Confirm Password Should Be Same ");

// Adding New Rule : New Password and Confirm Password Should Be Same
$.validator.addMethod("isPasswordSame", function(value, element) {
  return $('#password_reset').val() == $('#password_reset_confirm').val()
}, "*New Password and Confirm Password Should Be Same ");

// Adding New Rule : New Password and Confirm Password Should Be Same
$.validator.addMethod("isSetPasswordSame", function(value, element) {
  return $('#password_set').val() == $('#password_set_confirm').val()
}, "*Password and Confirm Password Should Be Same ");

// Adding New Rule: New Password and Old Password should not match input: by id
jQuery.validator.addMethod("isPasswordNotSame", function(value, element, param) {
  return this.optional(element) || value != $(param).val();
}, "New password should not be same as old");

$.validator.addMethod("date", function(value, element) {
  // put your own logic here, this is just a (crappy) example
  return value.match(/^([0-9]{2})-([0-9]{2})-([0-9]{4})$/);
},"Please enter a date in the format dd/mm/yyyy.");

// Adding Email Validation Rule
$.validator.addMethod("email_format",function(value){
  return /^[\w\-\.\+]+\@[a-zA-Z0-9\.\-]+\.[a-zA-z0-9]{2,4}$/.test(value);
},"Please Enter Valid email id ");

// Adding Password Check(allow only small letters with numeric)
$.validator.addMethod("pwcheck", function(value) {
  return /^[A-Za-z0-9\d=!\-@._*]*$/.test(value) // consists of only these
      && /[a-z]/.test(value) // has a lowercase letter
      && /\d/.test(value) // has a digit
},'please enter minimum 8 alpha numerals');

// Adding for check password with anyalphabets with numeric
$.validator.addMethod("check_password", function(value) {
  return /^[A-Za-z0-9\d=!\-@._*]*$/.test(value) // consists of only these
      && /\d/.test(value) // has a digit
},'please enter minimum 8 alpha numerals');

// Adding isText  Rule
$.validator.addMethod("isText",function(value){
  return /^[a-zA-Z ]*$/.test(value);
},"Please enter only Alphabet !");

// it will allow both http & https & www
$.validator.addMethod("isValideUrl",function(value,element){
  return this.optional( element ) || /^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/|www\.)[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/.test(value);
},"Please enter valid URL");

// pattern to check for password
$.validator.addMethod("patternCheck",function(value){
  return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$/.test(value);
},"Please enter valid password");

$("#signup_form").validate({
      rules: {
      investment_advisor: {
        required: true
      },
      first_name: {
        required: true,
        isText: true,
        minlength: 2
      },
      last_name: {
        required: true,
        isText: true
      },
      username: {
        required: true,
        email: true,
        email_format: true,
      },
      mobile: {
        minlength: 10,
        maxlength: 10,
        required: true,
        digits: true
      },
      terms:{
        required:true
      },
      gender:{
        required:true
      },
       birthdate: {
        required:true,
        date: true
      },
      sebi1:{
        required:true,
        alphanumeric: true,
        rangelength: [1, 15]
      },
      sebi_date:{
        required:true,
      },
      sebi_registration_date:{
        required:true,
      },
      amfi1:{
        required:true,
        alphanumeric: true,
        rangelength: [1, 15]
      },
      amfi_date:{
        required:true,
      },
      amfi_registration_date:{
        required:true,
      },
      irda1:{
        required:true,
        alphanumeric: true,
        rangelength: [1, 15]
      },
      irda_date:{
        required:true,
      },
      irda_registration_date:{
        required:true,
      },
      register_no1:{
        required:true,
        alphanumeric: true,
        rangelength: [1, 15]
      },
      organization1:{
        required:true
      },
      years:{
        max:100,
        min:0
      }
    },

    messages: {
      investment_advisor: {
        required: "Please select one option"
      },
      first_name: {
        required: "Please enter first name",
        minlength: "At least it should 2 letters "
      },
      last_name: {
        required: "Please enter last name "
      },
      username: {
        required: "Please enter Email ID",
        email: "Please enter valid Email ID",
        remote: "Email ID already exist"
      },
      mobile: {
        required: "Please enter valid mobile number",
        minlength: "Please enter 10 digits mobile number",
        maxlength: "Please enter 10 digits mobile number "
      },
      terms:{
        required: "Please Aceept Terms and Conditions"
      },
      gender:{
        required: "Please select gender"
      },
      birthdate: {
        required: "Please select valid date",
        date: "Date should be dd/mm/yyyy format"
      },
      sebi1:{
        required: "This field is required",
        alphanumeric: "Sebi number should be alpha numeric",
        rangelength:"Please Enter a valid Registration Number"
      },
      sebi_date:{
        required: "This field is required",
      },
      sebi_registration_date:{
        required: "This field is required",
      },
      amfi1:{
        required: "This field is required",
        alphanumeric: "Amfi number should be alpha numeric",
        rangelength:"Please Enter a valid Registration Number"
      },
      amfi_date:{
        required: "This field is required",
      },
      amfi_registration_date:{
        required: "This field is required",
      },
      irda1:{
        required: "This field is required",
        alphanumeric: "Irda number should be alpha numeric",
        rangelength:"Please Enter a valid Registration Number"
      },
      irda_date:{
        required: "This field is required",
      },
      irda_registration_date:{
        required: "This field is required",
      },
      register_no1:{
        required: "This field is required",
        alphanumeric: "Registration number should be alpha numeric",
        rangelength:"Please Enter a valid Registration Number"
      },
      organization1:{
        required: "This field is required"
      },
      years:{
        max:'practice of years cannot be more than 100 and less than 0',
        min:'practice of years cannot be more than 100 and less than 0'
      }
    },
    highlight: function(element) {
    $(element).closest('.control-group').removeClass('success').addClass('error');
    },
    unhighlight: function(element) {
    $(element).closest('.control-group').removeClass('error').addClass('success');
    },
    success: function(element) {
    //$(element).closest('.control-group').find('.fillimg').addClass('valid');
    // What is ".fillimg"?  That's not a real word.
    },
    errorPlacement: function (error, element) {
    $(element).closest('.control-group').find('.help-block').html(error.text());
    }
});

// Student Registration Form
$("#tags").validate({
    rules: {
      tag_name: {
        required: true,
        isText: true,
        minlength: 2
      }
    },

    messages: {
      tag_name: {
        required: "Please enter tag name !",
        minlength: "At least it should 2 letters !"
      }
    },

    highlight: function(element) {
    $(element).closest('.control-group').removeClass('success').addClass('error');
    },
    unhighlight: function(element) {
    $(element).closest('.control-group').removeClass('error').addClass('success');
    },
    success: function(element) {
    //$(element).closest('.control-group').find('.fillimg').addClass('valid');
    // What is ".fillimg"?  That's not a real word.
    },
    errorPlacement: function (error, element) {
    $(element).closest('.control-group').find('.help-block').html(error.text());
    }
});

// Student Registration Form
$("#reset_password").validate({
    rules: {
      resend_email: {
        required: true,
        email: true,
        email_format: true,
        remote: {
          url: "/signup/reset_email/",
          type: "POST",
          data: {
            username: function() {
                return $( "#resend_email" ).val();
            }
          }
        }
      }
    },

    messages: {
      resend_email: {
        required: "Please enter Email ID",
        email: "Please enter valid Email ID",
        remote: "Your email ID does not exist"
      }
    },

    highlight: function(element) {
    $(element).closest('.control-group').removeClass('success').addClass('error');
    },
    unhighlight: function(element) {
    $(element).closest('.control-group').removeClass('error').addClass('success');
    },
    success: function(element) {
    //$(element).closest('.control-group').find('.fillimg').addClass('valid');
    // What is ".fillimg"?  That's not a real word.
    },
    errorPlacement: function (error, element) {
    $(element).closest('.control-group').find('.help-block').html(error.text());
    }
});

$("#login_form").validate({
    rules: {
      username: {
        required: true
      },
      password:{
        required: true
      }
    },
    messages: {
      username:{
          required:"Please enter User Email ID"
      },
      password: {
        required: "Please enter password"
      }
    },

    highlight: function(element) {
    $(element).closest('.control-group').removeClass('success').addClass('error');
    },
    unhighlight: function(element) {
    $(element).closest('.control-group').removeClass('error').addClass('success');
    },
    success: function(element) {
    //$(element).closest('.control-group').find('.fillimg').addClass('valid');
    // What is ".fillimg"?  That's not a real word.
    },
    errorPlacement: function (error, element) {
    $(element).closest('.control-group').find('.help-block').html(error.text());
    }
});

// Validation For forgot password form
$("#forgot_pwd_form").validate({
    rules: {
      resend_email: {
        required: true
      }
    },
    messages: {
      resend_email:{
          required:"Please enter Email ID"
      }
    },

    highlight: function(element) {
    $(element).closest('.control-group').removeClass('success').addClass('error');
    },
    unhighlight: function(element) {
    $(element).closest('.control-group').removeClass('error').addClass('success');
    },
    success: function(element) {
    //$(element).closest('.control-group').find('.fillimg').addClass('valid');
    // What is ".fillimg"?  That's not a real word.
    },
    errorPlacement: function (error, element) {
    $(element).closest('.control-group').find('.help-block').html(error.text());
    }
});


$("#profile_picture_upload_form").validate({
    rules: {
      picture: {
        required: true,
        remote: {
          url: "/signup/user_profile_info/",
          type: "POST",
          data: {
            username: function() {
                return $( "#picture" ).val();
            }
          }
        }
        }
      },

    messages: {
      resend_email: {
        required: "Please choose file",
      }
    },

    highlight: function(element) {
    $(element).closest('.control-group').removeClass('success').addClass('error');
    },
    unhighlight: function(element) {
    $(element).closest('.control-group').removeClass('error').addClass('success');
    },
    success: function(element) {
    //$(element).closest('.control-group').find('.fillimg').addClass('valid');
    // What is ".fillimg"?  That's not a real word.
    },
    errorPlacement: function (error, element) {
    $(element).closest('.control-group').find('.help-block').html(error.text());
    }
});


$("#reset_password_form").validate({
    rules: {
      password_reset: {
        required: true,
        minlength: 8,
        maxlength: 20,
        patternCheck : true
      },
      password_reset_confirm: {
        required: true,
        isPasswordSame: true,
        minlength: 8,
        maxlength: 20,
        patternCheck : true
      }
    },

    messages: {
      password_reset: {
        required: "Please enter new password !",
        minlength: " please enter minimum 8 alpha numerals !",
        maxlength: "Your password should not be more than 20 Characters !",
        // patternCheck : "Password should contain atleast one uppercase, one lower case character, one digit and one special character"
      },
      password_reset_confirm: {
        required: "Please enter confirm password !",
        minlength: " please enter minimum 8 alpha numerals !",
        maxlength: "Your password should not be more than 20 Characters !",
        isPasswordSame: "Your new password and confirm password should be same !"
      }
    },

    highlight: function(element) {
    $(element).closest('.control-group').removeClass('success').addClass('error');
    },
    unhighlight: function(element) {
    $(element).closest('.control-group').removeClass('error').addClass('success');
    },
    success: function(element) {
    //$(element).closest('.control-group').find('.fillimg').addClass('valid');
    // What is ".fillimg"?  That's not a real word.
    },
    errorPlacement: function (error, element) {
    $(element).closest('.control-group').find('.help-block').html(error.text());
    }
});

$("#set_password_form").validate({
    rules: {
      password_set: {
        required: true,
        minlength: 8,
        maxlength: 20,
        patternCheck : true
      },
      password_set_confirm: {
        required: true,
        isSetPasswordSame: true,
        minlength: 8,
        maxlength: 20,
        patternCheck : true
      }
    },

    messages: {
      password_set: {
        required: "Please enter new password !",
        minlength: " please enter minimum 8 alpha numerals !",
        maxlength: "Your password should not be more than 20 Characters !",
        patternCheck : "Password should contain atleast one uppercase, one lower case character, one digit and one special character"
      },
      password_set_confirm: {
        required: "Please enter confirm password !",
        minlength: " please enter minimum 8 alpha numerals !",
        maxlength: "Your password should not be more than 20 Characters !",
        isSetPasswordSame: "Your new password and confirm password should be same !"
      }
    },

    highlight: function(element) {
    $(element).closest('.control-group').removeClass('success').addClass('error');
    },
    unhighlight: function(element) {
    $(element).closest('.control-group').removeClass('error').addClass('success');
    },
    success: function(element) {
    //$(element).closest('.control-group').find('.fillimg').addClass('valid');
    // What is ".fillimg"?  That's not a real word.
    },
    errorPlacement: function (error, element) {
    $(element).closest('.control-group').find('.help-block').html(error.text());
    }
});

$("#advisor_registration2").validate({
    rules: {
      question1: {
        required: true
      },
      question2: {
        required: true,
        minlength: 8,
        maxlength: 20
      },
      question3: {
        required: true,
        minlength: 8,
        maxlength: 20
      },
      question4: {
        required: true,
        minlength: 8,
        maxlength: 20
      },
      question5: {
        required: true,
        minlength: 8,
        maxlength: 20
      },
      question6: {
        required: true,
        minlength: 8,
        maxlength: 20
      },
      question7: {
        required: true,
        minlength: 8,
        maxlength: 20
      },
      question8: {
        required: true,
        minlength: 8,
        maxlength: 20
      },
      question9: {
        required: true,
        minlength: 8,
        maxlength: 20
      },
      question10: {
        required: true,
        minlength: 8,
        maxlength: 20
      },
      question11: {
        required: true,
        minlength: 8,
        maxlength: 20
      },
      question12: {
        required: true,
        minlength: 8,
        maxlength: 20
      },
      question13: {
        required: true,
        minlength: 8,
        maxlength: 20
      },
      question14: {
        required: true,
        minlength: 8,
        maxlength: 20
      },
      question15: {
        required: true,
        minlength: 8,
        maxlength: 20
      }
    },

    messages: {
      question1: {
        required: "Please select option !"
      },
      question2: {
        required: "Please enter your answer !",
        minlength: " Your password should be minimum 8 Characters !",
        maxlength: "Your password should not be more than 20 Characters !"
      },
      question3: {
        required: "Please enter your answer !",
        minlength: " Your password should be minimum 8 Characters !",
        maxlength: "Your password should not be more than 20 Characters !"
      },
      question4: {
        required: "Please enter your answer !",
        minlength: " Your password should be minimum 8 Characters !",
        maxlength: "Your password should not be more than 20 Characters !"
      },
      question5: {
        required: "Please enter your answer !",
        minlength: " Your password should be minimum 8 Characters !",
        maxlength: "Your password should not be more than 20 Characters !"
      },
      question6: {
        required: "Please enter your answer !",
        minlength: " Your password should be minimum 8 Characters !",
        maxlength: "Your password should not be more than 20 Characters !"
      },
      question7: {
        required: "Please enter your answer !",
        minlength: " Your password should be minimum 8 Characters !",
        maxlength: "Your password should not be more than 20 Characters !"
      },
      question8: {
        required: "Please enter your answer !",
        minlength: " Your password should be minimum 8 Characters !",
        maxlength: "Your password should not be more than 20 Characters !"
      },
      question9: {
        required: "Please enter your answer !",
        minlength: " Your password should be minimum 8 Characters !",
        maxlength: "Your password should not be more than 20 Characters !"
      },
      question10: {
        required: "Please enter your answer !",
        minlength: " Your password should be minimum 8 Characters !",
        maxlength: "Your password should not be more than 20 Characters !"
      },
      question11: {
        required: "Please enter your answer !",
        minlength: " Your password should be minimum 8 Characters !",
        maxlength: "Your password should not be more than 20 Characters !"
      },
      question12: {
        required: "Please enter your answer !",
        minlength: " Your password should be minimum 8 Characters !",
        maxlength: "Your password should not be more than 20 Characters !"
      },
      question13: {
        required: "Please enter your answer !",
        minlength: " Your password should be minimum 8 Characters !",
        maxlength: "Your password should not be more than 20 Characters !"
      },
      question14: {
        required: "Please enter your answer !",
        minlength: " Your password should be minimum 8 Characters !",
        maxlength: "Your password should not be more than 20 Characters !"
      },
      question15: {
        required: "Please enter your answer !",
        minlength: " Your password should be minimum 8 Characters !",
        maxlength: "Your password should not be more than 20 Characters !"
      }
    },

    highlight: function(element) {
    $(element).closest('.control-group').removeClass('success').addClass('error');
    },
    unhighlight: function(element) {
    $(element).closest('.control-group').removeClass('error').addClass('success');
    },
    success: function(element) {
    //$(element).closest('.control-group').find('.fillimg').addClass('valid');
    // What is ".fillimg"?  That's not a real word.
    },
    errorPlacement: function (error, element) {
    $(element).closest('.control-group').find('.help-block').html(error.text());
    }
});

$("#advisor_registration3").validate({
    rules: {
      certificate_upload: {
        required: true
      },
      address_upload: {
        required: true
      },
      registration_upload: {
        required: true
      },
      reference_upload: {
        required: true
      },
      qualification_upload: {
        required: true
      },
      appriciation_upload: {
        required: true
      },
      office_pic_upload: {
        required: true
      }
    },

    messages: {
      certificate_upload: {
        required: "Please choose file"
      },
      address_upload: {
        required: "Please choose file"
      },
      registration_upload: {
        required: "Please choose file"
      },
      reference_upload: {
        required: "Please choose file"
      },
      qualification_upload: {
        required: "Please choose file"
      },
      appriciation_upload: {
        required: "Please choose file"
      },
      office_pic_upload: {
        required: "Please choose file"
      }
    },

    highlight: function(element) {
    $(element).closest('.control-group').removeClass('success').addClass('error');
    },
    unhighlight: function(element) {
    $(element).closest('.control-group').removeClass('error').addClass('success');
    },
    success: function(element) {
    //$(element).closest('.control-group').find('.fillimg').addClass('valid');
    // What is ".fillimg"?  That's not a real word.
    },
    errorPlacement: function (error, element) {
    $(element).closest('.control-group').find('.help-block').html(error.text());
    }
});

// forget password validation
var token = $("#id_csrf_token").val();
$("#changepassword_form").validate({
    rules: {
      oldpassword: {
        required: true,
          minlength:8,
          maxlength: 20,
          remote: {
          url: "/signup/user_checkpassword/",
          type: "POST",
          beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken",token);
            },
          data: {
            username: function() {
              return $("#oldpassword").val();
            }
          }
        }
      },
      newpassword: {
        required: true,
        minlength:8,
        maxlength: 20,
        isPasswordNotSame:"#oldpassword",
        patternCheck : true
      },
      confirmpassword: {
        required: true,
        minlength:8,
        maxlength: 20,
        equalTo: "#newpassword"
      }
    },

    messages: {
      oldpassword: {
        required: "Please Enter Old Password",
        remote:"Please Enter Valid Password",
        minimum:"Please Enter Minimum 8 Alpha Numerals",
        maxlength:"Please Enter Not More Than 20 Characters"
      },
      newpassword: {
        required: "Please Enter New Password",
        minlength:"Please Enter Minimum 8 Alpha Numerals",
        maxlength: "Your password should not be more than 20 Characters !",
        patternCheck : "Password should contain atleast one uppercase, one lower case character, one digit and one special character"
      },
      confirmpassword: {
        required: "Please Enter Confirm Password",
        minlength:"Please Enter Minimum 8 Alpha Numerals",
        maxlength: "Your password should not be more than 20 Characters !",
        equalTo :"New Password and Confirm Password should be Same"
      }
    },

    highlight: function(element) {
    $(element).closest('.control-group').removeClass('success').addClass('error');
    },
    unhighlight: function(element) {
    $(element).closest('.control-group').removeClass('error').addClass('success');
    },
    success: function(element) {
    //$(element).closest('.control-group').find('.fillimg').addClass('valid');
    // What is ".fillimg"?  That's not a real word.
    },
    errorPlacement: function (error, element) {
    $(element).closest('.control-group').find('.help-block').html(error.text());
    }
});
//end of forget password validation

// nfadmin edit form validation
$("#body_user_profile_body").validate({
    rules: {
        first_name:{
            required:true,
            minlength:3,
            maxlength:50
        },
        last_name:{
            required:true,
            minlength:3,
            maxlength:50
        },
        username:{
            required:true,
            email:true
        },
        suffix:{
            required:true
        },
        birthdate:{
            required:true
        },
        gender:{
            required:true
        },
        door_no:{
            required:true
        },
        street_name:{
            required:true
        },
        address:{
            required:true
        },
        locality:{
            required:true
        },
        city:{
            required:true
        },
        state:{
            required:true
        },
        pincode:{
            required:true,
            digits:true
        },
        country:{
            required:true
        },
        nationality:{
            required:true
        },
        blood_group:{
            required:true
        },
        company_name:{
            required:true
        },
        company_location:{
            required:true
        },
        company_city:{
            required:true
        },
        company_website:{
            required:true,
            isValideUrl:true
        },
        designation:{
            required:true
        },
        annual_income:{
            required:true,
            digits:true
        },
        qualification:{
            required:true
        },
        college_name:{
            required:true
        },
        year_passout:{
            required:true
        },
        mobile:{
            required:true,
            digits:true,
            minlength:10,
            maxlength:10
        }
    },

    messages: {
        first_name:{
            required:"Please enter First Name",
            minlength:"Please enter minimum 3 Characters",
            maxlength:"Please enter less than 50 Characters"
        },
        last_name:{
            required:"Please enter Last Name",
            minlength:"Please enter minimum 3 Characters",
            maxlength:"Please enter less than 50 Characters"
        },
        username:{
            required:"Please enter Email ID"
        },
        suffix:{
            required:"Please select Suffix"
        },
        birthdate:{
            required:"Please enter Birthdate"
        },
        gender:{
            required:"Please select Gender"
        },
        door_no:{
            required:"Please enter Door Number"
        },
        street_name:{
            required:"Please enter Address1"
        },
        address:{
            required:"Please enter Address2"
        },
        locality:{
            required:"Please enter Locality"
        },
        city:{
            required:"Please enter City"
        },
        state:{
            required:"Please enter State"
        },
        pincode:{
            required:"Please enter Zipcode"
        },
        country:{
            required:"Please enter Country"
        },
        nationality:{
            required:"Please enter Nationality"
        },
        blood_group:{
            required:"Please enter Blood Group"
        },
        company_name:{
            required:"Please enter Company Name"
        },
        company_location:{
            required:"Please enter Company Location"
        },
        company_city:{
            required:"Please enter Company City"
        },
        company_website:{
            required:"Please enter Company Website"
        },
        designation:{
            required:"Please enter Designation"
        },
        annual_income:{
            required:"Please enter Annual Income"
        },
        qualification:{
            required:"Please enter Qualification"
        },
        college_name:{
            required:"Please enter College Name"
        },
        year_passout:{
            required:"Please enter Year Passout"
        },
        mobile:{
            required:"Please enter Mobile Number"
        }
    },

    highlight: function(element) {
    $(element).closest('.control-group').removeClass('success').addClass('error');
    },
    unhighlight: function(element) {
    $(element).closest('.control-group').removeClass('error').addClass('success');
    },
    success: function(element) {
    //$(element).closest('.control-group').find('.fillimg').addClass('valid');
    // What is ".fillimg"?  That's not a real word.
    },
    errorPlacement: function (error, element) {
    $(element).closest('.control-group').find('.help-block').html(error.text());
    }
});
//end of nfadmin edit form validation

// invite_to_rate
$("#invite_to_rate_form").validate({
    rules: {
        name: {
            required: true,
            minlength:3,
            maxlength:50,
        },
        phone:{
            required:true,
            digits:true,
            minlength:10,
            maxlength:10
        },
        email:{
            required:true,
            email:true
        }
    },
    messages: {
        name: {
            required: "Please enter email ID !",
            minlength:"Please enter minimum 3 characters",
            maxlength:"Please enter less than 50 characters"
        },
        phone:{
            required:"Please enter Phone number",
            minlength:"Please enter 10 digit Phone number",
            maxlength:"Please enter 10 digit Phone number"
        },
        email:{
            required:"Please enter Email ID"
        }
    },
    focusInvalid: false,
      invalidHandler: function(form, validator){
        if(!validator.numberOfInvalids())

          return;
        $('html, body').animate({
          scrollTop: $(validator.errorList[0].element).offset().top-200
        },500);
        validator.errorList[0].element.focus();
      },

    highlight: function(element) {
    $(element).closest('.control-group').removeClass('success').addClass('error');
    },
    unhighlight: function(element) {
    $(element).closest('.control-group').removeClass('error').addClass('success');
    },
    success: function(element) {
    //$(element).closest('.control-group').find('.fillimg').addClass('valid');
    // What is ".fillimg"?  That's not a real word.
    },
    errorPlacement: function (error, element) {
    $(element).closest('.control-group').find('.help-block').html(error.text());
    }
});
// end of validate the invite_to_rate

// validation for get_in_touch
$("#reia_contact_form").validate({
    rules: {
      name: {
        required: true
      },
      mobile_number: {
        required: true
      },
      email:{
        required: true,
        email: true,
        email_format: true,
      },
      location:{
        required: true
      },
      content_msg:{
        required:true
      }
    },
    messages: {
      name:{
          required:"Please Enter Your Name"
      },
      mobile_number:{
          required:"Please Enter Valid Mobile Number"
      },
      email:{
          required:"Please Enter Your Email ID",
          email: "Please Enter Valid Email Address",
          email_format: "Please Enter Valid Email Address"
      },
      location:{
        required: "Please Enter Your Location"
      },
      content_msg:{
        required: "Please Enter Your Queries"
      }
    },

    highlight: function(element) {
    $(element).closest('.control-group').removeClass('success').addClass('error');
    },
    unhighlight: function(element) {
    $(element).closest('.control-group').removeClass('error').addClass('success');
    },
    success: function(element) {
    //$(element).closest('.control-group').find('.fillimg').addClass('valid');
    // What is ".fillimg"?  That's not a real word.
    },
    errorPlacement: function (error, element) {
    $(element).closest('.control-group').find('.help-block').html(error.text());
    }
});
}); // End For Document Ready
