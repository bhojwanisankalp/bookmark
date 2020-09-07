from django.contrib import admin
from .models import Customer, Bookmark

# Register Customers Model in admin site.
admin.site.register(Customer)
# Register Bookmarks Model in admin site.
admin.site.register(Bookmark)