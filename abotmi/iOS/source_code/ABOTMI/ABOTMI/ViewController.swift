//
//  ViewController.swift
//  UPWRDZ
//
//  Created by Dos on 7/7/17.
//  Copyright © 2017 mobisir. All rights reserved.
//

import UIKit
import WebKit
import Social
import Foundation
import FBSDKCoreKit
import FBSDKLoginKit
import GoogleSignIn
import SVProgressHUD
import Photos
import AVFoundation
import FBSDKShareKit
var constant_url="https://test.abotmi.com/static/www/index.html"
let constant_url_linkdeln="https://test.abotmi.com/static/www/index.html"
let projectDomain="test.abotmi.com"
let signup_url_token="https://test.abotmi.com/api/check-email-exists/"
let url_linkdein_email = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"
let url_linkdein_details = "https://api.linkedin.com/v2/me?projection=(id,firstName,lastName)"
let socialshare_url="socialshareurl"
let socialshare_facebook="facebook"
let socialshare_twitter="twitter"
let socialshare_whatsapp="whatsapp"
let socialshare_linkdein="linkedin"
let socialshare_gmail="googleplus"
let picker=UIImagePickerController()
var count:Int = 0
var token_social:String = ""

var source:String = ""
var taskAComplete = false
var taskBComplete = false
var linkdeln_email = ""
var linkdeln_first = ""
var linkdeln_second = ""
var spinningActivityIndicator: UIActivityIndicatorView = UIActivityIndicatorView()
let container: UIView = UIView()
let loadingView: UIView = UIView()
let window = UIApplication.shared.keyWindow
func schemeAvailable(scheme: String) -> Bool {
    if let url = URL(string: scheme) {
        return UIApplication.shared.canOpenURL(url)
    }
    return false
}
var alertView: UIAlertController?
class ViewController: UIViewController, UIWebViewDelegate, GIDSignInUIDelegate,GIDSignInDelegate, UIImagePickerControllerDelegate, UINavigationControllerDelegate, UIAlertViewDelegate
{
    @IBOutlet var mywebview:  UIWebView!
    
    //linkdeln integration
    let linkedInKey = "81548p0fvaq3g7"
    
    let linkedInSecret = "tKr3Jx9nr4DSaVuP"
    
    let authorizationEndPoint = "https://www.linkedin.com/oauth/v2/authorization"
    
    let accessTokenEndPoint = "https://www.linkedin.com/oauth/v2/accessToken"
    let reachability = Reachability()!
    var imageView : UIImageView!
    let image = UIImage(named: "no-internet-connection.png")
    func myweb() {
        let fbInstalled = schemeAvailable(scheme: "fb://")
        let linkdeinInstalled = schemeAvailable(scheme: "linkedin://")
        let gplusInstalled = schemeAvailable(scheme: "gplus://")
        if fbInstalled == true
        {
            
            constant_url = constant_url+(constant_url.contains("socialapp") ? ",fbapp":"#/redirect/socialapp=fbapp")
        }
        if linkdeinInstalled == true
        {
            constant_url = constant_url+(constant_url.contains("socialapp") ? ",linkedinapp":"#/redirect/socialapp=linkedinapp")
        }
        
        
        let url=constant_url
        mywebview.allowsInlineMediaPlayback=true
        mywebview.scrollView.bounces = false
        mywebview.allowsInlineMediaPlayback = true
        mywebview.mediaPlaybackAllowsAirPlay = true
        mywebview.mediaPlaybackRequiresUserAction = false
        let myurl=NSURL(string: url)
        let myurlreq=NSURLRequest(url: myurl! as URL)
        mywebview.loadRequest(myurlreq as URLRequest)
        
    }
    
    func linkdeln_alertController()
    {
        let alert = UIAlertController(title: "Alert", message: "Please try again later", preferredStyle: UIAlertController.Style.alert)
        alert.addAction(UIAlertAction(title: "ok", style: UIAlertAction.Style.default, handler: nil))
        self.present(alert, animated: true, completion: nil)
    }
    func json_alertController()
    {
        let alert = UIAlertController(title: "Alert", message: "unable to get the data try again", preferredStyle: UIAlertController.Style.alert)
        alert.addAction(UIAlertAction(title: "ok", style: UIAlertAction.Style.default, handler: nil))
        self.present(alert, animated: true, completion: nil)
    }
    func startAuthorization() {
        // Specify the response type which should always be "code".
        let responseType = "code"
        // Set the redirect URL. Adding the percent escape characthers is necessary.
        let redirectURL = constant_url_linkdeln
        let encodedData = redirectURL.addingPercentEncoding(withAllowedCharacters: CharacterSet.urlHostAllowed)
        // Create a random string based on the time intervale (it will be in the form linkedin12345679).
        let state = "linkedin\(Int(NSDate().timeIntervalSince1970))"
        // Set preferred scope.
        let scope = "r_liteprofile,r_emailaddress"
        // Create the authorization URL string.
        var authorizationURL = "\(authorizationEndPoint)?"
        authorizationURL += "response_type=\(responseType)&"
        authorizationURL += "client_id=\(linkedInKey)&"
        authorizationURL += "redirect_uri=\(redirectURL)&"
        authorizationURL += "state=\(state)&"
        authorizationURL += "scope=\(scope)"
        // Create a URL request and load it in the web view.
        let request_url = NSURLRequest(url: NSURL(string: authorizationURL)! as URL)
        mywebview.loadRequest(request_url as URLRequest)
        
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        SVProgressHUD.show(withStatus: "please wait...")
        SVProgressHUD.setBackgroundColor(UIColor.clear)
        
        reachability.whenReachable = { reachability in
            DispatchQueue.main.async {
                if reachability.connection == .wifi{
                    print("Reachable via WiFI")
                    self.imageView.isHidden = true
                    self.mywebview.isUserInteractionEnabled = true
                    
                } else {
                    print("Reachable via Cellular")
                    self.imageView.isHidden = true
                    self.mywebview.isUserInteractionEnabled = true
                    
                }
            }
        }
        reachability.whenUnreachable = { reachability in
            DispatchQueue.main.async {
                print("Not reachable")
                SVProgressHUD.dismiss()
                self.imageView.isHidden = false
                self.mywebview.isUserInteractionEnabled = false
                
            }
        }
        do {
            try reachability.startNotifier()
        } catch {
            print("Unable to start notifier!")
        }
        
        let screenwidth = self.view.frame.size.width
        let screenheight = self.view.frame.size.height
        imageView = UIImageView(frame: CGRect(x: 0, y: 0, width: screenwidth, height: screenheight))
        imageView.clipsToBounds = true
        imageView.contentMode = .scaleAspectFill
        imageView.center = self.view.center
        imageView.image = image
        mywebview.scalesPageToFit = true
        mywebview.addSubview(imageView)
        imageView.isHidden = true
        imageView.alpha = 0
        mywebview.delegate = self
        picker.delegate=self
        myweb()
    }
    override func viewDidAppear(_ animated: Bool) {
        imageView.fadeIn()
        
        NotificationCenter.default.addObserver(self, selector: #selector(internetChanged),name: Notification.Name.reachabilityChanged,object: reachability)
        do {
            try reachability.startNotifier()
        } catch {
            print("Couldn't start reachability notifier!")
        }
    }
    
    @objc func internetChanged(note: NSNotification) {
        let reachability = note.object as! Reachability
        if reachability.connection == .none{
            if reachability.connection == .wifi {
                print("Reachable via WiFi")
                
            } else {
                print("Reachable via Cellular Data")
                
            }
        } else {
            print("Network not reachable")
        }
    }
    
    func sign(_ signIn: GIDSignIn!, didSignInFor user: GIDGoogleUser!, withError error: Error?) {
        do{
            self.customActivityIndicatory(self.view, startAnimate: true)
            
            if (error == nil) {
                
                let email = user.profile.email
                let gender=String("")
                let birthday=String("")
                let fullNameArr =  user.profile.name?.components(separatedBy: " ")
                let firs_name    = fullNameArr?[0]
                let last_name = fullNameArr?[1]
                source="GMAIL"
                self.getToken(gender: gender,first_name: String(describing:firs_name!),last_name: String(describing:last_name!),email: String(describing:email!),source: String(describing:source))
                
            } else {
                let alert = UIAlertController(title: "", message: "Try Again", preferredStyle: UIAlertController.Style.alert)
                alert.addAction(UIAlertAction(title: "ok", style: UIAlertAction.Style.default, handler: nil))
                self.present(alert, animated: true, completion: nil)
                self.customActivityIndicatory(self.view, startAnimate: false)
            }
        }catch{
            let alert = UIAlertController(title: "Alert", message: "Please try again network problem", preferredStyle: UIAlertController.Style.alert)
            alert.addAction(UIAlertAction(title: "ok", style: UIAlertAction.Style.default, handler: nil))
            self.present(alert, animated: true, completion: nil)
        }
    }
    
    func sign(_ signIn: GIDSignIn!, didDisconnectWith user: GIDGoogleUser!, withError error: Error!) {
        // Perform any operations when the user disconnects from app here.
        // ...
        
    }
    
    
    
    
    func customActivityIndicatory(_ viewContainer: UIView, startAnimate:Bool? = true) -> UIActivityIndicatorView {
        let mainContainer: UIView = UIView(frame: viewContainer.frame)
        mainContainer.center = viewContainer.center
        mainContainer.backgroundColor = UIColor.white
        mainContainer.alpha = 0.5
        mainContainer.tag = 789456123
        mainContainer.isUserInteractionEnabled = false
        
        let viewBackgroundLoading: UIView = UIView(frame: CGRect(x:0,y: 0,width: 80,height: 80))
        viewBackgroundLoading.center = viewContainer.center
        viewBackgroundLoading.backgroundColor = UIColor.black
        viewBackgroundLoading.alpha = 0.5
        viewBackgroundLoading.clipsToBounds = true
        viewBackgroundLoading.layer.cornerRadius = 15
        
        let activityIndicatorView: UIActivityIndicatorView = UIActivityIndicatorView()
        activityIndicatorView.frame = CGRect(x:0.0,y: 0.0,width: 40.0, height: 40.0)
        activityIndicatorView.style =
            UIActivityIndicatorView.Style.whiteLarge
        activityIndicatorView.center = CGPoint(x: viewBackgroundLoading.frame.size.width / 2, y: viewBackgroundLoading.frame.size.height / 2)
        if startAnimate!{
            viewBackgroundLoading.addSubview(activityIndicatorView)
            mainContainer.addSubview(viewBackgroundLoading)
            viewContainer.addSubview(mainContainer)
            activityIndicatorView.startAnimating()
        }else{
            for subview in viewContainer.subviews{
                if subview.tag == 789456123{
                    subview.removeFromSuperview()
                }
            }
        }
        return activityIndicatorView
    }
    
    func getToken(gender: String,first_name: String,last_name: String,email: String,source: String){
        print ("hii inside token")
        let myUrl_token = URL(string: signup_url_token)
        var request = URLRequest(url:myUrl_token!)
        request.httpMethod = "POST"// Compose a query string
        let postString = "email=\(email)&first_name=\(first_name)&last_name=\(last_name)&gender=\(gender)&source=\(source)&next_url=null";
        print (postString);
        request.httpBody = postString.data(using: String.Encoding.utf8);
        let task = URLSession.shared.dataTask(with: request) { (data: Data?, response: URLResponse?, error: Error?) in
            print (data!)
            if let httpResponse = response as? HTTPURLResponse {
                print("statusCode: \(httpResponse.statusCode)")
            }
            if error != nil
            {
                return
            }
            
            //Let's convert response sent from a server side script to a NSDictionary object:
            do {
                let json = try JSONSerialization.jsonObject(with: data!, options: .mutableContainers) as? NSDictionary
                
                if let parseJSON = json {
                    // Now we can access value of First Name by its key
                    //print (parseJSON)
                    token_social = (parseJSON["token"] as? String)!
                   let email_server = (parseJSON["email"] as? String)!
                   let email_status = (parseJSON["email_verified_status"] as? String)!
                   let email_firstname = (parseJSON["first_name"] as? String)!
                   let email_password = (parseJSON["password"] as? String)!
                    let email_source = (parseJSON["source"] as? String)!
                    let email_last_name = (parseJSON["last_name"] as? String)!
                    let email_gender = (parseJSON["gender"] as? String)!
                    let email_next_url = (parseJSON["next_url"] as? String)!
                    // Or you can create the one from Swift dictionary
                    // input payload
                    let inputPayload = ["token":token_social,"email":email_server,"email_verified_status":email_status,"first_name":email_firstname,"password":email_password,"last_name":email_last_name,"source":email_source,"gender":email_gender,"next_url":email_next_url]
                    // Serialize the Swift object into Data
                    let serializedData = try! JSONSerialization.data(withJSONObject: inputPayload, options: [])
                    // Encode the data into JSON string
                    let encodedData = String(data: serializedData, encoding: String.Encoding.utf8)
                    // Now pass this dictionary to javascript function (Assuming it exists in the HTML code)
                    
                   
                    
                    DispatchQueue.main.async {
                        let resultValue = self.mywebview.stringByEvaluatingJavaScript(from: "token('\(encodedData!)')")
                        self.customActivityIndicatory(self.view, startAnimate: false)
                    }
                    
                    
                }
            } catch {
                print(error)
            }
        }
        task.resume()
        
    }
    
    
    
    
    func webView(_ webView: UIWebView,
                 didFailLoadWithError error: Error)
    {
        print("error")
        
    }
    
    func alertforcamera()
    {
        //MARK:- CAMERA ACCESS CHECK
        
        let authorizationStatus = AVCaptureDevice.authorizationStatus(for: AVMediaType.video)
        switch authorizationStatus {
        case .notDetermined:
            // permission dialog not yet presented, request authorization
            AVCaptureDevice.requestAccess(for: AVMediaType.video,
                                          completionHandler: { (granted:Bool) -> Void in
                                            if granted {
                                                print("access granted")
                                            }
                                            else {
                                                print("access denied")
                                                self.alertPromptToAllowCameraAccessViaSetting()
                                                
                                            }
            })
        case .authorized:
            print("Access authorized")
        case .denied, .restricted:
            print ("no acess")
            self.alertPromptToAllowCameraAccessViaSetting()
        default:
            print("DO NOTHING")
        }
        
        
    }
    
    func requestForAccessToken(authorizationCode: String) {
        let grantType = "authorization_code"
        
        print (authorizationCode)
        let redirectURL = constant_url_linkdeln
        let encodedData = redirectURL.addingPercentEncoding(withAllowedCharacters: CharacterSet.urlHostAllowed)
        // Set the POST parameters.
        var postParams = "grant_type=\(grantType)&"
        postParams += "code=\(authorizationCode)&"
        postParams += "redirect_uri=\(redirectURL)&"
        postParams += "client_id=\(linkedInKey)&"
        postParams += "client_secret=\(linkedInSecret)"
        
        // Convert the POST parameters into a NSData object.
        
        let postData = postParams.data(using: String.Encoding.utf8)
        
        
        // Initialize a mutable URL request object using the access token endpoint URL string.
        let request_acessToken = NSMutableURLRequest(url: NSURL(string: accessTokenEndPoint)! as URL)
        
        // Indicate that we're about to make a POST request.
        request_acessToken.httpMethod = "POST"
        
        // Set the HTTP body using the postData object created above.
        request_acessToken.httpBody = postData
        
        // Add the required HTTP header field.
        request_acessToken.addValue("application/x-www-form-urlencoded;", forHTTPHeaderField: "Content-Type")
        
        
        // Initialize a NSURLSession object.
        let session = URLSession(configuration: URLSessionConfiguration.default)
        
        // Make the request.
        let task_acessToken: URLSessionDataTask = session.dataTask(with: request_acessToken as URLRequest) { (data, response, error) -> Void in
            // Get the HTTP status code of the request.
            let statusCode = (response as! HTTPURLResponse).statusCode
            print (statusCode)
            if statusCode == 200 {
                
                // Convert the received JSON data into a dictionary.
                do {
                    let json_acesstoken = try JSONSerialization.jsonObject(with: data!, options: .mutableContainers) as? NSDictionary
                    
                    if let parseJSON_token = json_acesstoken {
                        // Now we can access value of First Name by its key
                        let   accessToken = (parseJSON_token["access_token"] as? String)!
                        print (accessToken)
                        UserDefaults.standard.removeObject(forKey: "LIAccessToken")
                        UserDefaults.standard.set(accessToken, forKey: "LIAccessToken")
                        UserDefaults.standard.synchronize()
                        DispatchQueue.main.async {
                            self.customActivityIndicatory(self.view, startAnimate: true)
                            
                        }
                        
                        self.linkdelnProfileDetails()
                        self.linkdelnDetailsEmail()
                    }
                }catch {
                    self.customActivityIndicatory(self.view, startAnimate: false)
                    self.json_alertController()
                    print("Could not convert JSON data into a dictionary.")
                }
            }
            else{
                self.customActivityIndicatory(self.view, startAnimate: false)
                self.linkdeln_alertController()
            }
        }
        
        task_acessToken.resume()
    
        
        
    }
    
    func linkdelnProfileDetails()
    {
        if let accessToken = UserDefaults.standard.object(forKey: "LIAccessToken") {
            
            
            // Initialize a mutable URL request object.
            let request = NSMutableURLRequest(url: NSURL(string: url_linkdein_details)! as URL)
            
            // Indicate that this is a GET request.
            request.httpMethod = "GET"
            
            // Add the access token as an HTTP header field.
            request.addValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")
            
            // Initialize a NSURLSession object.
            let session = URLSession(configuration: URLSessionConfiguration.default)
            
            // Make the request.
            let task_details: URLSessionDataTask = session.dataTask(with: request as URLRequest) { (data, response, error) -> Void in
                // Get the HTTP status code of the request.
                let statusCode = (response as! HTTPURLResponse).statusCode
                print (statusCode)
                if statusCode == 200 {
                    // Convert the received JSON data into a dictionary.
                    do {
                        let json_details = try JSONSerialization.jsonObject(with: data!, options: []) as! NSDictionary
                        let json_first=json_details["firstName"] as! NSDictionary
                        let json_first_data=json_first["localized"] as! NSDictionary
                        linkdeln_first=(json_first_data["en_US"] as? String)!
                        let json_second=json_details["lastName"] as! NSDictionary
                        let json_second_data=json_second["localized"] as! NSDictionary
                        linkdeln_second=(json_second_data["en_US"] as? String)!
                        taskBComplete = true
                        self.checkResults()
                    } catch {
                        self.customActivityIndicatory(self.view, startAnimate: false)
                        self.json_alertController()
                        print(error)
                    }
                }
                else{
                    self.customActivityIndicatory(self.view, startAnimate: false)
                    self.linkdeln_alertController()
                }
            }
            
            task_details.resume()
            
            
            
            
        }
        
        
    }
    func linkdelnDetailsEmail()
    {
        if let accessToken = UserDefaults.standard.object(forKey: "LIAccessToken") {
            //fetching all details for user
            let request_details = NSMutableURLRequest(url: NSURL(string: url_linkdein_email)! as URL)
            
            // Indicate that this is a GET request.
            request_details.httpMethod = "GET"
            
            // Add the access token as an HTTP header field.
            request_details.addValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")
            
            // Initialize a NSURLSession object.
            let session_details = URLSession(configuration: URLSessionConfiguration.default)
            
            // Make the request.
            let task_details_user: URLSessionDataTask = session_details.dataTask(with: request_details as URLRequest) { (data, response, error) -> Void in
                // Get the HTTP status code of the request.
                let statusCode = (response as! HTTPURLResponse).statusCode
                print (statusCode)
                if statusCode == 200 {
                    // Convert the received JSON data into a dictionary.
                    
                    do {
                        let json_data = try? JSONSerialization.jsonObject(with: data!, options: []) as? [String: Any]
                        if let weatherArray = json_data!?["elements"] as? [[String:Any]],
                            let weather = weatherArray.first{
                            let json_email=weather["handle~"] as! NSDictionary
                            linkdeln_email = (json_email["emailAddress"] as? String)!
                            // the value is an optional.
                        }
                        taskAComplete = true
                        self.checkResults()
                    } catch {
                        self.customActivityIndicatory(self.view, startAnimate: false)
                        self.json_alertController()
                        print(error)
                    }
                }
                else{
                    self.customActivityIndicatory(self.view, startAnimate: false)
                    self.linkdeln_alertController()
                }
            }
            
            task_details_user.resume()
        }
    }
    
    
    func checkResults(){
        // Both tasks completed then function will be called!
        if taskAComplete && taskBComplete {
            print ("check results")
            let gender=String("")
            let first_name = linkdeln_first
            print (first_name)
            let last_name = linkdeln_second
            print (last_name)
            let email = linkdeln_email
            print (email)
            source = "LINKDEIN"
            self.getToken(gender: gender,first_name: String(describing:first_name),last_name: String(describing:last_name),email:String(describing: email),source:String(describing:source))
        }
    }
    
    
    func alertPromptToAllowCameraAccessViaSetting()
    {
        
        var accessDescription = Bundle.main.object(forInfoDictionaryKey: "NSPhotoLibraryUsageDescription") as? String
        var alertController = UIAlertController(title: accessDescription, message: "To give permissions tap on 'Change Settings' button", preferredStyle: .alert)
        var settingsAction = UIAlertAction(title: "Change Settings", style: .default, handler: {(_ action: UIAlertAction) -> Void in
            UIApplication.shared.openURL(URL(string: UIApplication.openSettingsURLString)!)
        })
        alertController.addAction(settingsAction)
        DispatchQueue.main.async(){
            self.present(alertController, animated: true)
        }
    }
    func webViewDidFinishLoad(_ webView : UIWebView) {
        //Page is loaded do what you want
        SVProgressHUD.dismiss()
    }
    
    func webView(_ webView: UIWebView, shouldStartLoadWith request: URLRequest, navigationType: UIWebView.NavigationType) -> Bool {
        
        let surl = request.url?.absoluteString
        print (surl)
        print ("request is\(request)")
        
        var url_link = URL(string: surl!)
        var domain = url_link?.host
        
        if domain == projectDomain {
            if url_link!.absoluteString.range(of: "code") != nil {
                // Extract the authorization code.
                if url_link!.absoluteString.range(of: "redirect") == nil
                {
                    print ("nothing")
                }
                else{
                    let urlParts = url_link!.absoluteString.components(separatedBy: "?")
                    let code = urlParts[1].components(separatedBy: "=")[1]
                    print (code)
                    requestForAccessToken(authorizationCode: code)
                   
                }
            }
        }
        
        if let scheme = request.url?.scheme{
            if scheme == "mike" {
                print ("hai")
                
            }
        }
        
        let url_split = request.url?.absoluteString
        if(url_split?.contains("#/app/myidentity/changepicture"))!
        {
            alertforcamera()
            
        }
        
        
        if(url_split?.contains("#/start/eipv"))!
        {
            alertforcamera()
            
        }
        
        
        
        
        if( url_split?.contains("nativeurl://logout"))!
        {
            myweb()
        }
        
        if( url_split?.contains("socialsignupurl"))!
        {
            print ("hii_signup");
            let url_splits = url_split?.components(separatedBy: "://")
            
            if surl=="socialsignupurl://google/" {
                GIDSignIn.sharedInstance().uiDelegate = self
                GIDSignIn.sharedInstance().signIn()
                GIDSignIn.sharedInstance().delegate = self
                
            }
            
            
            if surl=="socialsignupurl://facebook/" {
                print ("hai");
                do{
                    
                    print("inside print")
                    let fbLoginManager : FBSDKLoginManager = FBSDKLoginManager()
                    self.customActivityIndicatory(self.view, startAnimate: true)
                    fbLoginManager.logIn(withReadPermissions: ["email"], from: self) { (result, error) in
                        if (error == nil){
                            let fbloginresult : FBSDKLoginManagerLoginResult = result!
                            if fbloginresult.grantedPermissions != nil {
                                if(fbloginresult.grantedPermissions.contains("email"))
                                {
                                    getFBUserData()
                                }
                                
                            }
                            else{
                                let alert = UIAlertController(title: "", message: "Try Again", preferredStyle: UIAlertController.Style.alert)
                                alert.addAction(UIAlertAction(title: "ok", style: UIAlertAction.Style.default, handler: nil))
                                self.present(alert, animated: true, completion: nil)
                                self.customActivityIndicatory(self.view, startAnimate: false)
                            }
                        }
                        else{
                            let alert = UIAlertController(title: "", message: "Try Again", preferredStyle: UIAlertController.Style.alert)
                            alert.addAction(UIAlertAction(title: "ok", style: UIAlertAction.Style.default, handler: nil))
                            self.present(alert, animated: true, completion: nil)
                            self.customActivityIndicatory(self.view, startAnimate: false)
                        }
                        
                    }
                    
                    func getFBUserData()
                    {
                        print ("inside fb");
                        FBSDKGraphRequest(graphPath: "me", parameters: ["fields": "id, name, first_name, last_name,email"]).start(completionHandler: { (connection, result, error) -> Void in
                            if (error == nil){
                                let fbDetails = result as! NSDictionary
                                let gender = "nil"
                                let first_name = fbDetails["first_name"]
                                let last_name=fbDetails["last_name"]
                                let email=fbDetails["email"]
                                source = "facebook"
                               
                                self.getToken(gender: String(describing:gender),first_name: String(describing:first_name!),last_name: String(describing:last_name!),email: String(describing:email!),source: String(describing:source))
                                
                            }
                        })
                        
                        
                    }
                    
                }catch {
                    let alert = UIAlertController(title: "Alert", message: "Please try again network problem", preferredStyle: UIAlertController.Style.alert)
                    alert.addAction(UIAlertAction(title: "ok", style: UIAlertAction.Style.default, handler: nil))
                    self.present(alert, animated: true, completion: nil)
                    
                }
                
            }
            if surl=="socialsignupurl://linkedin/" {
                
                startAuthorization()
                
                
            }
        }
        
        if( url_split?.contains("socialshareurl"))!
        {
            let profileurl = request.url?.absoluteString
            let profileurlArr = profileurl?.components(separatedBy: "=")
            let upwardzprofile = profileurlArr?[1].removingPercentEncoding!
            let profile_url = profileurlArr?[0]
            let profile_url_signup = profile_url?.components(separatedBy: "://")
            let profile_url_signups = profile_url_signup?[1]
            let profile_url_signup_url = profile_url_signups?.components(separatedBy:"//")
            let profile_url_signup_urls = profile_url_signup_url?[0]
            if( profile_url_signup_urls==socialshare_facebook) {
                let msg:String = upwardzprofile!
                func shareToFacebook() {
                    
                    let fbInstalled = schemeAvailable(scheme: "fb://")
                    if fbInstalled == true
                    {
                        
                        let content = FBSDKShareLinkContent()
                        content.contentURL =  URL(string: msg)
                        let dialog : FBSDKShareDialog = FBSDKShareDialog()
                        dialog.fromViewController = self
                        dialog.shareContent = content
                        dialog.mode = FBSDKShareDialogMode.feedWeb
                        dialog.show()
                    }
                        
                    else {
                        let alert = UIAlertController(title: "Alert", message: "facebook   is not installed first install", preferredStyle: UIAlertController.Style.alert)
                        alert.addAction(UIAlertAction(title: "ok", style: UIAlertAction.Style.default, handler: nil))
                        self.present(alert, animated: true, completion: nil)
                    }
                    
                }
                
                shareToFacebook()
                
                
            } else if(profile_url_signup_urls==socialshare_whatsapp) {
                let msg:String = upwardzprofile!
                let urlWhats:String = "whatsapp://send?text=\(msg)"
                if let urlString =  urlWhats.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) {
                    if let whatsappURL = NSURL(string: urlString) {
                        if UIApplication.shared.canOpenURL(whatsappURL as URL) {
                            UIApplication.shared.openURL(whatsappURL as URL)
                        } else {
                            let alert = UIAlertController(title: "Alert", message: "Whatsup messenger App is not installed first install", preferredStyle: UIAlertController.Style.alert)
                            alert.addAction(UIAlertAction(title: "ok", style: UIAlertAction.Style.default, handler: nil))
                            self.present(alert, animated: true, completion: nil)
                        }
                    }
                }
            }
            else if(profile_url_signup_urls==socialshare_linkdein) {
                let msg:String = upwardzprofile!
                let url_linkdein:String = "linkedin://shareArticle?mini=true&url=\(msg)"
                if let urlString =  url_linkdein.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) {
                    if let URL_linkdein = NSURL(string: urlString) {
                        if UIApplication.shared.canOpenURL(URL_linkdein as URL) {
                            UIApplication.shared.openURL(URL_linkdein as URL)
                        } else {
                            let alert = UIAlertController(title: "Alert", message: "linkdein App is not installed first install", preferredStyle: UIAlertController.Style.alert)
                            alert.addAction(UIAlertAction(title: "ok", style: UIAlertAction.Style.default, handler: nil))
                            self.present(alert, animated: true, completion: nil)
                        }
                    }
                }
            }
                
                
            else if(profile_url_signup_urls==socialshare_gmail)
            {
                let msg:String = upwardzprofile!
                let url_gplus:String = "gplus://plus.google.com/share?text=\(msg)"
                if let urlString =  url_gplus.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) {
                    if let URL_gplus = NSURL(string: urlString) {
                        if UIApplication.shared.canOpenURL(URL_gplus as URL) {
                            UIApplication.shared.openURL(URL_gplus as URL)
                        } else {
                            let alert = UIAlertController(title: "Alert", message: "please install google plus app", preferredStyle: UIAlertController.Style.alert)
                            alert.addAction(UIAlertAction(title: "ok", style: UIAlertAction.Style.default, handler: nil))
                            self.present(alert, animated: true, completion: nil)
                        }
                    }
                }
                
                
            }
                
            else if(profile_url_signup_urls==socialshare_twitter) {
                let msg:String = upwardzprofile!
                let url_twitter = "twitter://post?message=\(msg)"
                if let urlStringtwitter =  url_twitter.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) {
                    if let URL_twitter = NSURL(string: urlStringtwitter) {
                        if UIApplication.shared.canOpenURL(URL_twitter as URL) {
                            UIApplication.shared.openURL(URL_twitter as URL)
                            
                        } else {
                            let alert = UIAlertController(title: "Alert", message: "Twitter app is not installed install it", preferredStyle: UIAlertController.Style.alert)
                            alert.addAction(UIAlertAction(title: "ok", style: UIAlertAction.Style.default, handler: nil))
                            self.present(alert, animated: true, completion: nil)
                        }
                    }
                }
                
                
            }
            
        }
        
        
        return true
    }
    
    
}
extension UIImageView {
    func fadeIn(withDuration duration: TimeInterval = 1) {
        UIView.animate(withDuration: duration, delay: 0.5, animations: {
            self.alpha = 1.5
        })
    }
    
    func fadeOut(withDuration duration: TimeInterval = 1) {
        UIView.animate(withDuration: duration, delay: 1, options: [.repeat], animations: {
            self.alpha = 0.0
        })
    }
}

