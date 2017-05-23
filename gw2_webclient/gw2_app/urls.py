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
from gw2_app import views
from views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [

    url(r'^$', views.homepage, name='homepage'),
    url(r'^registration/register/$', views.register, name='register'),
    url(r'^characters/$', views.getCharacterList, name='characters'),
    url(r'^characters/info/$', views.getCharacterInfo, name='characterinfo'),
    url(r'^bank/$', views.getBank, name='bank'),
    url(r'^characters/create/$', views.createCharacter, name='create_character'),
    url(r'^characters/create/created$', views.characterCreated, name='character_created'),
    url(r'^characters/list/$', views.list_characters, name='characters_list'),
    url(r'^characters/(?P<id>.*)/edit/$', views.edit_characters, name='edit_characters'),
    url(r'^characters/delete/$', views.delete_characters, name='delete_characters'),
    url(r'^characters/inventory/$', views.getInventory, name='inventory'),
    url(r'^characters/gear/$', views.getGear, name='gear'),
    url(r'^events/$', views.getEvents, name='events'),
    url(r'^professions/$', views.getInfoProfession, name='professions'),
    url(r'^professions/(?P<prof_id>.*)/training/$', views.getTraining, name='training'),
    url(r'^professions/(?P<prof_id>.*)/skills/$', views.getProfessionSkills, name='professionskills'),
    url(r'^professions/(?P<prof_id>.*)/weapons/$', views.getWeapons, name='weapons'),
    url(r'^accounts/profile/$', views.homepage, name='homepage'),
    url(r'^tradingpost/$', views.tradingPost, name='trading_post'),
    url(r'^tradingpost/current/$', views.getTradingPostCurrent, name='trading_post_current'),
    url(r'^tradingpost/history/$', views.getTradingPostHistory, name='trading_post_history'),
    url(r'^dailies/$', views.getDailyAchievement, name='dailies'),
    url(r'^pvp/$', views.pvp, name='pvp'),
    url(r'^pvp/stats/$', views.getPvPStats, name='pvp_stats'),
    url(r'^pvp/games/$', views.getPvPGames, name='pvp_games'),
    url(r'^api/character/$', APICharacterList.as_view(), name='character-list'),
    url(r'^api/character/(?P<pk>\d+)/$', APICharacterDetail.as_view(), name='character-detail'),
]

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['api', 'json', 'xml'])