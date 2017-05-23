# encoding=utf8
import json
import string


import requests
import urllib2
import bs4
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from forms import UserForm, CreateCharacterForm, ProfileForm
from models import PlayerProfile,Character
from django.http import HttpResponseRedirect
from django.utils import timezone

from . import forms

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
    "achievements": "achievements",
    "daily": "/daily",
    "pvp": "pvp/",
    "stats": "stats",
    "standings": "standings",
    "seasons": "seasons/",
    "games": "games",
    "maps": "maps/"
}


@csrf_exempt
def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form=ProfileForm(data=request.POST)
        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()


            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            profile=profile_form.save(commit=False)
            profile.user=user
            profile.save()
            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form=ProfileForm()

    # Render the template depending on the context.
    return render_to_response(
        'registration/register.html',
        {'user_form': user_form, 'profile_form':profile_form,'registered': registered},
        context)


def homepage(request):
    context = RequestContext(request)
    return render_to_response("homepage.html", {}, context)


@login_required
def getCharacterList(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        user = User.objects.get(id=request.user.id)
        profile = PlayerProfile.objects.filter(user=user).get()
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
        profile = PlayerProfile.objects.filter(user=user).get()
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
        profile = PlayerProfile.objects.filter(user=user).get()
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
        profile = PlayerProfile.objects.filter(user=user).get()
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
        profile = PlayerProfile.objects.filter(user=user).get()
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
    return render_to_response("trading_post.html", {}, context)


@login_required
def getTradingPostCurrent(request):
    context = RequestContext(request)

    if request.user.is_authenticated():
        user = User.objects.get(id=request.user.id)
        profile = PlayerProfile.objects.filter(user=user).get()
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
        profile = PlayerProfile.objects.filter(user=user).get()
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


def getDailyAchievement(request):
    context = RequestContext(request)
    token = "?id="
    URL_daily = URL + url_services["achievements"] + url_services["daily"]
    req_daily = requests.get(URL_daily)
    data_daily = json.loads(req_daily.text)
    dailies = []
    return_response = []
    dailies.append(data_daily["pve"])
    dailies.append(data_daily["pvp"])
    dailies.append(data_daily["wvw"])
    dailies.append(data_daily["fractals"])

    for i in dailies:
        for j in i:
            URL_achiv = URL + url_services["achievements"] + token + str(j["id"])
            req_achiv = requests.get(URL_achiv)
            data_achiv = json.loads(req_achiv.text)
            return_response.append((data_achiv["name"], data_achiv["requirement"]))

    return render_to_response(
        'daily.html',
        {'achievements': return_response},
        context)


def pvp(request):
    context = RequestContext(request)
    return render_to_response("pvp.html", {}, context)


@login_required
def getPvPStats(request):
    context = RequestContext(request)

    if request.user.is_authenticated():
        user = User.objects.get(id=request.user.id)
        profile = PlayerProfile.objects.filter(user=user).get()
        api = profile.apikey

    URL_pvpstats = URL + url_services["pvp"] + url_services["stats"] + url_services["token"] + api
    req_pvpstats = requests.get(URL_pvpstats)
    data_pvpstats = json.loads(req_pvpstats.text)
    URL_standings = URL + url_services["pvp"] + url_services["standings"] \
                      + url_services["token"] + api
    req_standings = requests.get(URL_standings)
    data_standings = json.loads(req_standings.text)

    return_response_winloss_stats = []
    return_response_standings = []
    return_response_winloss_professions = []

    return_response_winloss_stats.append((data_pvpstats["aggregate"]["wins"],
                                         data_pvpstats["aggregate"]["losses"],
                                         data_pvpstats["ladders"]["unranked"]["wins"],
                                         data_pvpstats["ladders"]["unranked"]["losses"],
                                         data_pvpstats["ladders"]["ranked"]["wins"],
                                         data_pvpstats["ladders"]["ranked"]["losses"]))

    for item in data_standings:
        url_seasons = URL + url_services["pvp"] + url_services["seasons"] + item["season_id"]
        req_seasons = requests.get(url_seasons)
        data_seasons = json.loads(req_seasons.text)
        result = []
        season_keys = ["division", "rating", "tier"]
        for i in item["current"]:
            if i in season_keys:
                result.append((item["current"][i]))
        return_response_standings.append((data_seasons["name"].encode("utf-8"),result))

    for profession in data_pvpstats["professions"]:
        return_response_winloss_professions.append((profession.encode("utf-8"),
                                                   data_pvpstats["professions"][profession]["wins"],
                                                   data_pvpstats["professions"][profession]["losses"]))

    return render_to_response(
        'pvp_stats.html',
        {'stats': return_response_winloss_stats,
         'professions': return_response_winloss_professions,
         'standings': return_response_standings},
        context)


@login_required
def getPvPGames(request):
    context = RequestContext(request)

    if request.user.is_authenticated():
        user = User.objects.get(id=request.user.id)
        profile = PlayerProfile.objects.filter(user=user).get()
        api = profile.apikey

    URL_pvpgames = URL + url_services["pvp"] + url_services["games"] \
                      + url_services["token"] + api
    req_pvpgames = requests.get(URL_pvpgames)
    data_pvpgames = json.loads(req_pvpgames.text)

    return_response_pvp_games = []

    for game in data_pvpgames:
        url_current_game = URL + url_services["pvp"] + url_services["games"] +\
                           url_services["token"] + api + "&id=" + game
        req_current_game = requests.get(url_current_game)
        data_current_game = json.loads(req_current_game.text)
        url_map = URL + url_services["maps"] + str(data_current_game["map_id"])
        req_map = requests.get(url_map)
        data_map = json.loads(req_map.text)


        return_response_pvp_games.append((data_map["name"].encode("utf-8"),
                                          data_current_game["result"].encode("utf-8"),
                                          data_current_game["team"].encode("utf-8"),
                                          data_current_game["profession"],
                                          data_current_game["scores"]["red"],
                                          data_current_game["scores"]["blue"]))

    return render_to_response(
        'pvp_games.html',
        {'games': return_response_pvp_games},
        context)
@csrf_exempt
@login_required
def createCharacter(request):
    context = RequestContext(request)
    if request.method == "POST":
        CreateCharacterForm = forms.CreateCharacterForm(data=request.POST)

        if CreateCharacterForm.is_valid():
            character = Character(name=CreateCharacterForm.cleaned_data['name'],
                                        race=CreateCharacterForm.cleaned_data['race'],
                                        gender=CreateCharacterForm.cleaned_data['gender'],
                                        level=CreateCharacterForm.cleaned_data['level'],
                                        guild=CreateCharacterForm.cleaned_data['guild'],
                                        profession_type=CreateCharacterForm.cleaned_data["profession_type"]
                                   )
            character.save()


            return HttpResponseRedirect('/characters/create/created')

        else:
            print(CreateCharacterForm.errors)

    else:
        CreateCharacterForm = forms.CreateCharacterForm()

    return render_to_response("createcharacter.html", {'CreateCharacterForm': CreateCharacterForm}, context)

@csrf_exempt
def characterCreated(request):
    context = RequestContext(request)
    return render_to_response("charactercreated.html", {}, context)

@login_required
def list_characters(request):
    l = []
    context = RequestContext(request)
    for i in Character.objects.all():
        l.append(i)
    l.reverse()
    return render_to_response("characters_list.html", {'list': l},context)

@csrf_exempt
@login_required
def edit_characters(request,id):
    char = Character.objects.get(name=id)
    if request.method == "POST":
        CreateCharacterForm = forms.CreateCharacterForm(data=request.POST)

        if CreateCharacterForm.is_valid():
            char_form = forms.CreateCharacterForm(request.POST, instance=char)
            char_form.save()
            return HttpResponseRedirect('/characters/list')
        else:
            char = Character.objects.get(name=id)
            CreateCharacterForm = forms.CreateCharacterForm(instance=char)
    else:
        CreateCharacterForm = forms.CreateCharacterForm(instance=char)

    return render(request, "edit_characters.html", {'CreateCharacterForm': CreateCharacterForm})

@csrf_exempt
@login_required
def delete_characters(request):


    if Character.objects.filter(name=request.GET.get('name')).exists():
        Character.objects.get(name=request.GET.get('name')).delete()

        return HttpResponseRedirect("/characters/list")






