from behave import *
import operator
from django.db.models import Q

use_step_matcher("parse")



count = 0


@then("Hi ha un personatge mes creat")
def step_impl(context):
    global count
    from gw2_app.models import Character
    assert count == Character.objects.count()


@when('Crea un personatge "{charname}"')
def step_impl(context, charname):
    global count
    context.browser.visit(context.get_url('/characters/create/'))
    form = context.browser.find_by_tag('form').first
    context.browser.fill('name', charname)
    context.browser.select('race', 'Human')
    context.browser.select('gender', 'Male')
    context.browser.fill('level', 80)
    context.browser.fill('guild', "The Guild")
    context.browser.select('profession_type', 'Guardian')
    form.find_by_value('create').first.click()
    count += 1