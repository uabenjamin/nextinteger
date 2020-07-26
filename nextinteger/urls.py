"""nextinteger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include, url
from api.views import (
    SignUpView,
    get_current,
    get_next,
    reset,
    api_key,
    signin,
    social_signin,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", SignUpView.as_view()),
    path("current/", get_current),
    path("next/", get_next),
    path("reset/", reset),
    path("apikey/", api_key),
    path("signin/", signin),
    path("social/signin/", social_signin),
]
