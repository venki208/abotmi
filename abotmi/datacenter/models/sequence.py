from django.db import models
from simple_history.models import HistoricalRecords

class Sequence(models.Model):
    last_sequence = models.IntegerField(default=0, null=True, blank=True)
    sequence_type = models.CharField(max_length=20, null=True, blank=True)
    prefix = models.CharField(max_length=5, null=True, blank=True)
    digit_len = models.CharField(max_length=5, null=True, blank=True)
    remark = models.TextField(null=True,blank=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True