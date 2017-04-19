"""gw2_webclient URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.contrib.auth.views import login, logout

from gw2_app import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^characters/$', views.getCharacterList, name='characters'),
    url(r'^characters/info/$', views.getCharacterInfo, name='characterinfo'),
    url(r'^bank/$', views.getBank, name='bank'),
    url(r'^characters/inventory/$', views.getInventory, name='inventory'),
    url(r'^characters/gear/$', views.getGear, name='gear'),
    url(r'^accounts/profile/$', views.homepage, name='homepage'),
    url(r'^events/$', views.getEvents, name='events'),
    url(r'^tradingpost/$', views.tradingPost, name='trading_post'),
    url(r'^tradingpost/current/$', views.getTradingPostCurrent, name='trading_post_current'),
    url(r'^tradingpost/history/$', views.getTradingPostHistory, name='trading_post_history'),
    url(r'^admin/', admin.site.urls),
]
