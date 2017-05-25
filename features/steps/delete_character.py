from behave import *

use_step_matcher("parse")

count = 0


@step('Hi ha un personatge creat pel usuari "{username}" amb nom "{charname}"')
def step_impl(context, username, charname):
    global count
    from gw2_app.models import Character, Profile
    from django.contrib.auth.models import User
    user = User.objects.filter(username=username).get()
    player = Profile.objects.filter(user__username=user.username).get()
    Character.objects.create(name=charname, player=player, race="Human", gender="Male",
                             level=80, guild="The Guild", profession_type="Guardian")
    count = Character.objects.count()


@when('Eliminar el personatge "{charname}"')
def step_impl(context, charname):
    global count
    context.browser.visit(context.get_url("/characters/delete/?name=" + charname))
    count -= 1


@then("Comprovo que s'ha borrat el personatge")
def step_impl(context):
    global count
    from gw2_app.models import Character
    assert count == Character.objects.count()