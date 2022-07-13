# python lib
import datetime
from datetimewidget.widgets import DateTimeWidget
# Django lib
from django import forms
# Constans
from . import constants
# Local imports
from common.views import get_uplyf_project_list


def get_my_choices():
    '''
    Getting Projects list from UPLYF
    '''
    project_result = get_uplyf_project_list()
    total_projects_list = [
        ('', 'Select')
    ]
    if project_result:
        project_result_list = [((p['project_name']+'-'+p['project_id']),(p['project_name']+'-'+p['project_id']))for p in project_result]
        total_projects_list = total_projects_list + project_result_list
    return total_projects_list


class CreateWebinarForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(CreateWebinarForm, self).__init__(*args, **kwargs)
        # self.fields['uplyf_project'] = forms.ChoiceField(
        #     required=False, choices=get_my_choices() )

    today = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    dateTimeOptions = {
        'format': 'yyyy-mm-dd hh:ii:ss',
        'autoclose': True,
        'showMeridian' : True,
        'startDate': '%s' %today
    }

    name = forms.CharField(
                max_length = 50,
                label = 'Room Name *',
                required = True,
                widget=forms.TextInput(
                    attrs={
                        'placeholder': 'Room Name'
                    }
                )
            )
    lobby_description = forms.CharField(
                            label = 'Lobby Description *',
                            widget = forms.Textarea(attrs={
                                'placeholder': 'Lobby Description'
                            }),
                            required = True,
                        )
    starts_at = forms.DateTimeField(
                    label = 'Schedule Date & Time *',
                    widget = DateTimeWidget(
                        attrs={
                            'required':'true',
                            'onfocus':'enable_starts_at();',
                            'onblur':'disable_starts_at();',
                            'placeholder':'Schedule Date & Time'
                        },
                        options = dateTimeOptions,
                        bootstrap_version = 3
                    ),
                    required = True
                )
    duration = forms.IntegerField(
                    label = 'Duration in Minutes *',
                    required = True,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Duration in Minutes'
                    })
                )
