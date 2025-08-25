# academics/admin.py
from django.contrib import admin
from .models import Academics

@admin.register(Academics)
class AcademicsAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'subject_name', 
        'subject_code',
        'get_department_display', 
        'year', 
        'resource_type', 
        'uploaded_at', 
        'views', 
        'is_active'
    ]
    
    list_filter = [
        'resource_type', 
        'is_active', 
        'uploaded_at', 
        'department', 
        'year'
    ]
    
    search_fields = [
        'title', 
        'description', 
        'subject_name', 
        'subject_code', 
        'tags'
    ]
    
    readonly_fields = ['views', 'uploaded_at', 'updated_at']
    list_editable = ['is_active']
    ordering = ['-uploaded_at']
    list_per_page = 25
    date_hierarchy = 'uploaded_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'resource_type')
        }),
        ('Academic Details', {
            'fields': ('department', 'year', 'subject_name', 'subject_code'),
            'description': 'Specify the academic context for this resource'
        }),
        ('Content', {
            'fields': ('file', 'external_link', 'tags'),
            'description': 'Upload a file or provide an external link'
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Statistics', {
            'fields': ('views', 'uploaded_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Automatically tracked information'
        }),
    )
    
    def get_department_display(self, obj):
        """Display full department name instead of code"""
        return obj.get_department_display_name()
    get_department_display.short_description = 'Department'
    get_department_display.admin_order_field = 'department'
    
    def get_queryset(self, request):
        """Optimize queries"""
        return super().get_queryset(request)
    
    def save_model(self, request, obj, form, change):
        """Custom save logic if needed"""
        super().save_model(request, obj, form, change)
    
    # Add custom actions
    actions = ['mark_as_active', 'mark_as_inactive', 'reset_view_count']
    
    def mark_as_active(self, request, queryset):
        """Mark selected resources as active"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} resources marked as active.')
    mark_as_active.short_description = "Mark selected resources as active"
    
    def mark_as_inactive(self, request, queryset):
        """Mark selected resources as inactive"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} resources marked as inactive.')
    mark_as_inactive.short_description = "Mark selected resources as inactive"
    
    def reset_view_count(self, request, queryset):
        """Reset view count for selected resources"""
        updated = queryset.update(views=0)
        self.message_user(request, f'View count reset for {updated} resources.')
    reset_view_count.short_description = "Reset view count"

# Optional: Custom admin site configuration
admin.site.site_header = "Academic Resources Admin"
admin.site.site_title = "Academic Resources"
admin.site.index_title = "Manage Academic Resources"