import os
import subprocess
import hashlib

def generate(tex):
    """It's a task for rqworker. Let see the options:

    :param tex: the tex template
    :type tex: str or unicode
    :return: the urls for pdf and png
    :rtype: tuple of strings
    """
    #: Before generate a pdf with xelatex, we need to write the tex template to file
    base = '/var/www/cv'
    static = os.path.join(base, 'img', 'pdf')
    if not os.path.exists(static):
        os.mkdir(static)
    name = hashlib.md5(tex.encode('utf-8')).hexdigest()
    ptex = os.path.join(static, name + '.tex')
    pgpdf = os.path.join(base, name + '.pdf')
    ppdf = os.path.join(static, name + '.pdf')
    ppng = os.path.join(static, name + '.png')
    if not os.path.exists(ptex):
        tex_file = open(ptex, 'w')
        tex_file.write(tex.encode('utf8'))
        tex_file.close()
        for i in range(0, 2):
            #: We need to generate the pdf twice
            subprocess.call(['xelatex', ptex], cwd='/var/www/cv')
        #: And then we need to move the generated pdf to static location
        os.rename(pgpdf, ppdf)
        #: generate a png preview
        subprocess.call(['convert', ppdf + '[0]', ppng])
        for ext in ['aux', 'bcf', 'log', 'out', 'run.xml']:
            try:
                #: and remove all temporary files
                os.remove(os.path.join(base, name + '.%s' % ext))
            except:
                pass
    pdf = 'http://cv.newsroller/img/pdf/%s.pdf' % name
    png = 'http://cv.newsroller/img/pdf/%s.png' % name
    return pdf, png
