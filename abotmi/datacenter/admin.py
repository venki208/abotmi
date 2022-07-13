from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import UserProfile, Advisor, \
        AdvisorType, ReferralPoints, ReferralPointsType, \
        NoticeBoard, TrackWebinar, TransactionsDetails, AdvisorRating, Testimonial
# Register your models here.
admin.site.register(UserProfile, SimpleHistoryAdmin)
admin.site.register(Advisor, SimpleHistoryAdmin)
admin.site.register(AdvisorType, SimpleHistoryAdmin)
admin.site.register(ReferralPoints, SimpleHistoryAdmin)
admin.site.register(ReferralPointsType, SimpleHistoryAdmin)
admin.site.register(NoticeBoard, SimpleHistoryAdmin)
admin.site.register(TrackWebinar, SimpleHistoryAdmin)
admin.site.register(TransactionsDetails, SimpleHistoryAdmin)
admin.site.register(AdvisorRating)
admin.site.register(Testimonial)
admin.autodiscover()
admin.autodiscover_modules()
