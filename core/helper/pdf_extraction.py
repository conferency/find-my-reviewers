import json

import os

from core.helper.pdf2string import pdf2string


def generate_path(rootpath):
    for dirpath, dirnames, filenames in os.walk(rootpath):
        for filename in filenames:
            if ".pdf" in filename:
                if "._" not in filename:
                    yield os.path.join(dirpath, filename)


def getkeywords(pdfpath, return_json=False):
    string = pdf2string(pdfpath)
    try:
        ix = string.index('Keywords')
        afterk = string[ix:]
        ak = afterk.replace('\n \n', '\n\n')
        l = ak.split('\n\n')
        if l[0].strip() == 'Keywords':
            rawk = l[1]
        else:
            rawk = l[0]
        keywords = []
        for k in rawk.split(','):
            t = k.replace('Keywords', '').replace(':', '').replace('-\n', '').replace('.', '').replace('\n',
                                                                                                       ' ').strip().replace(
                '  ', ' ')
            keywords.append(t)
        d = {}
        d['status'] = 'Success'
        d['keywords'] = keywords
        if return_json:
            return json.dumps(d)
        else:
            return d
    except:
        print('In this PDF file, no author-provided keywords are found')
        print('Path is: %s' % pdfpath)
        d = {}
        d['status'] = 'Failure'
        d['keywords'] = None
        if return_json:
            return json.dumps(d)
        else:
            return d
