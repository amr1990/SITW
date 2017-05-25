from behave import *

use_step_matcher("parse")


@given(u'Existeix un usuari "{username}" amb contrasenya "{password}"')
def step_impl(context, username, password):
    from django.contrib.auth.models import User
    from gw2_app.models import Profile
    u = User.objects.create_user(username=username, email="a@a.com", password=password)
    Profile.objects.create(user=u, apikey="53E26455-4E94-524E-AD8A-3D55E9EDAD73223663B8-9503-4414-A9F4-3734F7BC50C1",
                           city="city", country="country")


@given('Faig login com a usuari "{username}" amb contrasenya "{password}"')
def step_impl(context, username, password):
    context.browser.visit(context.get_url('/accounts/login/'))
    form = context.browser.find_by_tag('form').first
    context.browser.fill('username', username)
    context.browser.fill('password', password)
    form.find_by_value('login').first.click()
