from django.test import TestCase
from django.urls import reverse, resolve
from ..views import (
    index, about, sections, hospitality, tourism,
    course_details, contact, diplomas, tourism_diplomas,
    hospitality_diplomas, diploma_details
)

class URLTests(TestCase):
    def test_index_url(self):
        """Test index URL"""
        url = reverse('home')
        self.assertEqual(resolve(url).func, index)

    def test_about_url(self):
        """Test about URL"""
        url = reverse('about')
        self.assertEqual(resolve(url).func, about)

    def test_sections_url(self):
        """Test sections URL"""
        url = reverse('sections')
        self.assertEqual(resolve(url).func, sections)

    def test_hospitality_url(self):
        """Test hospitality URL"""
        url = reverse('hospitality')
        self.assertEqual(resolve(url).func, hospitality)

    def test_tourism_url(self):
        """Test tourism URL"""
        url = reverse('tourism')
        self.assertEqual(resolve(url).func, tourism)

    def test_course_details_url(self):
        """Test course details URL"""
        url = reverse('course-details', args=[1])
        self.assertEqual(resolve(url).func, course_details)

    def test_contact_url(self):
        """Test contact URL"""
        url = reverse('contact')
        self.assertEqual(resolve(url).func, contact)

    def test_diplomas_url(self):
        """Test diplomas URL"""
        url = reverse('diplomas')
        self.assertEqual(resolve(url).func, diplomas)

    def test_tourism_diplomas_url(self):
        """Test tourism diplomas URL"""
        url = reverse('tourism-diplomas')
        self.assertEqual(resolve(url).func, tourism_diplomas)

    def test_hospitality_diplomas_url(self):
        """Test hospitality diplomas URL"""
        url = reverse('hospitality-diplomas')
        self.assertEqual(resolve(url).func, hospitality_diplomas)

    def test_diploma_details_url(self):
        """Test diploma details URL"""
        url = reverse('diploma-details', args=[1])
        self.assertEqual(resolve(url).func, diploma_details)