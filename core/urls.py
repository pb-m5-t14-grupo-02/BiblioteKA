"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from .constrains import way, URLS, USERS, AUTHORS
from django_rest_passwordreset.views import reset_password_request_token

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(way(AUTHORS, URLS))),
    path("api/", include(way(USERS, URLS))),
    path('api/reset/password_reset/', reset_password_request_token),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
