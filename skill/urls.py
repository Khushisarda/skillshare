from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static   # ✅ added

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),  # example
]

# ✅ This makes media files (profile pics) work in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
