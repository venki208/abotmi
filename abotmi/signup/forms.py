
from django import forms
from django.forms.utils import ErrorList

from datacenter.models import TrackReferrals, UserReferral

class UploadFileForm(forms.Form):
    education_documents = forms.FileField()


class InviteAdvisorForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
            'placeholder': 'contact@reiaglobal.com',\
            'onfocus':'this.placeholder=""', 'onblur':'this.placeholder="contact@reiaglobal.com"' },
        ),
        required=True,
        error_messages={'required': 'Please Enter Your Email'}
    )
    phone = forms.RegexField(
        regex=r'^\d{10}$',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'9876543210',\
            'onfocus':'this.placeholder=""', 'onblur':'this.placeholder="9876543210"' }),
        error_message=("please enter 10 digits Number"),
        error_messages={'required': 'Please Enter Your Mobile no.'}
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'John',\
        'onfocus':'this.placeholder=""', 'onblur':'this.placeholder="John"' }),
        required=True,
        error_messages={'required': 'Please Enter Referrer Name'}
    )
    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Bengaluru',\
        'onfocus':'this.placeholder=""', 'onblur':'this.placeholder="Bengaluru"'}),
        required=False,
        error_messages={'required': 'Please Enter Location'}
    )
    products_serviced = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Product serviced',\
        'onfocus':'this.placeholder=""', 'onblur':'this.placeholder="Product serviced"'}),
        required=False
    )
    registered_financial_advisor = forms.ChoiceField(
        choices=[(1,'Yes'), (0,'No')],
        widget=forms.RadioSelect(),
        required=False
    )
    referral_user_type = forms.CharField(
        widget=forms.HiddenInput(
            attrs={'value': 'advisor', 'class': 'form-control'}
        ),
        required=False
    )
    referred_by = forms.CharField(
        widget=forms.HiddenInput(attrs={'class': 'form-control'}),
        required=False
    )
    sebi_reg_no = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'INB011289536 (BSE)',\
        'onfocus':'this.placeholder=""', 'onblur':'this.placeholder="INB011289536 (BSE)"'}),
        required=False,
        label='SEBI Registration Number'
    )
    amfi_reg_no = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'IR/IMD/DF/21/2061',\
        'onfocus':'this.placeholder=""', 'onblur':'this.placeholder="IR/IMD/DF/21/2061"'}),
        required=False,
        label='AMFI Registration Number'
    )
    irda_reg_no = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'2409_GI_2004_ENG',\
        'onfocus':'this.placeholder=""', 'onblur':'this.placeholder="2409_GI_2004_ENG"'}),
        required=False,
        label='IRDA Registration Number'
    )
    crisil_verified_no = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'SME4GISE1',\
        'onfocus':'this.placeholder=""', 'onblur':'this.placeholder="SME4GISE1"'}),
        required=False,
        label='CRISIL Verified Number')
    know_duration = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'2',\
        'onfocus':'this.placeholder=""', 'onblur':'this.placeholder="2"'}),
        required=False,
        min_value=1,
        max_value=99,
        label='How long you know'
    )
    believe_become_advisor = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'',\
        'onfocus':'this.placeholder=""', 'onblur':'this.placeholder=""'}),
        label='Why do you believe he can be become an advisor',
        required=False
    )

    class Meta:
        model = TrackReferrals
        fields = ('name', 'email', 'phone', 'location', 'referred_by',
                  'products_serviced', 'registered_financial_advisor',
                  'sebi_reg_no', 'amfi_reg_no', 'irda_reg_no',
                  'crisil_verified_no', 'know_duration',
                  'believe_become_advisor')


class memberreferform(forms.ModelForm):
    email = forms.EmailField()
    phone = forms.RegexField(
        regex=r'^\d{10}$',
        error_message=("please enter 10 digits Number"),
        required=True
    )

    class Meta:
        model = UserReferral
        fields = ('name', 'email', 'phone')

    def clean(self):
        if UserReferral.objects.filter(phone=self.cleaned_data.get('phone')):
            self._errors['phone'] = ErrorList()
            self._errors['phone'].append("cellphone number already exists")
        elif UserReferral.objects.filter(email=self.cleaned_data.get('email')):
            self._errors['email'] = ErrorList()
            self._errors['email'].append("Email-id already exists")
        else:
            return self.cleaned_data
