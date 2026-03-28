from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, WhoAmIView,
    CandidateProfileView, MatchedJobsView, ApplyJobView, AllJobsView,
    EmployerProfileView, EmployerJobsView, RankedCandidatesView, ApplicationStatusView,
    EditJobView, AISalaryAssessmentView, AILearningPathView, CandidateApplicationsView
)

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('whoami', WhoAmIView.as_view()),
    path('jobs/feed', AllJobsView.as_view()),
    # Candidate APIs
    path('candidate/profile', CandidateProfileView.as_view()),
    path('candidate/matched-jobs', MatchedJobsView.as_view()),
    path('candidate/apply', ApplyJobView.as_view()),
    path('candidate/applications', CandidateApplicationsView.as_view()),
    path('candidate/job/<int:job_id>/salary-check', AISalaryAssessmentView.as_view()),
    path('candidate/job/<int:job_id>/learning-path', AILearningPathView.as_view()),
    # Employer APIs
    path('employer/profile', EmployerProfileView.as_view()),   # extra for completeness
    path('employer/job', EmployerJobsView.as_view()),          # post new job
    path('employer/jobs', EmployerJobsView.as_view()),         # get posted jobs
    path('employer/job/<int:job_id>/ranked-candidates', RankedCandidatesView.as_view()),
    path('employer/application/<int:app_id>/status', ApplicationStatusView.as_view()),
    path('employer/job/<int:job_id>/edit', EditJobView.as_view()),
]
