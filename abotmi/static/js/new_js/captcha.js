var login_recaptcha, email_signup_recaptcha, forgot_password_recaptcha;

// function for loading Forgot pwd recaptcha
function load_forgot_pwd_recaptcha(){
    if (forgot_password_recaptcha == null){
        forgot_password_recaptcha = grecaptcha.render('Recaptcha_forgot_password_button', {
            'sitekey': recapkey,
            'callback': correctCaptcha_forgot
        });
    }
    grecaptcha.reset(forgot_password_recaptcha);
}

// function for loading Email Signup(Direct Signup) recaptcha
function load_email_signup_recaptcha(){
    if (email_signup_recaptcha == null) {
        email_signup_recaptcha = grecaptcha.render('Recaptcha_email_signup_button', {
            'sitekey': recapkey,
            'callback': correctCaptcha_signup
        });
    }
    grecaptcha.reset(email_signup_recaptcha);
}

// function for loading Login recaptcha
function load_login_recaptcha(){
    if (login_recaptcha == null){
        login_recaptcha = grecaptcha.render('Recaptcha_login_button', {
            'sitekey': recapkey,
            'callback': correctCaptcha
        });
    }
    grecaptcha.reset(login_recaptcha);
}

// function for loading Refer Friend recaptcha
function refer_friend_recaptcha(){
    if (recaptcha_refer_button == null) {
        recaptcha_refer_button = grecaptcha.render('Recaptcha_refer_friend_button', {
            'sitekey': recapkey,
            'callback': correctCaptcha_referfriend
        });
    }
    grecaptcha.reset(recaptcha_refer_button);
}


// Validating the Login form Recaptcha
var correctCaptcha = function (response) {
    validate_recptcha(login_recaptcha, 'help_login_recpatcha');
};
// Validating the Forgot Password form Recaptcha
var correctCaptcha_forgot = function (response) {
    validate_recptcha(forgot_password_recaptcha, 'help_forgot_recpatcha');
};
// Validating the Signup form Recaptcha
var correctCaptcha_signup = function (response) {
    validate_recptcha(email_signup_recaptcha, 'help_signup_recpatcha');
};
// Validating the refer friend form Recaptcha
var correctCaptcha_referfriend = function (response) {
    validate_recptcha(recaptcha_refer_button, 'help_refer_freind_recpatcha');
};