from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from views import APICharacterList, APICharacterDetail, APIWeaponList, APIWeaponDetail, APIProfessionBuildList, \
    APIProfessionBuildDetail

urlpatterns = [
    url(r'^weapons/$', APIWeaponList.as_view(), name='weapon-list'),
    url(r'^weapons/(?P<pk>\d+)/$', APIWeaponDetail.as_view(), name='weapon-detail'),
    url(r'^professions/$', APIProfessionBuildList.as_view(), name='profession-list'),
    url(r'^professions/(?P<pk>\d+)/$', APIProfessionBuildDetail.as_view(), name='profession-detail'),
    url(r'^character/$', APICharacterList.as_view(), name='character-list'),
    url(r'^character/(?P<pk>\d+)/$', APICharacterDetail.as_view(), name='character-detail'),
]

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['api', 'json'])
