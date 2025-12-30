from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.utils import timezone
class Statics(models.Model):
    num1 = models.IntegerField(_('New Students'),blank=True)
    num2 = models.IntegerField(_('Succesed Students'),blank=True)
    num3 = models.IntegerField(_('Current Teachers'),blank=True)
    num4 = models.IntegerField(_('Awards'),blank=True)

class Course(models.Model):
    section = models.ForeignKey('Section', on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    title_en = models.CharField(_('Title (EN)'), max_length=200)
    title_ar = models.CharField(_('Title (AR)'), max_length=200, blank=True)
    description_en = models.TextField(_('Description (EN)'), blank=True)
    def en_description_with_breaks(self):
        return format_html(self.description_en.replace('\n', '<br>'))
    description_ar = models.TextField(_('Description (AR)'), blank=True)
    def ar_description_with_breaks(self):
        return format_html(self.description_ar.replace('\n', '<br>'))
    image = models.ImageField(_('Thumbnail'), upload_to='course_thumbs/', null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_en

    def short_description(self, lang='en', words=5):
        """Return the first `words` words of the description for the given language."""
        text = self.description_en if lang == 'en' else (self.description_ar or self.description_en)
        parts = text.split()
        if len(parts) <= words:
            return text
        return ' '.join(parts[:words]) + '...'
    @property
    def short_description_text(self):
        from django.utils import translation
        lang = translation.get_language()[:2]
        return self.short_description(lang=lang)

    def image_url(self):
        """Return the image URL if set, otherwise None (template will fallback to static)."""
        if self.image:
            return self.image.url
        return None





class Diploma(models.Model):
    section = models.ForeignKey('Section', on_delete=models.SET_NULL, null=True, blank=True, related_name='diploma')
    title_en = models.CharField(_('Title (EN)'), max_length=200)
    title_ar = models.CharField(_('Title (AR)'), max_length=200, blank=True)
    description_en = models.TextField(_('Description (EN)'), blank=True)
    def en_description_with_breaks(self):
        return format_html(self.description_en.replace('\n', '<br>'))
    description_ar = models.TextField(_('Description (AR)'), blank=True)
    def ar_description_with_breaks(self):
        return format_html(self.description_ar.replace('\n', '<br>'))
    image = models.ImageField(_('Thumbnail'), upload_to='diploma_thumbs/', null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_en

    def short_description(self, lang='en', words=5):
        """Return the first `words` words of the description for the given language."""
        text = self.description_en if lang == 'en' else (self.description_ar or self.description_en)
        parts = text.split()
        if len(parts) <= words:
            return text
        return ' '.join(parts[:words]) + '...'
    @property
    def short_description_text(self):
        from django.utils import translation
        lang = translation.get_language()[:2]
        return self.short_description(lang=lang)

    def image_url(self):
        """Return the image URL if set, otherwise None (template will fallback to static)."""
        if self.image:
            return self.image.url
        return None


class Section(models.Model):
    """A department or section (e.g. Hotel, Travel) to which courses belong."""
    name_en = models.CharField(_('Name (EN)'), max_length=100)
    name_ar = models.CharField(_('Name (AR)'), max_length=100, blank=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')

    def __str__(self):
        return self.name_en


class LocationDetail(models.Model):
    """Institute contact details and location information."""
    phone_1 = models.CharField(_('Phone 1'), max_length=30, blank=True)
    phone_2 = models.CharField(_('Phone 2'), max_length=30, blank=True)
    phone_3 = models.CharField(_('Phone 3'), max_length=30, blank=True)
    email = models.EmailField(_('Email'), blank=True)
    address_en = models.CharField(_('Address (EN)'), max_length=255, blank=True)
    address_ar = models.CharField(_('Address (AR)'), max_length=255, blank=True)
    facebook = models.URLField(_('Facebook URL'), blank=True)
    instagram = models.URLField(_('Instagram URL'), blank=True)
    is_active = models.BooleanField(_('Active'), default=True, help_text=_('Only the most recent active record will be displayed'))
    created = models.DateTimeField(_('Created'), default=timezone.now)

    class Meta:
        verbose_name = _('Institute Information')
        verbose_name_plural = _('Institute Information')

    def __str__(self):
        return str(_('Institute Contact Information'))

    def save(self, *args, **kwargs):
        if self.is_active:
            # Deactivate all other records
            LocationDetail.objects.exclude(id=self.id).update(is_active=False)
        super().save(*args, **kwargs)

    @classmethod
    def get_institute_info(cls):
        """Get the active institute information (creates default if none exists)."""
        info = cls.objects.filter(is_active=True).first()
        if info is None:
            info = cls.objects.create(is_active=True)
        return info



class Message(models.Model):
    name = models.CharField(_('Name'), max_length=200)
    email = models.EmailField(_('Email'), max_length=254)
    subject = models.CharField(_('Subject'), max_length=200)
    message = models.TextField(_('Message'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Message from {self.name} <{self.email}> on {self.created:%Y-%m-%d %H:%M}"