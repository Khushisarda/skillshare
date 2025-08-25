
from django.contrib import admin
from .models import Profile
from .models import UserProfile, Skill
from .models import Project

admin.site.register(Project)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "branch", "year", "college")
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "bio")   # show these columns in admin list view
    search_fields = ("user__username", "bio")

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)         # show skill name in admin
    search_fields = ("name",)