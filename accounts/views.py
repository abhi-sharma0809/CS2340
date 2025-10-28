from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db import models
from .models import Profile, RecruiterProfile, Message, EmailLog
from .forms import ProfileForm, RecruiterRegistrationForm, RecruiterProfileForm, JobSeekerRegistrationForm
from django.contrib.auth.models import User

def signup(request):
    if request.method == "POST":
        form = JobSeekerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create profile with default location (empty is fine for job seekers)
            Profile.objects.get_or_create(
                user=user,
                defaults={'location': ''}
            )
            login(request, user)
            return redirect("accounts:profile")
    else:
        form = JobSeekerRegistrationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def view_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    # Ensure location is set for recruiters
    if profile.user_type == 'recruiter' and not profile.location:
        profile.location = 'N/A - Recruiter'
        profile.save()
    return render(request, "accounts/profile_detail.html", {"profile": profile})

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    # Ensure location is set for recruiters
    if profile.user_type == 'recruiter' and not profile.location:
        profile.location = 'N/A - Recruiter'
        profile.save()
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "accounts/profile_form.html", {"form": form})

def public_profile(request, username):
    owner = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=owner)
    # Ensure location is set for recruiters
    if profile.user_type == 'recruiter' and not profile.location:
        profile.location = 'N/A - Recruiter'
        profile.save()
    if not profile.is_public and request.user != owner:
        return HttpResponseForbidden("This profile is private.")
    return render(request, "accounts/public_profile.html", {"owner": owner, "profile": profile})

def recruiter_signup(request):
    """Registration form specifically for recruiters"""
    if request.method == "POST":
        form = RecruiterRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create profile with recruiter type and default location
            profile, _ = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'user_type': 'recruiter',
                    'location': 'N/A - Recruiter'
                }
            )
            # Ensure location is set even if profile already existed
            if not profile.location:
                profile.location = 'N/A - Recruiter'
                profile.save()
            login(request, user)
            messages.success(request, "Welcome! Please complete your company profile.")
            return redirect("accounts:recruiter_profile")
        else:
            # Form is not valid, show errors
            messages.error(request, "Please correct the errors below.")
    else:
        form = RecruiterRegistrationForm()
    return render(request, "registration/recruiter_signup.html", {"form": form})

@login_required
def recruiter_profile(request):
    """View and edit recruiter company profile"""
    try:
        recruiter_profile = request.user.recruiter_profile
    except RecruiterProfile.DoesNotExist:
        recruiter_profile = None
    
    if request.method == "POST":
        if recruiter_profile:
            form = RecruiterProfileForm(request.POST, instance=recruiter_profile)
        else:
            form = RecruiterProfileForm(request.POST)
        
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Company profile updated successfully!")
            return redirect("accounts:recruiter_profile")
    else:
        if recruiter_profile:
            form = RecruiterProfileForm(instance=recruiter_profile)
        else:
            form = RecruiterProfileForm()
    
    return render(request, "accounts/recruiter_profile.html", {
        "form": form,
        "recruiter_profile": recruiter_profile
    })

@login_required
def recruiter_dashboard(request):
    """Main dashboard for recruiters"""
    # Check if user is a recruiter
    try:
        profile = Profile.objects.get(user=request.user)
        if not profile.is_recruiter:
            messages.error(request, "Access denied. This area is for recruiters only.")
            return redirect("core:home")
    except Profile.DoesNotExist:
        messages.error(request, "Please complete your profile setup.")
        return redirect("accounts:profile")
    
    # Get recruiter profile
    try:
        recruiter_profile = request.user.recruiter_profile
    except RecruiterProfile.DoesNotExist:
        recruiter_profile = None
    
    # Get recruiter's jobs (for now, all jobs since we don't have job ownership yet)
    from jobs.models import Job, JobApplication
    jobs = Job.objects.all().order_by('-created_at')[:10]  # Recent jobs
    total_applications = JobApplication.objects.count()
    
    return render(request, "accounts/recruiter_dashboard.html", {
        "recruiter_profile": recruiter_profile,
        "jobs": jobs,
        "total_applications": total_applications
    })


# Communication Views (CRM-22 & CRM-23)

@login_required
def send_message(request, recipient_id):
    """Send an in-platform message to a candidate (CRM-22)"""
    recipient = get_object_or_404(User, id=recipient_id)
    
    # Check if sender is a recruiter
    try:
        sender_profile = Profile.objects.get(user=request.user)
        if not sender_profile.is_recruiter:
            return JsonResponse({'error': 'Only recruiters can send messages'}, status=403)
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)
    
    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        body = request.POST.get('body', '').strip()
        job_application_id = request.POST.get('job_application_id')
        
        if not subject or not body:
            return JsonResponse({'error': 'Subject and body are required'}, status=400)
        
        # Create message
        message = Message.objects.create(
            sender=request.user,
            recipient=recipient,
            subject=subject,
            body=body
        )
        
        # Link to job application if provided
        if job_application_id:
            try:
                from jobs.models import JobApplication
                job_app = JobApplication.objects.get(id=job_application_id)
                message.job_application = job_app
                message.save()
            except JobApplication.DoesNotExist:
                pass
        
        return JsonResponse({
            'success': True,
            'message': 'Message sent successfully',
            'message_id': message.id
        })
    
    return JsonResponse({'error': 'POST method required'}, status=405)


@login_required
def send_email(request, recipient_id):
    """Send an email to a candidate through the platform (CRM-23)"""
    recipient = get_object_or_404(User, id=recipient_id)
    
    # Check if sender is a recruiter
    try:
        sender_profile = Profile.objects.get(user=request.user)
        if not sender_profile.is_recruiter:
            return JsonResponse({'error': 'Only recruiters can send emails'}, status=403)
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)
    
    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        body = request.POST.get('body', '').strip()
        job_application_id = request.POST.get('job_application_id')
        
        if not subject or not body:
            return JsonResponse({'error': 'Subject and body are required'}, status=400)
        
        if not recipient.email:
            return JsonResponse({'error': 'Recipient has no email address'}, status=400)
        
        # Create email log entry
        email_log = EmailLog.objects.create(
            sender=request.user,
            recipient_email=recipient.email,
            recipient_name=f"{recipient.first_name} {recipient.last_name}".strip() or recipient.username,
            subject=subject,
            body=body,
            status='pending'
        )
        
        # Link to job application if provided
        if job_application_id:
            try:
                from jobs.models import JobApplication
                job_app = JobApplication.objects.get(id=job_application_id)
                email_log.job_application = job_app
                email_log.save()
            except JobApplication.DoesNotExist:
                pass
        
        # Send the actual email
        try:
            send_mail(
                subject=f"[GT Job Finder] {subject}",
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            email_log.status = 'sent'
            email_log.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Email sent successfully',
                'email_id': email_log.id
            })
        except Exception as e:
            email_log.status = 'failed'
            email_log.error_message = str(e)
            email_log.save()
            
            return JsonResponse({
                'error': f'Failed to send email: {str(e)}'
            }, status=500)
    
    return JsonResponse({'error': 'POST method required'}, status=405)


@login_required
def get_messages(request):
    """Get messages for the current user"""
    user_messages = Message.objects.filter(
        models.Q(sender=request.user) | models.Q(recipient=request.user)
    ).order_by('-timestamp')[:50]  # Limit to recent 50 messages
    
    messages_data = []
    for msg in user_messages:
        messages_data.append({
            'id': msg.id,
            'sender': msg.sender.username,
            'recipient': msg.recipient.username,
            'subject': msg.subject,
            'body': msg.body,
            'timestamp': msg.timestamp.isoformat(),
            'is_read': msg.is_read,
            'is_sent_by_me': msg.sender == request.user,
            'job_title': msg.job_application.job.title if msg.job_application else None
        })
    
    return JsonResponse({'messages': messages_data})


@login_required
def get_emails(request):
    """Get emails sent by the current user (recruiters only)"""
    try:
        sender_profile = Profile.objects.get(user=request.user)
        if not sender_profile.is_recruiter:
            return JsonResponse({'error': 'Only recruiters can view email logs'}, status=403)
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)
    
    emails = EmailLog.objects.filter(sender=request.user).order_by('-timestamp')[:50]
    
    emails_data = []
    for email in emails:
        emails_data.append({
            'id': email.id,
            'recipient_email': email.recipient_email,
            'recipient_name': email.recipient_name,
            'subject': email.subject,
            'body': email.body,
            'timestamp': email.timestamp.isoformat(),
            'status': email.status,
            'job_title': email.job_application.job.title if email.job_application else None
        })
    
    return JsonResponse({'emails': emails_data})


@login_required
def mark_message_read(request, message_id):
    """Mark a message as read"""
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    message.is_read = True
    message.save()
    
    return JsonResponse({'success': True})


@login_required
def messages_page(request):
    """Display messages page for job seekers"""
    return render(request, "accounts/messages.html")


@login_required
def recruiter_messages_page(request):
    """Display messages page for recruiters"""
    return render(request, "accounts/recruiter_messages.html")


@login_required
def send_reply(request):
    """Send a reply to a message (job seekers can reply to recruiters)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        import json
        data = json.loads(request.body)
        
        recipient_username = data.get('recipient_username', '').strip()
        subject = data.get('subject', '').strip()
        body = data.get('body', '').strip()
        job_application_id = data.get('job_application_id')
        
        if not recipient_username or not subject or not body:
            return JsonResponse({'error': 'Recipient, subject, and body are required'}, status=400)
        
        # Get recipient user
        try:
            recipient = User.objects.get(username=recipient_username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Recipient not found'}, status=404)
        
        # Create message
        message = Message.objects.create(
            sender=request.user,
            recipient=recipient,
            subject=subject,
            body=body
        )
        
        # Link to job application if provided
        if job_application_id:
            try:
                from jobs.models import JobApplication
                job_app = JobApplication.objects.get(id=job_application_id)
                message.job_application = job_app
                message.save()
            except JobApplication.DoesNotExist:
                pass
        
        return JsonResponse({
            'success': True,
            'message': 'Reply sent successfully',
            'message_id': message.id
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
