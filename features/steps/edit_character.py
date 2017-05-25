from behave import *
import operator

from django.db.models import Q

use_step_matcher("parse")
count = 0

@when('Editar un personatge "{charname}" canviant el nom a "{newcharname}" i guild a "{newguild}"')
def step_impl(context, charname, newcharname, newguild):
    context.browser.visit(context.get_url("/characters/" + charname + "/edit/"))
    form = context.browser.find_by_tag('form').first

    context.browser.fill('name', newcharname)
    context.browser.fill('guild', newguild)
    form.find_by_value('edit').first.click()


@step("Segueix existint el mateix nombre de personatge")
def step_impl(context):
    global count
    from gw2_app.models import Character
    assert count == Character.objects.count()


@step('Existeix un personatge creat pel usuari "{username}" amb nom "{charname}"')
def step_impl(context, username, charname):
    global count
    from gw2_app.models import Character, Profile
    from django.contrib.auth.models import User
    user = User.objects.filter(username=username).get()
    player = Profile.objects.filter(user__username=user.username).get()
    Character.objects.create(name=charname, player=player, race="Human", gender="Male",
                             level=80, guild="The Guild", profession_type="Guardian")
    count = Character.objects.count()


@then('Comprovo que s\'ha modificat el personatge amb el camp nom "{newcharname}" i camp guild "{newguild}"')
def step_impl(context, newcharname, newguild):
    from gw2_app.models import Character
    char = Character.objects.filter(name=newcharname).get()
    assert char.name == newcharname and char.guild == newguild