from django.contrib import admin
from .models.user import User
from .models.profile import Profile

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
