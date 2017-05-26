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
        new_ccount = Character.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(new_ccount, self.ccount+1)


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
        self.assertEqual(Character.objects.get().name, self.ModCharacter['name'])

class WrongEditCharacterTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'test5',
            'password': '8900'}
        self.falseCredentials = {
            'username': 'test123',
            'password': '5678'}
        u = User.objects.create_user(**self.credentials)
        u2 = User.objects.create_user(**self.falseCredentials)
        p = Profile.objects.create(user=u,
                                   apikey="53E26455-4E94-524E-AD8A-3D55E9EDAD73223663B8-9503-4414-A9F4-3734F7BC50C1",
                                   city="city", country="country")
        p2 = Profile.objects.create(user=u2,
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
        self.client.logout()

    def test_wrongeditCharacter(self):
        self.client.login(**self.falseCredentials)
        response = self.client.post('/characters/' + self.Character['name'] + '/edit/', self.ModCharacter)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Character.objects.get().name, self.Character['name'])


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
        self.ccount = Character.objects.count()


    def test_deleteCharacter(self):
        response = self.client.post('/characters/delete/?name=' + self.Character['name'])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Character.objects.count(), self.ccount-1)


class WrongDeleteCharacterTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'test5',
            'password': '8900'}
        self.falseCredentials = {
            'username': 'test123',
            'password': '5678'}
        u = User.objects.create_user(**self.credentials)
        u2 = User.objects.create_user(**self.falseCredentials)
        p = Profile.objects.create(user=u,
                                   apikey="53E26455-4E94-524E-AD8A-3D55E9EDAD73223663B8-9503-4414-A9F4-3734F7BC50C1",
                                   city="city", country="country")
        p2 = Profile.objects.create(user=u2,
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
        self.ccount = Character.objects.count()
        self.client.logout()

    def test_wrongdeleteCharacter(self):
        self.client.login(**self.falseCredentials)
        response = self.client.post('/characters/delete/?name=' + self.Character['name'])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Character.objects.count(), self.ccount)
