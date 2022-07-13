'''
author: Madhu
created_date: May 27 2016
'''
import datetime
from django import forms
from datetimewidget.widgets import DateWidget
from datacenter.models import TransactionsDetails

class InviteAdvisorToRateForm(forms.Form):
    '''
    author: Madhu
    created_date: May 27 2016
    this form is to invite advisor to rate, it is a basic form
    '''
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control','placeholder':'John',\
            'onfocus':'this.placeholder=""', 'onblur':'this.placeholder="John"'}
        ),
        required=True,
        error_messages={'required': 'Please Enter Referrer Name'}
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'class': 'form-control','placeholder':'contact@reiaglobal.com',\
            'onfocus':'this.placeholder=""', 'onblur':'this.placeholder="contact@reiaglobal.com"'}),
        required=True,
        error_messages={
            'required': 'Please Enter Your Email'
        }
    )
    mobile = forms.RegexField(
        regex=r'^\d{10}$',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'9876543210',\
            'onfocus':'this.placeholder=""', 'onblur':'this.placeholder="9876543210"'}),
        error_message=("please enter 10 digits Number"),
        error_messages={'required': 'Please Enter Your Mobile no.'}
    )

class PaymentForm(forms.ModelForm):
    # today = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    dateTimeOptions = {
        'format': 'yyyy-mm-dd',
        'autoclose': True
    }

    bank_name = forms.CharField(
        label = "Bank Name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder':'Bank Name',
            }
        ),
        required=True,
        error_messages={'required': 'Please Enter Bank Name'}
    )
    cheque_dd_no = forms.CharField(
        label = "Reference Number",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder':'cheque / DD / NEFT Ref No',
            }
        ),
        required=True,
        error_messages={'required': 'Please Enter Reference Number'}
    )
    cheque_dd_date = forms.DateField(
        label= "Date of Payment",
        widget=DateWidget(
            attrs={
                'required':'true',
                'onfocus':'enable_cheque_dd_date();',
                'onblur':'disable_cheque_dd_date();'
            },
            options=dateTimeOptions,
            bootstrap_version=3
        ),
        required = True,
        error_messages={'required': 'Please select date of payment'}
    )
    discounted_amount = forms.CharField(
        label = 'Amount',
        required = True,
        widget = forms.TextInput(attrs={'readonly':'readonly'})
    )
    description = forms.CharField(
        label = 'Years Selected',
        required = True,
        widget = forms.TextInput(attrs={'readonly':True})
    )
    scaned_doc = forms.FileField(
        label='Reference Document',
        required=False,
    )

    class Meta:
        model = TransactionsDetails
        fields = (
            'bank_name',
            'cheque_dd_no',
            'cheque_dd_date',
            'discounted_amount',
            'description',
            'scaned_doc'
        )
