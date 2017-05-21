from __future__ import print_function
import json
from gw2_app import models

import requests
from django.core.management.base import BaseCommand


class Command(BaseCommand):
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
        "maps": "maps/",
        "specs": "specializations/",
    }

    def handle(self, *args, **options):
        url_professions = Command.URL + Command.url_services["professions"]
        url_skills = Command.URL + Command.url_services["skills"]

        prof_req = requests.get(url_professions)
        skills_req = requests.get(url_professions)

        prof_data =json.loads(prof_req.text)
        skills_data = json.loads(skills_req.text)

        self.getProfession(url_professions, prof_data)
        self.getWeapons(url_professions, prof_data)
        self.getWeaponSkills(url_professions, url_skills, prof_data)
        self.getProfessionSkills(url_professions, url_skills, prof_data)
        self.getSpecs(url_professions, prof_data)
        self.getTraits(url_professions, prof_data)

    def getProfession(self, url_professions, prof_data):
        for profession in prof_data:
            url_prof = url_professions + "/" + profession

            req_prof = requests.get(url_prof)

            data_prof = json.loads(req_prof.text)
            weapons = data_prof["weapons"].keys()
            for weapon in weapons:
                wep = models.Weapon(weapontype=weapon)
                if models.Weapon.objects.count() == 0:
                    wep.save()
                if models.Weapon.objects.filter(weapontype=weapon):
                    pass
                else:
                    wep.save()

    def getWeapons(self, url_professions, prof_data):
        w = []

        for profession in prof_data:
            repeatdos = False
            url_prof = url_professions + "/" + profession

            req_prof = requests.get(url_prof)

            data_prof = json.loads(req_prof.text)

            weapons = data_prof["weapons"].keys()
            p = models.ProfessionBuild(name=data_prof["name"])
            if models.ProfessionBuild.objects.count() == 0:
                wep.save()
            for e in models.ProfessionBuild.objects.all():
                if e.name == p.name:
                    repeatdos = True
                    break
            if repeatdos:
                break
            p.save()
            for weapon in weapons:
                wep = models.Weapon.objects.filter(weapontype=weapon).get()
                w.append(wep)
            profe = models.ProfessionBuild.objects.filter(name=data_prof["name"]).get()
            profe.weapons.set(w)
            profe.save()
            w = []

    def getWeaponSkills(self, url_professions, url_skills, prof_data):
        for profession in prof_data:
            url_prof = url_professions + "/" + profession

            req_prof = requests.get(url_prof)

            data_prof = json.loads(req_prof.text)

            wep = data_prof["weapons"].keys()

            for weapon in wep:
                weaponskilllist = data_prof["weapons"][weapon]["skills"]
                for i in weaponskilllist:
                    id = i["id"]
                    url_skill = url_skills + str(id)

                    skill_request = requests.get(url_skill)

                    skill_data = json.loads(skill_request.text)

                    prof = models.ProfessionBuild.objects.filter(name=profession).get()
                    w = models.Weapon.objects.filter(weapontype=weapon).get()

                    wskill = models.WeaponSkill(name=skill_data["name"], description=skill_data["description"],
                                                weapon=w, profession=prof)
                    if models.WeaponSkill.objects.count() == 0:
                        wskill.save()
                    if models.WeaponSkill.objects.filter(name=skill_data["name"]):
                        pass
                    else:
                        wskill.save()

    def getProfessionSkills(self, url_professions, url_skills, prof_data):
        for profession in prof_data:
            url_prof = url_professions + "/" + profession

            req_prof = requests.get(url_prof)

            data_prof = json.loads(req_prof.text)

            for skill in data_prof["skills"]:
                url_skill = url_skills + str(skill["id"])

                skill_request = requests.get(url_skill)

                skill_data = json.loads(skill_request.text)

                prof = models.ProfessionBuild.objects.filter(name=profession).get()

                s = models.ProfessionSkill(name=skill_data["name"], description=skill_data["description"],
                                           profession=prof)

                if models.ProfessionSkill.objects.count() == 0:
                    s.save()
                if models.ProfessionSkill.objects.filter(name=skill_data["name"]):
                    pass
                else:
                    s.save()

    def getSpecs(self, url_professions, prof_data):
        for profession in prof_data:
            url_prof = url_professions + "/" + profession

            req_prof = requests.get(url_prof)

            data_prof = json.loads(req_prof.text)

            for spec in data_prof["specializations"]:
                url_spec = Command.URL + Command.url_services["specs"] + str(spec)

                req_specs = requests.get(url_spec)

                data_specs = json.loads(req_specs.text)

                prof = models.ProfessionBuild.objects.filter(name=profession).get()

                spec = models.Specialization(name=data_specs["name"], profession=prof, iselite=data_specs["elite"])

                if models.Specialization.objects.filter(name=data_specs["name"]):
                    pass
                else:
                    spec.save()

    def getTraits(self, url_professions, prof_data):
        for profession in prof_data:
            url_prof = url_professions + "/" + profession

            req_prof = requests.get(url_prof)

            data_prof = json.loads(req_prof.text)

            for spec in data_prof["specializations"]:
                url_spec = Command.URL + Command.url_services["specs"] + str(spec)

                req_specs = requests.get(url_spec)

                data_specs = json.loads(req_specs.text)

                minor_traits = data_specs["minor_traits"]
                major_traits = data_specs["major_traits"]

                for majortrait in major_traits:
                    url_trait = Command.URL + Command.url_services["traits"] + str(majortrait)

                    trait_req = requests.get(url_trait)

                    trait_data = json.loads(trait_req.text)

                    spec = models.Specialization.objects.filter(name=data_specs["name"]).get()

                    trait = models.Trait(name=trait_data["name"], description=trait_data["description"],
                                         spec=spec, ismajor=True)

                    if models.Trait.objects.filter(name=trait_data["name"]):
                        pass
                    else:
                        trait.save()

                for minortrait in minor_traits:
                    url_trait = Command.URL + Command.url_services["traits"] + str(minortrait)

                    trait_req = requests.get(url_trait)

                    trait_data = json.loads(trait_req.text)

                    spec = models.Specialization.objects.filter(name=data_specs["name"]).get()

                    trait = models.Trait(name=trait_data["name"], description=trait_data["description"],
                                         spec=spec, ismajor=False)

                    if models.Trait.objects.filter(name=trait_data["name"]):
                        pass
                    else:
                        trait.save()