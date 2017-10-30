#!/usr/bin/env python

from io import StringIO
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter

from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
import re


def pdf2string(fpath):
    debug = 0
    # input option

    pagenos = set()
    password = ''
    maxpages = 0
    # output option
    imagewriter = None
    rotation = 0
    stripcontrol = False
    layoutmode = 'normal'
    codec = 'utf-8'
    pageno = 1
    scale = 1
    caching = True
    showpageno = True
    laparams = LAParams()

    PDFDocument.debug = debug
    PDFParser.debug = debug
    CMapDB.debug = debug
    PDFPageInterpreter.debug = debug

    rsrcmgr = PDFResourceManager(caching=caching)
    outfp = StringIO()

    # get text string only
    device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                           imagewriter=imagewriter)

    fp = file(fpath, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, pagenos,
                                      maxpages=maxpages, password=password,
                                      caching=caching, check_extractable=True):
        page.rotate = (page.rotate+rotation) % 360
        try:
            interpreter.process_page(page)
        except:
            print("Error while processing a page in " + fpath)
            pass
    fp.close()
    string = outfp.getvalue()
    outfp.close()
    return string


def clean(text):
    text = text.replace("- ", "")
    return text


def text_blob_tokenise(path):
    text = " "
    try:
        text += pdf2string(path)
    except:
        print("Error occurred while parsing: " + path)
    text = clean(text)
    return text
