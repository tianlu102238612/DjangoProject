"""vote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from vote import settings
from django.conf.urls import url, include
from polls.views import show_subjects,show_teachers,good_or_bad,login,logout,get_captcha

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',show_subjects),
    path('teachers/',show_teachers),
    path('good/',good_or_bad),
    path('bad/',good_or_bad),
    path('login.html',login),
    path('login/',login),
    path('',logout),
    path('captcha/', get_captcha)
]

if settings.DEBUG:

    import debug_toolbar

    urlpatterns.insert(0, path('__debug__/', include(debug_toolbar.urls)))