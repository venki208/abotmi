import json

from rest_framework import serializers

from datacenter.models import UserProfile, Advisor, UploadDocuments, UserStatus


class GetNotApprovedRegulatory(serializers.ModelSerializer):
    '''
    Getting Regulatory registration uploaded documentsand status
    '''
    def get_advisor_regulatory_status(self, obj):
        reg_type = self.context.get('reg_type', None)
        final_adv_obj = UserStatus.objects.filter(user_profile = obj).first()
        if reg_type == 'SEBI':
            final_advisor_regulatory_status = final_adv_obj.sebi_status
        elif reg_type == 'IRDA':
            final_advisor_regulatory_status = final_adv_obj.irda_status
        elif reg_type == 'AMFI':
            final_advisor_regulatory_status = final_adv_obj.amfi_status
        elif reg_type == 'others':
            final_advisor_regulatory_status = final_adv_obj.regulatory_other_status
        else:
            final_advisor_regulatory_status = None
        return final_advisor_regulatory_status

    def get_reg_no(self, obj):
        reg_type = self.context.get('reg_type', None)
        if reg_type == 'SEBI':
            final_reg_number = obj.advisor.sebi_number
        elif reg_type == 'IRDA':
            final_reg_number = obj.advisor.irda_number
        elif reg_type == 'AMFI':
            final_reg_number = obj.advisor.amfi_number
        elif reg_type == 'others':
            final_reg_number = obj.advisor.other_registered_number
        elif reg_type == 'rera':
            advisor_obj = Advisor.objects.filter(user_profile = obj).first()
            if advisor_obj.rera_details:
                final_reg_number = advisor_obj.rera_details
            else:
                final_reg_number = None
        else:
            final_reg_number = None
        return final_reg_number

    def get_doc_url(self, obj):
        reg_type = self.context.get('reg_type', None)
        kwargs = {}
        kwargs['user_profile'] = obj
        if reg_type == 'SEBI':
            kwargs['documents_type'] = 'sebi_certificate'
        elif reg_type == 'AMFI':
            kwargs['documents_type'] = 'amfi_certificate'
        elif reg_type == 'IRDA':
            kwargs['documents_type'] = 'irda_certificate'
        elif reg_type == 'others':
            kwargs['documents_type'] = 'others_certificate'
        final_doc_url = UploadDocuments.objects.filter(**kwargs).first()
        if final_doc_url:
            return final_doc_url.documents
        else:
            return None

    def get_renewal_doc(self, obj):
        reg_type = self.context.get('reg_type', None)
        kwargs = {}
        kwargs['user_profile'] = obj
        if reg_type == 'SEBI':
            kwargs['documents_type'] = 'sebi_renewal_certificate'
        elif reg_type == 'AMFI':
            kwargs['documents_type'] = 'amfi_renewal_certificate'
        elif reg_type == 'IRDA':
            kwargs['documents_type'] = 'irda_renewal_certificate'
        elif reg_type == 'others':
            kwargs['documents_type'] = 'others_renewal_certificate'
        final_renewal_doc_url = UploadDocuments.objects.filter(**kwargs)
        if final_renewal_doc_url:
            return final_renewal_doc_url
        else:
            return None
    
    def get_others_authorized_organisation(self, obj):
        reg_organization = obj.advisor.other_registered_organisation
        if reg_organization:
            return reg_organization
        else:
            return None
            
    advisor_regulatory_status = serializers.SerializerMethodField()
    reg_no = serializers.SerializerMethodField()
    doc_url = serializers.SerializerMethodField()
    renewal_doc = serializers.SerializerMethodField()
    others_authorized_organisation = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            'first_name',
            'last_name',
            'email',
            'mobile',
            'reg_no',
            'doc_url',
            'advisor_regulatory_status',
            'renewal_doc',
            'others_authorized_organisation'
        )


class GetAdditionalQualificationDocs(serializers.ModelSerializer):
    '''
    Getting Additionl Qualification documents url and status
    '''
    def get_heighest_qua_doc_status(self, obj):
        user_status_obj = obj.status
        return user_status_obj.highest_qualification_status
    
    def get_heighest_qua_doc_url(self, obj):
        doc_url = None
        heighst_edu_obj = UploadDocuments.objects.filter(
            documents_type='highest_qualification_upload', user_profile = obj
            ).first()
        if heighst_edu_obj:
            doc_url = heighst_edu_obj.documents.url
        return doc_url

    heighest_qua_doc_status = serializers.SerializerMethodField()
    heighest_qua_doc_url = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            'first_name',
            'last_name',
            'email',
            'mobile',
            'qualification',
            'additional_qualification',
            'heighest_qua_doc_status',
            'heighest_qua_doc_url'
        )