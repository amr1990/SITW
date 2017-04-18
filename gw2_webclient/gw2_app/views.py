# encoding=utf8
import json
import string

import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext

from models import UserProfile

URL = "https://api.guildwars2.com/v2/"
url_services = {
    "token": "?access_token=",
    "character": "characters/",
    "core": "/core/",
    "inventory": "/inventory/",
    "items": "items/",
    "account": "account/",
    "bank": "bank/",
    "titles": "titles/",
}


def homepage(request):
    context = RequestContext(request)
    return render_to_response('homepage.html', {}, context)


@login_required
def getCharacterList(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        user = User.objects.get(id=request.user.id)
        profile = UserProfile.objects.filter(user=user).get()
        api = profile.apikey
    URL_char = URL + url_services["character"] + url_services["token"] + api
    req_char = requests.get(URL_char)
    data_char = json.loads(req_char.text)

    return render_to_response(
        'characters.html',
        {'characters': data_char},
        context)


@login_required
def getCharacterInfo(request):
    context = RequestContext(request)
    charname = request.GET.get('name')
    if request.user.is_authenticated():
        user = User.objects.get(id=request.user.id)
        profile = UserProfile.objects.filter(user=user).get()
        api = profile.apikey
    URL_charinfo = URL + url_services["character"] + charname + url_services["core"] + url_services["token"] + api
    req_charinfo = requests.get(URL_charinfo)
    data_charinfo = json.loads(req_charinfo.text)
    info_params = data_charinfo.keys()
    char_info = []
    for item in info_params:
        if data_charinfo[item]:
            if item == "title":
                URL_titles = URL + url_services["titles"] + str(data_charinfo["title"])
                req_titles = requests.get(URL_titles)
                data_titles = json.loads(req_titles.text)
                res = data_titles["name"]
            else:
                res = unicode(data_charinfo[item])
            char_info.append([string.capwords(item), res])
    return render_to_response(
        'infochar.html',
        {'charinfo': char_info},
        context)

def getInventory(request):
    context = RequestContext(request)
    charname = request.GET.get('name')
    if request.user.is_authenticated():
        user = User.objects.get(id=request.user.id)
        profile = UserProfile.objects.filter(user=user).get()
        api = profile.apikey

    url = URL + url_services["character"] + charname + url_services[
        "inventory"] + url_services["token"] + api
    req_inventory = requests.get(url)
    data_inventory = json.loads(req_inventory.text)
    return_response_inventory = []

    for bag in data_inventory["bags"]:
        for item in bag["inventory"]:
            if item:
                url_items = URL + url_services["items"] + str(item["id"])
                req_items = requests.get(url_items)
                data_items = json.loads(req_items.text)
                itemname = data_items["name"]
                return_response_inventory.append((itemname, item["count"]))

    return render_to_response('inventory.html', {'inventory': return_response_inventory, 'name': charname}, context)

@login_required
def getBank(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        user = User.objects.get(id=request.user.id)
        profile = UserProfile.objects.filter(user=user).get()
        api = profile.apikey

    url = URL + url_services["account"] + url_services["bank"] + url_services["token"] + api
    req_bank = requests.get(url)
    data_bank = json.loads(req_bank.text)
    return_response_bank = []

    for item in data_bank:
        if item:
            url_items = URL + url_services["items"] + str(item["id"])
            req_items = requests.get(url_items)
            data_items = json.loads(req_items.text)
            itemname = data_items["name"]
            return_response_bank.append((itemname, item["count"]))

    return render_to_response(
        'bank.html',
        {'bank': return_response_bank},
        context)