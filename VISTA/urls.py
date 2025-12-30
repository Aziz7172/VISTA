"""
URL configuration for VISTA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]
from . import views

urlpatterns += [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('sections/', views.sections, name='sections'),
    path('hospitality/', views.hospitality, name='hospitality'),
    path('tourism/', views.tourism, name='tourism'),
    path('diplomas/', views.diplomas, name='diplomas'),
    path('diplomas/hospitality/', views.hospitality_diplomas, name='hospitality-diplomas'),
    path('diplomas/tourism/', views.tourism_diplomas, name='tourism-diplomas'),
    path('course/<int:course_id>/', views.course_details, name='course-details'),
    path('diploma/<int:diploma_id>/', views.diploma_details, name='diploma-details'),
    path('contact/', views.contact, name='contact'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
