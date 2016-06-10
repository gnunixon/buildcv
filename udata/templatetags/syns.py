# -*- coding: utf-8 -*-
from django import template
import re

register = template.Library()

def texify(value=None):
    """
    This is a filter for make given text to be valid for latex

    :param value: a given text
    :type value: str or unicode
    :returns: a tex-formated string or empty string
    :rtype: str or unicode
    """
    if value:
        value = re.sub(r' ([,\.!\?;])', r'\1 ', value)
        value = re.sub(r'([%&\$])', r'\\\1', value)
        value = re.sub(r'([ \(])"', r'\1``', value)
        value = re.sub(r'^"', '``', value)
        value = re.sub(r'([ \)\.!\?,])"', r"\1''", value)
        value = re.sub('"$', "''", value)
        value = re.sub(' +', ' ', value)
        value = re.sub(r'\n', '\n\n', value)
        return value
    else:
        return ''

register.filter('texify', texify)


def fdate(inst):
    """
    :param inst: an instance of work or study
    :type inst: :py:class:`udata.models.Work` or :py:class:`udata.models.Study`
    :returns: a formated string of years diapason for be included in tex
    :rtype: str
    """
    if inst.begin_year == inst.end_year:
        return str(inst.begin_year)
    elif inst.end_year == 65535:
        return str(inst.begin_year) + u'--наст.'
    else:
        if inst.begin_year is None:
            return str(inst.end_year)
        else:
            return str(inst.begin_year) + '--' + str(inst.end_year)

register.filter('fdate', fdate)
