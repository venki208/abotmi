from django.conf import settings
db_alias = getattr(settings, 'ADVISOR_CHECK_DB_ALIAS', 'default')


class AdvisorCheckRouter(object):
    """
    A router to control all database operations on models in the
    advisor_check application.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read advisor_check models go to db_alias.
        """
        if model._meta.app_label == "advisor_check":
            return db_alias
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write advisor_check models go to db_alias.
        """
        if model._meta.app_label == "advisor_check":
            return db_alias
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the advisor_check app is involved.
        """
        if obj1._meta.app_label == 'advisor_check' or \
           obj2._meta.app_label == 'advisor_check':
                return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the advisor_check app only appears in the
        db_alias database.
        """
        if app_label == 'advisor_check':
            return db == db_alias
        else:
            return db == 'default'
