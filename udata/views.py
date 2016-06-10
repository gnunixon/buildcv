from django.shortcuts import render
from django.http import JsonResponse
from udata.models import Study, Work, Awards, Ability, CV, CVTemplate, Human
from udata.models import LangSkill, LangSkillVal, Message
from fb import API

fbapi = API('', '')


def create_study(inst, faculty, begin_year, end_year, human):
    """
    This function create an study instance for given human in all languages.

    :param inst: name of institution
    :type inst: str or unicode
    :param faculty: name of faculty
    :type faculty: str or unicode
    :param begin_year: year when start the studies
    :type begin_year: int
    :param end_year: year when end the studies
    :type end_year: int
    :param human: linked human instance
    :type human: udata.models.Human
    :return: study instance
    :rtype: udata.models.Study
    """
    study = Study.objects.language(human.lang).create(
        inst=inst,
        faculty=faculty,
        end_year=end_year,
        begin_year=begin_year,
        human=human)
    study.save()
    for l in ['ro', 'ru', 'en']:
        if l != human.lang:
            study.translate(l)
            study.inst = inst
            study.faculty=None
            study.save()
    return study


def _m_response(m_id):
    """ It's a helper function for make an response with id of response group
    of messages and the total number of this messages.

    :param m_id: The id of first message in the group
    :type m_id: int
    """
    total = Message.objects.filter(parent=m_id).count()
    return JsonResponse({'success': True, 'message': m_id, 'total': total})


def create_work(human, inst, position, begin_year, end_year, comments):
    """
    Create a new :py:class:`udata.models.Work`

    :param human: a linked human instance
    :type human: udata.models.Human
    :param inst: institution name
    :type inst: str
    :param position: position name
    :type position: str
    :param begin_year: the begin work year
    :type begin_year: int
    :param end_year: the end work year
    :type end_year: int
    :param comments: comments about this work
    :type comments: str
    :return: a resulted instance
    :rtype: udata.models.Work
    """
    w = Work.objects.language(human.lang).create(
        inst=inst,
        function=position,
        comments=comments,
        begin_year=begin_year,
        end_year=end_year,
        human=human)
    w.save()
    for l in ['ro', 'ru', 'en']:
        if l != human.lang:
            w.translate(l)
            w.inst = inst
            w.function = position
            w.comments = comments
            w.save()
    return w


def base(request, lang=None):
    """
    It's our base view. If the user is not authenticated, then we ask him
    for authentication. If he's authenticated for the first time we need to:

        * create a new human
        * pupulate his general information from facebook account (like email and name)
        * ask facebook for informations about education and work places and
        * create new :py:module:`udata.models.Study` and :py:module:`udata.models.Work`

    We have the optional param

    :param lang: it's give us the language code. If not given, we will use the language code from human object
    :type lang: str
    """
    languages = ['ro', 'ru', 'en']
    if request.user.is_authenticated():
        try:
            human = request.user.human
            if not lang:
                lang = human.lang
            elif human.lang != lang:
                human.lang = lang
                human.save()
        except:
            if not lang:
                lang = 'en'
            user = request.user
            u = user.social_auth.first()
            user_access_token = u.access_token
            info = fbapi.using(user_access_token).me.get()
            email = info['email']
            human = Human(
                name=request.user.get_full_name(),
                web='www.example.com',
                email=email,
                phone='xxx.xxx.xxx.xxx',
                user=request.user,
                lang=lang
            )
            human.save()
            if 'work' in info:
                for work in info['work']:
                    try:
                        comments = work.get('description', None)
                        inst = work.get('employer', None)
                        position = work.get('position', None)
                        start_date = work.get('start_date', None)
                        end_date = work.get('end_date', None)
                        if inst and start_date:
                            function, end_year = [None]*2
                            if position:
                                function = position.get('name', None)
                            begin_year = int(start_date.split('-')[0])
                            if end_date:
                                end_year = int(end_date.split('-')[0])
                            w = create_work(human, inst['name'], function, begin_year,
                                            end_year, comments)
                    except:
                        pass
            if 'education' in info:
                for edu in info['education']:
                    try:
                        school = edu.get('school', None)
                        year = edu.get('year', None)
                        if school:
                            inst = school['name']
                            if year:
                                year = year['name']
                            study = create_study(inst=inst, faculty=None,
                                                 end_year=year, begin_year=None,
                                                 human=human)
                    except:
                        pass

    return render(request, 'index.html', locals())


def human(request):
    """ Add a human instance. The user is need to be logged in.
    If the human instance exists - edit it. At the end - re-generate all CVs of this human by calling :py:meth:`udata.models.CV.generate_pdf`

    :param request.GET['name']: the name of human
    :type request.GET['name']: str
    :param request.GET['web']: the url of web-site if any
    :type request.GET['web']: str
    :param request.GET['email']: the e-mail
    :type request.GET['email']: str
    :param request.GET['phone']: the phone number
    :type request.GET['phone']: str
    :return: a JsonResponse dict with success statement

    .. todo:: Need to verify fails and response with corresponding message. For now it response allways `{'success': True}`"""

    name = request.GET.get('name', None)
    web = request.GET.get('web', None)
    email = request.GET.get('email', None)
    phone = request.GET.get('phone', None)
    if request.user.human:
        request.user.human.name = name
        request.user.human.web = web
        request.user.human.email = email
        request.user.human.phone = phone
        request.user.human.save()
        m = Message(title="Your general informations was edited", success=True, human=request.user.human)
        m.save()
        m.parent = m.id
        m.send = True
        m.save()
        for cv in request.user.human.cv_set.all():
            m_ids = cv.generate_messages(m.id)
            cv.generate_pdf(m_ids)
        return _m_response(m.id)


def studies(request):
    """ Create or edit existing :py:class:`udata.models.Study` instance.
    The user need to be logged in and have associated :py:class:`udata.models.Human`.
    If we edit a study instance, at the end of this function we regenerate all pdfs of :py:class:`udata.models.CV` associated with it by calling :py:meth:`udata.models.CV.generate_pdf`

    :param request.user.human: The human for how we add or edit this study instance.
    :type request.user.human: udata.models.Human
    :param request.GET['id']: If the id is present, this meen we need to edit a :py:class:`udata.models.Study` instance with given id, if it's associated to current human.
    :type request.GET['id']: int
    :param request.GET['inst']: The name of institution
    :type request.GET['inst']: str
    :param request.GET['faculty']: The name of faculty
    :type request.GET['faculty']: str
    :param request.GET['begin_year']: The beggining year of studies. Not mandatory.
    :type request.GET['begin_year']: int
    :param request.GET['end_year']: The ending year of studies. Not mandatory.
    :type request.GET['end_year']: int
    """
    success = True
    human = request.user.human
    id = request.GET.get('id', False)
    inst = request.GET.get('inst', False)
    faculty = request.GET.get('faculty', False)
    begin_year = request.GET.get('begin_year', False)
    end_year = request.GET.get('end_year', 65535)
    cvs = request.GET.getlist('cvs[]', None)
    if end_year == '':
        end_year = 65535
    message = 'The study element was succesfull added'
    if id:
        study = human.study_set.language(human.lang).filter(id=id).first()
        study.inst = inst
        study.faculty = faculty
        study.begin_year = begin_year
        study.end_year = end_year
        message = 'The study element was succesfull edited'
        study.save()
    else:
        study = create_study(inst=inst, faculty=faculty, end_year=end_year,
                                begin_year=begin_year, human=human)
    for cv in study.cv_set.all():
        cv.studies.remove(study)
        cv.save()
    for cv_id in cvs:
        cv = human.cv_set.filter(id=cv_id).first()
        if cv:
            cv.studies.add(study)
            cv.save()
    m = Message(title=message, success=True, send=True, human=human)
    m.save()
    m.parent = m.id
    m.save()
    for cv in request.user.human.cv_set.all():
        m_ids = cv.generate_messages(m.id)
        cv.generate_pdf(m_ids)
    return _m_response(m.id)


def get_studies(request):
    """
    :return: a list of studies of current human
    :rtype: JsonResponse
    :param request.user.human: a current human
    :type request.user.human: udata.models.Human
    """
    human = request.user.human
    study_list = []
    for study in human.study_set.language(human.lang).all():
        cvs = []
        for cv in study.cv_set.all():
            cvs.append(cv.id)
        end_year = study.end_year
        if study.end_year == 65535:
            end_year = None
        study_list.append({
            'id': study.id,
            'inst': study.inst,
            'faculty': study.faculty,
            'cvs': cvs,
            'begin_year': study.begin_year,
            'end_year': end_year})
    return JsonResponse(study_list, safe=False)


def studies_delete(request):
    """
    Delete the :py:class:`udata.models.Study` with given id if it's associated to current :py:class:`udata.models.Human`.

    :return: success statement ({'success': True})
    :rtype: JsonResponse
    :param request.GET['id']: The id of :py:class:`udata.models.Study` instance to delete
    :type request.GET['id']: int
    :param request.user.human: The current human instance
    :type request.user.human: udata.models.Human

    .. todo:: Need to give success: False response in case of invalid or inexistent `request.GET['id']` or of inexistent `request.user.human`.
    """
    id = request.GET.get('id', False)
    if id:
        study = request.user.human.study_set.filter(id=id).first()
        cv_list = list(study.cv_set.all())
        study.delete()
        message = 'The study element was deleted'
        m = Message(title=message, success=True, send=True, human=request.user.human)
        m.save()
        m.parent = m.id
        m.save()
        for cv in cv_list:
            m_ids = cv.generate_messages(m.id)
            cv.generate_pdf(m_ids)
        return _m_response(m.id)


def works(request):
    human = request.user.human
    id = request.GET.get('id', False)
    inst = request.GET.get('inst', False)
    function = request.GET.get('function', False)
    comments = request.GET.get('comments', None)
    begin_year = request.GET.get('begin_year', False)
    end_year = request.GET.get('end_year', 65535)
    cvs= request.GET.getlist('cvs[]', None)
    if end_year == '':
        end_year = 65535
    message = 'The work element was succesfull added'
    if id:
        work = human.work_set.language(human.lang).filter(id=id).first()
        work.edit(inst, function, comments, begin_year, end_year)
        message = 'The work element was succesfull edited'
    else:
        work = create_work(human, inst, function, begin_year, end_year, comments)
    for cv in work.cv_set.all():
        cv.works.remove(work)
        cv.save()
    for cv_id in cvs:
        cv = human.cv_set.filter(id=cv_id).first()
        if cv:
            cv.works.add(work)
            cv.save()
    m = Message(title=message, success=True, send=True, human=human)
    m.save()
    m.parent = m.id
    m.save()
    for cv in request.user.human.cv_set.all():
        m_ids = cv.generate_messages(m.id)
        cv.generate_pdf(m_ids)
    return _m_response(m.id)


def get_works(request):
    human = request.user.human
    work_list = []
    for work in human.work_set.language(human.lang).all():
        cvs = []
        for cv in work.cv_set.all():
            cvs.append(cv.id)
        end_year = work.end_year
        if work.end_year == 65535:
            end_year = None
        work_list.append({
            'id': work.id,
            'inst': work.inst,
            'function': work.function,
            'comments': work.comments,
            'cvs': cvs,
            'begin_year': work.begin_year,
            'end_year': end_year})
    return JsonResponse(work_list, safe=False)


def works_delete(request):
    id = request.GET.get('id', False)
    if id:
        work = request.user.human.work_set.filter(id=id).first()
        cv_list = list(work.cv_set.all())
        work.delete()
        message = 'The work element was deleted'
        m = Message(title=message, success=True, send=True, human=request.user.human)
        m.save()
        m.parent = m.id
        m.save()
        for cv in cv_list:
            m_ids = cv.generate_messages(m.id)
            cv.generate_pdf(m_ids)
        return _m_response(m.id)


def awards(request):
    human = request.user.human
    id = request.GET.get('id', False)
    title = request.GET.get('title', False)
    description = request.GET.get('description', None)
    year = request.GET.get('year', False)
    cvs = request.GET.getlist('cvs[]', None)
    message = 'The award element was succesfull added'
    if id:
        award = human.awards_set.language(human.lang).filter(id=id).first()
        award.title = title
        award.year = year
        award.description = description
        award.save()
        message = 'The award element was succesfull edited'
    else:
        award = Awards.objects.language(human.lang).create(
            human=human,
            year=year, title=title, description=description)
        award.save()
        for lang in ['en', 'ro', 'ru']:
            if lang != human.lang:
                award.translate(lang)
                award.title = title
                award.description = description
                award.save()
    m = Message(title=message, success=True, send=True, human=human)
    m.save()
    m.parent = m.id
    m.save()
    for cv in award.cv_set.all():
        cv.awards.remove(award)
        cv.save()
    for cv_id in cvs:
        cv = human.cv_set.filter(id=cv_id).first()
        if cv:
            cv.awards.add(award)
            cv.save()
    for cv in human.cv_set.all():
        m_ids = cv.generate_messages(m.id)
        cv.generate_pdf(m_ids)
    return _m_response(m.id)


def get_awards(request):
    human = request.user.human
    award_list = []
    for award in human.awards_set.language(human.lang).all():
        cvs = []
        for cv in award.cv_set.all():
            cvs.append(cv.id)
        award_list.append({
            'id': award.id,
            'title': award.title,
            'description': award.description,
            'cvs': cvs,
            'year': award.year})
    return JsonResponse(award_list, safe=False)


def awards_delete(request):
    id = request.GET.get('id', False)
    if id:
        award = request.user.human.awards_set.filter(id=id).first()
        cv_list = list(award.cv_set.all())
        award.delete()
        message = 'The award element was deleted'
        m = Message(title=message, success=True, send=True, human=request.user.human)
        m.save()
        m.parent = m.id
        m.save()
        for cv in cv_list:
            m_ids = cv.generate_messages(m.id)
            cv.generate_pdf(m_ids)
        return _m_response(m.id)


def abilities(request):
    human = request.user.human
    id = request.GET.get('id', False)
    title = request.GET.get('title', False)
    description = request.GET.get('description', False)
    cvs = request.GET.getlist('cvs[]', None)
    message = 'The ability element was succesfull added'
    if id:
        ability = human.ability_set.language(human.lang).filter(id=id).first()
        ability.title = title
        ability.comment = description
        ability.save()
        message = 'The ability element was succesfull edited'
    else:
        ability = Ability.objects.language(human.lang).create(human=human,
                          title=title, comment=description)
        ability.save()
        for lang in ['en', 'ro', 'ru']:
            if lang != human.lang:
                ability.translate(lang)
                ability.title = title
                ability.comment = description
                ability.save()
    m = Message(title=message, success=True, send=True, human=human)
    m.save()
    m.parent = m.id
    m.save()
    for cv in ability.cv_set.all():
        cv.abilities.remove(ability)
        cv.save()
    for cv_id in cvs:
        cv = human.cv_set.filter(id=cv_id).first()
        if cv:
            cv.abilities.add(ability)
            cv.save()
    for cv in human.cv_set.all():
        m_ids = cv.generate_messages(m.id)
        cv.generate_pdf(m_ids)
    return _m_response(m.id)


def get_abilities(request):
    human = request.user.human
    ability_list = []
    for ability in human.ability_set.language(human.lang).all():
        cvs = []
        for cv in ability.cv_set.all():
            cvs.append(cv.id)
        ability_list.append({
            'id': ability.id,
            'title': ability.title,
            'cvs': cvs,
            'description': ability.comment})
    return JsonResponse(ability_list, safe=False)


def abilities_delete(request):
    id = request.GET.get('id', False)
    if id:
        ability = request.user.human.ability_set.filter(id=id).first()
        cv_list = list(ability.cv_set.all())
        ability.delete()
        message = 'The ability element was deleted'
        m = Message(title=message, success=True, send=True, human=request.user.human)
        m.save()
        m.parent = m.id
        m.save()
        for cv in cv_list:
            m_ids = cv.generate_messages(m.id)
            cv.generate_pdf(m_ids)
        return _m_response(m.id)


def cv(request):
    human = request.user.human
    id = request.GET.get('id', None)
    title = request.GET.get('title', None)
    studies = request.GET.getlist('studies[]', None)
    works = request.GET.getlist('works[]', None)
    awards = request.GET.getlist('awards[]', None)
    abilities = request.GET.getlist('abilities[]', None)
    if id:
        cv = human.cv_set.filter(id=id).first()
        for study in cv.studies.all():
            cv.studies.remove(study)
        for work in cv.works.all():
            cv.works.remove(work)
        for award in cv.awards.all():
            cv.awards.remove(award)
        for ability in cv.abilities.all():
            cv.abilities.remove(ability)
    else:
        cv = CV(title=title,
                human=request.user.human,
                public=False,
                template=CVTemplate.objects.get(id=3))
        cv.save()
        for lang in ['ro', 'ru', 'en']:
            cv.translate(lang)
            cv.save()
    if not studies and not works and not awards and not abilities:
        studies = human.study_set.all()
        for study in studies:
            cv.studies.add(study)
        works = human.work_set.all()
        for work in works:
            cv.works.add(work)
        awards = human.awards_set.all()
        for award in awards:
            cv.awards.add(award)
        abilities = human.ability_set.all()
        for ability in abilities:
            cv.abilities.add(ability)
    if studies:
        studies = human.study_set.filter(id__in=studies).all()
        for study in studies:
            cv.studies.add(study)
    if works:
        works = human.work_set.filter(id__in=works).all()
        for work in works:
            cv.works.add(work)
    if awards:
        awards = human.awards_set.filter(id__in=awards).all()
        for award in awards:
            cv.awards.add(award)
    if abilities:
        abilities = human.ability_set.filter(id__in=abilities).all()
        for ability in abilities:
            cv.abilities.add(ability)
    cv.title = title
    cv.save()
    m = Message(title='The CV was edited', success=True, send=True, human=human)
    m.save()
    m.parent = m.id
    m.save()
    m_ids = cv.generate_messages(m.id)
    cv.generate_pdf(m_ids)
    return _m_response(m.id)


def get_cvs(request):
    human = request.user.human
    cv_list = []
    for cv in human.cv_set.language(human.lang).filter(public=True).all():
        study_list = []
        work_list = []
        award_list = []
        ability_list = []
        for study in cv.studies.all():
            study_list.append(study.id)
        for work in cv.works.all():
            work_list.append(work.id)
        for award in cv.awards.all():
            award_list.append(award.id)
        for ability in cv.abilities.all():
            ability_list.append(ability.id)
        cv_list.append({
            'id': cv.id,
            'title': cv.title,
            'studies': study_list,
            'works': work_list,
            'awards': award_list,
            'abilities': ability_list,
            'pdf': cv.pdf,
            'image': cv.png
        })
    return JsonResponse(cv_list, safe=False)


def cv_delete(request):
    id = request.GET.get('id', False)
    if id:
        cv = request.user.human.cv_set.filter(id=id).first()
        cv.delete()
    return JsonResponse({'success': True})


def cv_send(request):
    id = request.GET.get('id', False)
    if id:
        cv = request.user.human.cv_set.filter(id=id).first()
        subject = request.GET.get('subject', None)
        text = request.GET.get('text', None)
        recipient = request.GET.get('recipient', None)
        lang = request.user.human.lang
        if cv and recipient and subject:
            cv.send_mail(lang, subject, text, recipient)
    m = Message(title='Your e-mail was sent', success=True, send=True, human=request.user.human)
    m.save()
    return _m_response(m.id)


def lang(request):
    id = request.GET.get('id', False)
    lang = request.GET.get('lang', None)
    read = request.GET.get('read', 1)
    write = request.GET.get('write', 1)
    speak = request.GET.get('speak', 1)
    if id:
        lskill = request.user.human.langskill_set.filter(id=id).first()
        message = 'The language skill "%s" was edit' % lang
    else:
        lskill = LangSkill()
        message = 'The language skill "%s" was added' % lang
    lskill.language = lang
    lskill.read = LangSkillVal.objects.get(id=read)
    lskill.write = LangSkillVal.objects.get(id=write)
    lskill.speak = LangSkillVal.objects.get(id=speak)
    lskill.human = request.user.human
    lskill.save()
    m = Message(title=message, success=True, human=request.user.human)
    m.save()
    m.parent = m.id
    m.send = True
    m.save()
    for cv in request.user.human.cv_set.all():
        m_ids = cv.generate_messages(m.id)
        cv.generate_pdf(m_ids)
    return _m_response(m.id)


def get_lang(request):
    languages = []
    for lang in request.user.human.langskill_set.all():
        languages.append({
            'id': lang.id,
            'lang': lang.language,
            'read': lang.read.id,
            'write': lang.write.id,
            'speak': lang.speak.id
        })
    return JsonResponse(languages, safe=False)


def lang_delete(request):
    """ Function for deleting an associated with this human :py:class:`udata.models.LangSkill` instance.

    :param request.GET['id']: the id of :py:class:`udata.models.LangSkill` instance to be deleted
    :type request.GET['id']: int
    :param request.user.human: current human instance
    :type request.user.human: udata.models.Human

    .. todo:: Need to verify success of operation and give the failure message if the operation is failed.
    """
    id = request.GET.get('id', False)
    if id:
        lang = request.user.human.langskill_set.filter(id=id).first()
        cv_list = request.user.human.cv_set.all()
        lang.delete()
        message = 'The study element was deleted'
        m = Message(title=message, success=True, send=True, human=request.user.human)
        m.save()
        m.parent = m.id
        m.save()
        for cv in cv_list:
            m_ids = cv.generate_messages(m.id)
            cv.generate_pdf(m_ids)
        return _m_response(m.id)


def change_language(request):
    """ Change the current language of human. Need for translating reasons and for know what language will be set by default on next accesing page.

    :param request.GET['lang']: a name of language in locale format. Something like 'ru', 'ro', 'en'. For now we support 3 languages: romanian, russian and english.
    :type request.GET['lang']: str"""
    lang = request.GET.get('lang', None)
    if lang:
        request.user.human.lang = lang
        request.user.human.save()
    return JsonResponse({'success': True, 'message': 'You change language to %s' % lang})


def get_messages(request):
    """
    This function get all active messages for current human and delete them after sending.
    """
    parent_id = request.GET.get('parent_id', None)
    message_list = request.user.human.message_set.filter(parent=parent_id).all()
    if not message_list:
        return JsonResponse({'finish': True})
    message_list = message_list.filter(send=True).all()
    messages = []
    for message in message_list:
        m = {
            'success': message.success,
            'message': message.title,
            'reload': message.to_reload
        }
        messages.append(m)
        message.delete()
    return JsonResponse(messages, safe=False)
