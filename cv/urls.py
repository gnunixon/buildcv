from django.conf.urls import patterns, include, url
from django.contrib import admin
from udata.views import base, human, studies, get_studies, studies_delete
from udata.views import get_works, works, works_delete
from udata.views import get_awards, awards, awards_delete
from udata.views import get_abilities, abilities, abilities_delete
from udata.views import lang, get_lang, lang_delete, change_language
from udata.views import cv, get_cvs, cv_delete, cv_send
from udata.views import get_messages

urlpatterns = patterns('',
                       url(r'^$', base),
                       url(r'^(?P<lang>\w{0,2})/$', base),
                       url(r'^human/$', human),
                       url(r'^studies/$', studies),
                       url(r'^studies/get/$', get_studies),
                       url(r'^studies/delete/$', studies_delete),
                       url(r'^works/$', works),
                       url(r'^works/get/$', get_works),
                       url(r'^works/delete/$', works_delete),
                       url(r'^awards/$', awards),
                       url(r'^awards/get/$', get_awards),
                       url(r'^awards/delete/$', awards_delete),
                       url(r'^abilities/$', abilities),
                       url(r'^abilities/get/$', get_abilities),
                       url(r'^abilities/delete/$', abilities_delete),
                       url(r'^cvs/$', cv),
                       url(r'^cvs/get/$', get_cvs),
                       url(r'^cvs/delete/$', cv_delete),
                       url(r'^cvs/send/$', cv_send),
                       url(r'^lang/$', lang),
                       url(r'^lang/get/$', get_lang),
                       url(r'^lang/delete/$', lang_delete),
                       url(r'^human/lang/$', change_language),
                       url(r'^messages/$', get_messages),

                       url('', include('social.apps.django_app.urls', namespace='social')),
                       url('', include('django.contrib.auth.urls', namespace='auth')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^i18n/', include('django.conf.urls.i18n')),
                       )
