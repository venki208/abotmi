# python lib
import datetime

# Django lib
from django import forms
from datetimewidget.widgets import DateTimeWidget, TimeWidget


class MeetupForm(forms.Form):
    today = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    dateTimeOptions = {
        'format': 'yyyy-mm-dd hh:ii:ss',
        'autoclose': True,
        'showMeridian': True,
        'startDate': '%s' % (today)
    }
    scheduled = forms.DateTimeField(
                    label='Schedule Date & Time',
                    widget=DateTimeWidget(
                        options=dateTimeOptions,
                        bootstrap_version=3,
                        attrs={
                            'onchange': 'check_validation(name,"help_id_scheduled");',
                            'readonly': 'true'
                        },
                    )
                )

    def __init__(self, *args, **kwargs):
        super(MeetupForm, self).__init__(*args, **kwargs)
