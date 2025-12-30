from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from ..models import Course, Section, LocationDetail, Message, Diploma

class ModelTests(TestCase):
    def setUp(self):
        """Set up test data"""
        # Create a section
        self.section = Section.objects.create(
            name_en="Tourism",
            name_ar="سياحة",
            slug="tourism"
        )
        
        # Create a course
        self.course = Course.objects.create(
            section=self.section,
            title_en="Test Course",
            title_ar="دورة اختبار",
            description_en="Test description",
            description_ar="وصف اختبار"
        )
        
        # Create a diploma
        self.diploma = Diploma.objects.create(
            section=self.section,
            title_en="Test Diploma",
            title_ar="دبلوم اختبار",
            description_en="Test diploma description",
            description_ar="وصف دبلوم اختبار"
        )

    def test_section_str(self):
        """Test Section string representation"""
        self.assertEqual(str(self.section), "Tourism")

    def test_course_str(self):
        """Test Course string representation"""
        self.assertEqual(str(self.course), "Test Course")

    def test_course_short_description(self):
        """Test Course short description"""
        self.assertEqual(
            self.course.short_description(lang='en'),
            "Test description"
        )
        self.assertEqual(
            self.course.short_description(lang='ar'),
            "وصف اختبار"
        )

    def test_diploma_str(self):
        """Test Diploma string representation"""
        self.assertEqual(str(self.diploma), "Test Diploma")

    def test_diploma_short_description(self):
        """Test Diploma short description"""
        self.assertEqual(
            self.diploma.short_description(lang='en'),
            "Test diploma description"
        )
        self.assertEqual(
            self.diploma.short_description(lang='ar'),
            "وصف دبلوم اختبار"
        )

class LocationDetailTests(TestCase):
    def test_get_institute_info_creates_default(self):
        """Test get_institute_info creates default if none exists"""
        self.assertEqual(LocationDetail.objects.count(), 0)
        info = LocationDetail.get_institute_info()
        self.assertEqual(LocationDetail.objects.count(), 1)
        self.assertTrue(info.is_active)

    def test_only_one_active_record(self):
        """Test that only one record can be active at a time"""
        # Create first record
        info1 = LocationDetail.objects.create(
            phone_1="123",
            email="test1@example.com",
            is_active=True
        )
        
        # Create second record
        info2 = LocationDetail.objects.create(
            phone_1="456",
            email="test2@example.com",
            is_active=True
        )
        
        # Refresh from database
        info1.refresh_from_db()
        info2.refresh_from_db()
        
        # Check that only info2 is active
        self.assertFalse(info1.is_active)
        self.assertTrue(info2.is_active)

    def test_get_institute_info_returns_active(self):
        """Test get_institute_info returns the active record"""
        # Create two records
        LocationDetail.objects.create(
            phone_1="123",
            email="old@example.com",
            is_active=False
        )
        active = LocationDetail.objects.create(
            phone_1="456",
            email="active@example.com",
            is_active=True
        )
        
        info = LocationDetail.get_institute_info()
        self.assertEqual(info, active)
        self.assertEqual(info.email, "active@example.com")