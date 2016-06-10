class Base

    constructor: ->
        @datas = {
            'studies': [],
            'works': [],
            'awards': [],
            'abilities': []
        }
        lang_options = {
            resGetPath: '/static/locales/__ns__-__lng__.json',
            fallbackLng: 'ru',
            preload: ['ru', 'ro', 'en'],
            lng: "{{ request.user.human.lang }}"
        }
        $.i18n.init(lang_options)
        $('body *').i18n()
        @scroll = $("html").niceScroll()
        @cvs = []
        @current_cv = new CurriculumVitae {'id': null, 'title': '', 'studies': [], 'works': [], 'awards': [], 'abilities': [], 'pdf': '', 'image': ''}
        @current_language = new Language {'id': null, 'lang': '', 'read': 1, 'write': 1, 'speak': 1}
        @current_language.render_form()
        @active_study = null
        @active_work = null
        @active_award = null
        @active_ability = null
        @get_studies()
        @get_works()
        @get_awards()
        @get_abilities()
        @get_languages()
        @get_cvs()

    get: (params) ->
        $.get params.url, (data) =>
            base.datas[params.list] = []
            $(params.container).html ''
            $.each data, ->
                item = eval(params.class)
                item.render()
                base.datas[params.list].push item
            @current_cv.populate()
            @scroll.resize()
            if @active_study
                for study in @datas.studies
                    if study.id == @active_study
                        @study_form.populate study
            if @active_work
                for work in @datas.works
                    if work.id == @active_work
                        @work_form.populate work
            if @active_award
                for award in @datas.awards
                    if award.id == @active_award
                        @award_form.populate award
            if @active_ability
                for ability in @datas.abilities
                    if ability.id == @active_ability
                        @ability_form.populate ability

    get_studies: ->
        @get {'url': '/studies/get/', 'list': 'studies', 'container': '#studies tbody', 'class': 'new Study(this);'}

    get_works: ->
        @get {'url': '/works/get/', 'list': 'works', 'container': '#work tbody', 'class': 'new Work(this);'}

    get_awards: ->
        @get {'url': '/awards/get/', 'list': 'awards', 'container': '#awards tbody', 'class': 'new Award(this);'}

    get_abilities: ->
        @get {'url': '/abilities/get/', 'list': 'abilities', 'container': '#skills tbody', 'class': 'new Ability(this);'}

    get_languages: ->
        $.get '/lang/get/', (data) ->
            $('#languages tbody').html ''
            $.each data, ->
                lang = new Language this
                lang.render()
            @scroll.resize()

    get_cvs: (update=false) ->
        $.get '/cvs/get/', (data) ->
            $('#cv-previews').html ''
            $.each data, ->
                cv = new CurriculumVitae this
                cv.render()
                base.cvs.push cv
            if not update
                base.make_forms()
            @scroll.resize()

    make_forms: ->
        @study_form = new Form {'id': '#studyForm', 'action': '/studies/', 'submit': 'Add', 'callback': 'base.get_studies()', 'clear_callback': 'base.active_study=null', 'fields':
            [
                {'name': 'begin_year', 'type': 'number', 'ph': 'From', 'message': 'Please enter the year when you begin studies'},
                {'name': 'end_year', 'type': 'number', 'ph': 'To', 'message': 'Please enter the year when you finish the studies'},
                {'name': 'inst', 'type': 'text', 'ph': 'School', 'message': 'Please enter the name of institution'},
                {'name': 'faculty', 'type': 'text', 'ph': 'Faculty', 'message': 'Please enter the name of faculty'}
            ]
        }
        @study_form.render()

        @work_form = new Form {'id': '#workForm', 'action': '/works/', 'submit': 'Add', 'callback': 'base.get_works()', 'clear_callback': 'base.active_work=null', 'fields':
            [
                {'name': 'begin_year', 'type': 'number', 'ph': 'From', 'message': 'Please enter the year when you begin work'},
                {'name': 'end_year', 'type': 'number', 'ph': 'To', 'message': 'Please enter the year when you finish the work'},
                {'name': 'inst', 'type': 'text', 'ph': 'Institution', 'message': 'Please enter the name of institution'},
                {'name': 'function', 'type': 'text', 'ph': 'Position', 'message': 'Please enter your function'},
                {'name': 'comments', 'widget': 'textarea', 'type': 'text', 'ph': 'Comments', 'message': 'Please enter aditional informations about your work'}
            ]
        }
        @work_form.render()

        @award_form = new Form {'id': '#awardForm', 'action': '/awards/', 'submit': 'Add', 'callback': 'base.get_awards()', 'clear_callback': 'base.active_award=null', 'fields':
            [
                {'name': 'year', 'type': 'number', 'ph': 'Year', 'message': 'Please enter the year'},
                {'name': 'title', 'type': 'text', 'ph': 'Title', 'message': 'Please enter the title'},
                {'name': 'description', 'type': 'text', 'widget': 'textarea', 'ph': 'Description', 'message': 'Please enter the description'}
            ]
        }
        @award_form.render()

        @ability_form = new Form {'id': '#abilityForm', 'action': '/abilities/', 'submit': 'Add', 'callback': 'base.get_abilities()', 'clear_callback': 'base.active_ability=null', 'fields':
            [
                {'name': 'title', 'type': 'text', 'ph': 'Title', 'message': 'Please enter the title'},
                {'name': 'description', 'type': 'text', 'widget': 'textarea', 'ph': 'Description', 'message': 'Please enter the description'}
            ]
        }
        @ability_form.render()
        @scroll.resize()


class Send
    constructor: (id) ->
        @id = id

    render: ->
        template = '
        	<div class="modal-dialog">
        		<div class="modal-content">
        			<div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
                        <h4>Sending your CV by email</h4>
                    </div>
        			<div class="modal-body clearfix">
                        <form id="sendingForm"></form>
                    </div>
        		</div>
        	</div>
        '
        @preview = $(document.createElement('DIV')).addClass('modal')
        content = swig.render template
        @preview.html content
        $('body').append @preview
        send_form = new Form {'id': '#sendingForm', 'action': '/cvs/send/', 'submit': 'Send', 'callback': null, 'clear_callback': null, 'fields':
            [
                {'name': 'subject', 'type': 'text', 'ph': 'Subject', 'message': 'Please enter the subject of email'},
                {'name': 'recipient', 'type': 'email', 'ph': 'The e-mail address of receiver', 'message': 'Please enter the receiver'},
                {'name': 'text', 'type': 'text', 'widget': 'textarea', 'ph': 'The message body', 'message': 'Please enter the message'}
            ]
        }
        send_form.render()
        $('input[name="id"]', send_form.preview).val @id
        $('.formSubmit', send_form.preview).click =>
            $(@preview).modal 'hide'
            $(@preview).remove()
        $(@preview).modal 'show'

class CurriculumVitae
    constructor: (data) ->
        @id = data.id
        @title = data.title
        @studies = data.studies
        @works = data.works
        @awards = data.awards
        @abilities = data.abilities
        @pdf = data.pdf
        @image = data.image

    save: ->
        $.get '/cvs/', {'id': @id, 'title': @title, 'studies': @studies, 'works': @works, 'awards': @awards, 'abilities': @abilities}, (data) =>
            p_bar = new Progress {'id': data.message, 'total': data.total}
            p_bar.render()
            p_bar.check()

    render: ->
        template = '
            <a href="{{ cv.pdf }}">
                <img src="{{ cv.image }}" alt="{{ cv.title }}" class="img-thumbnail" />
                <p><strong>{{ cv.title }}</strong></p>
            </a>
            <p>
                <button class="send btn btn-default">Send</button>
                <button class="edit btn btn-default">Edit</button>
                <button class="delete btn btn-default">Delete</button>
            </p>
        '
        @preview = $(document.createElement('DIV')).addClass('col-md-3')
        content = swig.render template, locals: {cv: @}
        @preview.html content
        $('#cv-previews').prepend @preview
        $('.edit', @preview).click =>
            @populate()
            $('html, body').animate({
                scrollTop: ($("#generateCV").offset().top - 100)
            }, 500)
        $('button.delete', @preview).click =>
            confirm = new Confirm {'id': @id, 'url': '/cvs/delete/', 'callback': 'base.get_cvs()'}
            confirm.render()
        $('button.send', @preview).click =>
            send = new Send @id
            send.render()

    populate: ->
        base.current_cv = @
        $('#generateCV input').val @title
        $('input[type="checkbox"]').prop 'checked', false
        for study in @studies
            for s in base.datas['studies']
                if study == s.id
                    $('input[type="checkbox"]', s.preview).prop 'checked', 'yes'
        for work in @works
            for w in base.datas['works']
                if work == w.id
                    $('input[type="checkbox"]', w.preview).prop 'checked', 'yes'
        for award in @awards
            for a in base.datas['awards']
                if award == a.id
                    $('input[type="checkbox"]', a.preview).prop 'checked', 'yes'
        for ability in @abilities
            for ab in base.datas['abilities']
                if ability == ab.id
                    $('input[type="checkbox"]', ab.preview).prop 'checked', 'yes'


class Language

    constructor: (data) ->
        @id = data.id
        @lang = data.lang
        @read = data.read
        @write = data.write
        @speak = data.speak

    clear_form: ->
        @id = null
        @lang = ''
        @read = 1
        @write = 1
        @speak = 1
        @render_form()

    render_form: ->
        template = '
                <input name="id" type="hidden" value="{{ form.id }}" />
                <div class="row">
                    <div class="col-md-6 col-md-offset-3">
                        <div class="form-group">
                        	<input type="text" class="form-control" placeholder="Language *" data-i18n="[placeholder]Language" name="lang" value="{{ form.lang }}"/>
                        </div>
                        <p>
                        	<strong data-i18n="Read">Read: </strong>
                        </p>
                        <div class="form-group">
                        	<div id="read-slider"></div>
                        </div>
                        <p>
                        	<strong data-i18n="Write">Write: </strong>
                        </p>
                        <div class="form-group">
                        	<div id="write-slider"></div>
                        </div>
                        <p>
                        	<strong data-i18n="Speak">Speak: </strong>
                        </p>
                        <div class="form-group">
                        	<div id="speak-slider"></div>
                        </div>
                    </div>
                    <div class="clearfix"></div>
                    <div class="col-lg-12 text-center">
                        <div class="alert"></div>
                        <div class="formClear btn btn-xl danger" data-i18n="Clear the form">Clear the form</div>
                        <button type="button" class="formSubmit btn btn-xl" data-i18n="Add">Add</button>
                    </div>
                </div>
        '
        @form_preview = $('#langForm')
        content = swig.render template, locals: {form: @}
        @form_preview.html content
        @read_slider = $('#read-slider', @form_preview).slider({
            min: 1,
            max: 6,
            range: "min",
            value: @read,
            slide: (event, ui) =>
                @read = ui.value
        })
        @write_slider = $('#write-slider', @form_preview).slider({
            min: 1,
            max: 6,
            range: "min",
            value: @write,
            slide: (event, ui) =>
                @write = ui.value
        })
        @speak_slider = $('#speak-slider', @form_preview).slider({
            min: 1,
            max: 6,
            range: "min",
            value: @speak,
            slide: (event, ui) =>
                @speak = ui.value
        })
        $('.formSubmit', @form_preview).click =>
            @lang = $('[name="lang"]', @form_preview).val()
            $.get '/lang/', {'id': @id, 'lang': @lang, 'read': @read, 'write': @write, 'speak', @speak}, (data) ->
                base.get_languages()
                p_bar = new Progress {'id': data.message, 'total': data.total}
                p_bar.render()
                p_bar.check()
            @clear_form()

        $('.formClear', @form_preview).click =>
            @clear_form()
        $('body *').i18n()

    render: ->
        template = '
                <td class="sel">{{ data.lang }}</td>
                <td class="sel">{{ data.read }}</td>
                <td class="sel">{{ data.write }}</td>
                <td class="sel">{{ data.speak }}</td>
                <td class="text-right">
                    <button type="button" class="btn btn-default edit page-scroll" aria-label="Edit">
                        <span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>
                    </button>
                    <button type="button" class="btn btn-default delete" aria-label="Delete">
                        <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                    </button>
                </td>
        '
        @preview = $(document.createElement('TR'))
        content = swig.render template, locals: {data: @}
        @preview.html content
        $('.edit', @preview).click =>
            @render_form()
        $('#languages tbody').append @preview
        $('.delete', @preview).click =>
            confirm = new Confirm {'id': @id, 'url': '/lang/delete/', 'callback': 'base.get_languages()'}
            confirm.render()


class Form

    constructor: (data) ->
        @id = data.id
        @action = data.action
        @fields = data.fields
        @submit = data.submit
        @callback = data.callback
        @clear_callback = data.clear_callback

    clear_form: ->
        $('[name="id"]', @id).val ''
        $.each $('.form-group input, .form-group textarea', @preview), ->
            $(this).val ''
        $.each $('input[type="checkbox"]', @preview), ->
            $(this).attr 'checked', false

    form_content: ->
        ret = {}
        ret['cvs'] = []
        ret['id'] = $('[name="id"]', @id).val()
        for field in @fields
            ret[field.name] = $("[name=" + field['name'] + "]", @id).val()
        $.each $('input[type="checkbox"]', @preview), ->
            if $(this).is(':checked')
                ret['cvs'].push $(this).val()
        return ret

    populate: (data) ->
        @clear_form()
        $('html, body').animate({
            scrollTop: ($(@id).offset().top - 100)
        }, 500)
        $('[name="id"]', @id).val data.id
        for field in @fields
            $("[name=" + field['name'] + "]", @id).val data[field['name']]
        for c_id in data.cvs
            $('input[name="cvs"].cv' + c_id, @preview).prop 'checked', 'yes'

    render: ->
        template = '
                <input name="id" type="hidden" value="" />
                <div class="row">
                    <div class="{% if form.callback %}col-md-6 col-md-offset-3{% else %}col-lg-12{% endif %}">
                        {% for field in form.fields %}
                            <div class="form-group">
                                {% if field.widget == "textarea" %}
                                    <textarea class="form-control" placeholder="{{ field.ph }}" data-i18n="[placeholder]{{ field.ph }}" name="{{ field.name }}" required data-validation-required-message="{{ field.message }}"></textarea>
                                {% else %}
                                    <input type="{{ field.type }}" class="form-control" placeholder="{{ field.ph }}" data-i18n="[placeholder]{{ field.ph }}" name="{{ field.name }}" required data-validation-required-message="{{ field.message }}">
                                {% endif %}
                                <p class="help-block text-danger"></p>
                            </div>
                        {% endfor %}
                        {% if form.callback %}
                            <p>
                                <b data-i18n="Include in CV:">Include in CV:</b>
                            </p>
                            {% for cv in cvs %}
                                <div class="checkbox">
                                <label><input class="cv{{ cv.id }}" name="cvs" type="checkbox" value="{{ cv.id }}">{{ cv.title }}</label>
                                </div>
                            {% endfor %}
                        {% endif %}
                    </div>
                    <div class="clearfix"></div>
                    <div class="col-lg-12 text-center">
                        <div class="alert"></div>
                        <div class="formClear btn btn-xl danger" data-i18n="Clear the form">Clear the form</div>
                        <button type="button" class="formSubmit btn btn-xl" data-i18n="{{ form.submit }}">{{ form.submit }}</button>
                    </div>
                </div>
        '
        @preview = $(@id)
        content = swig.render template, locals: {form: @, cvs: base.cvs}
        @preview.html content
        $('body *').i18n()
        $('.formClear', @preview).click =>
            @clear_form()
        $('.formSubmit', @preview).click =>
            $.get @action, @form_content(), (data) =>
                if data.success == true
                    eval @callback
                    @clear_form()
                    eval @clear_callback
                p_bar = new Progress {'id': data.message, 'total': data.total}
                p_bar.render()
                p_bar.check()

base = new Base


class Confirm

    constructor: (data) ->
        @url = data.url
        @id = data.id
        @callback = data.callback

    render: ->
        template = '
        	<div class="modal-dialog">
        		<div class="modal-content">
        			<div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
                        <h4>Are you sure want to delete this item?</h4>
                    </div>
        			<div class="modal-body clearfix">Be carefull, this can not be undone</div>
        			<div class="modal-footer">
                        <div class="btn btn-success delete">Yes, delete it</div>
                        <div class="btn btn-default" data-dismiss="modal">Cancel</div>
                    </div>
        		</div>
        	</div>
        '
        @modal = $(document.createElement('DIV')).addClass('modal')
        content = swig.render template, locals: {modal: @}
        $(@modal).html content
        $('body').append @modal
        $('div.delete', @modal).click =>
            $.get @url, {'id': @id}, (data) =>
                eval(@callback)
                base.scroll.resize()
                $(@modal).modal 'hide'
                $(@modal).remove()
                p_bar = new Progress {'id': data.message, 'total': data.total}
                p_bar.render()
                p_bar.check()
        $(@modal).modal 'show'


class Study

    constructor: (data) ->
        @id = data.id
        @inst = data.inst
        @faculty = data.faculty
        @begin_year = data.begin_year
        @end_year = data.end_year
        @cvs = data.cvs

    render: ->
        template = '
                <td class="sel"><input type="checkbox"></td>
                <td class="sel">{{ study.begin_year }}</td>
                <td class="sel">{{ study.end_year }}</td>
                <td class="sel">{{ study.inst }}</td>
                <td class="sel">{{ study.faculty }}</td>
                <td class="text-right">
                    <button type="button" class="btn btn-default edit page-scroll" aria-label="Edit">
                        <span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>
                    </button>
                    <button type="button" class="btn btn-default delete" aria-label="Delete">
                        <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                    </button>
                </td>
        '
        @preview = $(document.createElement('TR'))
        content = swig.render template, locals: {study: @}
        @preview.html content
        $('button.delete', @preview).click =>
            confirm = new Confirm {'id': @id, 'url': '/studies/delete/', 'callback': 'base.get_studies()'}
            confirm.render()
        $('button.edit', @preview).click =>
            base.study_form.populate @
            location.hash = '#studiesInfo'
            base.active_study = @id
        $('.sel', @preview).click =>
            index = base.current_cv.studies.indexOf @.id
            if index > -1
                base.current_cv.studies.splice(index, 1)
                $('input[type="checkbox"]', @preview).prop 'checked', false
            else
                base.current_cv.studies.push @.id
                $('input[type="checkbox"]', @preview).prop 'checked', 'yes'
        $('#studies tbody').append @preview


class Work

    constructor: (data) ->
        @id = data.id
        @inst = data.inst
        @function = data.function
        @comments = data.comments
        @begin_year = data.begin_year
        @end_year = data.end_year
        @cvs = data.cvs

    render: ->
        template = '
                <td class="sel"><input type="checkbox"></td>
                <td class="sel">{{ work.begin_year }}</td>
                <td class="sel">{{ work.end_year }}</td>
                <td class="sel">{{ work.inst }}</td>
                <td class="sel">
                    {{ work.function }}
                    {% if work.comments %}
                        <br />{{ work.comments|safe }}
                    {% endif %}
                </td>
                <td class="text-right">
                    <button type="button" class="btn btn-default edit page-scroll" aria-label="Edit">
                        <span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>
                    </button>
                    <button type="button" class="btn btn-default delete" aria-label="Delete">
                        <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                    </button>
                </td>
        '
        @preview = $(document.createElement('TR'))
        content = swig.render template, locals: {work: @}
        @preview.html content
        $('button.delete', @preview).click =>
            confirm = new Confirm {'id': @id, 'url': '/works/delete/', 'callback': 'base.get_works()'}
            confirm.render()
        $('button.edit', @preview).click =>
            base.work_form.populate @
            base.active_work = @id
        $('.sel', @preview).click =>
            index = base.current_cv.works.indexOf @.id
            if index > -1
                base.current_cv.works.splice(index, 1)
                $('input[type="checkbox"]', @preview).prop 'checked', false
            else
                base.current_cv.works.push @.id
                $('input[type="checkbox"]', @preview).prop 'checked', 'yes'
        $('#work tbody').append @preview


class Award

    constructor: (data) ->
        @id = data.id
        @title = data.title
        @year = data.year
        @description = data.description
        @cvs = data.cvs

    render: ->
        template = '
                <td class="sel"><input type="checkbox"></td>
                <td class="sel">{{ award.year }}</td>
                <td class="sel">{{ award.title }}</td>
                <td class="sel">
                    {% if award.description %}
                        {{ award.description|safe }}
                    {% endif %}
                </td>
                <td class="text-right">
                    <button type="button" class="btn btn-default edit page-scroll" aria-label="Edit">
                        <span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>
                    </button>
                    <button type="button" class="btn btn-default delete" aria-label="Delete">
                        <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                    </button>
                </td>
        '
        @preview = $(document.createElement('TR'))
        content = swig.render template, locals: {award: @}
        @preview.html content
        $('button.delete', @preview).click =>
            confirm = new Confirm {'id': @id, 'url': '/awards/delete/', 'callback': 'base.get_awards()'}
            confirm.render()
        $('button.edit', @preview).click =>
            base.award_form.populate @
            base.active_award = @id
        $('.sel', @preview).click =>
            index = base.current_cv.awards.indexOf @.id
            if index > -1
                base.current_cv.awards.splice(index, 1)
                $('input[type="checkbox"]', @preview).prop 'checked', false
            else
                base.current_cv.awards.push @.id
                $('input[type="checkbox"]', @preview).prop 'checked', 'yes'
        $('#awards tbody').append @preview


class Ability

    constructor: (data) ->
        @id = data.id
        @title = data.title
        @description = data.description
        @cvs = data.cvs

    render: ->
        template = '
                <td class="sel"><input type="checkbox"></td>
                <td class="sel">{{ ability.title }}</td>
                <td class="sel">
                    {{ ability.description|safe }}
                </td>
                <td class="text-right">
                    <button type="button" class="btn btn-default edit page-scroll" aria-label="Edit">
                        <span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>
                    </button>
                    <button type="button" class="btn btn-default delete" aria-label="Delete">
                        <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                    </button>
                </td>
        '
        @preview = $(document.createElement('TR'))
        content = swig.render template, locals: {ability: @}
        @preview.html content
        $('button.delete', @preview).click =>
            confirm = new Confirm {'id': @id, 'url': '/abilities/delete/', 'callback': 'base.get_abilities()'}
            confirm.render()
        $('button.edit', @preview).click =>
            base.ability_form.populate @
            base.active_ability = @id
        $('.sel', @preview).click =>
            index = base.current_cv.abilities.indexOf @.id
            if index > -1
                base.current_cv.abilities.splice(index, 1)
                $('input[type="checkbox"]', @preview).prop 'checked', false
            else
                base.current_cv.abilities.push @.id
                $('input[type="checkbox"]', @preview).prop 'checked', 'yes'
        $('#skills tbody').append @preview


class Progress

    constructor: (data) ->
        @id = data.id
        @total = data.total

    render: ->
        template = '
            <div class="progress">
                <div class="progress-bar progress-bar-striped active" role="progressbar"
                    aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width:0%">
                        0%
                </div>
            </div>
        '
        @preview = $(document.createElement('DIV')).addClass('bar-container')
        content = swig.render template
        @preview.html content
        $('#progress-info').append @preview

    check: ->
        me = @
        step = 100/@total
        current_val = 0
        interval = setInterval(->
            $.get '/messages/', {'parent_id': me.id}, (data) =>
                if data.finish
                    clearInterval interval
                    $.notify 'All jobs are done!', 'success'
                    $(me.preview).remove()
                else
                    $.each data, ->
                        if this.success
                            m_type = 'success'
                        else
                            m_type = 'danger'
                        current_val += step
                        $('.progress-bar', me.preview).html this.message
                        $('.progress-bar', me.preview).attr 'aria-valuenow', current_val
                        $('.progress-bar', me.preview).css 'width', current_val + '%'
                        if this.reload == 'cv'
                            base.get_cvs(true)
        , 5000)


$('.formSubmit', '#generateCV').click =>
    base.current_cv.title = $('input', '#generateCV').val()
    base.current_cv.save()

$('.formClear', '#generateCV').click =>
    base.current_cv = new CurriculumVitae {'id': null, 'title': '', 'studies': [], 'works': [], 'awards': [], 'abilities': [], 'pdf': '', 'image': ''}
    $.each $('input', '#generateCV'), ->
        $(this).val ''
    $.each $('input[type="checkbox"]'), ->
        $(this).attr 'checked', false

$('.lang').click ->
    $.get '/human/lang/', {'lang': $(this).text()}, (data) =>
        base.get_studies()
        base.get_works()
        base.get_awards()
        base.get_abilities()
        base.get_languages()
        base.get_cvs(true)
        i18n.setLng($(this).text())
        $('body *').i18n()
        $('.lang').removeClass 'active'
        $('.lang.' + $(this).text()).addClass 'active'

$('.formSubmit', '#generalForm').click =>
    form = $('#generalForm')
    $.get '/human/', {'name': $('[name="name"]', form).val(), 'web': $('[name="web"]', form).val(), 'phone': $('[name="phone"]', form).val(), 'email': $('[name="email"]', form).val()}, (data) ->
        p_bar = new Progress {'id': data.message, 'total': data.total}
        p_bar.render()
        p_bar.check()
