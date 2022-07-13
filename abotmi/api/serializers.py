from rest_framework import serializers
from django.contrib.auth.models import User
from datacenter.models import UserProfile, Advisor, MeetUpEvent, TrackWebinar,\
    AffiliatedCompany, CompanyAdvisorMapping, MeetUpEvent, AdvisorRating, TransactionsDetails,UploadDocuments

from django.db.models import Avg

from common.constants import MEMBER_TYPE
from common.views import get_binary_image

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active')

class UploadDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadDocuments
        fields = ('id','documents', 'documents_type', 'registration_number', 'status', 'created_date','modified_date')

class UserProfileSerializer(serializers.ModelSerializer):

    def get_avg_rating(self, obj):
        rating_avg = AdvisorRating.objects.filter(advisor = obj.advisor, user_type = MEMBER_TYPE)
        final_rating = rating_avg.exclude(
            avg_rating__lte=0.0).aggregate(Avg('avg_rating'))['avg_rating__avg']
        return final_rating

    def get_picture(self, obj):
        return get_binary_image(obj)

    def get_payment(self, obj):
        details = TransactionsDetails.objects.filter(user_profile=obj).values_list('bank_name','cheque_dd_no','cheque_dd_date','discounted_amount','description').first()
        return details
    
    def get_batch_code(self, obj):
        return obj.batch_code
    avg_rating = serializers.SerializerMethodField()
    picture = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField()
    batch_code = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'user',
            'first_name',
            'last_name',
            'email',
            'mobile',
            'picture',
            'door_no',
            'street_name',
            'address',
            'locality',
            'landmark',
            'city',
            'state',
            'country',
            'pincode',
            'gender',
            'is_admin',
            'is_advisor',
            'is_member',
            'referral_code',
            'avg_rating',
            'languages_known_read_write',
            'mother_tongue',
            'language_known',
            'my_belief',
            'payment',
            'qualification',
            'college_name',
            'year_passout',
            'my_belief',
            'self_description',
            'batch_code'
        )


class USerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()


class AdvisorSerializer(serializers.ModelSerializer):
    """docstring for AdvisorSerializer ."""

    user_profile =  UserProfileSerializer()
    class Meta:
        model = Advisor
        fields = (
            'id',
            'my_promise',
            'questions',
            'is_confirmed_advisor',
            'is_register_advisor',
            'is_wpb_user',
            'is_certified_advisor',
            'crisil_registration_number',
            'crisil_expiry_date',
            'is_registered_advisor',
            'total_advisors_connected',
            'user_profile',
            'crisil_application_status'
        )

class MeetupSerializer(serializers.ModelSerializer):

    def get_organizer_email(self, obj):
        return obj.user_profile.email  

    def get_organizer_name(self, obj):
        return obj.user_profile.first_name
    
    def get_organizer_mobile(self, obj):
        return obj.user_profile.mobile 
    
    organizer_email = serializers.SerializerMethodField()
    organizer_name = serializers.SerializerMethodField()
    organizer_mobile = serializers.SerializerMethodField()
    class Meta:
        model = MeetUpEvent
        fields = (
            'organizer_email', 
            'organizer_name',
            'organizer_mobile',
            'meetup_location',
            'meetup_landmark',
            'name',
            'scheduled',
            'address',
            'meetup_event_id', 
            'description',
            'duration',
            'uplyf_project',
            'category',
            'registered_user_count',
            'is_deleted'
        )
    

class MeetupUpdateSerializer(serializers.ModelSerializer):

    def get_organizer_email(self, obj):
        return obj.user_profile.email

    def get_organizer_name(self, obj):
        return obj.user_profile.first_name

    def get_organizer_mobile(self, obj):
        return obj.user_profile.mobile

    def get_str_schedule(self, obj):
        return str(obj.scheduled)

    organizer_email = serializers.SerializerMethodField()
    organizer_name = serializers.SerializerMethodField()
    organizer_mobile = serializers.SerializerMethodField()
    str_schedule = serializers.SerializerMethodField()

    class Meta:
        model = MeetUpEvent
        fields = (
            'organizer_email',
            'organizer_name',
            'organizer_mobile',
            'meetup_location',
            'meetup_landmark',
            'name',
            'str_schedule',
            'address',
            'meetup_event_id',
            'description',
            'duration',
            'uplyf_project',  
            'category',
            'registered_user_count',
            'is_deleted'

        )


class WebinarSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrackWebinar
        depth = 1


class ComapnySerializer(serializers.ModelSerializer):
    class Meta:
        model = AffiliatedCompany
        # user_profile = serializers.RelatedField(many=True, read_only=True)
        fields = (
            'company_name',
            'tagline',
            'logo',
            'user_profile'
        )

class CompanyAdvisorsList(serializers.ModelSerializer):
    advisor_user_profile =  UserProfileSerializer()
    class Meta:
        model = CompanyAdvisorMapping
        fields = (
            'status',
            # 'company_name',
            'advisor_user_profile'
        )

class AdvisorRegistrationSerializer(serializers.Serializer):
    """
    serializers: Advisor Registration: FASIA
    """
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(
        min_length=1, max_length=250, required=True)
    last_name = serializers.CharField(
        min_length=1, max_length=250, required=True)
    gender = serializers.CharField(required=True)
    mobile = serializers.CharField(max_length=25, required=True)
    sm_source = serializers.CharField(required=True)
    user_role = serializers.CharField(required=True)
