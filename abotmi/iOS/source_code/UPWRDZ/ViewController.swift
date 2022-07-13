//
//  ViewController.swift
//  UPWRDZ
//
//  Created by Dos on 7/7/17.
//  Copyright © 2017 mobisir. All rights reserved.
//

import UIKit
import Social
import Foundation
import FBSDKCoreKit
import FBSDKLoginKit
import Firebase
import GoogleSignIn
import TwitterKit
import TwitterCore
import FirebaseAuth
import FBSDKShareKit
import FBSDKMessengerShareKit
var constant_url="https://dev1.upwrdz.com/static/www/index.html"
let signup_url_token="https://dev1.upwrdz.com/api/social-signup-login/"
let url_linkdein = "https://api.linkedin.com/v1/people/~:(id,first-name,last-name,maiden-name,email-address)"
let socialshare_url="socialshareurl"
let socialshare_facebook="facebook"
let socialshare_twitter="twitter"
let socialshare_whatsapp="whatsapp"
let socialshare_linkdein="linkedin"
let socialshare_gmail="googleplus"
var count:Int = 0
var token_social:String = ""
var source:String = ""
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
class ViewController: UIViewController, UIWebViewDelegate, GIDSignInUIDelegate, GIDSignInDelegate {
    
    @IBOutlet var mywebview: UIWebView!
    func myweb() {
        
        let fbInstalled = schemeAvailable(scheme: "fb://")
        let linkdeinInstalled = schemeAvailable(scheme: "linkedin://")
        let gplusInstalled = schemeAvailable(scheme: "gplus://")
        if fbInstalled == true
        {
          
            constant_url = constant_url+(constant_url.contains("socialapp") ? ",fbapp":"#/login/socialapp=fbapp")
        }
               if linkdeinInstalled == true
        {
            constant_url = constant_url+(constant_url.contains("socialapp") ? ",linkedinapp":"#/login/socialapp=linkedinapp")
        }
        
        if gplusInstalled == true
        {
          constant_url = constant_url+(constant_url.contains("socialapp") ? ",gplusapp":"#/login/socialapp=gplusapp")
        }
        let url=constant_url
        let myurl=NSURL(string: url)
        let myurlreq=NSURLRequest(url: myurl! as URL)
        mywebview.loadRequest(myurlreq as URLRequest)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        mywebview.delegate = self
        myweb()
    }
    
    func sign(_ signIn: GIDSignIn!, didSignInFor user: GIDGoogleUser!, withError error: Error?) {
        do{
        
        if let error = error {
            // ...
            return
        }
        guard let idtoken=user.authentication.idToken else {return }
        guard let acesstoken=user.authentication.accessToken else { return }
        let credential = try GoogleAuthProvider.credential(withIDToken: idtoken, accessToken: acesstoken)
        
        Auth.auth().signIn(with: credential) { (user, error) in
            if let err = error
            {
                return
            }

            let gender=String("")
            let email = user?.email
            let fullNameArr =  user?.displayName?.components(separatedBy: " ")
            let firs_name    = fullNameArr?[0]
            let last_name = fullNameArr?[1]
            source="GMAIL"
            self.getToken(gender: gender!,first_name: String(describing:firs_name!),last_name: String(describing:last_name!),email: String(describing:email!),source: String(describing:source))
            
        }
        }catch{
            let alert = UIAlertController(title: "Alert", message: "Please try again network problem", preferredStyle: UIAlertControllerStyle.alert)
            alert.addAction(UIAlertAction(title: "ok", style: UIAlertActionStyle.default, handler: nil))
            self.present(alert, animated: true, completion: nil)
        }
    }
    
    func sign(_ signIn: GIDSignIn!, didDisconnectWith user: GIDGoogleUser!, withError error: Error!) {
        // Perform any operations when the user disconnects from app here.
        // ...
    }
    
    
   
    func getToken(gender: String,first_name: String,last_name: String,email: String,source: String){
        let myUrl_token = URL(string: signup_url_token)
        var request = URLRequest(url:myUrl_token!)
        request.httpMethod = "POST"// Compose a query string
        let postString = "email=\(email)&first_name=\(first_name)&last_name=\(last_name)&gender=\(gender)&source=\(source)&next_url=null";
        request.httpBody = postString.data(using: String.Encoding.utf8);
        let task = URLSession.shared.dataTask(with: request) { (data: Data?, response: URLResponse?, error: Error?) in
            if error != nil
            {
                return
            }
            
            //Let's convert response sent from a server side script to a NSDictionary object:
            do {
                let json = try JSONSerialization.jsonObject(with: data!, options: .mutableContainers) as? NSDictionary
                
                if let parseJSON = json {
                    // Now we can access value of First Name by its key
                    token_social = (parseJSON["token"] as? String)!
                    
                }
            } catch {
                print(error)
            }
        }
        task.resume()
        let url1=constant_url
        let myurl=NSURL(string: url1)
        let myurlreq=NSURLRequest(url: myurl! as URL)
        self.mywebview.loadRequest(myurlreq as URLRequest)
    }
    
    func webViewDidStartLoad(_ webView: UIWebView) {
       
        count = count + 1
        if (count > 1)
        {
        container.frame = UIScreen.main.bounds
        container.backgroundColor = UIColor(hue: 0, saturation: 0, brightness: 0, alpha: 0)
        loadingView.frame = CGRect(x: 0, y: 0, width: 768, height: 978)
        loadingView.center = container.center
        loadingView.backgroundColor = UIColor(hue: 100/300, saturation: 70/100, brightness: 80/100, alpha: 1)
        loadingView.clipsToBounds = true
        loadingView.layer.cornerRadius = 40
        
        spinningActivityIndicator.frame = CGRect(x: 0, y: 0, width: 768, height: 978)
        spinningActivityIndicator.hidesWhenStopped = true
        spinningActivityIndicator.activityIndicatorViewStyle = UIActivityIndicatorViewStyle.whiteLarge
        spinningActivityIndicator.center = CGPoint(x: loadingView.frame.size.width / 2, y: loadingView.frame.size.height / 2)
        loadingView.addSubview(spinningActivityIndicator)
        container.addSubview(loadingView)
        window?.addSubview(container)
        spinningActivityIndicator.startAnimating()
        UIApplication.shared.beginIgnoringInteractionEvents()
        }
    }
    
    func webViewDidFinishLoad(_ webView: UIWebView) {
    
        if (count > 1){
        let str = "token(\"\(token_social)\")"
        var returnedString = mywebview.stringByEvaluatingJavaScript(from: str)
           //The below code is delay for 2 seconds
            var delay = max(0.0, 2.0)
            DispatchQueue.main.asyncAfter(deadline: .now() + delay) {
                spinningActivityIndicator.stopAnimating()
                UIApplication.shared.endIgnoringInteractionEvents()
                container.removeFromSuperview()
        
                  }
        }
        
        
    }
    
    func webView(_ webView: UIWebView, shouldStartLoadWith request: URLRequest, navigationType: UIWebViewNavigationType) -> Bool {
        let surl = request.url?.absoluteString
        let url_split = request.url?.absoluteString
        let url_splits = url_split?.components(separatedBy: "://")
        let urlshare = url_splits?[0]
        let secondsplit=url_splits?[1]
                if surl=="socialsignupurl://google/" {
            GIDSignIn.sharedInstance().uiDelegate = self
            GIDSignIn.sharedInstance().signIn()
            GIDSignIn.sharedInstance().delegate = self
             
        }
        
        
         if surl=="socialsignupurl://facebook/" {
            do{
            let fbLoginManager : FBSDKLoginManager =  try FBSDKLoginManager()
            fbLoginManager.logIn(withReadPermissions: ["email","public_profile"], from: self) { (result, error) -> Void in
                if (error == nil){
                    let facebook_credential = FacebookAuthProvider.credential(withAccessToken: FBSDKAccessToken.current().tokenString)
                    Auth.auth().signIn(with: facebook_credential) { (user, error) in
                        if let error = error {
                            // ...
                            return
                        }
                       
                    getFBUserData()
                    
                }
            }
        
        func getFBUserData(){
            FBSDKGraphRequest(graphPath: "me", parameters: ["fields": "id, name, first_name, last_name,email,gender"]).start(completionHandler: { (connection, result, error) -> Void in
                if (error == nil){
                    let fbDetails = result as! NSDictionary
                    let gender = fbDetails["gender"]
                    let first_name = fbDetails["first_name"]
                    let last_name=fbDetails["last_name"]
                    let email=fbDetails["email"]
                    source = "FACEBOOK"
                    self.getToken(gender: String(describing:gender!),first_name: String(describing:first_name!),last_name: String(describing:last_name!),email: String(describing:email!),source: String(describing:source))
                    
                }
            })
            
            
                }
        }
            }catch {
                let alert = UIAlertController(title: "Alert", message: "Please try again network problem", preferredStyle: UIAlertControllerStyle.alert)
                alert.addAction(UIAlertAction(title: "ok", style: UIAlertActionStyle.default, handler: nil))
                self.present(alert, animated: true, completion: nil)
            
            }
            
        }
        if surl=="socialsignupurl://linkedin/" {
            
            do{
                let link  =  try LISDKSessionManager.createSession(withAuth: [LISDK_BASIC_PROFILE_PERMISSION,LISDK_EMAILADDRESS_PERMISSION], state: nil, showGoToAppStoreDialog: true, successBlock: { (sucess)  in
                let session = LISDKSessionManager.sharedInstance().session
                
                if LISDKSessionManager.hasValidSession() {
                    LISDKAPIHelper.sharedInstance().getRequest(url_linkdein, success: { (response) -> Void in
                        func convertToDictionary(text: String) -> [String: Any]? {
                            if let data = text.data(using: .utf8) {
                                do {
                                    return try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any]
                                } catch {
                                    print(error.localizedDescription)
                                }
                            }
                            return nil
                        }
                        
                        let str = response?.data
                        let dict = convertToDictionary(text: str!)
                        let gender=String("")
                        let first_name = dict?["firstName"]
                        let last_name = dict?["lastName"]
                        let email = dict?["emailAddress"]
                         source = "LINKDEIN"
                        self.getToken(gender: gender!,first_name: String(describing:first_name!),last_name: String(describing:last_name!),email:String(describing: email!),source:String(describing:source))
                        
                    }, error: { (error) -> Void in
                       
                    })
                }
                
                
            }) { (error) -> Void in
                
            }
                
            }catch {
                let alert = UIAlertController(title: "Alert", message: "Please try again network problem", preferredStyle: UIAlertControllerStyle.alert)
                alert.addAction(UIAlertAction(title: "ok", style: UIAlertActionStyle.default, handler: nil))
                self.present(alert, animated: true, completion: nil)
            }
            
                    }
        
        if  urlshare==socialshare_url {
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
                        let alert = UIAlertController(title: "Alert", message: "facebook   is not installed first install", preferredStyle: UIAlertControllerStyle.alert)
                        alert.addAction(UIAlertAction(title: "ok", style: UIAlertActionStyle.default, handler: nil))
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
                            let alert = UIAlertController(title: "Alert", message: "Whatsup messenger App is not installed first install", preferredStyle: UIAlertControllerStyle.alert)
                            alert.addAction(UIAlertAction(title: "ok", style: UIAlertActionStyle.default, handler: nil))
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
                        let alert = UIAlertController(title: "Alert", message: "linkdein App is not installed first install", preferredStyle: UIAlertControllerStyle.alert)
                        alert.addAction(UIAlertAction(title: "ok", style: UIAlertActionStyle.default, handler: nil))
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
                        let alert = UIAlertController(title: "Alert", message: "please install google plus app", preferredStyle: UIAlertControllerStyle.alert)
                        alert.addAction(UIAlertAction(title: "ok", style: UIAlertActionStyle.default, handler: nil))
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
                            let alert = UIAlertController(title: "Alert", message: "URL cannot be opened ", preferredStyle: UIAlertControllerStyle.alert)
                            alert.addAction(UIAlertAction(title: "ok", style: UIAlertActionStyle.default, handler: nil))
                            self.present(alert, animated: true, completion: nil)
                        }
                    }
                }
                
                
            }
                
            }
            
        
        return true
    }
    
    
}
