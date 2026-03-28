from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import CandidateProfile, EmployerProfile, Job, Application
from .serializers import (
    CandidateProfileSerializer, EmployerProfileSerializer,
    JobSerializer, ApplicationSerializer, UserSerializer
)
# 👍 All this error is show because it can't see the virtual Environment it see only local environment 

User = get_user_model()





def is_admin(request):
    """Check if the request user is authenticated and is staff."""
    return request.user.is_authenticated and request.user.is_staff


class CsrfExemptAPIView(APIView):
    """Base class for all admin views: uses standard session auth with CSRF enforced."""
    authentication_classes = [SessionAuthentication]
    permission_classes = []


class AdminLoginView(CsrfExemptAPIView):
    """Admin-specific login endpoint. Only allows is_staff users."""

    def get(self, request):
        get_token(request)
        return Response({'csrfToken': get_token(request)})

    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_staff:
            return Response({'error': 'You do not have admin access'}, status=status.HTTP_403_FORBIDDEN)
        login(request, user)
        get_token(request)
        return Response({'message': 'Admin login successful', 'username': user.username})


class AdminLogoutView(CsrfExemptAPIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out'})


class AdminCheckView(CsrfExemptAPIView):
    """Check if current session is a valid admin session."""

    def get(self, request):
        if is_admin(request):
            return Response({'authenticated': True, 'username': request.user.username})
        return Response({'authenticated': False}, status=status.HTTP_401_UNAUTHORIZED)


class AdminStatsView(CsrfExemptAPIView):
    def get(self, request):
        if not is_admin(request):
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        return Response({
            'total_users': User.objects.count(),
            'total_jobs': Job.objects.count(),
            'total_applications': Application.objects.count(),
            'total_candidates': CandidateProfile.objects.count(),
            'total_employers': EmployerProfile.objects.count(),
        })


# ──────────────────────────────────────────────────────────────────
# USERS
# ──────────────────────────────────────────────────────────────────

class AdminUsersView(CsrfExemptAPIView):
    def get(self, request):
        if not is_admin(request):
            return Response({'error': 'Admin access required'}, status=403)
        users = User.objects.all().order_by('id').values(
            'id', 'username', 'email', 'role', 'is_staff', 'is_active', 'date_joined'
        )
        return Response(list(users))

    def post(self, request):
        if not is_admin(request):
            return Response({'error': 'Admin access required'}, status=403)
        data = request.data.copy()
        password = data.pop('password', None)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            if password:
                user.set_password(password)
            if data.get('is_staff'):
                user.is_staff = True
            user.save()
            return Response({'id': user.id, 'username': user.username}, status=201)
        return Response(serializer.errors, status=400)


class AdminUserDetailView(CsrfExemptAPIView):
    def get(self, request, user_id):
        if not is_admin(request):
            return Response({'error': 'Admin access required'}, status=403)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_staff': user.is_staff,
            'is_active': user.is_active,
        })

    def patch(self, request, user_id):
        if not is_admin(request):
            return Response({'error': 'Admin access required'}, status=403)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        data = request.data
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'role' in data:
            user.role = data['role']
        if 'is_staff' in data:
            user.is_staff = bool(data['is_staff'])
        if 'is_active' in data:
            user.is_active = bool(data['is_active'])
        if 'password' in data and data['password']:
            user.set_password(data['password'])
        user.save()
        return Response({'message': 'User updated'})

    def delete(self, request, user_id):
        if not is_admin(request):
            return Response({'error': 'Admin access required'}, status=403)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        if user == request.user:
            return Response({'error': 'Cannot delete your own account'}, status=400)
        user.delete()
        return Response({'message': 'User deleted'})


# ──────────────────────────────────────────────────────────────────
# JOBS
# ──────────────────────────────────────────────────────────────────

class AdminJobsView(CsrfExemptAPIView):
    def get(self, request):
        if not is_admin(request):
            return Response({'error': 'Admin access required'}, status=403)
        jobs = Job.objects.all().order_by('-created_at')
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not is_admin(request):
            return Response({'error': 'Admin access required'}, status=403)
        employer_id = request.data.get('employer_id')
        try:
            employer = EmployerProfile.objects.get(id=employer_id)
        except EmployerProfile.DoesNotExist:
            return Response({'error': 'Employer profile not found'}, status=404)
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employer=employer)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class AdminJobDetailView(CsrfExemptAPIView):
    def get(self, request, job_id):
        if not is_admin(request):
            return Response({'error': 'Admin access required'}, status=403)
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status=404)
        serializer = JobSerializer(job)
        return Response(serializer.data)

    def patch(self, request, job_id):
        if not is_admin(request):
            return Response({'error': 'Admin access required'}, status=403)
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status=404)
        serializer = JobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, job_id):
        if not is_admin(request):
            return Response({'error': 'Admin access required'}, status=403)
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status=404)
        job.delete()
        return Response({'message': 'Job deleted'})


# ──────────────────────────────────────────────────────────────────
# APPLICATIONS
# ──────────────────────────────────────────────────────────────────

class AdminApplicationsView(CsrfExemptAPIView):
    def get(self, request):
        if not is_admin(request):
            return Response({'error': 'Admin access required'}, status=403)
        applications = Application.objects.all().order_by('-created_at')
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)


class AdminApplicationDetailView(CsrfExemptAPIView):
    def patch(self, request, app_id):
        if not is_admin(request):
            return Response({'error': 'Admin access required'}, status=403)
        try:
            application = Application.objects.get(id=app_id)
        except Application.DoesNotExist:
            return Response({'error': 'Application not found'}, status=404)
        status_val = request.data.get('status')
        if status_val and status_val in ['Applied', 'Shortlisted', 'Rejected']:
            application.status = status_val
            application.save()
            return Response({'message': 'Status updated'})
        return Response({'error': 'Invalid status'}, status=400)

    def delete(self, request, app_id):
        if not is_admin(request):
            return Response({'error': 'Admin access required'}, status=403)
        try:
            application = Application.objects.get(id=app_id)
        except Application.DoesNotExist:
            return Response({'error': 'Application not found'}, status=404)
        application.delete()
        return Response({'message': 'Application deleted'})


# ──────────────────────────────────────────────────────────────────
# CANDIDATE PROFILES
# ──────────────────────────────────────────────────────────────────

class AdminCandidateProfilesView(CsrfExemptAPIView):
    def get(self, request):
        if not is_admin(request):
            return Response({'error': 'Admin access required'}, status=403)
        profiles = CandidateProfile.objects.all().select_related('user')
        serializer = CandidateProfileSerializer(profiles, many=True)
        return Response(serializer.data)


class AdminCandidateProfileDetailView(CsrfExemptAPIView):
    def patch(self, request, profile_id):
        if not is_admin(request):
            return Response({'error': 'Admin access required'}, status=403)
        try:
            profile = CandidateProfile.objects.get(id=profile_id)
        except CandidateProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)
        serializer = CandidateProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, profile_id):
        if not is_admin(request):
            return Response({'error': 'Admin access required'}, status=403)
        try:
            profile = CandidateProfile.objects.get(id=profile_id)
        except CandidateProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)
        profile.delete()
        return Response({'message': 'Candidate profile deleted'})


# ──────────────────────────────────────────────────────────────────
# EMPLOYER PROFILES
# ──────────────────────────────────────────────────────────────────

class AdminEmployerProfilesView(CsrfExemptAPIView):
    def get(self, request):
        if not is_admin(request):
            return Response({'error': 'Admin access required'}, status=403)
        profiles = EmployerProfile.objects.all().select_related('user')
        serializer = EmployerProfileSerializer(profiles, many=True)
        return Response(serializer.data)


class AdminEmployerProfileDetailView(CsrfExemptAPIView):
    def patch(self, request, profile_id):
        if not is_admin(request):
            return Response({'error': 'Admin access required'}, status=403)
        try:
            profile = EmployerProfile.objects.get(id=profile_id)
        except EmployerProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)
        serializer = EmployerProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, profile_id):
        if not is_admin(request):
            return Response({'error': 'Admin access required'}, status=403)
        try:
            profile = EmployerProfile.objects.get(id=profile_id)
        except EmployerProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)
        profile.delete()
        return Response({'message': 'Employer profile deleted'})
