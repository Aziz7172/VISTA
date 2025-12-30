from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Course, Section, Message, Statics, Diploma, LocationDetail


def index(request):
    courses = Course.objects.all().order_by('-created')[:6]
    success = False
    error = None
    # Use the most recent Statics record (by id). If none exist, `numbers` will be None.
    numbers = Statics.objects.order_by('-id').first()
    if request.method == 'POST':
        # basic field extraction (CSRF is enforced by template)
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()

        if not (name and email and subject and message_text):
            error = 'Please fill all required fields.'
        else:
            # enforce max 2 messages per day per email
            today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            msgs_today = Message.objects.filter(email__iexact=email, created__gte=today_start).count()
            if msgs_today >= 2:
                error = 'You have reached the maximum of 2 messages today. Please try again tomorrow.'
            else:
                Message.objects.create(name=name, email=email, subject=subject, message=message_text)
                success = True

    return render(request, 'index.html', {
        'numbers': numbers,
        'courses': courses,
        'success': success,
        'error': error,
        'info': LocationDetail.get_institute_info(),
    })

def about(request):
    return render(request, 'About.html')

def sections(request):
    return render(request, 'sections.html')

def hospitality(request):
    # Get courses that belong to the Hospitality Training section
    hospitality_section = get_object_or_404(Section, slug='hospitality')
    courses = Course.objects.filter(section=hospitality_section).order_by('-created')
    return render(request, 'RESTAURANT.html', {'courses': courses})

def tourism(request):
    # Get courses that belong to the Tourism Training section
    tourism_section = get_object_or_404(Section, slug='tourism')
    courses = Course.objects.filter(section=tourism_section).order_by('-created')
    return render(request, 'TRAVEL.html', {'courses': courses})

def course_details(request, course_id=None):
    course = None
    if course_id:
        course = get_object_or_404(Course, id=course_id)
    return render(request, 'course-details.html', {'course': course})


def hospitality_diplomas(request):
    """Render a list of hospitality-related diplomas."""
    hospitality_section = get_object_or_404(Section, slug='hospitality')
    diplomas = Diploma.objects.filter(section=hospitality_section).order_by('-created')
    return render(request, 'hospitality_diplomas.html', {'diplomas': diplomas})

def tourism_diplomas(request):
    """Render a list of tourism-related diplomas."""
    tourism_section = get_object_or_404(Section, slug='tourism')
    diplomas = Diploma.objects.filter(section=tourism_section).order_by('-created')
    return render(request, 'tourism_diplomas.html', {'diplomas': diplomas})

def diplomas(request):
    """Render a list of all diplomas (landing page)."""
    diplomas = Diploma.objects.all().order_by('-created')
    return render(request, 'diplomas.html', {'diplomas': diplomas})


def diploma_details(request, diploma_id=None):
    diploma = None
    if diploma_id:
        diploma = get_object_or_404(Diploma, id=diploma_id)
    return render(request, 'diploma-details.html', {'diploma': diploma})

from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings

def contact(request):
    success = False
    error = None

    if request.method == 'POST':
        # basic field extraction (CSRF is enforced by template)
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()

        if not (name and email and subject and message_text):
            error = 'Please fill all required fields.'
        else:
            # enforce max 2 messages per day per email
            today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            msgs_today = Message.objects.filter(email__iexact=email, created__gte=today_start).count()
            if msgs_today >= 2:
                error = 'You have reached the maximum of 2 messages today. Please try again tomorrow.'
            else:
                Message.objects.create(name=name, email=email, subject=subject, message=message_text)
                success = True

    return render(request, 'Contact.html', {
        'success': success,
        'error': error,
        'info': LocationDetail.get_institute_info(),
    })
