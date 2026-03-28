from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CandidateProfile, EmployerProfile, Job, Application

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CandidateProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    applications_count = serializers.SerializerMethodField()

    class Meta:
        model = CandidateProfile
        fields = '__all__'

    def get_applications_count(self, obj):
        return obj.applications.count()

class EmployerProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = EmployerProfile
        fields = ('id', 'username', 'company_name', 'pincode', 'contact_name', 'contact_phone', 'contact_email')

class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='employer.company_name', read_only=True)
    applicants_count = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = '__all__'
        extra_kwargs = {'employer': {'read_only': True}} # Set in view

    def get_applicants_count(self, obj):
        return obj.applications.count()

class ApplicationSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='candidate.user.username', read_only=True)
    candidate_skills = serializers.CharField(source='candidate.skills', read_only=True)
    candidate_experience = serializers.IntegerField(source='candidate.experience', read_only=True)
    candidate_pincode = serializers.CharField(source='candidate.pincode', read_only=True)
    candidate_phone = serializers.CharField(source='candidate.phone', read_only=True)
    candidate_contact_email = serializers.CharField(source='candidate.contact_email', read_only=True)
    candidate_eval_score = serializers.FloatField(source='match_score', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    class Meta:
        model = Application
        fields = '__all__'
        extra_kwargs = {'candidate': {'read_only': True}, 'match_score': {'read_only': True}}
