from django.contrib import admin
from .models import AddQuery, profile, queryNotification

# Register your models here.
admin.site.register(profile)
admin.site.register(AddQuery)
admin.site.register(queryNotification)
