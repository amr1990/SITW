from behave import *

use_step_matcher("parse")


@given(u'Existeix un usuari "{user}" amb contrasenya "{password}"')
def step_impl(context, user, password):
    from django.contrib.auth.models import User
    from gw2_app.models import Profile
    u = User.objects.create_user(username=user, email="a@a.com", password=password)
    Profile.objects.create(user=u, apikey="53E26455-4E94-524E-AD8A-3D55E9EDAD73223663B8-9503-4414-A9F4-3734F7BC50C1",
                           city="city", country="country")


@given(u'I login as user "{user}" with password "{password}"')
def step_impl(context, user, password):
    context.browser.visit(context.get_url('/accounts/login/'))
    form = context.browser.find_by_tag('form').first
    context.browser.fill('id_username', user)
    context.browser.fill('id_password', password)
    form.find_by_value('submit').first.click()


@given('Faig login com a usuari "user" amb contrasenya "password"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass