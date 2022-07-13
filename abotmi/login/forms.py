from django import forms
import datetime
from datacenter.models import UserProfile, Member, UploadDocuments
from datetimewidget.widgets import DateWidget


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class UserProfileForm(forms.ModelForm):
    end_date = datetime.date(
        (datetime.date.today().year - 21),
        datetime.date.today().month,
        datetime.date.today().day
    )
    start_date = datetime.date(
        end_date.year - 78,
        end_date.month,
        end_date.day,
    )
    dateOptions = {
        'format': 'yyyy-mm-dd',
        'autoclose': True,
        'showMeridian': True,
        'endDate': '%s' % end_date,
        'startDate': '%s' % start_date,
    }
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    SUFFIX_CHOICES = (
        ('', 'select'),
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Miss', 'Miss'),
        ('Dr', 'Dr'),
        ('Prof', 'Prof'),
    )
    BLOOD_GROUP_CHOICES = (
        ('', 'select'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    )
    suffix = forms.ChoiceField(
        choices=SUFFIX_CHOICES,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    first_name = forms.RegexField(
        regex=r'^[a-zA-Z]{1,20}$',
        label="First Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder':'John',\
            'onfocus':'this.placeholder=""', 'onblur':'this.placeholder="John"'
        }),
        error_message=("please enter only characters"),
        error_messages={'required': "please enter your first name"},
        required=True)
    middle_name = forms.RegexField(
        regex=r'^[a-zA-Z ]{1,20}$',
        label="Middle Name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder':'John',\
                'onfocus':'this.placeholder=""', 'onblur':'this.placeholder="John"'
            }
        ),
        error_message=("please enter only characters"),
        required=False,
    )
    last_name = forms.RegexField(
        regex=r'^[a-zA-Z]{1,20}$',
        label="Last Name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder':'John',\
                'onfocus':'this.placeholder=""', 'onblur':'this.placeholder="John"'
            }
        ),
        error_message=("please enter only characters"),
        error_messages={'required': "please enter your last name"},
        required=True,
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'contact@reiaglobal.com'
            }
        ),
        required=True
    )
    mobile = forms.RegexField(
        regex=r'^\d{10}$',
        label="Mobile",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder':'9876543210',\
                'onfocus':'this.placeholder=""', 'onblur':'this.placeholder="9876543210"'
            }
        ),
        required=True,
        error_message=("please enter only numbers"),
        error_messages={'required': "please enter your phone number"},
    )
    father_name = forms.RegexField(
        regex=r'^[a-zA-Z ]{1,40}$',
        label="Father Name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder':'John',\
                'onfocus':'this.placeholder=""', 'onblur':'this.placeholder="John"'
            }
        ),
        error_message=("please enter only characters"),
        error_messages={'required': "please enter your father's name"},
        required=False
    )
    birthdate = forms.DateField(
        label='Birth Date',
        widget=DateWidget(
            usel10n=True,
            options=dateOptions,
            bootstrap_version=3,
        ),
        required=False
    )
    know_duration = forms.IntegerField(
        label="How long do you know him/her ?",
        min_value=1,
        max_value=99,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '4 in years',\
                'onfocus':'this.placeholder=""', 'onblur':'this.placeholder="4 in years"'
            }
        ),
        required=True,
    )
    know_how = forms.RegexField(
        regex=r'^[a-zA-Z .,;\'"]{5,}$',
        label="How do you know him/her?",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'How do you know him/her',\
                'onfocus':'this.placeholder=""', 'onblur':'this.placeholder="How do you know him/her"'
            }
        ),
        error_message=("please describe using characters,\
                       minimum 10 characters"),
        required=True,
    )

    class Meta:
        model = UserProfile
        fields = (
            'suffix', 'first_name', 'middle_name',
            'last_name', 'email', 'mobile', 'father_name',
            'birthdate', 'know_duration', 'know_how'
        )


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ()


class UploadDocumentsForm(forms.ModelForm):
    DOCUMENTS_TYPE_CHOICES = (
        ('', 'select'),
        ('Adhaar', 'adhaar'),
        ('Driving Licence', 'driving_licence'),
        ('Passport', 'passport'),
        ('Bank details', 'bank_details'),
    )
    documents_type = forms.ChoiceField(
        choices=DOCUMENTS_TYPE_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )
    registration_number = forms.CharField(
        label="Registration Number",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'AQZ123QW',\
                'onfocus':'this.placeholder=""', 'onblur':'this.placeholder="AQZ123QW"'
            }
        ),
        required=False
    )

    class Meta:
        model = UploadDocuments
        fields = ('documents_type', 'registration_number')
