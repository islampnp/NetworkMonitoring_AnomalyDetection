"""NetworkMonitoring_AnomalyDetection URL Configuration

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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from anomalydetection import views as anomalymonitoring_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls, name='ad'),
    path('home/', anomalymonitoring_views.home, name='home'),
    path('monitoring/', anomalymonitoring_views.monitoring, name='monitoring'),
    path('detection/', anomalymonitoring_views.detection, name='detection'),
    path('simple_upload/', anomalymonitoring_views.simple_upload, name='simple_upload'),
    path('detectionsrealtime/', anomalymonitoring_views.detectionsrealtime, name='detectionsrealtime'),
    path('realtime/',anomalymonitoring_views.realtime,name='realtime'),
    path('detectionsrealtimefun/',anomalymonitoring_views.detectionsrealtimefun,name='detectionsrealtimefun'),

    
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('', auth_views.LoginView.as_view(template_name='users/authentification/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/authentification/logout.html'), name='logout'),
    path('startcicflowmter/',anomalymonitoring_views.startcicflowmter,name='startcicflowmter'),
    path('showdata/',anomalymonitoring_views.showdata,name='showdata'),
    path('showcsvfile/',anomalymonitoring_views.showcsvfile,name='showcsvfile'),
    path('deletefile/',anomalymonitoring_views.deletefile,name='deletefile'),

    path('stopcicflowmter/',anomalymonitoring_views.stopcicflowmter,name='stopcicflowmter'),
    path('satrtanomleisdetection/',anomalymonitoring_views.satrtanomleisdetection,name='satrtanomleisdetection'),

    
]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)