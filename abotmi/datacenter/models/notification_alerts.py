import datetime

from mongoengine import *

from datacenter.views import GetOrCreateQuerySet


class NotificationTemplate(Document):
    '''
    Storing Noification templates
    template * -> Store Notification template
    template_type -> Store type of notifications template
    '''
    template = StringField(unique=True)
    template_type = StringField(max_length=100, unique=True)
    catogery = StringField(max_length=250)
    created_date = DateTimeField(required=True, default=datetime.datetime.now)
    modified_date = DateTimeField()

    meta = {
        'queryset_class': GetOrCreateQuerySet
    }

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(NotificationTemplate, self).save(*args, **kwargs)

    def __str__(self):
        return self.template


class TemplateData(EmbeddedDocument):
    data_type = StringField(required=True)
    value = StringField(required=False)


class Notification(Document):
    '''
    Storing Notification data to send to User
    user_profile_id * {id} -> UserProfile table id
    template_id * {object(id)} -> NotificationTemplate table id
    read_status * {Boolean} -> True/False (default takes False)
    values {array} -> store values need to pass to templates
    ex:
    template:
        "Hi {}, Signup Completed Successfully."
    values:
        ['Jhon']
    obj.get_temlate():
        returns `"Hi Jhon, Signup Completed Successfully."`
    '''
    sender_id = StringField(required=False)
    receive_id = StringField(required=True)
    template_id = ReferenceField('NotificationTemplate')
    view_status = BooleanField(default=False)
    read_status = BooleanField(default=False)
    action_url = StringField(required=False)
    template_data = ListField(EmbeddedDocumentField(TemplateData), default=[])
    values = ListField(default=[])
    receive_id_from = StringField(required=False)
    sender_id_from = StringField(required=False)
    created_date = DateTimeField(required=True, default=datetime.datetime.now)
    modified_date = DateTimeField()

    meta = {
        'queryset_class': GetOrCreateQuerySet
    }

    def get_template(self, values, *args, **kwargs):
        if type(values) == list:
            return self.template_id.template.format(*values)
        else:
            raise Exception('values should be list, but found {}'.format(type(values)))

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Notification, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.template_id)
