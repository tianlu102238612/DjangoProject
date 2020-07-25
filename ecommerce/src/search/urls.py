from django.conf.urls import url
from django.urls import path

from .views import (SearchProductView)

urlpatterns = [
    path('', SearchProductView.as_view()),]

