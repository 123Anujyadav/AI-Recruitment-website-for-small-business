from django.urls import path
from .admin_views import (
    AdminLoginView, AdminLogoutView, AdminCheckView, AdminStatsView,
    AdminUsersView, AdminUserDetailView,
    AdminJobsView, AdminJobDetailView,
    AdminApplicationsView, AdminApplicationDetailView,
    AdminCandidateProfilesView, AdminCandidateProfileDetailView,
    AdminEmployerProfilesView, AdminEmployerProfileDetailView,
)

urlpatterns = [
    # Auth
    path('login', AdminLoginView.as_view()),
    path('logout', AdminLogoutView.as_view()),
    path('check', AdminCheckView.as_view()),

    # Dashboard stats
    path('stats', AdminStatsView.as_view()),

    # Users
    path('users', AdminUsersView.as_view()),
    path('users/<int:user_id>', AdminUserDetailView.as_view()),

    # Jobs
    path('jobs', AdminJobsView.as_view()),
    path('jobs/<int:job_id>', AdminJobDetailView.as_view()),

    # Applications
    path('applications', AdminApplicationsView.as_view()),
    path('applications/<int:app_id>', AdminApplicationDetailView.as_view()),

    # Candidate Profiles
    path('candidates', AdminCandidateProfilesView.as_view()),
    path('candidates/<int:profile_id>', AdminCandidateProfileDetailView.as_view()),

    # Employer Profiles
    path('employers', AdminEmployerProfilesView.as_view()),
    path('employers/<int:profile_id>', AdminEmployerProfileDetailView.as_view()),
]
