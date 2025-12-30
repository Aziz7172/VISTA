from django.test import TestCase, Client
from django.urls import reverse
from django.utils import translation
from ..models import Course, Section, LocationDetail, Message, Diploma

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test data
        self.tourism_section = Section.objects.create(
            name_en="Tourism",
            name_ar="سياحة",
            slug="tourism"
        )
        self.hospitality_section = Section.objects.create(
            name_en="Hospitality",
            name_ar="ضيافة",
            slug="hospitality"
        )
        
        self.course = Course.objects.create(
            section=self.tourism_section,
            title_en="Test Course",
            title_ar="دورة اختبار",
            description_en="Test description",
            description_ar="وصف اختبار"
        )
        
        self.tourism_diploma = Diploma.objects.create(
            section=self.tourism_section,
            title_en="Tourism Test Diploma",
            title_ar="دبلوم اختبار سياحة",
            description_en="Test tourism diploma description",
            description_ar="وصف دبلوم اختبار سياحة"
        )
        
        self.hospitality_diploma = Diploma.objects.create(
            section=self.hospitality_section,
            title_en="Hospitality Test Diploma",
            title_ar="دبلوم اختبار ضيافة",
            description_en="Test hospitality diploma description",
            description_ar="وصف دبلوم اختبار ضيافة"
        )

        self.info = LocationDetail.objects.create(
            phone_1="123456789",
            email="test@example.com",
            address_en="Test Address",
            address_ar="عنوان اختبار",
            is_active=True
        )

    def test_index_view(self):
        """Test index view"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertIn('courses', response.context)
        self.assertIn('info', response.context)
        self.assertEqual(response.context['info'], self.info)

    def test_contact_view(self):
        """Test contact view"""
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Contact.html')
        self.assertIn('info', response.context)
        self.assertEqual(response.context['info'], self.info)

    def test_contact_form_submission(self):
        """Test contact form submission"""
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test Message'
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Message.objects.filter(email='test@example.com').exists())

    def test_tourism_view(self):
        """Test tourism view"""
        response = self.client.get(reverse('tourism'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'TRAVEL.html')
        self.assertIn('courses', response.context)
        self.assertQuerySetEqual(
            response.context['courses'],
            Course.objects.filter(section__slug='tourism'),
            transform=lambda x: x
        )

    def test_hospitality_view(self):
        """Test hospitality view"""
        response = self.client.get(reverse('hospitality'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'RESTAURANT.html')

    def test_course_details_view(self):
        """Test course details view"""
        response = self.client.get(reverse('course-details', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course-details.html')
        self.assertEqual(response.context['course'], self.course)

    def test_language_switch(self):
        """Test language switching"""
        # Test English
        response = self.client.post(reverse('set_language'), data={'language': 'en'})
        self.assertEqual(response.status_code, 302)  # Should redirect
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'VISTA')
        self.assertContains(response, self.course.title_en)

        # Test Arabic
        response = self.client.post(reverse('set_language'), data={'language': 'ar'})
        self.assertEqual(response.status_code, 302)  # Should redirect
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'فيستا')
        self.assertContains(response, self.course.title_ar)

    def test_diplomas_view(self):
        """Test diplomas view"""
        response = self.client.get(reverse('diplomas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'diplomas.html')
        self.assertIn('diplomas', response.context)
        self.assertIn(self.tourism_diploma, response.context['diplomas'])

    def test_tourism_diplomas_view(self):
        """Test tourism diplomas view"""
        response = self.client.get(reverse('tourism-diplomas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tourism_diplomas.html')
        self.assertIn('diplomas', response.context)

    def test_hospitality_diplomas_view(self):
        """Test hospitality diplomas view"""
        response = self.client.get(reverse('hospitality-diplomas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hospitality_diplomas.html')
        self.assertIn('diplomas', response.context)

    def test_diploma_details_view(self):
        """Test diploma details view"""
        response = self.client.get(reverse('diploma-details', args=[self.tourism_diploma.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'diploma-details.html')
        self.assertEqual(response.context['diploma'], self.tourism_diploma)