"""bookmark_manager URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

#To Change the heading of Admin Site
admin.site.site_header = 'Bookmark Manager Admin Settings'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('bookmark.urls'))
]
