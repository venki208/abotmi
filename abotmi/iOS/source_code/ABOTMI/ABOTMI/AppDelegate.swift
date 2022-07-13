//
//  AppDelegate.swift
//  UPWRDZ
//
//  Created by Dos on 7/7/17.
//  Copyright © 2017 mobisir. All rights reserved.
//

import UIKit
import WebKit
import FBSDKCoreKit
import FBSDKLoginKit
import GoogleSignIn
import AVFoundation
@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {
    var window: UIWindow?
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        GIDSignIn.sharedInstance().clientID = "1002893254921-krtvfasf7nh8og9n8j48jolm3kt7nhdk.apps.googleusercontent.com"
        GIDSignIn.sharedInstance().shouldFetchBasicProfile = true
        FBSDKApplicationDelegate.sharedInstance().application(application, didFinishLaunchingWithOptions: launchOptions)
        return true
    }
    
    
    func application(_ app: UIApplication, open url: URL,options: [UIApplication.OpenURLOptionsKey : Any] = [:]) -> Bool {
        let googlesign = GIDSignIn.sharedInstance().handle(url, sourceApplication:options[UIApplication.OpenURLOptionsKey.sourceApplication] as! String!, annotation: nil)
        let checkFB = FBSDKApplicationDelegate.sharedInstance().application(app, open: url, sourceApplication:options[ UIApplication.OpenURLOptionsKey.sourceApplication] as! String!, annotation: nil)
        let linkdein = LISDKCallbackHandler.application(app, open: url, sourceApplication:options[ UIApplication.OpenURLOptionsKey.sourceApplication] as! String!, annotation: nil)
        return googlesign || checkFB || linkdein
        
    }
    
    
    
    func applicationWillResignActive(_ application: UIApplication) {
        // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
        // Use this method to pause ongoing tasks, disable timers, and invalidate graphics rendering callbacks. Games should use this method to pause the game.
        
        
    }
    
    func applicationDidEnterBackground(_ application: UIApplication) {
        // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
        // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
        
    }
    
    func applicationWillEnterForeground(_ application: UIApplication) {
        // Called as part of the transition from the background to the active state; here you can undo many of the changes made on entering the background.
        
        
    }
    
    func applicationDidBecomeActive(_ application: UIApplication) {
        // Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
        
        //print ("hii_samiiii")
        //SVProgressHUD.show(withStatus: "please wait...")
        //(window?.rootViewController as? ViewController)?.alertforcamera()
    }
    
    func applicationWillTerminate(_ application: UIApplication) {
        // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
    }
    
    
    
}

