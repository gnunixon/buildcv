from django.db import models
from django.template import Template, Context
from django.contrib import admin
from django.template.base import add_to_builtins
from django.contrib.auth.models import User
import django_rq
from hvad.models import TranslatableModel, TranslatedFields
import hashlib
import json
from django.core.mail import EmailMessage
import urllib2


def task_finalize(id, lang, pdf, png, name, m_id):
    # save pdf
    fpdf = open('/var/www/cv/img/pdf/%s.pdf' % name, 'w')
    fpdf.write(pdf)
    fpdf.close()
    pdf_url = '/img/pdf/%s.pdf' % name
    # save png
    fpng = open('/var/www/cv/img/pdf/%s.png' % name, 'w')
    fpng.write(png)
    fpng.close()
    png_url = '/img/pdf/%s.png' % name
    cv = CV.objects.language(lang).get(id=id)
    cv.public = True
    cv.save()
    cv.pdf = pdf_url
    cv.png = png_url
    hashes = {}
    if cv.hashes:
        hashes = json.loads(cv.hashes)
    hashes[name] = {'pdf': pdf_url, 'png': png_url}
    cv.hashes = json.dumps(hashes)
    cv.save()
    if m_id:
        message = cv.human.message_set.filter(id=m_id).first()
        if message:
            message.send = True
            message.save()
    return True


class CVTemplate(models.Model):
    """
    Template for making CV
    """
    #: the title of template, must be a string
    title = models.CharField(max_length=128)
    #: the template itself, must be a string
    text = models.TextField()
    image = models.ImageField(upload_to='cv_thumbs')

    def __unicode__(self):
        return self.title
admin.site.register(CVTemplate)


class Human(models.Model):
    """
    General information about user
    """
    #: the name of user
    name = models.CharField(max_length=255)
    #: his birthday (not used now)
    birthday = models.DateField(blank=True, null=True)
    #: his phone number as string (any format)
    phone = models.CharField(max_length=255)
    #: his email (a valid email)
    email = models.EmailField()
    #: his website
    web = models.CharField(max_length=1024, blank=True, null=True)
    #: the linked Django user for login
    user = models.OneToOneField(User)
    #: the actual language, used for translate web-interface
    lang = models.CharField(max_length=8, blank=True, null=True, default="ro")

    def __unicode__(self):
        return self.name

    def prenume(self):
        """For some templates we need to separate name and surname. This method will get the surname

        :return: the surname of :py:class:`udata.models.Human`
        :rtype: str

        :Example:
        >>> human = Human.objects.get(id=1)
        >>> human.prenume()
        u'Viorel'
        """
        return self.name.split()[0]

    def nume(self):
        """Similar to :py:meth:`udata.models.Human.prenume`, it's get the name of human

        :return: the first name of :py:class:`udata.models.Human`
        :rtype: str

        :Example:
        >>> human = Human.objects.get(id=1)
        >>> human.nume()
        u'Roman'
        """
        return self.name.split()[1]
admin.site.register(Human)


class Message(models.Model):
    """
    This is the messages for human. The webapp will check the existence of messages every few seconds/minutes.
    """
    #: The message itself
    title = models.CharField(max_length=255)
    #: The part of the page to reload on success
    to_reload = models.CharField(max_length=255, blank=True, null=True)
    #: Tell if the operation was successful
    success = models.BooleanField(default=True)
    #: The human for who is this message
    human = models.ForeignKey(Human)
    #: The parent id of group of messages
    parent = models.IntegerField(blank=True, null=True)
    #: Show if the message is ready to be sent
    send = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title


class Study(TranslatableModel):
    """
    What studies have user (like liceum, school, university etc.)
    """
    #: The name of institution (Oxford University, ULIM, Stefan cel Mare Liceum
    inst = models.CharField(max_length=255)
    translations = TranslatedFields(
        #: The translated name of faculty (Journalism and PR Department, real profile, etc.)
        faculty=models.CharField(max_length=255, blank=True, null=True),
    )
    #: The year when the studies began
    begin_year = models.IntegerField(blank=True, null=True)
    #: The year when studies finished
    end_year = models.IntegerField(default=65535)
    #: The linked :py:class:`udata.models.Human`
    human = models.ForeignKey(Human)

    class Meta:
        ordering = ['-end_year', '-begin_year']

    def __unicode__(self):
        return self.inst

admin.site.register(Study)


class Work(TranslatableModel):
    """
    Work experience

    .. todo:: need to make function param to be a ForeignKey and make a new model with a list of all localized variants of positions
    """
    #: The name of employer (like Leg&Co SRL or Microsoft)
    inst = models.CharField(max_length=255)
    #: The translations for position and some comments
    translations = TranslatedFields(
        function=models.CharField(max_length=255),
        comments=models.CharField(max_length=4096, blank=True, null=True)
    )
    """
    :param function: the localized name of position
    :type function: str
    :param comments: the localized comments about this position
    :type comments: str
    """
    #: Year when the user start to work on this position
    begin_year = models.IntegerField(blank=True, null=True)
    #: Year when he ends to work on this position
    end_year = models.IntegerField(default=65535)
    #: The linked :py:class:`udata.models.Human`
    human = models.ForeignKey(Human)

    class Meta:
        ordering = ['-end_year', '-begin_year']

    def __unicode__(self):
        return self.inst

    def edit(self, inst, function, comments, begin_year, end_year):
        """ Method for edit the Work instance with given language

        :param inst: The name of employer
        :type inst: str or unicode
        :param function: localized name of position
        :type function: str or unicode
        :param comments: localized comments about this work
        :type comments: str or unicode
        :param begin_year: year when the user start to work in this position
        :type begin_year: int
        :param end_year: year when he ends to work in this position
        :type end_year: int

        :return: True if all works fine
        :rtype: boolean
        """

        self.inst = inst
        self.function = function
        self.comments = comments
        self.begin_year = begin_year
        self.end_year = end_year
        self.save()
        return True
admin.site.register(Work)


class Awards(TranslatableModel):
    """
    Diploms, awards, courses etc.
    """
    translations = TranslatedFields(
        title=models.CharField(max_length=255),
        description=models.TextField(blank=True, null=True)
    )
    """translations for title and description

    :param title: the name of award
    :type title: str
    :param description: the description of award
    :type description: text"""

    #: The year when this award was gained
    year = models.IntegerField()
    #: The linked :py:class:`udata.models.Human`
    human = models.ForeignKey(Human)

    class Meta:
        ordering = ['-year', ]

    def __unicode__(self):
        return self.title
admin.site.register(Awards)


class Ability(TranslatableModel):
    """
    Skills
    """
    translations = TranslatedFields(
        title=models.CharField(max_length=128),
        comment=models.CharField(max_length=1024)
    )
    """translated title and comments for skills.

    :param title: The name of skill (like Vectorial graphic or Text Processing)
    :type title: str or unicode
    :param comment: The explanetion of skill (like Adobe Illustrator, Inkscape, good knowleges of MS Word etc.)
    :type comment: str or unicode"""
    #: the linked :py:class:`udata.models.Human`
    human = models.ForeignKey(Human)

    def __unicode__(self):
        return self.title
admin.site.register(Ability)


class Language(models.Model):
    """ The language model. For now we allow each user to create it's own set of languages.

    .. todo:: Make a general set of languages and allow user to choose from this list and not create thousends of records in db.
    """
    #: The name of language
    title = models.CharField(max_length=128)

    def __unicode__(self):
        return self.title
admin.site.register(Language)


class LangSkillVal(models.Model):
    """ This is a set of language skill vals in europass format.

    * A1 - very basic knowleges
    * A2 - beginer
    * B1 - can understand something
    * B2 - can understand more
    * C1 - profy
    * C2 - almost nativ user
    """
    #: The title of language skill as indicated in comment before. Not for editing.
    title = models.CharField(max_length=2)
    translations = TranslatedFields(
        description=models.CharField(max_length=128, blank=True, null=True),
    )

    def __unicode__(self):
        return self.title
admin.site.register(LangSkillVal)


class LangSkill(models.Model):
    """ It's a set of language skills of given human

    .. todo:: need to make language to be a list, and user can choose from this list.
    """
    #: The language name
    language = models.CharField(max_length=128)
    #: Reading skills :py:class:`udata.models.LangSkillVal`
    read = models.ForeignKey(LangSkillVal, related_name='read_skill')
    #: Writing skills :py:class:`udata.models.LangSkillVal`
    write = models.ForeignKey(LangSkillVal, related_name='write_skill')
    #: Speaking skills :py:class:`udata.models.LangSkillVal`
    speak = models.ForeignKey(LangSkillVal, related_name='speak_skill')
    #: Associated human
    human = models.ForeignKey(Human)

    def __unicode__(self):
        return self.language
admin.site.register(LangSkill)


class CV(TranslatableModel):
    """
    One of many sets of data, choised for create one CV

    .. todo:: need to add localized fileds for pdfs and png and remove method :py:meth:`udata.models.CV.paths`
    """
    #: The title of generated CV. Usualy is used in the header of resulted pdf
    title = models.CharField(max_length=255)
    #: The parent :py:class:`udata.models.Human`
    human = models.ForeignKey(Human)
    #: The list of included :py:class:`udata.models.Study`
    studies = models.ManyToManyField(Study)
    #: The list of included :py:class:`udata.models.Work`
    works = models.ManyToManyField(Work)
    #: The list of included :py:class:`udata.models.Ability`
    abilities = models.ManyToManyField(Ability, blank=True, null=True)
    #: The list of included :py:class:`udata.models.Awards`
    awards = models.ManyToManyField(Awards, blank=True, null=True)
    #: If the CV is generated successful - this value will be True
    public = models.BooleanField(default=False)
    #: The template for generate pdf, more on :py:class:`udata.models.CVTemplate`
    template = models.ForeignKey(CVTemplate)
    #: Hashes of all generated pdfs (for deduplication)
    hashes = models.TextField(blank=True, null=True)
    translations = TranslatedFields(
        pdf=models.CharField(blank=True, null=True, max_length=255),
        png=models.CharField(blank=True, null=True, max_length=255)
    )
    """
    The urls for localized versions of pdf and png.

    :param pdf: url to generated pdf in given language
    :type pdf: str
    :param png: url to generated png in given language
    :type png: str
    """

    def __unicode__(self):
        return self.title

    def generate_messages(self, m_id):
        """
        This method generate the messages for saving cv instance.

        :param m_id: The id of parent message
        :type m_id: int
        :return: A dict of created but not sended messages ids
        :rtype: dict
        """
        new_m = Message(
            title='The CV "%s" was put in order to be re-generate' % self.title,
            success=True, human=self.human, parent=m_id, send=True
        )
        new_m.save()
        m_ids = {}
        for lang in ['ro', 'ru', 'en']:
            new_m = Message(
                title='The CV "%s-%s" was generated' % (self.title, lang),
                success=True, human=self.human, to_reload='cv', parent=m_id
            )
            new_m.save()
            m_ids[lang] = new_m.id
        return m_ids

    def generate_tex(self, lang):
        """Generate a tex file from template in given language

        :param lang: the language for translate template
        :type lang: str or unicode
        :return: the tex file
        :rtype: str"""
        tpl = Template(self.template.text)
        studies = self.studies.language(lang).all()
        works = self.works.language(lang).all()
        awards = self.awards.language(lang).all()
        abilities = self.abilities.language(lang).all()
        tex = tpl.render(Context({'cv': self, 'studies': studies,
                                    'works': works, 'awards': awards,
                                    'abilities': abilities, 'lang': lang}))
        return str(tex.encode('utf-8'))

    def generate_pdf(self, m_ids=None):
        """
        This method generates the pdfs of cv in all languages.

        In the begin we generate the tex file from template by calling :py:meth:`udata.models.CV.generate_tex`, then we create the jobs using `django_rq` and call :py:func:`udata.models.generate` function.

        :param m_ids: The dictionary with ids of messages to be sent on generating cv in every language. Ex.: {'ro': 156, 'ru': 157, 'en': 158}
        :type m_ids: dict
        """
        success = True
        # message = 'The CV was succesfull saved'
        for lang in ['ro', 'en', 'ru']:
            tex = self.generate_tex(lang)
            name = hashlib.md5(tex).hexdigest()
            hashes = {}
            if self.hashes:
                hashes = json.loads(self.hashes)
            if name in hashes:
                cv = self.translations.filter(language_code=lang).first()
                cv.pdf = hashes[name]['pdf']
                cv.png = hashes[name]['png']
                cv.save()
                if m_ids:
                    message = self.human.message_set.filter(id=m_ids[lang]).first()
                    if message:
                        message.send = True
                        message.save()
            else:
                m_id = None
                if m_ids:
                    m_id = m_ids[lang]
                django_rq.enqueue('task.generate', tex, self.id, lang, name, m_id)
        return {'success': success, 'message': 'We are adding your jobs in queue'}

    def send_mail(self, lang, subject, text, recipient):
        """
        This method will send an email to given recipient with attached cv pdf

        :param lang: The language of sending CV
        :type lang: str
        :param subject: The subject of sending email
        :type subject: str
        :param text: The body of sending email
        :type text: str
        :param recipient: The target email
        :type recipient: str
        """
        pdf = self.translations.filter(language_code=lang).first().pdf
        pdf_content = urllib2.urlopen('http://buildcv.org' + pdf).read()
        pdf_name = '%s_%s_CV_%s-%s.pdf' % (self.human.nume(),
                                           self.human.prenume(),
                                           self.title, lang)
        message = EmailMessage(subject, text, 'look4work@buildcv.org', [recipient],
                               [], reply_to=[self.human.email])
        message.attach(pdf_name, pdf_content, 'application/pdf')
        message.send()
        return {'success': True, 'message': 'The email was sent'}
admin.site.register(CV)

add_to_builtins('udata.templatetags.syns')
