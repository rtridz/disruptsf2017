"""disrupt2017 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from core import views
from core.views import *

urlpatterns = [

    url(r'^admin/', admin.site.urls),

    url(r'^index/', indexView.as_view()), #template_name='index.html'
    url(r"^login/$", login),

    url(r'^needhelp/', needhelp),
    url(r'^wannahelp/', wannahelp),
    url(r'^operator/', operator),
    url(r'^shelter_list/', shelter_list),
    url(r'^(?P<shelter_id>[0-9]+)/$', views.shelter_info, name='shelter_detail'),
    url(r'^shelters/', views.shelters_map, name='shelter_map')
]
