from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CandidateProfile, EmployerProfile, Job, Application

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CandidateProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    applications_count = serializers.SerializerMethodField()

    class Meta:
        model = CandidateProfile
        fields = '__all__'
        read_only_fields = ['resume_text', 'resume_parsed_skills', 'resume_experience', 'resume_ats_score', 'resume_summary']

    def validate_pincode(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("Pincode must be exactly 6 digits.")
        return value

    def validate_phone(self, value):
        if value and (not value.isdigit() or len(value) != 10):
            raise serializers.ValidationError("Phone number must be exactly 10 digits.")
        return value

    def get_applications_count(self, obj):
        return obj.applications.count()

class EmployerProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = EmployerProfile
        fields = (
            'id', 'username', 'company_name', 'pincode', 'city', 'contact_name', 
            'contact_phone', 'contact_email', 'about', 'website_links', 'org_details'
        )

    def validate_pincode(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("Pincode must be exactly 6 digits.")
        return value

    def validate_contact_phone(self, value):
        if value and (not value.isdigit() or len(value) != 10):
            raise serializers.ValidationError("Contact phone number must be exactly 10 digits.")
        return value

class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='employer.company_name', read_only=True)
    applicants_count = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = '__all__'
        extra_kwargs = {'employer': {'read_only': True}, 'expires_at': {'read_only': True}} # Set in view

    def validate_pincode(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("Pincode must be exactly 6 digits.")
        return value

    def get_applicants_count(self, obj):
        return obj.applications.count()

class ApplicationSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='candidate.user.username', read_only=True)
    candidate_skills = serializers.CharField(source='candidate.skills', read_only=True)
    candidate_experience = serializers.IntegerField(source='candidate.experience', read_only=True)
    candidate_pincode = serializers.CharField(source='candidate.pincode', read_only=True)
    candidate_phone = serializers.CharField(source='candidate.phone', read_only=True)
    candidate_contact_email = serializers.CharField(source='candidate.contact_email', read_only=True)
    candidate_city = serializers.CharField(source='candidate.city', read_only=True)
    candidate_social_links = serializers.CharField(source='candidate.social_links', read_only=True)
    candidate_eval_score = serializers.FloatField(source='match_score', read_only=True)
    candidate_resume_ats_score = serializers.FloatField(source='candidate.resume_ats_score', read_only=True)
    candidate_resume_summary = serializers.CharField(source='candidate.resume_summary', read_only=True)
    candidate_resume_file = serializers.FileField(source='candidate.resume_file', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    class Meta:
        model = Application
        fields = '__all__'
        extra_kwargs = {'candidate': {'read_only': True}, 'match_score': {'read_only': True}}
