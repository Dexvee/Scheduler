from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('base.urls')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('schedules/', include(('schedules.urls', 'schedules'), namespace='schedules')),
    path('admin/', admin.site.urls),
]
