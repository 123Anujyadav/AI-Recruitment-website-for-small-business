from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.utils import timezone
from datetime import timedelta
from .models import CandidateProfile, EmployerProfile, Job, Application
from .serializers import (
    UserSerializer, CandidateProfileSerializer, EmployerProfileSerializer,
    JobSerializer, ApplicationSerializer
)
from . import ai_services

def delete_expired_jobs():
    """Deletes jobs that have passed their expiration timestamp."""
    expired_jobs = Job.objects.filter(expires_at__lt=timezone.now())
    if expired_jobs.exists():
        expired_jobs.delete()

class WhoAmIView(APIView):
    """Returns current authenticated user's role and username, or 401 if not logged in."""
    permission_classes = [AllowAny]
    def get(self, request):
        if request.user and request.user.is_authenticated:
            return Response({'role': request.user.role, 'username': request.user.username})
        return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # UserSerializer.create() calls create_user() which already hashes the
            # password — calling set_password() again would double-hash it.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Log error for better visibility during testing
        print(f"[ERROR] Registration Invalid: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            # Make sure CSRF token is rotated and provided
            get_token(request)
            return Response({'message': 'Logged in successfully', 'role': user.role})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out'})

class CandidateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if request.user.role != 'candidate':
            return Response({'error': 'Only candidates can view this'}, status=403)
        profile, _ = CandidateProfile.objects.get_or_create(
            user=request.user,
            defaults={'skills': '', 'pincode': '', 'city': '', 'experience': 0}
        )
        serializer = CandidateProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != 'candidate':
            return Response({'error': 'Only candidates can update profile'}, status=403)
        profile, created = CandidateProfile.objects.get_or_create(
            user=request.user,
            defaults={'skills': '', 'pincode': '', 'city': '', 'experience': 0}
        )
        serializer = CandidateProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class MatchedJobsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'candidate':
            return Response({'error': 'Only candidates can view this'}, status=403)
        profile = getattr(request.user, 'candidate_profile', None)
        if not profile:
            return Response({'error': 'Profile not found'}, status=404)
        
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

class AllJobsView(APIView):
    permission_classes = [AllowAny] # Or IsAuthenticated depending on if logged out users can see feed, let's say AllowAny

    def get(self, request):
        delete_expired_jobs()
        city = request.query_params.get('city')
        jobs = Job.objects.all().order_by('-created_at')
        if city:
            jobs = jobs.filter(city__icontains=city)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

class ApplyJobView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'candidate':
            return Response({'error': 'Only candidates can apply'}, status=403)
        job_id = request.data.get('job_id')
        job = Job.objects.filter(id=job_id).first()
        if not job:
            return Response({'error': 'Job not found'}, status=404)
        # Use getattr to avoid RelatedObjectDoesNotExist if profile is missing
        profile = getattr(request.user, 'candidate_profile', None)
        if not profile:
            return Response({'error': 'Candidate profile not found. Please complete your profile first.'}, status=404)

        # ── Step 1: Compute raw skill score (up to 70 pts) ──────────────────
        # Guard against None/empty skills fields
        c_skills = set([s.strip().lower() for s in (profile.skills or '').split(',') if s.strip()])
        j_skills = set([s.strip().lower() for s in (job.required_skills or '').split(',') if s.strip()])
        total_req = len(j_skills)
        matched = len(c_skills.intersection(j_skills))

        skill_score = (matched / total_req) * 70 if total_req > 0 else 70
        is_same_city = str(profile.city).strip().lower() == str(job.city).strip().lower() and profile.city != ''
        city_score = 20 if is_same_city else 0

        # ── Step 2: Determine if THIS candidate is same-pincode ──────────────
        is_same_pincode = str(profile.pincode).strip() == str(job.pincode).strip()
        location_score = 30 if is_same_pincode else 0
        total_score = skill_score + location_score + city_score

        # ── Step 3: Pincode-aware relative ranking ───────────────────────────
        #
        # Rule:  If ANY same-pincode candidate has applied, every out-of-pincode
        #        candidate must rank BELOW ALL same-pincode candidates.
        #
        # How we enforce this:
        #   a) If this candidate is OUT-of-pincode → cap their score just below
        #      the LOWEST same-pincode applicant's score (if one exists).
        #   b) If this candidate IS same-pincode → after saving, re-cap every
        #      existing out-of-pincode applicant whose score is >= this new
        #      candidate's score.

        if not is_same_pincode:
            # All existing same-pincode applications for this job
            same_pincode_apps = Application.objects.filter(
                job=job,
                candidate__pincode=job.pincode
            )
            if same_pincode_apps.exists():
                min_same_score = same_pincode_apps.order_by('match_score').first().match_score
                # Cap out-of-pincode score just below the lowest same-pincode score
                if total_score >= min_same_score:
                    total_score = max(0.0, min_same_score - 0.01)

        # ── Step 4: Save / update this application ───────────────────────────
        app, created = Application.objects.get_or_create(
            candidate=profile,
            job=job,
            defaults={'match_score': total_score}
        )
        if not created:
            app.match_score = total_score
            app.save()

        # ── Step 5: If same-pincode, re-cap existing out-of-pincode applicants ─
        if is_same_pincode:
            # Find all out-of-pincode applicants whose score is >= this candidate's score
            out_of_pincode_apps = Application.objects.filter(
                job=job
            ).exclude(candidate__pincode=job.pincode).exclude(candidate=profile)

            for oop_app in out_of_pincode_apps:
                if oop_app.match_score >= total_score:
                    oop_app.match_score = max(0.0, total_score - 0.01)
                    oop_app.save()

        return Response({
            'message': 'Applied successfully',
            'match_score': round(total_score, 2),
            'pincode_match': is_same_pincode
        })

class EmployerProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.role != 'employer':
            return Response({'error': 'Only employers can view this'}, status=403)
        profile, _ = EmployerProfile.objects.get_or_create(
            user=request.user,
            defaults={'company_name': '', 'pincode': '', 'city': ''}
        )
        serializer = EmployerProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != 'employer':
            return Response({'error': 'Only employers can update profile'}, status=403)
        profile, created = EmployerProfile.objects.get_or_create(
            user=request.user,
            defaults={'company_name': '', 'pincode': '', 'city': ''}
        )
        serializer = EmployerProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class EmployerJobsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'employer':
            return Response({'error': 'Only employers can view this'}, status=403)
        delete_expired_jobs()
        profile, _ = EmployerProfile.objects.get_or_create(
            user=request.user,
            defaults={'company_name': '', 'pincode': '', 'city': ''}
        )
        jobs = Job.objects.filter(employer=profile)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != 'employer':
            return Response({'error': 'Only employers can post jobs'}, status=403)
        profile, _ = EmployerProfile.objects.get_or_create(
            user=request.user,
            defaults={'company_name': '', 'pincode': '', 'city': ''}
        )
        
        timer_value = request.data.get('timer_value')
        timer_unit = request.data.get('timer_unit', 'hours')
        expires_at = None
        
        if timer_value and int(timer_value) > 0:
            val = int(timer_value)
            if timer_unit == 'hours':
                expires_at = timezone.now() + timedelta(hours=val)
            elif timer_unit == 'days':
                expires_at = timezone.now() + timedelta(days=val)
            elif timer_unit == 'months':
                expires_at = timezone.now() + timedelta(days=val * 30)
            
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employer=profile, expires_at=expires_at)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class RankedCandidatesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):
        if request.user.role != 'employer':
            return Response({'error': 'Only employers can view this'}, status=403)
        employer_profile = getattr(request.user, 'employer_profile', None)
        if not employer_profile:
            return Response({'error': 'Employer profile not found'}, status=404)
        job = Job.objects.filter(id=job_id, employer=employer_profile).first()
        if not job:
            return Response({'error': 'Job not found'}, status=404)

        applications = Application.objects.filter(job=job).order_by('-match_score')
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

class CandidateApplicationsView(APIView):
    """Returns the list of jobs this candidate has applied to."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'candidate':
            return Response({'error': 'Only candidates can view this'}, status=403)
        profile = getattr(request.user, 'candidate_profile', None)
        if not profile:
            return Response([], status=200)
        applications = Application.objects.filter(candidate=profile).order_by('-created_at').select_related('job', 'job__employer')
        data = []
        for app in applications:
            data.append({
                'application_id': app.id,
                'job_id': app.job.id,
                'job_title': app.job.title,
                'company_name': app.job.employer.company_name,
                'pincode': app.job.pincode,
                'salary': str(app.job.salary),
                'match_score': round(app.match_score, 2),
                'status': app.status,
                'applied_at': app.created_at.strftime('%d %b %Y'),
                'contact_name': app.job.employer.contact_name if app.status == 'Shortlisted' else None,
                'contact_phone': app.job.employer.contact_phone if app.status == 'Shortlisted' else None,
                'contact_email': app.job.employer.contact_email if app.status == 'Shortlisted' else None,
                'website_links': app.job.employer.website_links if app.status == 'Shortlisted' else None,
            })
        return Response(data)

class PublicEmployerProfileView(APIView):
    """Returns public employer details for a specific job. Hides contact details unless the candidate is shortlisted."""
    permission_classes = [AllowAny]

    def get(self, request, job_id):
        job = Job.objects.filter(id=job_id).first()
        if not job:
            return Response({'error': 'Job not found'}, status=404)
            
        is_shortlisted = False
        if request.user and request.user.is_authenticated:
            # If candidate, check if they are shortlisted for this job
            if hasattr(request.user, 'candidate_profile'):
                app = Application.objects.filter(job=job, candidate=request.user.candidate_profile).first()
                if app and app.status == 'Shortlisted':
                    is_shortlisted = True
            # If same employer, show everything
            elif hasattr(request.user, 'employer_profile'):
                if job.employer == request.user.employer_profile:
                    is_shortlisted = True

        emp = job.employer
        data = {
            'company_name': emp.company_name,
            'pincode': emp.pincode,
            'city': emp.city,
            'about': emp.about,
            'website_links': emp.website_links,
            'org_details': emp.org_details,
        }

        if is_shortlisted:
            data['contact_name'] = emp.contact_name
            data['contact_phone'] = emp.contact_phone
            data['contact_email'] = emp.contact_email

        return Response(data)


class ApplicationStatusView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, app_id):
        if request.user.role != 'employer':
            return Response({'error': 'Only employers can update application status'}, status=403)
        employer_profile = getattr(request.user, 'employer_profile', None)
        if not employer_profile:
            return Response({'error': 'Employer profile not found'}, status=404)
        application = Application.objects.filter(id=app_id, job__employer=employer_profile).first()
        if not application:
            return Response({'error': 'Application not found'}, status=404)

        new_status = request.data.get('status')
        if new_status in ['Applied', 'Shortlisted', 'Rejected']:
            application.status = new_status
            application.save()
            return Response({'message': 'Status updated'})
        return Response({'error': 'Invalid status'}, status=400)


class EditJobView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):
        if request.user.role != 'employer':
            print(f"DEBUG: 403 Forbidden - User {request.user.username} role is {request.user.role}")
            return Response({'error': 'Only employers can edit jobs'}, status=403)
        profile = getattr(request.user, 'employer_profile', None)
        if not profile:
            return Response({'error': 'Employer profile not found'}, status=404)
        job = Job.objects.filter(id=job_id, employer=profile).first()
        if not job:
            return Response({'error': 'Job not found or you do not own this job'}, status=404)
        serializer = JobSerializer(job)
        return Response(serializer.data)

    def patch(self, request, job_id):
        if request.user.role != 'employer':
            print(f"DEBUG: 403 Forbidden - User {request.user.username} role is {request.user.role}")
            return Response({'error': 'Only employers can edit jobs'}, status=403)
        profile = getattr(request.user, 'employer_profile', None)
        if not profile:
            return Response({'error': 'Employer profile not found'}, status=404)
        job = Job.objects.filter(id=job_id, employer=profile).first()
        if not job:
            return Response({'error': 'Job not found or you do not own this job'}, status=404)
            
        timer_value = request.data.get('timer_value')
        timer_unit = request.data.get('timer_unit', 'hours')
        if timer_value is not None:
            if int(timer_value) > 0:
                val = int(timer_value)
                if timer_unit == 'hours':
                    job.expires_at = timezone.now() + timedelta(hours=val)
                elif timer_unit == 'days':
                    job.expires_at = timezone.now() + timedelta(days=val)
                elif timer_unit == 'months':
                    job.expires_at = timezone.now() + timedelta(days=val * 30)
            else:
                job.expires_at = None
            job.save()

        serializer = JobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, job_id):
        if request.user.role != 'employer':
            print(f"DEBUG: 403 Forbidden - User {request.user.username} role is {request.user.role}")
            return Response({'error': 'Only employers can delete jobs'}, status=403)
        profile = getattr(request.user, 'employer_profile', None)
        if not profile:
            return Response({'error': 'Employer profile not found'}, status=404)
        job = Job.objects.filter(id=job_id, employer=profile).first()
        if not job:
            return Response({'error': 'Job not found or you do not own this job'}, status=404)
        job.delete()
        return Response({'message': 'Job deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class AISalaryAssessmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):
        if request.user.role != 'candidate':
            return Response({'error': 'Only candidates can view this'}, status=403)
        
        job = Job.objects.filter(id=job_id).first()
        if not job:
            return Response({'error': 'Job not found'}, status=404)
            
        profile = getattr(request.user, 'candidate_profile', None)
        if not profile:
            return Response({'error': 'Candidate profile not found'}, status=404)
            
        assessment = ai_services.assess_salary(
            job_title=job.title,
            job_skills=job.required_skills,
            job_location=job.pincode,
            job_salary=str(job.salary),
            candidate_skills=profile.skills,
            candidate_exp=profile.experience
        )
        
        return Response(assessment)


class AILearningPathView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):
        if request.user.role != 'candidate':
            return Response({'error': 'Only candidates can generate learning paths'}, status=403)
            
        job = Job.objects.filter(id=job_id).first()
        if not job:
            return Response({'error': 'Job not found'}, status=404)
            
        profile = getattr(request.user, 'candidate_profile', None)
        if not profile:
            return Response({'error': 'Candidate profile not found'}, status=404)
            
        learning_path = ai_services.generate_learning_path(
            job_title=job.title,
            job_skills=job.required_skills,
            candidate_skills=profile.skills
        )
        
        return Response(learning_path)

import PyPDF2

class AIResumeAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'candidate':
            return Response({"error": "Only candidates can upload resumes."}, status=status.HTTP_403_FORBIDDEN)

        try:
            profile = getattr(request.user, 'candidate_profile')
        except AttributeError:
            return Response({"error": "Candidate profile not found."}, status=status.HTTP_404_NOT_FOUND)

        resume_file = request.FILES.get('resume_file')
        
        if resume_file:
            # Handle PDF extraction
            try:
                reader = PyPDF2.PdfReader(resume_file)
                extracted_text = ""
                for page in reader.pages:
                    extracted_text += page.extract_text() or ""
                
                # Check if we successfully extracted anything
                if not extracted_text.strip():
                     return Response({"error": "No parseable text found in PDF."}, status=status.HTTP_400_BAD_REQUEST)

                profile.resume_file = resume_file
                profile.resume_text = extracted_text
            except Exception as e:
                 return Response({"error": f"Failed to read PDF. Ensure it is a valid PDF document. Details: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "No resume file provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Analyze extracted text
        analysis = ai_services.analyze_resume(profile.resume_text)
        if "error" in analysis and "status" in analysis and analysis["status"] == "Error":
            # Some error happened in ai service
            return Response({"error": analysis["message"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        profile.resume_parsed_skills = analysis.get("skills", "")
        profile.resume_experience = analysis.get("experience_years", 0)
        profile.resume_ats_score = analysis.get("ats_score", 0.0)
        profile.resume_summary = analysis.get("summary", "")
        profile.save()

        return Response({
            "message": "Resume analyzed successfully",
            "skills": profile.resume_parsed_skills,
            "experience": profile.resume_experience,
            "ats_score": profile.resume_ats_score,
            "summary": profile.resume_summary
        }, status=status.HTTP_200_OK)
