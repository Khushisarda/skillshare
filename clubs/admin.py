from django.contrib import admin
from .models import Club, Post

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "coordinator")
    search_fields = ("name", "slug", "coordinator__username")
    prepopulated_fields = {"slug": ("name",)}

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request):
        # Only superusers can create clubs
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        # Only superusers can edit clubs or assign coordinators
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "club", "author", "created_at")
    search_fields = ("title", "club__name", "author__username")
    list_filter = ("club",)
