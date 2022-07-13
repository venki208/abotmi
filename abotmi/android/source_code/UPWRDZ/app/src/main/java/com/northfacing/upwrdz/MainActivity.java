package com.northfacing.upwrdz;

import android.Manifest;
import android.annotation.SuppressLint;
import android.annotation.TargetApi;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.support.v4.content.ContextCompat;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.content.pm.Signature;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.support.v4.app.ActivityCompat;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Environment;
import android.os.Parcelable;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.Display;
import android.view.View;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.Toast;
import com.facebook.AccessToken;
import com.facebook.CallbackManager;
import com.facebook.FacebookCallback;
import com.facebook.FacebookException;
import com.facebook.FacebookSdk;
import com.facebook.GraphRequest;
import com.facebook.GraphResponse;
import com.facebook.Profile;
import com.facebook.login.LoginManager;
import com.facebook.login.LoginResult;
import com.linkedin.platform.LISessionManager;
import com.linkedin.platform.utils.Scope;
import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONArray;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLEncoder;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Date;
import java.util.Iterator;
import java.util.List;

import static android.view.View.GONE;
import static android.view.View.VISIBLE;

public class MainActivity extends AppCompatActivity {

    public static  String domain_url= "https://abotmi.com/";
    public static  String base_url = domain_url+"static/www/index.html";
    public static final String signup_api= domain_url+"api/check-email-exists/";
    private static final String  linkedinurl = "https://api.linkedin.com/v1/people/~:(id,first-name,last-name,emailAddress)";
    public static final String PACKAGE = "com.ptg.upwrdz";

    private static final String url_linkdein_email = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))";
    private static final String url_linkdein_details = "https://api.linkedin.com/v2/me?projection=(id,firstName,lastName)";
    /*CONSTANT FOR THE AUTHORIZATION PROCESS linkdeln*/

    //This is the public api key of our application
    private static final String API_KEY = "8167t78er6wycq";
    //This is the private api key of our application
    private static final String SECRET_KEY = "EsKaLIDEfZOIucs5";
    //This is any string we want to use. This will be used for avoid CSRF attacks. You can generate one here: http://strongpasswordgenerator.com/
    private static final String STATE = "E3ZYKC1T6H2yP4f";
    //This is the url that LinkedIn Auth process will redirect to. We can put whatever we want that starts with http:// or https:// .
    //We use a made up url that we will intercept when redirecting. Avoid Uppercases.
    private static final String REDIRECT_URI = base_url;
    /*********************************************/

    //These are constants used for build the urls
    private static final String AUTHORIZATION_URL = "https://www.linkedin.com/oauth/v2/authorization";
    private static final String ACCESS_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken";
    private static final String SECRET_KEY_PARAM = "client_secret";
    private static final String RESPONSE_TYPE_PARAM = "response_type";
    private static final String GRANT_TYPE_PARAM = "grant_type";
    private static final String GRANT_TYPE = "authorization_code";
    private static final String RESPONSE_TYPE_VALUE ="code";
    private static final String CLIENT_ID_PARAM = "client_id";
    private static final String STATE_PARAM = "state";
    private static final String REDIRECT_URI_PARAM = "redirect_uri";
    private static final String SCOPE_PARAM = "scope";
    private static final String SCOPE = "r_liteprofile,r_emailaddress";
    /*---------------------------------------*/

    public static String acesstoken ="";
    public boolean taskAComplete = false;
    public boolean taskBComplete = false;
    public static String emailAddress ="";
    public static String firstName ="";
    public static String lastName ="";

    private static final String QUESTION_MARK = "?";
    private static final String AMPERSAND = "&";
    private static final String EQUALS = "=";

    /*---------------------------------------*/
    public static final String NOTPROVIDED ="";
    // google return value
    private static final int RC_SIGN_IN = 007;
    private static String facebook = "";
    private static String  linkedin ="";
    private Uri mCapturedImageURI;
    private static final int CAMERA_RESULTCODE=1;
//    private GoogleSignInOptions gso;
//    private GoogleApiClient mGoogleApiClient;
    private ValueCallback<Uri> mUploadMessage;
    private static final int FILECHOOSER_RESULTCODE=002;
    public CallbackManager callbackManager;
    public static  ImageView imagebycode;
    public static  LinearLayout myLayout;
    public Activity activity;
    public static WebView webview;

    private String mCM;
    private ValueCallback<Uri> mUM;
    private ValueCallback<Uri[]> mUMA;
    private final static int FCR=1;

    //select whether you want to upload multiple files (set 'true' for yes)
    private boolean multiple_files = false;


    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent intent) {

        super.onActivityResult(requestCode, resultCode, intent);
        if(Build.VERSION.SDK_INT >= 21){
            Uri[] results = null;
            //checking if response is positive
            if(resultCode== Activity.RESULT_OK){
                if(requestCode == FCR){
                    if(null == mUMA){
                        return;
                    }
                    if(intent == null || intent.getData() == null){
                        if(mCM != null){
                            results = new Uri[]{Uri.parse(mCM)};
                        }
                    }else{
                        String dataString = intent.getDataString();
                        if(dataString != null){
                            results = new Uri[]{Uri.parse(dataString)};
                        } else {
                            if(multiple_files) {
                                if (intent.getClipData() != null) {
                                    final int numSelectedFiles = intent.getClipData().getItemCount();
                                    results = new Uri[numSelectedFiles];
                                    for (int i = 0; i < numSelectedFiles; i++) {
                                        results[i] = intent.getClipData().getItemAt(i).getUri();
                                    }
                                }
                            }
                        }
                    }
                }
            }
            mUMA.onReceiveValue(results);
            mUMA = null;
        }else if(requestCode == FCR){
            if(null == mUM) return;
            Uri result = intent == null || resultCode != RESULT_OK ? null : intent.getData();
            mUM.onReceiveValue(result);
            mUM = null;
        }



//        if(requestCode==CAMERA_RESULTCODE) {
//            if (null == this.mUploadMessage) {
//                return;
//            }
//            Uri result=null;
//            try{
//                if (resultCode != RESULT_OK) {
//                    result = null;
//                } else {
//                    // retrieve from the private variable if the intent is null
//                    result = intent == null ? mCapturedImageURI : intent.getData();
//                    Toast.makeText(getApplicationContext(),"Please wait your image is loading", Toast.LENGTH_LONG).show();
//                }
//            } catch(Exception e) {
//                Toast.makeText(getApplicationContext(), "activity :"+e, Toast.LENGTH_LONG).show();
//            }
//            mUploadMessage.onReceiveValue(result);
//            mUploadMessage = null;
//        } else if(requestCode==FILECHOOSER_RESULTCODE) {
//            if (null == mUploadMessage) return;
//            Uri result = intent == null || resultCode != RESULT_OK ? null : intent.getData();
//            mUploadMessage.onReceiveValue(result);
//            mUploadMessage = null;
//        } else if (requestCode == RC_SIGN_IN) {
//            GoogleSignInResult result = Auth.GoogleSignInApi.getSignInResultFromIntent(intent);
//            if (result.isSuccess()) {
//                GoogleSignInAccount acct = result.getSignInAccount();
//                // Get account information
//                try {
//                    JSONObject params = new JSONObject();
//                    params.put("name", acct.getDisplayName());
//                    params.put("email", acct.getEmail());
//                    params.put("first_name", acct.getGivenName());
//                    params.put("last_name", acct.getFamilyName());
//                    params.put("gender", NOTPROVIDED);
//                    params.put("birthday", NOTPROVIDED);
//                    params.put("next_url","");
//                    params.put("source", "GOOGLE");
//
//                    new GetToken(new GetToken.AsyncResponse() {
//                        @Override
//                        public void processFinish(JSONObject output) throws JSONException {
//                            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.KITKAT) {
//                                webview.evaluateJavascript("token("+output+");", null);
//                            } else {
//                                webview.loadUrl("javascript:token("+output+");");
//                            }
//                        }
//                    }).execute(params);
//                } catch(JSONException e) {
//                    e.printStackTrace();
//                }
//            } else {
//                Toast.makeText(getApplicationContext(), "Try Again", Toast.LENGTH_LONG).show();
//                if(mGoogleApiClient !=null) {
//                    mGoogleApiClient.stopAutoManage(MainActivity.this);
//                    mGoogleApiClient.disconnect();
//                }
           // }
         else if (facebook == "success") {
            callbackManager.onActivityResult(requestCode, resultCode, intent);
        } else if (linkedin == "success"){
            LISessionManager.getInstance(getApplicationContext()).onActivityResult(this, requestCode, resultCode, intent);
        } else {
            callbackManager.onActivityResult(requestCode,resultCode,intent);
        }
    }
    public void linkededinApiHelper() {

        if (taskAComplete && taskBComplete) {
            try {
                JSONObject json = new JSONObject();
                json.put("email", emailAddress.toString());
                json.put("first_name", firstName.toString());
                json.put("last_name", lastName.toString());
                json.put("gender", NOTPROVIDED);
                json.put("birthday", NOTPROVIDED);
                json.put("source", "LINKEDIN");
                json.put("next_url", "");
                new GetToken(new GetToken.AsyncResponse() {
                    @Override
                    public void processFinish(JSONObject output) throws JSONException {
                        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.KITKAT) {
                            webview.evaluateJavascript("token(" + output+ ");", null);
                        } else {
                            webview.loadUrl("javascript:token(" + output + ");");
                        }
                    }
                }).execute(json);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }



        //commented code for future reference

//        LISessionManager sessionManager = LISessionManager.getInstance(getApplicationContext());
//        LISession session = sessionManager.getSession();
//        boolean accessTokenValid = session.isValid();
//
//        if (accessTokenValid) {
//            final String[] res = {""};
//            APIHelper apiHelper = APIHelper.getInstance(getApplicationContext());
//            apiHelper.getRequest(this,linkedinurl, new ApiListener() {
//                @Override
//                public void onApiSuccess(ApiResponse result) {
//                    try {
//                        res[0] = result.toString();
//                        Log.e("Response ", res[0]);
//                        JSONObject response = result.getResponseDataAsJson();
//                        try {
//                            JSONObject json = new JSONObject();
//                            json.put("email", response.get("emailAddress").toString());
//                            json.put("first_name", response.get("firstName").toString());
//                            json.put("last_name", response.get("lastName").toString());
//                            json.put("gender", NOTPROVIDED);
//                            json.put("birthday", NOTPROVIDED);
//                            json.put("source", "LINKEDIN");
//                            json.put("next_url","");
//                            new GetToken(new GetToken.AsyncResponse() {
//                                @Override
//                                public void processFinish(JSONObject output) throws JSONException {
//                                    if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.KITKAT) {
//                                        webview.evaluateJavascript("token("+output+");", null);
//                                    } else {
//                                        webview.loadUrl("javascript:token("+output+");");
//                                    }
//                                }
//                            }).execute(json);
//                        } catch (Exception e) {
//                            e.printStackTrace();
//                        }
//                    } catch (Exception e) {
//                        e.printStackTrace();
//                    }
//                }
//
//                @Override
//                public void onApiError(LIApiError error) {
//
//                }
//            });
//        }
    }




    @SuppressLint("WrongViewCast")

    @Override
    public void onCreate(Bundle savedInstanceState) {
        System.out.println("hii");
        webview = (WebView) findViewById(R.id.webview);
        super.onCreate(savedInstanceState);
        getInstalledApplications();
        try {

            PackageInfo info = getPackageManager().getPackageInfo(PACKAGE,PackageManager.GET_SIGNATURES);

            for (Signature signature : info.signatures) {

                MessageDigest md = MessageDigest.getInstance("SHA");
                md.update(signature.toByteArray());

                // for  later use
                System.out.println("hii_key");
                System.out.println(Base64.encodeToString(md.digest(), Base64.DEFAULT));
                Log.d("KeyHash:", Base64.encodeToString(md.digest(), Base64.DEFAULT));
            }
        } catch (PackageManager.NameNotFoundException e) {

        } catch (NoSuchAlgorithmException e) {

        }
        setContentView(R.layout.activity_main);
        ImageView imagebyCode = new ImageView(this);
        imagebyCode.setOnClickListener(null);
        imagebyCode.setImageResource(R.drawable.nointernet);
        Display display = getWindowManager().getDefaultDisplay();
        int width = display.getWidth();
        int height = display.getHeight();
        LinearLayout.LayoutParams params = new LinearLayout
                .LayoutParams(width, height);
        imagebyCode.setLayoutParams(params);
        myLayout = (LinearLayout) findViewById(R.id.trans);
        myLayout.addView(imagebyCode);
        myLayout.setVisibility(GONE);
        //Check Internet connection
        if (isNetworkAvailable()) {
            webview = (WebView) findViewById(R.id.webview);
            WebSettings settings = webview.getSettings();
            settings.setJavaScriptEnabled(true);
            settings.setJavaScriptCanOpenWindowsAutomatically(true);
            settings.setBuiltInZoomControls(true);
            settings.setDomStorageEnabled(true);
            settings.setSupportMultipleWindows(true);
            settings.setAllowFileAccess(true);
            if(Build.VERSION.SDK_INT >= 21){
                settings.setMixedContentMode(0);
                webview.setLayerType(View.LAYER_TYPE_HARDWARE, null);
            }else if(Build.VERSION.SDK_INT >= 19){
                webview.setLayerType(View.LAYER_TYPE_HARDWARE, null);
            }else {
                webview.setLayerType(View.LAYER_TYPE_SOFTWARE, null);
            }
            settings.setLoadsImagesAutomatically(true);
            settings.setAllowFileAccessFromFileURLs(true);
            settings.setAllowUniversalAccessFromFileURLs(true);
            webview.setWebChromeClient(new WebChromeClient() {


//                public void openFileChooser(ValueCallback<Uri> uploadMsg) {
//                    mUploadMessage = uploadMsg;
//                    Intent i = new Intent(Intent.ACTION_GET_CONTENT);
//                    i.addCategory(Intent.CATEGORY_OPENABLE);
//                    i.setType("*/*");
//                    MainActivity.this.startActivityForResult(Intent.createChooser(i, "File Chooser"), FILECHOOSER_RESULTCODE);
//                }


                @SuppressLint("ObsoleteSdkInt")
                @SuppressWarnings("unused")
                public void openFileChooser(ValueCallback<Uri> uploadMsg,String acceptType, String capture) {
                    mUM = uploadMsg;
                    Intent i = new Intent(Intent.ACTION_GET_CONTENT);
                    i.addCategory(Intent.CATEGORY_OPENABLE);
                    i.setType("*/*");
                    if (multiple_files && Build.VERSION.SDK_INT >= 18) {
                        i.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
                    }
                    startActivityForResult(Intent.createChooser(i, "File Chooser"), FCR);
                }




                //handling input[type="file"] requests for android API 21+
                @SuppressLint("InlinedApi")
                public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> filePathCallback, FileChooserParams fileChooserParams) {
                    if (file_permission()) {
                        String[] perms = {Manifest.permission.WRITE_EXTERNAL_STORAGE, Manifest.permission.READ_EXTERNAL_STORAGE, Manifest.permission.CAMERA};

                        //checking for storage permission to write images for upload
                        if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED && ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                            ActivityCompat.requestPermissions(MainActivity.this, perms, FCR);

                            //checking for WRITE_EXTERNAL_STORAGE permission
                        } else if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
                            ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE, Manifest.permission.READ_EXTERNAL_STORAGE}, FCR);

                            //checking for CAMERA permissions
                        } else if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                            ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.CAMERA}, FCR);
                        }
                        if (mUMA != null) {
                            mUMA.onReceiveValue(null);
                        }
                        mUMA = filePathCallback;
                        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                        if (takePictureIntent.resolveActivity(MainActivity.this.getPackageManager()) != null) {
                            File photoFile = null;
                            try {
                                photoFile = createImageFile();
                                takePictureIntent.putExtra("PhotoPath", mCM);
                            } catch (IOException ex) {
                                //Log.e(TAG, "Image file creation failed", ex);
                            }
                            if (photoFile != null) {
                                mCM = "file:" + photoFile.getAbsolutePath();
                                takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, Uri.fromFile(photoFile));
                            } else {
                                takePictureIntent = null;
                            }
                        }
                        Intent contentSelectionIntent = new Intent(Intent.ACTION_GET_CONTENT);
                        contentSelectionIntent.addCategory(Intent.CATEGORY_OPENABLE);
                        contentSelectionIntent.setType("image/*");
                        if (multiple_files) {
                            contentSelectionIntent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
                        }
                        Intent[] intentArray;
                        if (takePictureIntent != null) {
                            intentArray = new Intent[]{takePictureIntent};
                        } else {
                            intentArray = new Intent[0];
                        }

                        Intent chooserIntent = new Intent(Intent.ACTION_CHOOSER);
                        chooserIntent.putExtra(Intent.EXTRA_INTENT, contentSelectionIntent);
                        chooserIntent.putExtra(Intent.EXTRA_TITLE, "File Chooser");
                        chooserIntent.putExtra(Intent.EXTRA_INITIAL_INTENTS, intentArray);
                        startActivityForResult(chooserIntent, FCR);
                        return true;
                    }else{
                        return false;
                    }
                }

                // For Android 3.0+
                public void openFileChooser( final ValueCallback uploadMsg, String acceptType) {
                    if (acceptType.contains("image-camera/*")) {
                        final CharSequence[] items = { "Take Photo", "Choose from Library"};
                        AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
                        builder.setTitle("Add Photo");
                        builder.setCancelable(false);
                        builder.setItems(items, new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int item) {
                                if (items[item].equals("Take Photo")) {
                                    mUploadMessage = uploadMsg;
                                    Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                                    File externalDataDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DCIM);
                                    File cameraDataDir = new File(externalDataDir.getAbsolutePath() +
                                            File.separator + "browser-photos");
                                    cameraDataDir.mkdirs();
                                    String mCameraFilePath = cameraDataDir.getAbsolutePath() +
                                            File.separator + System.currentTimeMillis() + ".jpg";
                                    mCapturedImageURI = Uri.fromFile(new File(mCameraFilePath));
                                    cameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, mCapturedImageURI);
                                    Intent i = new Intent(Intent.ACTION_GET_CONTENT);
                                    i.addCategory(Intent.CATEGORY_OPENABLE);
                                    i.setType("image/*");
                                    Intent chooserIntent = Intent.createChooser(i, "Image Chooser");
                                    chooserIntent.putExtra(Intent.EXTRA_INITIAL_INTENTS, new Parcelable[]{cameraIntent});
                                    MainActivity.this.startActivityForResult(
                                            Intent.createChooser(cameraIntent, "File Chooser"),
                                            MainActivity.CAMERA_RESULTCODE
                                    );
                                }
                                else
                                {
                                    mUploadMessage = uploadMsg;
                                    Intent i = new Intent(Intent.ACTION_GET_CONTENT);
                                    i.addCategory(Intent.CATEGORY_OPENABLE);
                                    i.setType("image/*");
                                    MainActivity.this.startActivityForResult(
                                            Intent.createChooser(i, "File Chooser"),
                                            MainActivity.FILECHOOSER_RESULTCODE
                                    );
                                }
                            }
                        });
                        builder.show();
                    }

                    else if (acceptType.contains("image/*")) {
                        mUploadMessage = uploadMsg;
                        Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                        File externalDataDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DCIM);
                        File cameraDataDir = new File(externalDataDir.getAbsolutePath() + File.separator + "browser-photos");
                        cameraDataDir.mkdirs();
                        String mCameraFilePath = cameraDataDir.getAbsolutePath() +
                                File.separator + System.currentTimeMillis() + ".jpg";
                        mCapturedImageURI = Uri.fromFile(new File(mCameraFilePath));
                        cameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, mCapturedImageURI);
                        Intent i = new Intent(Intent.ACTION_GET_CONTENT);
                        i.addCategory(Intent.CATEGORY_OPENABLE);
                        i.setType("*/*");
                        Intent chooserIntent = Intent.createChooser(i, "Image Chooser");
                        chooserIntent.putExtra(Intent.EXTRA_INITIAL_INTENTS, new Parcelable[]{cameraIntent});

                        MainActivity.this.startActivityForResult(
                                Intent.createChooser(cameraIntent, "File Browser"),
                                CAMERA_RESULTCODE
                        );
                    } else {
                        mUploadMessage = uploadMsg;
                        Intent i = new Intent(Intent.ACTION_GET_CONTENT);
                        i.addCategory(Intent.CATEGORY_OPENABLE);
                        i.setType("*/*");
                        MainActivity.this.startActivityForResult(
                                Intent.createChooser(i, "File Browser"),
                                FILECHOOSER_RESULTCODE
                        );
                    }
                }



                //For Android 4.1
//                public void openFileChooser(final ValueCallback<Uri> uploadMsg, String acceptType, String capture) {
//
//                    if (acceptType.contains("image-camera/*")) {
//                        final CharSequence[] items = { "Take Photo", "Choose from Library"};
//                        AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
//                        builder.setTitle("Add Photo");
//                        builder.setCancelable(false);
//                        builder.setItems(items, new DialogInterface.OnClickListener() {
//                            @Override
//                            public void onClick(DialogInterface dialog, int item) {
//                                if (items[item].equals("Take Photo")) {
//                                    mUploadMessage = uploadMsg;
//                                    Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
//                                    File externalDataDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DCIM);
//                                    File cameraDataDir = new File(externalDataDir.getAbsolutePath() +
//                                            File.separator + "browser-photos");
//                                    cameraDataDir.mkdirs();
//                                    String mCameraFilePath = cameraDataDir.getAbsolutePath() +
//                                            File.separator + System.currentTimeMillis() + ".jpg";
//                                    mCapturedImageURI = Uri.fromFile(new File(mCameraFilePath));
//                                    cameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, mCapturedImageURI);
//                                    Intent i = new Intent(Intent.ACTION_GET_CONTENT);
//                                    i.addCategory(Intent.CATEGORY_OPENABLE);
//                                    i.setType("image/*");
//                                    Intent chooserIntent = Intent.createChooser(i, "Image Chooser");
//                                    chooserIntent.putExtra(Intent.EXTRA_INITIAL_INTENTS, new Parcelable[]{cameraIntent});
//                                    MainActivity.this.startActivityForResult(
//                                            Intent.createChooser(cameraIntent, "File Chooser"),
//                                            MainActivity.CAMERA_RESULTCODE
//                                    );
//                                }
//                                else
//                                {
//                                    mUploadMessage = uploadMsg;
//                                    Intent i = new Intent(Intent.ACTION_GET_CONTENT);
//                                    i.addCategory(Intent.CATEGORY_OPENABLE);
//                                    i.setType("image/*");
//                                    MainActivity.this.startActivityForResult(
//                                            Intent.createChooser(i, "File Chooser"),
//                                            MainActivity.FILECHOOSER_RESULTCODE
//                                    );
//                                }
//                            }
//                        });
//                        builder.show();
//                    }
//
//                    else if (acceptType.contains("image/*")) {
//                        mUploadMessage = uploadMsg;
//                        Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
//                        File externalDataDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DCIM);
//                        File cameraDataDir = new File(externalDataDir.getAbsolutePath() +
//                                File.separator + "browser-photos");
//                        cameraDataDir.mkdirs();
//                        String mCameraFilePath = cameraDataDir.getAbsolutePath() +
//                                File.separator + System.currentTimeMillis() + ".jpg";
//                        mCapturedImageURI = Uri.fromFile(new File(mCameraFilePath));
//
//                        cameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, mCapturedImageURI);
//                        Intent i = new Intent(Intent.ACTION_GET_CONTENT);
//                        i.addCategory(Intent.CATEGORY_OPENABLE);
//                        i.setType("image/*");
//                        Intent chooserIntent = Intent.createChooser(i, "Image Chooser");
//                        chooserIntent.putExtra(Intent.EXTRA_INITIAL_INTENTS, new Parcelable[]{cameraIntent});
//
//                        MainActivity.this.startActivityForResult(
//                                Intent.createChooser(cameraIntent, "File Chooser"),
//                                MainActivity.CAMERA_RESULTCODE
//                        );
//
//                    } else {
//                        mUploadMessage = uploadMsg;
//                        Intent i = new Intent(Intent.ACTION_GET_CONTENT);
//                        i.addCategory(Intent.CATEGORY_OPENABLE);
//                        i.setType("*/*");
//                        MainActivity.this.startActivityForResult(
//                                Intent.createChooser(i, "File Chooser"),
//                                MainActivity.FILECHOOSER_RESULTCODE
//                        );
//                    }
//                }
            });
            webview.setWebViewClient(new CustomWebViewClient());
            System.out.println("webview url");
            webview.loadUrl(base_url);

        } else {
            checkNetworkConnection();
        }

    }


    public boolean file_permission(){
        if(Build.VERSION.SDK_INT >=23 && (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED || ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED)) {
            ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE, Manifest.permission.CAMERA}, 1);
            return false;
        }else{
            return true;
        }
    }

    //creating new image file here
    private File createImageFile() throws IOException{
        @SuppressLint("SimpleDateFormat") String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String imageFileName = "img_"+timeStamp+"_";
        File storageDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES);
        return File.createTempFile(imageFileName,".jpg",storageDir);
    }

    public void otpretreival(String otpsms)
    {

        StringBuilder buf=new StringBuilder("javascript:otp('"+otpsms+"')");
        webview.loadUrl(buf.toString());
    }

    public void getInstalledApplications(){
        final PackageManager pm = getPackageManager();
        //get a list of installed apps.
        List<ApplicationInfo> packages = pm.getInstalledApplications(PackageManager.GET_META_DATA);

        for (ApplicationInfo packageInfo : packages) {
            if (packageInfo.packageName.startsWith("com.facebook") &&  !packageInfo.packageName.contentEquals("com.facebook.orca")) {
                base_url = base_url+(base_url.contains("socialapp")?",fbapp":"#/redirect/socialapp=fbapp");

            } else if (packageInfo.packageName.startsWith("com.linkedin")) {
                base_url = base_url+(base_url.contains("socialapp")?",linkedinapp":"#/redirect/socialapp=linkedinapp");
            }else{
                continue;
            }
        }
    }


    // Method to change the text status
    public void changeTextStatus(boolean isConnected) {
        // Change status according to boolean value
        if (isConnected) {
            myLayout.setVisibility(GONE);

        }
        else {
            myLayout.setVisibility(VISIBLE);

        }
    }


    public void linkdelnEmailDetails(){
        new GetRequestAsyncTask(new GetRequestAsyncTask.AsyncResponse() {
            @Override
            public void processFinish(JSONObject output) throws JSONException {
                JSONArray jsonArray = output.optJSONArray("elements");
                JSONObject jsonObject = jsonArray.getJSONObject(0);
                String name= jsonObject.optString("handle~").toString();
                JSONObject obj = new JSONObject(name);
                emailAddress=obj.getString("emailAddress");
                taskAComplete = true;
                linkededinApiHelper();
            }
        }).execute(url_linkdein_email);

    }

    public void linkdelnProfileDetails(){
        new GetRequestAsyncTask(new GetRequestAsyncTask.AsyncResponse() {
            @Override
            public void processFinish(JSONObject output) throws JSONException {

                JSONObject obj1 = new JSONObject(output.getString("firstName"));
                JSONObject obj1_firstname = new JSONObject(obj1.getString("localized"));
                firstName=obj1_firstname.getString("en_US");
                JSONObject obj2 = new JSONObject(output.getString("lastName"));
                JSONObject obj2_lastname = new JSONObject(obj2.getString("localized"));
                lastName=obj2_lastname.getString("en_US");
                taskBComplete = true;
                linkededinApiHelper();

            }
        }).execute(url_linkdein_details);

    }

    private static String getAuthorizationUrl(){
        return AUTHORIZATION_URL
                +QUESTION_MARK+RESPONSE_TYPE_PARAM+EQUALS+RESPONSE_TYPE_VALUE
                +AMPERSAND+CLIENT_ID_PARAM+EQUALS+API_KEY
                +AMPERSAND+STATE_PARAM+EQUALS+STATE
                +AMPERSAND+REDIRECT_URI_PARAM+EQUALS+REDIRECT_URI+AMPERSAND+SCOPE_PARAM+EQUALS+SCOPE;
    }
    /**
     * Method that generates the url for get the access token from the Service
     * @return Url
     */
    private static String getAccessTokenUrl(String authorizationToken){
        return ACCESS_TOKEN_URL
                +QUESTION_MARK
                +GRANT_TYPE_PARAM+EQUALS+GRANT_TYPE
                +AMPERSAND
                +RESPONSE_TYPE_VALUE+EQUALS+authorizationToken
                +AMPERSAND
                +CLIENT_ID_PARAM+EQUALS+API_KEY
                +AMPERSAND+SECRET_KEY_PARAM+EQUALS+SECRET_KEY+AMPERSAND
                +REDIRECT_URI_PARAM+EQUALS+base_url;
    }

    @Override
    protected void onPause() {
        super.onPause();
        MyApplication.activityPaused();// On Pause notify the Application
    }

    @Override
    protected void onResume() {
        super.onResume();
        MyApplication.activityResumed();// On Resume notify the Application
    }


    public void checkNetworkConnection(){
        AlertDialog.Builder builder =new AlertDialog.Builder(this);
        builder.setTitle("No internet Connection");
        builder.setMessage("Please turn on internet connection to continue");
        builder.setNegativeButton("close", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                finish();
            }
        });
        AlertDialog alertDialog = builder.create();
        alertDialog.setCancelable(false);
        alertDialog.show();
    }

    public boolean isNetworkAvailable() {
        ConnectivityManager connectivityManager = (ConnectivityManager) getApplicationContext().getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo activeNetworkInfo = connectivityManager.getActiveNetworkInfo();
        return activeNetworkInfo != null && activeNetworkInfo.isConnected();
    }

    @Override
    public void onBackPressed() {
        //no backbutton handling
//        return;

        // commented for future use , when we need backbutton functionality but as of now not needed
        if(webview != null) {
//            WebBackForwardList mWebBackForwardList = webview.copyBackForwardList();
//            if (mWebBackForwardList.getCurrentIndex() > 0) {
//                String historyUrl = mWebBackForwardList.getItemAtIndex(mWebBackForwardList.getCurrentIndex() - 1).getUrl();
//                String currentUrl = mWebBackForwardList.getItemAtIndex(mWebBackForwardList.getCurrentIndex()).getUrl();
//                if (historyUrl.startsWith(base_url + "#/login") && !currentUrl.startsWith(base_url + "#/forgot_password")) {
            new AlertDialog.Builder(this)
                    .setIcon(android.R.drawable.ic_dialog_alert)
                    .setTitle("Exit!")
                    .setMessage("Are you sure you want to close?")
                    .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            finish();
                        }

                    })
                    .setNegativeButton("No", null)
                    .show();
        }
//                  else if (webview.canGoBack()) {
//                    webview.goBack();
//                } else {
//                    new AlertDialog.Builder(this)
//                            .setIcon(android.R.drawable.ic_dialog_alert)
//                            .setTitle("Exit!")
//                            .setMessage("Are you sure you want to close?")
//                            .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
//                                @Override
//                                public void onClick(DialogInterface dialog, int which) {
//                                    finish();
//                                }
//
//                            })
//                            .setNegativeButton("No", null)
//                            .show();
//                }
//            } else {
//                new AlertDialog.Builder(this)
//                        .setIcon(android.R.drawable.ic_dialog_alert)
//                        .setTitle("Exit!")
//                        .setMessage("Are you sure you want to close?")
//                        .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
//                            @Override
//                            public void onClick(DialogInterface dialog, int which) {
//                                finish();
//                            }
//
//                        })
//                        .setNegativeButton("No", null)
//                        .show();
//            }
//        }
//        else{
//            finish();
//        }
    }

//    @Override
//    public void onConnectionFailed(@NonNull ConnectionResult connectionResult) {
//
//    }

    public class CustomWebViewClient extends WebViewClient {
        public void onPageFinished(WebView view,String url){
            super.onPageFinished(view, url);
            findViewById(R.id.splashscreen).setVisibility(GONE);
            findViewById(R.id.webview).setVisibility(VISIBLE);
            ConnectivityManager cm =
                    (ConnectivityManager)getSystemService(Context.CONNECTIVITY_SERVICE);

            NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
            boolean isConnected = activeNetwork != null && activeNetwork.isConnected();
            if(isConnected) {
                // if network present do nothing
            } else {
                checkNetworkConnection();
            }
        }

        @SuppressWarnings("deprecation")
        @Override
        public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
            AlertDialog.Builder builder =new AlertDialog.Builder(MainActivity.this);
            builder.setTitle("Please check your network connection");
            builder.setMessage("Try again later");
            builder.setNegativeButton("Try Again", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    dialog.cancel();
                }
            });
            AlertDialog alertDialog = builder.create();
            alertDialog.setCancelable(false);
            //alertDialog.show();
        }

        @TargetApi(android.os.Build.VERSION_CODES.M)
        @Override
        public void onReceivedError(WebView view, WebResourceRequest req, WebResourceError rerr) {
            ConnectivityManager cm =
                    (ConnectivityManager)getSystemService(Context.CONNECTIVITY_SERVICE);

            NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
            boolean isConnected = activeNetwork != null && activeNetwork.isConnected();
            if(isConnected) {
                AlertDialog.Builder builder =new AlertDialog.Builder(MainActivity.this);
                builder.setTitle("Please check your network connection");
                builder.setMessage("Try again later");
                builder.setNegativeButton("Try again", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.cancel();
                    }
                });
                AlertDialog alertDialog = builder.create();
                alertDialog.setCancelable(false);
               // alertDialog.show();
            }
        }


        public void checkNetworkConnection(){
            webview.setVisibility(View.GONE);
            AlertDialog.Builder builder =new AlertDialog.Builder(MainActivity.this);
            builder.setTitle("No internet Connection");
            builder.setMessage("Please turn on internet connection to continue");
            builder.setNegativeButton("Exit", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    finish();
                }
            });
            AlertDialog alertDialog = builder.create();
            alertDialog.setCancelable(false);
            alertDialog.show();
        }

        @Override
        public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
            return super.shouldInterceptRequest(view, request);
        }

        private Scope buildScope() {
            return Scope.build(Scope.R_BASICPROFILE, Scope.W_SHARE,Scope.R_EMAILADDRESS);
        }



        @SuppressWarnings("deprecation")
        @Override
        public boolean shouldOverrideUrlLoading(WebView view, String url) {
             //redirect url will start from here
            System.out.println("weview url");
            System.out.println(url);
            if(url.startsWith(REDIRECT_URI)) {
                Uri uri = Uri.parse(url);
                //We take from the url the authorizationToken and the state token. We have to check that the state token returned by the Service is the same we sent.
                //If not, that means the request may be a result of CSRF and must be rejected.
                String stateToken = uri.getQueryParameter(STATE_PARAM);
                //If the user doesn't allow authorization to our application, the authorizationToken Will be null.
                String authorizationToken = uri.getQueryParameter(RESPONSE_TYPE_VALUE);
                if (authorizationToken != null) {
                    //Generate URL for requesting Access Token
                    String accessTokenUrl = getAccessTokenUrl(authorizationToken);
                    //We make the request in a AsyncTask
                    new PostRequestAsyncTask(new PostRequestAsyncTask.AsyncResponse() {
                        @Override
                        public void processFinish(JSONObject output) throws JSONException {
                            acesstoken = "";
                            acesstoken = output.has("access_token") ? output.getString("access_token") : null;

                        }
                    }).execute(accessTokenUrl);
                    new Thread(new Runnable() {
                        @Override
                        public void run() {
                            linkdelnProfileDetails();
                        }
                    }).start();
                    new Thread(new Runnable() {
                        @Override
                        public void run() {
                            linkdelnEmailDetails();
                        }
                    }).start();


                }
                else{
                    Toast.makeText(MainActivity.this, "Please try again later problem in linkdeln", Toast.LENGTH_LONG).show();
                }
            }



            if(url.startsWith("downloadpdf://")){
                String filename = url.split("://")[1].split(",")[0];
                String file = url.split(",")[2];
                File dwldsPath = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS) + "/"+filename);
                byte[] pdfAsBytes = Base64.decode(file, 0);
                FileOutputStream os = null;
                try {
                    os = new FileOutputStream(dwldsPath, false);
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                }
                try {
                    os.write(pdfAsBytes);
                    os.flush();
                    os.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }

                Toast.makeText(getApplicationContext(), "Downloading File",Toast.LENGTH_LONG).show();

                File openfile = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS) + "/"+filename);
                Intent intent = new Intent(Intent.ACTION_VIEW);
                intent.setDataAndType(Uri.fromFile(openfile), "application/pdf");
                startActivity(intent);

            }

            else if(url.startsWith("socialsignupurl://facebook")) {
                ConnectivityManager cm =
                        (ConnectivityManager)getSystemService(Context.CONNECTIVITY_SERVICE);

                NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
                boolean isConnected = activeNetwork != null &&
                        activeNetwork.isConnected();
                if(isConnected) {
                    facebook = "success";
                    facebookSignIn();
                }
                else{
                    Toast.makeText(MainActivity.this, "No Internet Connection", Toast.LENGTH_LONG).show();

                }
            }

//            else if (url.startsWith("socialsignupurl://google/")){
//                ConnectivityManager cm =
//                        (ConnectivityManager)getSystemService(Context.CONNECTIVITY_SERVICE);
//
//                NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
//                boolean isConnected = activeNetwork != null &&
//                        activeNetwork.isConnected();
//                if(isConnected) {
//                    gso = new GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
//                            .requestEmail()
//                            .build();
//                    if (mGoogleApiClient == null || !mGoogleApiClient.isConnected()) {
//                        try {
//                            mGoogleApiClient = new GoogleApiClient.Builder(MainActivity.this)
//                                    .enableAutoManage(MainActivity.this, MainActivity.this/* OnConnectionFailedListener */)
//                                    .addApi(Auth.GOOGLE_SIGN_IN_API, gso)
//                                    .build();
//                        } catch (Exception e) {
//                            e.printStackTrace();
//                        }
//                    }
//                    Intent signInIntent = Auth.GoogleSignInApi.getSignInIntent(mGoogleApiClient);
//                    startActivityForResult(signInIntent, RC_SIGN_IN);
//
//                }
//                else
//                {
//                    Toast.makeText(MainActivity.this, "No Internet Connection", Toast.LENGTH_LONG).show();
//                }
//            }


            else if (url.startsWith("socialsignupurl://linkedin/")) {
                ConnectivityManager cm =
                        (ConnectivityManager)getSystemService(Context.CONNECTIVITY_SERVICE);

                NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
                boolean isConnected = activeNetwork != null &&
                        activeNetwork.isConnected();
                if(isConnected) {
                    linkedin = "success";

                    //Get the authorization Url
                    String authUrl = getAuthorizationUrl();
                    Log.i("Authorize","Loading Auth Url: "+authUrl);
                    //Load the authorization URL into the webView
                    webview.loadUrl(authUrl);
                    //commented code for future reference
//                    LISessionManager.getInstance(getApplicationContext()).init(MainActivity.this, buildScope(), new AuthListener() {
//
//                        @Override
//                        public void onAuthSuccess() {
//                            linkededinApiHelper();
//                        }
//
//                        @Override
//                        public void onAuthError(LIAuthError error) {
//
//                            Toast.makeText(getApplicationContext(), "Try Again", Toast.LENGTH_LONG).show();
//                        }
//                    }, true);
                }
                else{
                    Toast.makeText(MainActivity.this, "No Internet Connection", Toast.LENGTH_LONG).show();
                }
            }

            else if(url.startsWith("socialshareurl://")) {
                url = url.replaceAll("socialshareurl://", "");


                if (url.startsWith("whatsapp://")) {
                    Uri uri = Uri.parse(url);
                    String msg = uri.getQueryParameter("text");
                    Intent sendIntent = new Intent();
                    sendIntent.setAction(Intent.ACTION_SEND);
                    sendIntent.putExtra(Intent.EXTRA_TEXT, msg);
                    sendIntent.setType("text/plain");
                    boolean whatsappfound = false;
                    List<ResolveInfo> matches2 = getPackageManager()
                            .queryIntentActivities(sendIntent, 0);

                    for (ResolveInfo info : matches2) {
                        if (info.activityInfo.packageName.toLowerCase().startsWith(
                                "com.whatsapp")) {
                            sendIntent.setPackage(info.activityInfo.packageName);
                            whatsappfound = true;
                            break;
                        }
                    }

                    if (whatsappfound) {
                        startActivity(sendIntent);
                    } else {
                        Toast.makeText(MainActivity.this, "Whatsapp app is not installed in your mobile", Toast.LENGTH_LONG).show();
                    }
                    return true;
                }


                if (url.startsWith("facebook://")) {
                    Uri uri = Uri.parse(url);
                    String msg = uri.getQueryParameter("text");
                    Intent sendIntent = new Intent();
                    sendIntent.setAction(Intent.ACTION_SEND);
                    sendIntent.putExtra(Intent.EXTRA_TEXT, msg);
                    sendIntent.setType("text/plain");
                    boolean facebook = false;
                    List<ResolveInfo> matches2 = getPackageManager()
                            .queryIntentActivities(sendIntent, 0);

                    for (ResolveInfo info : matches2) {
                        if (info.activityInfo.name.toLowerCase().contains(
                                "facebook")) {
                            sendIntent.setPackage(info.activityInfo.packageName);
                            facebook = true;
                            break;
                        }
                    }

                    if (facebook)
                    {
                        startActivity(sendIntent);
                    } else {
                        Toast.makeText(MainActivity.this, "Facebook app is not installed in your mobile", Toast.LENGTH_LONG).show();
                    }
                    return true;
                }

                if (url.startsWith("googleplus://")) {
//                    Uri uri = Uri.parse(url);
//                    String msg = uri.getQueryParameter("text");
//                    Intent sendIntent = new Intent();
//                    sendIntent.setAction(Intent.ACTION_SEND);
//                    sendIntent.putExtra(Intent.EXTRA_TEXT, msg);
//                    sendIntent.setType("text/plain");
//                    boolean googleplusfound = false;
//                    List<ResolveInfo> matches2 = getPackageManager()
//                            .queryIntentActivities(sendIntent, 0);
//
//                    for (ResolveInfo info : matches2) {
//                        if (info.activityInfo.packageName.toLowerCase().startsWith(
//                                "com.google.android.apps.plus")) {
//                            sendIntent.setPackage(info.activityInfo.packageName);
//                            googleplusfound = true;
//                            break;
//                        }
//                    }
//
//                    if (googleplusfound) {
//                        startActivity(sendIntent);
//                    } else {
//                        Toast.makeText(MainActivity.this, "Google+ app is not installed in your mobile", Toast.LENGTH_LONG).show();
//                    }
                    return true;
                }

                if (url.startsWith("linkedin://")) {
                    Uri uri = Uri.parse(url);
                    String msg = uri.getQueryParameter("text");
                    Intent sendIntent = new Intent();
                    sendIntent.setAction(Intent.ACTION_SEND);
                    sendIntent.putExtra(Intent.EXTRA_TEXT, msg);
                    sendIntent.setType("text/plain");
                    boolean linkedinAppFound = false;
                    List<ResolveInfo> matches2 = getPackageManager()
                            .queryIntentActivities(sendIntent, 0);

                    for (ResolveInfo info : matches2) {
                        if (info.activityInfo.packageName.toLowerCase().startsWith(
                                "com.linkedin")) {
                            sendIntent.setPackage(info.activityInfo.packageName);
                            linkedinAppFound = true;
                            break;
                        }
                    }

                    if (linkedinAppFound) {
                        startActivity(sendIntent);
                    } else {
                        Toast.makeText(MainActivity.this, "LinkedIn app is not installed in your mobile", Toast.LENGTH_LONG).show();
                    }
                    return true;
                }

                if (url.startsWith("twitter://")) {
                    Uri uri = Uri.parse(url);
                    String msg = uri.getQueryParameter("text");
                    Intent sendIntent = new Intent();
                    sendIntent.setAction(Intent.ACTION_SEND);
                    sendIntent.putExtra(Intent.EXTRA_TEXT, msg);
                    sendIntent.setType("text/plain");
                    boolean twitterAppFound = false;
                    List<ResolveInfo> matches2 = getPackageManager()
                            .queryIntentActivities(sendIntent, 0);

                    for (ResolveInfo info : matches2) {
                        if (info.activityInfo.packageName.toLowerCase().startsWith(
                                "com.twitter")) {
                            sendIntent.setPackage(info.activityInfo.packageName);
                            twitterAppFound = true;
                            break;
                        }
                    }

                    if (twitterAppFound) {
                        startActivity(sendIntent);
                    } else {
                        Toast.makeText(MainActivity.this, "Twitter app is not installed in your mobile", Toast.LENGTH_LONG).show();
                    }
                    return true;

                }
            }
            else if (url.startsWith("nativeurl://logout")) {

                getInstalledApplications();
//                if (mGoogleApiClient != null)
//                {
//                    mGoogleApiClient.stopAutoManage(MainActivity.this);
//                    mGoogleApiClient.disconnect();
//                }
                webview.loadUrl(base_url);

            }

            else {
                webview.loadUrl(url);
            }
            return true;
        }
//        @Override
//        public void onReceivedSslError(WebView view, SslErrorHandler handler, SslError error) {
//            handler.proceed(); // Ignore SSL certificate errors
//        }
        @TargetApi(25)
        public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request){

            String url =request.getUrl().toString();


            //This method will be called when the Auth proccess redirect to our RedirectUri.
            //We will check the url looking for our RedirectUri.
            if(url.startsWith(REDIRECT_URI)) {

                Uri uri = Uri.parse(url);
                //We take from the url the authorizationToken and the state token. We have to check that the state token returned by the Service is the same we sent.
                //If not, that means the request may be a result of CSRF and must be rejected.
                String stateToken = uri.getQueryParameter(STATE_PARAM);
                //If the user doesn't allow authorization to our application, the authorizationToken Will be null.
                String authorizationToken = uri.getQueryParameter(RESPONSE_TYPE_VALUE);
                if (authorizationToken != null) {
                    //Generate URL for requesting Access Token
                    String accessTokenUrl = getAccessTokenUrl(authorizationToken);
                    //We make the request in a AsyncTask
                    new PostRequestAsyncTask(new PostRequestAsyncTask.AsyncResponse() {
                        @Override
                        public void processFinish(JSONObject output) throws JSONException {
                            acesstoken = "";
                            acesstoken = output.has("access_token") ? output.getString("access_token") : null;

                        }
                    }).execute(accessTokenUrl);

                    new Thread(new Runnable() {
                        @Override
                        public void run() {
                            linkdelnProfileDetails();
                        }
                    }).start();
                    new Thread(new Runnable() {
                        @Override
                        public void run() {
                            linkdelnEmailDetails();
                        }
                    }).start();

                }
                else{
                    Toast.makeText(MainActivity.this, "Please try again later problem in linkdeln", Toast.LENGTH_LONG).show();
                }
            }


            if(url.startsWith("downloadpdf://")){
                String filename = url.split("://")[1].split(",")[0];
                String file = url.split(",")[2];
                File dwldsPath = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS) + "/"+filename);
                byte[] pdfAsBytes = Base64.decode(file, 0);
                FileOutputStream os = null;

                try {
                    os = new FileOutputStream(dwldsPath, false);
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                }

                try {
                    os.write(pdfAsBytes);
                    os.flush();
                    os.close();

                } catch (IOException e) {
                    e.printStackTrace();
                }

                Toast.makeText(getApplicationContext(), "Downloading File",Toast.LENGTH_LONG).show();
                File openfile = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS) + "/"+filename);
                Intent intent = new Intent(Intent.ACTION_VIEW);
                intent.setDataAndType(Uri.fromFile(openfile), "application/pdf");
                startActivity(intent);
            } else if (url.startsWith("socialsignupurl://facebook")) {
                ConnectivityManager cm =
                        (ConnectivityManager)getSystemService(Context.CONNECTIVITY_SERVICE);

                NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
                boolean isConnected = activeNetwork != null && activeNetwork.isConnected();
                if(isConnected) {
                    facebookSignIn();
                } else {
                    Toast.makeText(MainActivity.this, "No Internet Connection", Toast.LENGTH_LONG).show();
                }
//            } else if (url.startsWith("socialsignupurl://google/")){
//                ConnectivityManager cm =
//                        (ConnectivityManager)getSystemService(Context.CONNECTIVITY_SERVICE);
//
//                NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
//                boolean isConnected = activeNetwork != null && activeNetwork.isConnected();
//                if(isConnected) {
//                    gso = new GoogleSignInOptions
//                            .Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
//                            .requestEmail()
//                            .build();
//                    mGoogleApiClient = new GoogleApiClient
//                            .Builder(MainActivity.this)
//                            .enableAutoManage(MainActivity.this, MainActivity.this/* OnConnectionFailedListener */)
//                            .addApi(Auth.GOOGLE_SIGN_IN_API, gso)
//                            .build();
//                    Intent signInIntent = Auth.GoogleSignInApi.getSignInIntent(mGoogleApiClient);
//                    startActivityForResult(signInIntent, RC_SIGN_IN);
//                } else {
//                    Toast.makeText(MainActivity.this, "No Internet Connection", Toast.LENGTH_LONG).show();
//                }
            }
               else if (url.startsWith("socialsignupurl://linkedin/")) {
                ConnectivityManager cm =
                        (ConnectivityManager)getSystemService(Context.CONNECTIVITY_SERVICE);

                NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
                boolean isConnected = activeNetwork != null && activeNetwork.isConnected();
                if(isConnected) {
                    linkedin = "success";
                    //Get the authorization Url
                    String authUrl = getAuthorizationUrl();
                    Log.i("Authorize","Loading Auth Url: "+authUrl);
                    //Load the authorization URL into the webView
                    webview.loadUrl(authUrl);


//                    LISessionManager.getInstance(getApplicationContext()).init(MainActivity.this, buildScope(), new AuthListener() {
//                        @Override
//                        public void onAuthSuccess() {
//                            linkededinApiHelper();
//                        }
//
//                        @Override
//                        public void onAuthError(LIAuthError error) {
//                            Toast.makeText(getApplicationContext(), "Try Again", Toast.LENGTH_LONG).show();
//                        }
//                    }, true);
                } else {
                    Toast.makeText(MainActivity.this, "No Internet Connection", Toast.LENGTH_LONG).show();
                }
            } else if (url.contains("socialshareurl://")) {
                url = url.replaceAll("socialshareurl://", "");
                if (url.startsWith("whatsapp://")) {
                    Uri uri = Uri.parse(url);
                    String msg = uri.getQueryParameter("text");
                    Intent sendIntent = new Intent();
                    sendIntent.setAction(Intent.ACTION_SEND);
                    sendIntent.putExtra(Intent.EXTRA_TEXT, msg);
                    sendIntent.setType("text/plain");
                    boolean whatsappfound = false;
                    List<ResolveInfo> matches2 = getPackageManager().queryIntentActivities(sendIntent, 0);
                    for (ResolveInfo info : matches2) {
                        if (info.activityInfo.packageName.toLowerCase().startsWith("com.whatsapp")) {
                            sendIntent.setPackage(info.activityInfo.packageName);
                            whatsappfound = true;
                            break;
                        }
                    }

                    if (whatsappfound) {
                        startActivity(sendIntent);
                    } else {
                        Toast.makeText(MainActivity.this, "Whatsapp app is not installed in your mobile", Toast.LENGTH_LONG).show();
                    }
                    return true;
                }

                if (url.startsWith("facebook://")) {
                    Uri uri = Uri.parse(url);
                    String msg = uri.getQueryParameter("text");
                    Intent sendIntent = new Intent();
                    sendIntent.setAction(Intent.ACTION_SEND);
                    sendIntent.putExtra(Intent.EXTRA_TEXT, msg);
                    sendIntent.setType("text/plain");
                    boolean facebook = false;
                    List<ResolveInfo> matches2 = getPackageManager().queryIntentActivities(sendIntent, 0);
                    for (ResolveInfo info : matches2) {
                        if (info.activityInfo.name.toLowerCase().contains("facebook")) {
                            sendIntent.setPackage(info.activityInfo.packageName);
                            facebook = true;
                            break;
                        }
                    }

                    if (facebook) {
                        startActivity(sendIntent);
                    } else {
                        Toast.makeText(MainActivity.this, "Facebook app is not installed in your mobile", Toast.LENGTH_LONG).show();
                    }
                    return true;
                }

                if (url.startsWith("googleplus://")) {
//                    Uri uri = Uri.parse(url);
//                    String msg = uri.getQueryParameter("text");
//                    Intent sendIntent = new Intent();
//                    sendIntent.setAction(Intent.ACTION_SEND);
//                    sendIntent.putExtra(Intent.EXTRA_TEXT, msg);
//                    sendIntent.setType("text/plain");
//                    boolean googleplusfound = false;
//                    List<ResolveInfo> matches2 = getPackageManager().queryIntentActivities(sendIntent, 0);
//
//                    for (ResolveInfo info : matches2) {
//                        if (info.activityInfo.packageName.toLowerCase().startsWith("com.google.android.apps.plus")) {
//                            sendIntent.setPackage(info.activityInfo.packageName);
//                            googleplusfound = true;
//                            break;
//                        }
//                    }
//
//                    if (googleplusfound) {
//                        startActivity(sendIntent);
//                    } else {
//                        Toast.makeText(MainActivity.this, "Google+ app is not installed in your mobile", Toast.LENGTH_LONG).show();
//                    }
//                    return true;
                }

                if (url.startsWith("linkedin://")) {
                    Uri uri = Uri.parse(url);
                    String msg = uri.getQueryParameter("text");
                    Intent sendIntent = new Intent();
                    sendIntent.setAction(Intent.ACTION_SEND);
                    sendIntent.putExtra(Intent.EXTRA_TEXT, msg);
                    sendIntent.setType("text/plain");
                    boolean linkedinAppFound = false;
                    List<ResolveInfo> matches2 = getPackageManager().queryIntentActivities(sendIntent, 0);

                    for (ResolveInfo info : matches2) {
                        if (info.activityInfo.packageName.toLowerCase().startsWith("com.linkedin")) {
                            sendIntent.setPackage(info.activityInfo.packageName);
                            linkedinAppFound = true;
                            break;
                        }
                    }

                    if (linkedinAppFound) {
                        startActivity(sendIntent);
                    } else {
                        Toast.makeText(MainActivity.this, "LinkedIn app is not installed in your mobile", Toast.LENGTH_LONG).show();
                    }
                    return true;
                }

                if (url.startsWith("twitter://")) {
                    Uri uri = Uri.parse(url);
                    String msg = uri.getQueryParameter("text");
                    Intent sendIntent = new Intent();
                    sendIntent.setAction(Intent.ACTION_SEND);
                    sendIntent.putExtra(Intent.EXTRA_TEXT, msg);
                    sendIntent.setType("text/plain");
                    boolean twitterAppFound = false;
                    List<ResolveInfo> matches2 = getPackageManager().queryIntentActivities(sendIntent, 0);

                    for (ResolveInfo info : matches2) {
                        if (info.activityInfo.packageName.toLowerCase().startsWith("com.twitter")) {
                            sendIntent.setPackage(info.activityInfo.packageName);
                            twitterAppFound = true;
                            break;
                        }
                    }

                    if (twitterAppFound) {
                        startActivity(sendIntent);
                    } else {
                        Toast.makeText(MainActivity.this, "Twitter app is not installed in your mobile", Toast.LENGTH_LONG).show();
                    }
                    return true;
                }

            } else if (url.startsWith("nativeurl://logout")) {
                getInstalledApplications();
//                if (mGoogleApiClient != null) {
//                    mGoogleApiClient.stopAutoManage(MainActivity.this);
//                    mGoogleApiClient.disconnect();
//                }
                webview.loadUrl(base_url);
            } else {
                webview.loadUrl(url);
            }
            return true;
        }
    }

    public void facebookSignIn(){
        System.out.println("hiii_samo2");
        FacebookSdk.sdkInitialize(getApplicationContext());
        FacebookSdk.setApplicationId(this.getString(R.string.facebook_app_id));
        callbackManager = CallbackManager.Factory.create();

        // Commented for Now need to get approval from facebook
        // LoginManager.getInstance().logInWithReadPermissions(MainActivity.this, Arrays.asList("public_profile", "user_friends","email", "user_birthday"));
        LoginManager.getInstance().logInWithReadPermissions(MainActivity.this, Arrays.asList("email"));
        LoginManager.getInstance().registerCallback(callbackManager, new FacebookCallback<LoginResult>() {
            @Override
            public void onSuccess(LoginResult loginResult) {
                //if you want to do not use this
                System.out.println("hiii_samo");
                Toast.makeText(MainActivity.this, "Success", Toast.LENGTH_LONG).show();
                AccessToken accessToken = loginResult.getAccessToken();
                Profile profile = Profile.getCurrentProfile();
                GraphRequest request = GraphRequest.newMeRequest(loginResult.getAccessToken(),
                        new GraphRequest.GraphJSONObjectCallback() {
                            @Override
                            public void onCompleted(JSONObject object, GraphResponse response) {
                                Log.v("LoginActivity Response ", object.toString());
                                try {
                                    JSONObject json = new JSONObject();
                                    json.put("name",object.getString(("name")));
                                    json.put("email",object.getString(("email")));
                                    json.put("first_name",object.getString(("first_name")));
                                    json.put("last_name",object.getString(("last_name")));
                                    json.put("gender","");
                                    // user_birthday permission need to get from facebook
                                    //json.put("birthday",object.getString(("birthday")));
                                    json.put("birthday", NOTPROVIDED);
                                    json.put("source","facebook");
                                    json.put("next_url","");
                                     System.out.println("json");
                                    System.out.println(json);


                                    new GetToken(new GetToken.AsyncResponse() {
                                        @Override
                                        public void processFinish(JSONObject output) throws JSONException {

                                            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.KITKAT) {
                                                webview.evaluateJavascript("token("+output+");", null);
                                            } else {
                                                webview.loadUrl("javascript:token("+output+");");
                                            }
                                        }
                                    }).execute(json);
                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }
                            }

                        });
                Bundle parameters = new Bundle();
                parameters.putString("fields", "id,first_name,last_name,name,email,gender,birthday");
                request.setParameters(parameters);
                request.executeAsync();
            }

            @Override
            public void onCancel() {

            }

            @Override
            public void onError(FacebookException error) {

            }

        });
    }





    private static class PostRequestAsyncTask extends AsyncTask<String, Void, JSONObject> {

        public interface AsyncResponse {
            void processFinish(JSONObject output) throws JSONException;
        }

        public AsyncResponse delegate = null;

        public PostRequestAsyncTask(AsyncResponse delegate){
            this.delegate = delegate;
        }

        @Override
        protected JSONObject doInBackground(String... urls) {
            String url = urls[0];
            String token = null;
            JSONObject jsonobject = null;
            URL urlToRequest = null;
            try {
                urlToRequest = new URL(url);
                HttpURLConnection urlConnection = (HttpURLConnection) urlToRequest.openConnection();
                urlConnection.setDoOutput(true);
                urlConnection.setRequestMethod("POST");
                urlConnection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
                OutputStream os = urlConnection.getOutputStream();
                os.close();
                int responseCode=urlConnection.getResponseCode();
                if (responseCode == HttpURLConnection.HTTP_OK) {
                    BufferedReader in=new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
                    StringBuffer sb = new StringBuffer("");
                    String line="";
                    while((line = in.readLine()) != null) {
                        sb.append(line);
                        break;
                    }
                    in.close();
                    token = sb.toString();
                } else {
                    JSONObject err = new JSONObject();
                    err.put("false",responseCode);
                }
            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch(IOException e){
                e.printStackTrace();
            } catch(Exception e){
                e.printStackTrace();
            }

            try {
                jsonobject = new JSONObject(token);
            } catch (JSONException e) {
                e.printStackTrace();
            }

            return jsonobject;
        }

        @Override
        protected void onPostExecute(JSONObject result) {
            try {
                delegate.processFinish(result);
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }

    }



    private static class GetRequestAsyncTask extends AsyncTask<String, Void, JSONObject> {

        public interface AsyncResponse {
            void processFinish(JSONObject output) throws JSONException;
        }

        public AsyncResponse delegate = null;

        public GetRequestAsyncTask(AsyncResponse delegate){
            this.delegate = delegate;
        }

        @Override
        protected JSONObject doInBackground(String... urls) {
            String url = urls[0];
            String token = null;
            JSONObject jsonobject = null;
            URL urlToRequest = null;
            try {

                URL obj = new URL(url);
                HttpURLConnection con = (HttpURLConnection) obj.openConnection();
                con.setRequestMethod("GET");
                //add request header
                con.setRequestProperty("Authorization", "Bearer " + acesstoken);
                int responseCode = con.getResponseCode();
                if (responseCode == HttpURLConnection.HTTP_OK) {
                    BufferedReader in = new BufferedReader(
                            new InputStreamReader(con.getInputStream()));
                    String inputLine;
                    StringBuffer response = new StringBuffer();
                    while ((inputLine = in.readLine()) != null) {
                        response.append(inputLine);
                    }
                    in.close();

                    token = response.toString();
                }else{
                    JSONObject err_info = new JSONObject();
                    err_info.put("false",responseCode);
                }

            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch(IOException e){
                e.printStackTrace();
            } catch(Exception e){
                e.printStackTrace();
            }

            try {
                jsonobject = new JSONObject(token);
            } catch (JSONException e) {
                e.printStackTrace();
            }

            return jsonobject;
        }

        @Override
        protected void onPostExecute(JSONObject result) {
            try {
                delegate.processFinish(result);
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }




    private static class GetToken extends AsyncTask<JSONObject, Void, JSONObject> {

        public interface AsyncResponse {
            void processFinish(JSONObject output) throws JSONException;
        }

        public AsyncResponse delegate = null;

        public GetToken(AsyncResponse delegate){
            this.delegate = delegate;
        }

        @Override
        protected JSONObject doInBackground(JSONObject... json) {
            String token = null;
            JSONObject jsonobject = null;
            //URL urlToRequest = null;
            try {

                //URL obj = new URL(url);
                //                HttpURLConnection con = (HttpURLConnection) obj.openConnection();
                //                con.setRequestMethod("GET");
                //                //add request header
                //                con.setRequestProperty("Authorization", "Bearer " + acesstoken);
                //                int responseCode = con.getResponseCode();

                URL urlToRequest_server = new URL(signup_api);
                HttpURLConnection urlConnection_server = (HttpURLConnection) urlToRequest_server.openConnection();
                //urlConnection_server.setDoOutput(true);
                urlConnection_server.setRequestMethod("POST");
                urlConnection_server.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
                OutputStream os = urlConnection_server.getOutputStream();
                BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(os, "UTF-8"));
                writer.write(getPostDataString(json[0]));
                writer.flush();
                writer.close();
                os.close();
                int responseCode=urlConnection_server.getResponseCode();

                if (responseCode == HttpURLConnection.HTTP_OK) {
                    BufferedReader in=new BufferedReader(new InputStreamReader(urlConnection_server.getInputStream()));
                    StringBuffer sb = new StringBuffer("");
                    String line="";
                    while((line = in.readLine()) != null) {
                        sb.append(line);
                        break;
                    }
                    in.close();
                    token = sb.toString();
                } else {
                    JSONObject err = new JSONObject();
                    err.put("false",responseCode);
                }
            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch(IOException e){
                e.printStackTrace();
            } catch(Exception e){
                e.printStackTrace();
            }

            try {
                jsonobject = new JSONObject(token);
            } catch (JSONException e) {
                e.printStackTrace();
            }

            return jsonobject;
        }

        @Override
        protected void onPostExecute(JSONObject result) {
            try {
                delegate.processFinish(result);
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }

    public static String getPostDataString(JSONObject params) throws Exception {

        StringBuilder result = new StringBuilder();
        boolean first = true;
        Iterator<String> itr = params.keys();
        while(itr.hasNext()){
            String key= itr.next();
            Object value = params.get(key);

            if (first)
                first = false;
            else
                result.append("&");

            result.append(URLEncoder.encode(key, "UTF-8"));
            result.append("=");
            result.append(URLEncoder.encode(value.toString(), "UTF-8"));
        }
        return result.toString();
    }

//code commented just for now
//    public static class  IncomingSms extends BroadcastReceiver {
//        public String otpnumber;
//
//        @Override
//        public void onReceive(Context context, Intent intent) {
//
//            final Bundle bundle = intent.getExtras();
//            try {
//                if (bundle != null) {
//                    final Object[] pdusObj = (Object[]) bundle.get("pdus");
//                    for (int i = 0; i < pdusObj.length; i++) {
//                        SmsMessage currentMessage = SmsMessage.createFromPdu((byte[]) pdusObj[i]);
//                        String phoneNumber = currentMessage.getDisplayOriginatingAddress();
//                        String senderNum = phoneNumber;
//                        String message = currentMessage.getDisplayMessageBody();
//                        try {
//                            if (senderNum.contains("UPWRDZ")) {
//                                String CurrentString = message;
//                                String[] separated = CurrentString.split(" ");
//                                otpnumber = separated[separated.length - 1];
//                                String str = otpnumber;
//                                otpnumber = str.substring(0, str.length()-1);
//                                new MainActivity().otpretreival(otpnumber);
//
//                            }
//
//
//                        } catch (Exception e) {
//                        }
//
//                    }
//                }
//
//            } catch (Exception e) {
//
//            }
//        }
//
//    }




}

