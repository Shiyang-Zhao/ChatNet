from django.contrib import admin
from .models.chat import Chat
from .models.message import Message

# Register your models here.
admin.site.register(Chat)
admin.site.register(Message)
