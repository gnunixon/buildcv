#-*- coding: utf-8 -*-
from django.test import TestCase
from udata.templatetags.syns import texify, fdate
from udata.models import Work, Human, Study, CV, generate
from udata.views import create_work, create_study
import random


rus = u'Русский'
reg = 'Regular frase'
very_long = 'a'*256
null = None
false = False


# Create your tests here.
class FiltersTest(TestCase):
    fixtures = ['fix.json',]

    def test_texify(self):
        ts = 'Hello , World ! Are you there ? I am ; your father .'
        res = 'Hello, World! Are you there? I am; your father. '
        self.assertEqual(texify(ts), res)
        ts = 'Leg&Co have 50% of our production and gain 5.000$ in this quartal'
        res = 'Leg\&Co have 50\% of our production and gain 5.000\$ in this quartal'
        self.assertEqual(texify(ts), res)
        ts = '"What does this mean?" - asked he. "May be is a mistake?" ("No, Mua-ha-ha-ha!"). "Aha, sure"'
        res = "``What does this mean?\'\' - asked he. ``May be is a mistake?\'\' (``No, Mua-ha-ha-ha!\'\'). ``Aha, sure''"
        self.assertEqual(texify(ts), res)

    def test_fdate(self):
        work = Work.objects.first()
        for begin_year in [random.randint(1990, 2015), null, false]:
            for end_year in [random.randint(1990, 2015), null, false]:
                work.begin_year = begin_year
                work.end_year = end_year
                fdate(work)


class WorkTest(TestCase):
    fixtures = ['fix.json',]

    def test_create_work(self):
        human = Human.objects.get(id=1)
        work = create_work(human=human,
                    inst='Leg&Co SRL',
                    position=u'Половик',
                    begin_year=2014,
                    end_year=2015,
                    comments='It was nice!')
        self.assertEqual(isinstance(work, Work), True)

    def test_edit_work(self):
        work = Work.objects.language('ru').first()
        for inst in [rus, reg]:
            for function in [rus, reg]:
                for begin_year in [random.randint(1990, 2015), null]:
                    for end_year in [random.randint(1990, 2015), null]:
                        for comments in [rus, reg, null]:
                            work.edit(
                                inst=inst,
                                function=function,
                                begin_year=begin_year,
                                end_year=end_year,
                                comments=comments)
                            id = work.id
                            self.assertEqual(Work.objects.language('ro').get(id=id).inst, inst)
                            self.assertEqual(Work.objects.language('ru').get(id=id).function, function)
                            self.assertEqual(Work.objects.language('ru').get(id=id).comments, comments)
                            self.assertEqual(Work.objects.language('ro').get(id=id).begin_year, begin_year)
                            self.assertEqual(Work.objects.language('ro').get(id=id).end_year, end_year)


class StudyTest(TestCase):
    fixtures = ['fix.json',]

    def test_create_study(self):
        human = Human.objects.get(id=1)
        study = create_study(human=human,
                             inst='ULIM',
                             faculty='A faculty',
                             begin_year=2011,
                             end_year=2014)
        self.assertEqual(isinstance(study, Study), True)


class CVTest(TestCase):
    fixtures = ['fix.json',]

    def test_generate_tex(self):
        cv = CV.objects.first()
        cv.generate_tex('ru')

    def test_generate(self):
        cv = CV.objects.first()
        tex = cv.generate_tex('ru')
        pdf, png = generate(id=cv.human.id, lang='ru', tex=tex)
        print tex, pdf, png
