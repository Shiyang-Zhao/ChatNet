"""
URL configuration for metasphere project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home, search, setting, history

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="metasphere"),
    path("home/", home, name="home"),
    path("search/", search, name="search-posts"),
    # path("sort/", sort, name="sort-posts"),
    path("sort/", home, name="sort-posts"),
    path("setting/", setting, name="setting"),
    path("history/", history, name="history"),
    path("users/", include("apps.users.urls")),
    path("posts/", include("apps.posts.urls")),
    path("chats/", include("apps.chats.urls")),
    path("notifications/", include("apps.notifications.urls")),
    path("stories/", include("apps.stories.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
