# encoding=utf8
import json
import string


import requests
import urllib2
import bs4
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
    "equipment": "/equipment/",
    "itemstats": "itemstats/",
    "professions": "professions",
    "skills": "skills/",
    "traits": "traits/",
    "trading_post": "commerce/transactions/",
    "current": "current/",
    "history": "history/",
    "buys": "buys/",
    "sells": "sells/",
}


def homepage(request):
    context = RequestContext(request)
    return render_to_response("homepage.html", {}, context)


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
def getGear(request):
    context = RequestContext(request)
    charname = request.GET.get('name')

    if request.user.is_authenticated():
        user = User.objects.get(id=request.user.id)
        profile = UserProfile.objects.filter(user=user).get()
        api = profile.apikey

    url = URL + url_services["character"] + charname + url_services["equipment"] + url_services["token"] + api
    req_gear = requests.get(url)
    data_gear = json.loads(req_gear.text)
    return_response_gear = []

    for item in data_gear["equipment"]:
        url_items = URL + url_services["items"] + str(item["id"])
        req_items = requests.get(url_items)
        data_items = json.loads(req_items.text)
        itemname = data_items["name"]
        itemtype = data_items["type"]
        itemdetails = data_items["details"]
        stat_data = []
        if "infix_upgrade" in itemdetails.keys():
            stats = itemdetails["infix_upgrade"]
            for stat in stats["attributes"]:
                stat_data.append((stat["attribute"], stat["modifier"]))
        if "stat_choices" in itemdetails.keys():
            stats = itemdetails["stat_choices"]
            for stat in stats:
                url_stat = URL + url_services["itemstats"] + str(stat)
                req_stat = requests.get(url_stat)
                data_stat = json.loads(req_stat.text)
                stat_data.append(("Stat Choice", data_stat["name"]))
        return_response_gear.append((itemname, itemtype, stat_data))

    return render_to_response('gear.html', {'stats': return_response_gear, 'name': charname}, context)


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


def getEvents(request):
    context = RequestContext(request)
    url = urllib2.urlopen('https://wiki.guildwars2.com/wiki/World_boss')
    htmlpage = url.read()
    url.close()
    item_clean = []
    item_final = []
    ignore_first = 0
    page_lxml = bs4.BeautifulSoup(htmlpage, "lxml")
    event_table = page_lxml.find("table", {"class": "mech1 mw-collapsible mw-collapsed table"})
    items = event_table.findAll("tr")

    for item in items:
        if ignore_first == 0:
            ignore_first += 1
        else:
            item_clean.append(item.text.encode("utf-8"))
    for i in item_clean:
        item_final.append([line for line in i.split('\n') if line.strip() != ''])

    return render_to_response(
        'events.html',
        {'events': item_final},
        context)


def getInfoProfession(request):
    context = RequestContext(request)
    URL_professions = URL + url_services["professions"]
    req_professions = requests.get(URL_professions)
    data_professions = json.loads(req_professions.text)

    return render_to_response(
        'professions.html',
        {'professions': data_professions},
        context)


def getTraining(request, prof_id):
    context = RequestContext(request)
    profnameurl = "/" + prof_id
    URL_professions = URL + url_services["professions"] + profnameurl
    req_professions = requests.get(URL_professions)
    data_professions = json.loads(req_professions.text)
    trainings = data_professions["training"]
    track_list = []
    return_list = []

    for training in trainings:
        for track in training["track"]:
            if track["type"] == "Skill":
                url_skills = URL + url_services["skills"] + str(track["skill_id"])
                req_skills = requests.get(url_skills)
                data = json.loads(req_skills.text)
            else:
                url_traits = URL + url_services["traits"] + str(track["trait_id"])
                req_traits = requests.get(url_traits)
                data = json.loads(req_traits.text)
            track_list.append((data["name"], data["description"], track["type"]))
        return_list.append([training["name"], track_list])
        track_list = []

    return render_to_response(
        'training.html',
        {'trainings': return_list,
         'prof': prof_id},
        context)


def getWeapons(request, prof_id):
    context = RequestContext(request)
    profnameurl = "/" + prof_id
    URL_professions = URL + url_services["professions"] + profnameurl
    req_professions = requests.get(URL_professions)
    data_professions = json.loads(req_professions.text)
    weapons = data_professions["weapons"]
    weaponlist = weapons.keys()
    data_skills = []
    response = []
    skills = []
    cont = 0

    for key in weaponlist:
        data_skills.append(weapons[key]["skills"])

    for skill in data_skills:
        for id in skill:
            url_wskills = URL + url_services["skills"] + str(id["id"])
            req_wskills = requests.get(url_wskills)
            data_wskills = json.loads(req_wskills.text)
            skills.append((id["slot"], data_wskills["name"], data_wskills["description"]))
        response.append([weaponlist[cont], skills])
        skills = []
        cont += 1

    return render_to_response(
        'weapons.html',
        {'weapons': weaponlist,
         'skills': response,
         'prof': prof_id},
        context)


def getProfessionSkills(request, prof_id):
    context = RequestContext(request)
    profnameurl = "/" + prof_id
    URL_professions = URL + url_services["professions"] + profnameurl
    req_professions = requests.get(URL_professions)
    data_professions = json.loads(req_professions.text)
    return_skills = []

    for skills in data_professions["skills"]:
        url_skills = URL + url_services["skills"] + str(skills["id"])
        req_skills = requests.get(url_skills)
        data_skills = json.loads(req_skills.text)
        return_skills.append((data_skills["name"], skills["slot"], data_skills["description"]))

    return render_to_response(
        'professionskills.html',
        {'skills': return_skills,
         'prof': prof_id},
        context)


def tradingPost(request):
    context = RequestContext(request)
    return render_to_response("trading_post.html", context)


@login_required
def getTradingPostCurrent(request):
    context = RequestContext(request)

    if request.user.is_authenticated():
        user = User.objects.get(id=request.user.id)
        profile = UserProfile.objects.filter(user=user).get()
        api = profile.apikey
    URL_currentinfobuys = URL + url_services["trading_post"] + url_services["current"] \
                      + url_services["buys"] + url_services["token"] + api
    URL_currentinfosells = URL + url_services["trading_post"] + url_services["current"] \
                      + url_services["sells"] + url_services["token"] + api
    req_currentinfobuys = requests.get(URL_currentinfobuys)
    req_currentinfosells = requests.get(URL_currentinfosells)
    data_currentinfobuys = json.loads(req_currentinfobuys.text)
    data_currentinfosells = json.loads(req_currentinfosells.text)

    return_response_current_buys = []
    return_response_current_sells = []

    for item in data_currentinfobuys:
        url_items = URL + url_services["items"] + str(item["item_id"])
        req_items = requests.get(url_items)
        data_items = json.loads(req_items.text)
        itemname = data_items["name"]
        return_response_current_buys.append((itemname.encode("utf-8"),
                                        item["quantity"],
                                        item["price"],
                                        item["created"].encode("utf-8")))

    for item in data_currentinfosells:
        url_items = URL + url_services["items"] + str(item["item_id"])
        req_items = requests.get(url_items)
        data_items = json.loads(req_items.text)
        itemname = data_items["name"]
        return_response_current_sells.append((itemname.encode("utf-8"),
                                        item["quantity"],
                                        item["price"],
                                        item["created"].encode("utf-8")))

    return render_to_response(
        'trading_post_current.html',
        {'buys': return_response_current_buys, 'sells': return_response_current_sells },
        context)


@login_required
def getTradingPostHistory(request):
    context = RequestContext(request)

    if request.user.is_authenticated():
        user = User.objects.get(id=request.user.id)
        profile = UserProfile.objects.filter(user=user).get()
        api = profile.apikey
    URL_historyinfobuys = URL + url_services["trading_post"] + url_services["history"] \
                      + url_services["buys"] + url_services["token"] + api
    URL_historyinfosells = URL + url_services["trading_post"] + url_services["history"] \
                      + url_services["sells"] + url_services["token"] + api
    req_historyinfobuys = requests.get(URL_historyinfobuys)
    req_historyinfosells = requests.get(URL_historyinfosells)
    data_historyinfobuys = json.loads(req_historyinfobuys.text)
    data_historyinfosells = json.loads(req_historyinfosells.text)

    return_response_history_buys = []
    return_response_history_sells = []

    for item in data_historyinfobuys:
        url_items = URL + url_services["items"] + str(item["item_id"])
        req_items = requests.get(url_items)
        data_items = json.loads(req_items.text)
        itemname = data_items["name"]
        return_response_history_buys.append((itemname.encode("utf-8"),
                                        item["quantity"],
                                        item["price"],
                                        item["created"].encode("utf-8"),
                                        item["purchased"].encode("utf-8")))

    for item in data_historyinfosells:
        url_items = URL + url_services["items"] + str(item["item_id"])
        req_items = requests.get(url_items)
        data_items = json.loads(req_items.text)
        itemname = data_items["name"]
        return_response_history_sells.append((itemname.encode("utf-8"),
                                        item["quantity"],
                                        item["price"],
                                        item["created"].encode("utf-8"),
                                        item["purchased"].encode("utf-8")))

    return render_to_response(
        'trading_post_history.html',
        {'buys': return_response_history_buys, 'sells': return_response_history_sells },
        context)
