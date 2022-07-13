
import datetime
from datetimewidget.widgets import DateWidget
from django import forms
from django.contrib.auth.models import User
from django.forms.extras import SelectDateWidget
from django.utils import timezone
from datacenter.models import UserProfile, Advisor, AdvisorType, User, Country, CrisilCertifications
from datetime import date
from nfadmin import constants

class User_Form(forms.ModelForm):
	first_name = forms.CharField(
		required=True, 
		widget=forms.TextInput(
			attrs={'class':'form-control input'}
		), 
		error_messages={'required':'Please enter First Name'}
	)
	last_name = forms.CharField(
		required=True, 
		widget=forms.TextInput(
			attrs={'class':'form-control input'}
		),
		error_messages={'required':'Please enter Last Name'}
	)

	class Meta:
		model  = User
		fields = ('first_name','last_name')


class Userprofile_Firsttab(forms.ModelForm):
	now = timezone.now()
	max_year = now.year
	min_year = now.year-constants.MIN_QUALIFICATION_YEAR
	SUFFIX_CHOICES = (
		('','--select--'),
		('Mr', 'Mr'),
		('Mrs', 'Mrs'),
		('Miss', 'Miss'),
		('Dr', 'Dr'),
		('Prof', 'Prof'),
		)
	GENDER_CHOICES = (
		('', 'select'),
		('M', 'Male'),
		('F', 'Female'),
		('O', 'Others'),
		)
	suffix = forms.ChoiceField(
		label="Title",
		choices=SUFFIX_CHOICES,
		error_messages={'required': 'Please Select Title'},
		required=True,
		widget=forms.Select(attrs={'class':'form-control'})
	)
	birthdate = forms.DateField(
		required=True,
		widget=forms.TextInput(
			attrs={'class':'datepicker form-control'}
		)
	)
	gender = forms.ChoiceField(
		choices= GENDER_CHOICES,
		required=True,
		widget=forms.Select(attrs={'class':'form-control input'}),
		error_messages={'required': 'Please Select Gender'},
	)
	door_no = forms.CharField(
		required=True,
		widget=forms.TextInput(attrs={'class':'form-control input'}),
		error_messages={'required':'Please Enter Door No'}
	)
	street_name = forms.CharField(
		label="Address1", 
		widget=forms.TextInput(attrs={'class':'form-control input'}), 
		required=True, 
		error_messages={'required':'Please Enter Address1'}
	)
	address = forms.CharField(
		label="Address2", 
		required=True, 
		widget=forms.TextInput(attrs={'class':'form-control input'}), 
		error_messages={'required':'Please Enter Address2'}
	)
	locality = forms.CharField(
		required=True, 
		widget=forms.TextInput(attrs={'class':'form-control input'}), 
		error_messages={'required':'Please Enter Locality'}
	)
	city = forms.CharField(
		required=True, 
		widget=forms.TextInput(attrs={'class':'form-control input'}), 
		error_messages={'required':'Please Enter City'}
	)
	state = forms.CharField(
		required=True, 
		widget=forms.TextInput(
			attrs={'class':'form-control input','readonly':'readonly'}
		),
		error_messages={'required':'Please Enter State'}
	)
	pincode = forms.CharField(
		required=True, 
		widget=forms.TextInput(
			attrs={'class':'form-control input','onChange':'check_pincode();'}
		), 
		error_messages={'required':'Please Enter Pincode'}
	)
	country = forms.CharField(
		required=True, 
		widget=forms.TextInput(attrs={'class':'form-control input'}), 
		error_messages={'required':'Please Enter Country'}
	)
	nationality = forms.CharField(
		required=True, 
		widget=forms.TextInput(attrs={'class':'form-control input'}), 
		error_messages={'required':'Please Enter Nationality'}
	)
	BLOOG_GROUP_CHOICES = (
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
	blood_group = forms.ChoiceField(
		required=True, 
		widget=forms.Select(attrs={'class':'form-control input'}),
		choices=BLOOG_GROUP_CHOICES, 
		error_messages={'required':'Please Select Blood Group'}
	)
	company_name = forms.CharField(
		required=True, 
		widget=forms.TextInput(attrs={'class':'form-control input'}),
		 error_messages={'required':'Please Enter Company Name'}
	)
	company_location = forms.CharField(
		required=True, 
		widget=forms.TextInput(attrs={'class':'form-control input'}), 
		error_messages={'required':'Please Enter Company Location'}
	)
	company_city = forms.CharField(
		required=True, 
		widget=forms.TextInput(attrs={'class':'form-control input'}), 
		error_messages={'required':'Please Enter Company City'}
	)
	company_website = forms.CharField(
		required=True, 
		widget=forms.TextInput(attrs={'class':'form-control input'}), 
		error_messages={'required':'Please Enter Company Website'}
	)
	designation = forms.CharField(
		required=True, 
		widget=forms.TextInput(attrs={'class':'form-control input'}), 
		error_messages={'required':'Please Enter Designation'}
	)
	annual_income = forms.CharField(
		required=True, 
		widget=forms.TextInput(attrs={'class':'form-control input'}), 
		error_messages={'required':'Please Enter Annual Income'}
	)
	qualification = forms.ChoiceField(
		required=True, 
		choices=constants.QUALIFICATION_LIST, 
		widget=forms.Select(attrs={'class':'form-control input'}), 
		error_messages={'required':'Please Enter Qualification'}
	)
	college_name = forms.CharField(
		required=True, 
		widget=forms.TextInput(attrs={'class':'form-control input'}), 
		error_messages={'required':'Please Enter College Name'}
	)
	YEAR_PASSOUT = [('','select')]
	for x in range(min_year, max_year):
		YEAR_PASSOUT.append((x,x))
	year_passout = forms.ChoiceField(
		label="Year of Passout", 
		required=True, 
		widget=forms.Select(attrs={'class':'form-control input'}), 
		choices=YEAR_PASSOUT, 
		error_messages={'required':'Please Enter Year of Passout'}
	)
	mobile = forms.CharField(
		required=True, 
		widget=forms.TextInput(attrs={'class':'form-control input'}), 
		error_messages={'required':'Please enter Mobile Number'}
	)
	email = forms.EmailField(
		required=True, 
		widget=forms.EmailInput(
			attrs={'class':'form-control input','readonly':'readonly'}
		), 
		error_messages={'required':'Please enter Email Id'}
	)

	class Meta:
		model  = UserProfile
		fields = ('email','suffix','birthdate','gender','door_no','street_name','address','locality','city','state','pincode','country','nationality','blood_group','company_name','company_location','company_city','company_website','designation','annual_income','qualification','college_name','year_passout','mobile')


class AdvisorCredibilityForm(forms.ModelForm):
	Professional_Education_Qualification = (
		('CA', 'CA'),
		('CFA', 'CFA'),
		('CPA', 'CPA'),
		('CAIA', 'CAIA'),
		('Others', 'Others'),
	)
	Financial_Instruments = (
		('Equity', 'Equity'),
		('Wealth Advisory', 'Wealth Advisory'),
		('Mutual Fund', 'Mutual Fund'),
		('Insurance', 'Insurance'),
		('Real Estate', 'Real Estate'),
		('Portfolio Management', 'Portfolio Management'),
		('Others', 'Others'),
	)
	is_registered_advisor = forms.ChoiceField(
		label="Is Registered Financial Advisor", 
		required=False, 
		choices=((False, 'No'), (True, 'Yes')),
		widget=forms.Select(
			attrs={'class':'form-control input','onChange':'show_regester_fields();'}
		)
	)
	sebi_number = forms.RegexField(
		label="Sebi Number",
		regex=r'^[a-zA-Z][a-zA-Z0-9\/]{0,15}[a-zA-Z0-9]$', 
		required=False,
		widget=forms.TextInput(
			attrs={'class':'form-control input'}
		),
		error_message=('Please Enter a Valid Sebi Number'), 
		error_messages={'required':'Please Enter a Valid Sebi Number'} 
	)
	amfi_number = forms.RegexField(
		label="Amfi Number",
		regex=r'^[a-zA-Z][a-zA-Z0-9\/]{0,15}[a-zA-Z0-9]$', 
		required=False, 
		widget=forms.TextInput(attrs={'class':'form-control input'}),
		error_message=('Please Enter a Valid Amfi Number '), 
		error_messages={'required':'Please Enter a valid Amfi Number'}
	)
	irda_number = forms.RegexField(
		label="Irda Number",
		regex=r'^[a-zA-Z][a-zA-Z0-9\/]{0,15}[a-zA-Z0-9]$', 
		required=False, 
		widget=forms.TextInput(attrs={'class':'form-control input'}),
		error_message=('Please Enter a Valid IRDA Number '), 
		error_messages={'required':'Please Enter a valid Irda Number'}
	)
	other_registered_number = forms.RegexField(
		label="Other Registration Number",
		regex=r'^[a-zA-Z][a-zA-Z0-9\/]{0,15}[a-zA-Z0-9]$', 
		required=False, 
		widget=forms.TextInput(attrs={'class':'form-control input'}),
		error_message=('Please Enter a Valid Registration Number '), 
		error_messages={'required':'Please Enter a valid Registration Number'}
	)
	sebi_expiry_date = forms.DateField(
		required=False, 
		widget=forms.TextInput(attrs={'class':'reg_exp_date form-control'})
	)
	irda_expiry_date = forms.DateField(
		required=False, 
		widget=forms.TextInput(attrs={'class':'reg_exp_date form-control'})
	)
	amfi_expiry_date = forms.DateField(
		required=False, 
		widget=forms.TextInput(attrs={'class':'reg_exp_date form-control'})
	)
	other_expiry_date = forms.DateField(
		required=False, 
		widget=forms.TextInput(attrs={'class':'reg_exp_date form-control'})
	)
	other_registered_organisation = forms.CharField(
		label="Registration Authority", 
		required=False, 
		widget=forms.TextInput(attrs={'class':'form-control input'}), 
		error_messages={'required':'Please Enter Registration Authority'}
	)
	practice_country = forms.ModelChoiceField(
		required=False,
		queryset = Country.objects.all()
	)
	practice_city = forms.RegexField(
		label="Practice City",
		regex=r'^[a-zA-Z]+$',
		required=False, 
		widget=forms.TextInput(attrs={'class':'form-control input'}), 
		error_messages={'required':'Please Enter Practice City'}
	)
	financial_instruments = forms.MultipleChoiceField(
		label="Financial Instruments", 
		required=False, 
		widget=forms.CheckboxSelectMultiple(),
		choices=Financial_Instruments,
		error_messages={'required':'Please Enter Financial Instruments'}
	)
	practice_years = forms.IntegerField(
		label="Practice Years",
		min_value = 0,
		max_value = 100, 
		required=False, 
		widget=forms.TextInput(attrs={'class':'form-control input'}), 
		error_messages={'required':'Please Enter Practice Years'}
	)
	other_financial_instruments = forms.RegexField(
		label="Other Financial Instruments", 
		regex= r'[a-zA-Z0-9]$',
		required=False, 
		widget=forms.TextInput(attrs={'class':'form-control input'}), 
		error_messages={'required':'Please Enter Other Financial Instruments'}
	)
	credibility_declaration_qualification = forms.ChoiceField(
		choices = Professional_Education_Qualification,
		label="Professional Educational Qualification", 
		required=False, 
		widget=forms.Select(attrs={'class':'form-control input'}), 
		error_messages={'required':'Please Enter Educational Qualification'}
	)
	class Meta:
		model  = Advisor
		fields = ('is_registered_advisor','sebi_number', 'amfi_number', 'irda_number',
		'other_registered_number','sebi_expiry_date','irda_expiry_date','amfi_expiry_date',
		'other_expiry_date','other_registered_organisation','practice_country',
		'practice_city','financial_instruments','practice_years',
		'other_financial_instruments','credibility_declaration_qualification')


class CrisilCertificateForm(forms.ModelForm):
    dateTimeOptions = {
        'format': 'yyyy-mm-dd',
        'autoclose': True
    }

    crisil_registration_number = forms.CharField(
        label = "CRISIL REG No",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder':'CRISIL REG No',
                'onchange':'check_validation(id);',
            }
        ),
        required=True,
        error_messages={'required': 'Please Enter CRISIL Registration No'}
    )
    crisil_issued_date = forms.DateField(
        label= "CRISIL Issued Date",
		widget = forms.TextInput(
			attrs = {
				'class': 'form-control issued_date',
				'placeholder': 'Issued Date',
				'onchange': 'check_validation(id);'
			}
		),
        required = True,
        error_messages={'required': 'Please select issued date'}
    )
    crisil_expiry_date = forms.DateField(
        label= "CRISIL Expiry Date",
		widget = forms.TextInput(
			attrs = {
				'class': 'form-control expiry_date',
				'placeholder': 'Expiry Date',
				'onchange': 'check_validation(id);'
			}
		),
        required = True,
        error_messages={'required': 'Please select expire date'}
    )

    crisil_report = forms.FileField(
        label='Crisil Report Document',
        required=True,
    )

    class Meta:
        model = CrisilCertifications
        fields = (
            'crisil_registration_number',
			'crisil_issued_date',
            'crisil_expiry_date',
            'crisil_report',
        )
