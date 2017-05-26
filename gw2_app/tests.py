from django.test import TestCase
from gw2_app.forms import *


class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'test1',
            'password': '1234'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        response = self.client.login(**self.credentials)
        self.assertTrue(response)


class WrongLogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'test1',
            'password': '1234'}
        self.falseCredentials = {
            'username': 'test123',
            'password': '5678'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        response = self.client.login(**self.falseCredentials)
        self.assertFalse(response)


class CreateCharacterTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'test5',
            'password': '8900'}
        u = User.objects.create_user(**self.credentials)
        p = Profile.objects.create(user=u,
                               apikey="53E26455-4E94-524E-AD8A-3D55E9EDAD73223663B8-9503-4414-A9F4-3734F7BC50C1",
                               city="city", country="country")
        self.Character = {
            'name': 'Espidow',
            'race': 'Human',
            'gender': 'Male',
            'level': '80',
            'guild': 'Best Thief and programmer',
            'profession_type': 'Thief',
        }
        self.ccount = Character.objects.count()
        self.client.login(**self.credentials)

    def test_createCharacter(self):
        form = CreateCharacterForm(data=self.Character)
        self.assertTrue(form.is_valid())
        response = self.client.post('/characters/create/', self.Character)
        self.assertEqual(response.status_code, 302)
        self.client.logout()


class EditCharacterTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'test5',
            'password': '8900'}
        u = User.objects.create_user(**self.credentials)
        p = Profile.objects.create(user=u,
                                   apikey="53E26455-4E94-524E-AD8A-3D55E9EDAD73223663B8-9503-4414-A9F4-3734F7BC50C1",
                                   city="city", country="country")
        self.Character = {
            'name': 'Espidow',
            'race': 'Human',
            'gender': 'Male',
            'level': '80',
            'guild': 'Best Thief and programmer',
            'profession_type': 'Thief',
        }
        self.ModCharacter = {
            'name': 'Aranthix',
            'race': 'Human',
            'gender': 'Female',
            'level': '80',
            'guild': 'Best buddy ever',
            'profession_type': 'Mesmer',
        }
        self.ccount = Character.objects.count()
        self.client.login(**self.credentials)
        self.client.post('/characters/create/', self.Character)

    def test_editCharacter(self):
        response = self.client.post('/characters/' + self.Character['name'] + '/edit/', self.ModCharacter)
        self.assertEqual(response.status_code, 302)
        self.client.logout()


class DeleteCharacterTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'test5',
            'password': '8900'}
        u = User.objects.create_user(**self.credentials)
        p = Profile.objects.create(user=u,
                                   apikey="53E26455-4E94-524E-AD8A-3D55E9EDAD73223663B8-9503-4414-A9F4-3734F7BC50C1",
                                   city="city", country="country")
        self.Character = {
            'name': 'Espidow',
            'race': 'Human',
            'gender': 'Male',
            'level': '80',
            'guild': 'Best Thief and programmer',
            'profession_type': 'Thief',
        }
        self.ccount = Character.objects.count()
        self.client.login(**self.credentials)
        self.client.post('/characters/create/', self.Character)

    def test_deleteCharacter(self):
        response = self.client.post('/characters/delete/?name=' + self.Character['name'])
        self.assertEqual(response.status_code, 302)
        self.client.logout()
