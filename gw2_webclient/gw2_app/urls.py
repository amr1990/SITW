from django.conf.urls import url, include
from views import APIWeaponList, APIWeaponDetail, APIProfessionBuildList, APIProfessionBuildDetail, APIWeaponSkillList
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^weapons/$', APIWeaponList.as_view(), name='weapon-list'),
    url(r'^weapons/(?P<pk>\d+)/$', APIWeaponDetail.as_view(), name='weapon-detail'),
    url(r'^professions/$', APIProfessionBuildList.as_view(), name='profession-list'),
    url(r'^professions/(?P<pk>\d+)/$', APIProfessionBuildDetail.as_view(), name='profession-detail'),
    url(r'^wskills/$', APIWeaponSkillList.as_view(), name='weaponskill-list'),
    url(r'^wskills/(?P<pk>\d+)/$', APIWeaponSkillList.as_view(), name='weaponskill-detail'),
]

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['api', 'json'])
