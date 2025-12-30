from django.contrib import admin
from .models import Course, Section
from .models import LocationDetail, Message, Statics, Diploma
from django.utils.html import format_html




admin.site.register(Message)
admin.site.register(Statics)
admin.site.register(Diploma)





@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_preview', 'title_en', 'title_ar', 'section', 'created')
    list_filter = ('section',)
    search_fields = ('title_en', 'title_ar')
    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto;"/>', obj.image.url)
        return format_html('<img src="{}" style="width: 100px; height: auto;"/>', '/static/images/meeting-01.jpg')

    thumbnail_preview.short_description = 'Thumbnail'


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_ar', 'slug')
    prepopulated_fields = {'slug': ('name_en',)}


@admin.register(LocationDetail)
class LocationDetailAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'phone_1')
    fieldsets = (
        ('Contact Information', {
            'fields': ('email', ('phone_1', 'phone_2', 'phone_3'))
        }),
        ('Address', {
            'fields': ('address_en', 'address_ar')
        }),
        ('Social Media', {
            'fields': ('facebook', 'instagram')
        }),
    )

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of the last LocationDetail instance."""
        return LocationDetail.objects.count() > 1

    def get_readonly_fields(self, request, obj=None):
        """Make created field readonly."""
        if obj:  # Editing an existing object
            return ['created']
        return []

    def save_model(self, request, obj, form, change):
        """Set older records as inactive when saving a new one."""
        if not change:  # If this is a new object
            LocationDetail.objects.update(is_active=False)
            obj.is_active = True
        super().save_model(request, obj, form, change)
