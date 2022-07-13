import os
import subprocess
from subprocess import STDOUT, PIPE
import requests
from datacenter.models import PanNumberVerfication, UserProfile
from reia.celery import app as celery_app
from . import constants


@celery_app.task(name="nsdl_verification", ignore_result=True)
def get_pan_details(pan_no, user_profile_id=None):
    # java ---- java command 
    # -classpath --- mention jar file
    # -ea ---- java class name
    # out.jks ---Java key store
    # <password> ---password
    # data -- data
    # out.sig -- output file
    pan_no = "^"+pan_no
    path = os.path.abspath(os.path.dirname(__file__))
    cmd = ['java',
            '-classpath', path+'/.:bcmail-jdk16-1.44.jar:'+path+'/.:bcprov-jdk16-1.44.jar',
            '-ea', 'pkcs7gen',
            path+'/out.jks',
            constants.NSDL_PWD,
            constants.NSDL_KEY+pan_no]
    proc = subprocess.Popen(cmd, stdout=PIPE, stderr=STDOUT, cwd=path)
    stdout,stderr = proc.communicate()
    pan_data = constants.NSDL_KEY+pan_no
    data = parameterpassing(pan_data, stdout)
    if user_profile_id:
        """
            If user profile id is passed
            we will create pan verification object
            only once per user.
        """
        user_profile = UserProfile.objects.get(id=user_profile_id)
        panV, status = PanNumberVerfication.objects.get_or_create(
            user_profile_id=user_profile.id
        )
        if status:
            panV.user_email = user_profile.email
            panV.user_first_name = user_profile.first_name
            panV.user_last_name = user_profile.last_name
            panV.pan_number = user_profile.pan_no
            panV.nsdl_pan_details = data
            panV.save()
    return data

def parameterpassing(data,signature):
    print data, signature
    data= {'data':data,'signature':signature}
    headers  = {'Content-Type': 'application/x-www-form-urlencoded'}
    req = requests.post('https://59.163.46.2/TIN/PanInquiryBackEnd',verify=False, headers=headers, data=data)
    json_res = req.content.encode('UTF-8')
    return json_res