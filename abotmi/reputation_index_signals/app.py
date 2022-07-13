from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class ReputationIndexSignalsConfig(AppConfig):
    name = 'reputation_index_signals'
    verbose_name = _('reputation_index_signals')

    def ready(self):
        import reputation_index_signals.signal_functions  # noqa
