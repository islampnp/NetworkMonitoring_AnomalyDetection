from django.urls import path

from . import views

urlpatterns = [
    path('', views.ss, name='index'),
]