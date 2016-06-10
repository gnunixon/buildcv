from django.forms import ModelForm
from udata.models import Human, Study, Work, Awards, Ability


class HumanForm(ModelForm):
    class Meta:
        model = Human


class StudyForm(ModelForm):
    class Meta:
        model = Study
        exclude = ['human', ]


class WorkForm(ModelForm):
    class Meta:
        model = Work
        exclude = ['human', ]


class AwardsForm(ModelForm):
    class Meta:
        model = Awards
        exclude = ['human', ]


class AbilityForm(ModelForm):
    class Meta:
        model = Ability
        exclude = ['human', ]
