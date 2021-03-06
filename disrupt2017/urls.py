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
from core.views import *

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^needhelp/submit$', add_victim),
    url(r'^wannahelp/$', wannahelp),
    url(r'^wannahelp/submit$', add_shelter),
    # url(r'^operator/', operator),
    url(r'^$', indexView),
    url(r"^login/$", login),
    url(r'^emergency_help/', emergency_help),
    url(r'^get_tickets/', get_tickets),
    # url(r'^wannahelp/', wannahelp),
    # url(r'^operator/', operator),
    # url(r'^(?P<shelter_id>[0-9]+)/$', views.shelter_info, name='shelter_detail'),
    # url(r'^shelters/', views.shelters_map, name='shelter_map')
]
