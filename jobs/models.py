from django.db import models
from django.core.validators import RegexValidator

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    ROLE_CHOICES = (
        ('candidate', 'Candidate'),
        ('employer', 'Employer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate')

    REQUIRED_FIELDS = ['email']

class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    skills = models.TextField(help_text="Comma separated skills")
    experience = models.IntegerField(help_text="Years of experience", default=0)
    pincode = models.CharField(
        max_length=6,
        validators=[RegexValidator(regex=r'^\d{6}$', message='Pincode must be exactly 6 digits.')]
    )
    city = models.CharField(max_length=100, blank=True, default='')
    phone = models.CharField(
        max_length=10, 
        blank=True, 
        default='', 
        validators=[RegexValidator(regex=r'^\d{10}$', message='Phone number must be exactly 10 digits.')],
        help_text="Contact phone number"
    )
    contact_email = models.EmailField(blank=True, default='', help_text="Contact email for employers")
    about = models.TextField(blank=True, default='', help_text="About the candidate")
    social_links = models.TextField(blank=True, default='', help_text="Portfolio, LinkedIn, GitHub links")

    def __str__(self):
        return self.user.username

class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=255)
    pincode = models.CharField(
        max_length=6,
        validators=[RegexValidator(regex=r'^\d{6}$', message='Pincode must be exactly 6 digits.')]
    )
    city = models.CharField(max_length=100, blank=True, default='')
    contact_name = models.CharField(max_length=255, blank=True, default='', help_text="HR Name")
    contact_phone = models.CharField(
        max_length=10, 
        blank=True, 
        default='', 
        validators=[RegexValidator(regex=r'^\d{10}$', message='Phone number must be exactly 10 digits.')],
        help_text="Contact Number"
    )
    contact_email = models.EmailField(blank=True, default='', help_text="HR Email")
    about = models.TextField(blank=True, default='', help_text="About the company")
    website_links = models.TextField(blank=True, default='', help_text="Company website or social links")
    org_details = models.TextField(blank=True, default='', help_text="Organization size, type, or other details")

    def __str__(self):
        return self.company_name

class Job(models.Model):
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    required_skills = models.TextField(help_text="Comma separated required skills")
    pincode = models.CharField(
        max_length=6,
        validators=[RegexValidator(regex=r'^\d{6}$', message='Pincode must be exactly 6 digits.')]
    )
    city = models.CharField(max_length=100, blank=True, default='')
    salary = models.DecimalField(
        max_digits=12, decimal_places=2,
        help_text="Annual salary in INR (required)"
    )
    is_walk_in = models.BooleanField(default=False, help_text="Whether this job accepts direct walk-ins")
    walk_in_address = models.TextField(blank=True, default='', help_text="Physical address for walk-in candidates")
    expires_at = models.DateTimeField(null=True, blank=True, help_text="Timestamp when the job expires and should be deleted")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    STATUS_CHOICES = (
        ('Applied', 'Applied'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
    )
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    match_score = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.user.username} -> {self.job.title}"
