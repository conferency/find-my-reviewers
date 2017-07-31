# -*- coding: utf-8 -*-
from cStringIO import StringIO
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
import re  # regular expression
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Constants
TAG_BEGIN = ""
TAG_TITLE = "TITLE"
TAG_TITLE_CONTENT = "TITLE_CONTENT"
TAG_AUTHOR_CONTENT = "AUTHOR_CONTENT"
TAG_ABSTRACT = "ABSTRACT"
TAG_ABSTRACT_CONTENT = "ABSTRACT_CONTENT"
TAG_ABSTRACT_FINISH = "ABSTRACT_FINISH"
TAG_KEYWORDS = "KEYWORDS"
TAG_KEYWORDS_CONTENT = "KEYWORDS_CONTENT"
TAG_UNKNOWN = "UNKNOWN"

# change this to test other files
pdf_path = "./papers/cswim2.pdf"

current_section = ""
regex = re.compile(r"<.*?>")
pre_section = TAG_BEGIN
# The miner needs a new attribute to help sectionalize a research papers
# Using Font type and size we can have more control over the miner.
pre_font_family = ""
pre_font_size = ""
title = ""
authors = set()
abstract = ""
keywords = ""


def decode_pdf(filename):
    global current_section
    global pre_section
    global pre_font_family
    global pre_font_size
    global title
    global authors
    global abstract
    global keywords

    current_section = ""
    pre_section = TAG_BEGIN
    pre_font_family = ""
    pre_font_size = ""
    title = ""
    authors = set()
    abstract = ""
    keywords = ""

    path = basedir + "/static/demos/paperminer/papers/" + filename
    # layout parameters
    laparams = LAParams()
    caching = True
    rsrcmgr = PDFResourceManager(caching=caching)
    outtype = 'html'
    out = StringIO()
    # Opens a file for reading only in binary format. The file pointer is
    # placed at the beginning of the file. This is the default mode.
    fp = file(path, 'rb')

    # parse PDF to HTML
    codec = 'utf-8'
    if outtype == 'text':
        device = TextConverter(rsrcmgr, out, codec=codec, laparams=laparams,
                               imagewriter=None)
    if outtype == 'xml':
        device = XMLConverter(rsrcmgr, out, codec=codec, laparams=laparams,
                              imagewriter=None)
    if outtype == 'html':
        device = HTMLConverter(rsrcmgr, out, codec=codec, laparams=laparams,
                               imagewriter=None)

    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    pagenos = set()
    # only process the first page
    max_page = 1
    p = 0
    for page in PDFPage.get_pages(fp, pagenos,
                                  maxpages=max_page, password=password,
                                  caching=caching, check_extractable=True):
        if p >= max_page:
            break
        interpreter.process_page(page)
    fp.close()
    device.close()
    # str_value is the first PDF page in HTML
    str_value = out.getvalue()
    out.close()

    # loop through each line in HTML
    for line in str_value.split('<br>'):
        analyze(line)
    result = [title.decode('utf-8'), authors,
              abstract.decode('utf-8'), keywords.decode('utf-8')]

    return result


# this function analyze each line and create sections
def analyze(line):
    global current_section
    global pre_font_family
    global pre_font_size
    # Search the xml output for font family and font size
    font_family = re.search('font-family: (.+?);', line)
    font_size = re.search('font-size:(.+?)"', line)

    # .strip() removes all whitespace at the start and end, including spaces, tabs, newlines and carriage returns.
    cleaned = clean_line(line.strip())
    #        if(font_family):
    # print "FONT: " + font_family.group(1) + " " + font_size.group(1) + " " +
    # cleaned

    #       If there exists wrtiting before the title, keep recursing
    #       Doesn't work because not all titles are bolded and breaks early.
    #        if font_family and pre_section == TAG_BEGIN and "bold" not in str(font_family.group(1)).lower():
    #            return

    if line.startswith("<") and line.find("</a>") < 0 and len(cleaned) > 0 and cleaned[0] != '\n':
        # This is a check to see if the preceeding line has the same font
        if pre_font_family == font_family.group(1) and pre_font_size == font_size.group(1):
            #  Add it to the section if the same font
            current_section += cleaned
            current_section += '\n'
            return
        else:
            # If it is a different font, create new section
            create_section(current_section)

            if cleaned is not None and len(cleaned) > 0 and cleaned[0] != '\n':
                current_section = cleaned
                current_section += '\n'
            else:
                current_section = ""

    elif cleaned is not None and len(cleaned) > 0 and cleaned[0] != '\n':
        # print "Adding: " + cleaned
        current_section += cleaned
        current_section += '\n'

    # Set new font family and size to recurse
    if font_family and len(cleaned) > 0 and cleaned[0] != '\n':
        pre_font_family = font_family.group(1)
    if font_size and len(cleaned) > 0 and cleaned[0] != '\n':
        pre_font_size = font_size.group(1)


# this function removes all HTML tags and return the string of the line
def clean_line(line):
    line = line.replace("\n", "")  # remove new line \n
    after_cleaned = ""
    # The method split() returns a list of all the words in the string, using
    # str as the separator (splits on all whitespace if left unspecified)
    for l in line.split(">"):
        if l.startswith("<") or l.find("</a") != -1:
            continue  # skip the words with < or has </a
        else:
            ls = l.split("<")
            after_cleaned += " "
            after_cleaned += ls[0]
    return after_cleaned.strip()


def create_section(sec):
    global pre_section
    global abstract
    if pre_section == TAG_BEGIN and sec != "":
        pre_section = TAG_TITLE
        set_title(sec)
    elif pre_section == TAG_TITLE:
        # Needed a use case for papers without Authors after title
        if sec.strip().upper() == "ABSTRACT":
            pre_section = TAG_AUTHOR_CONTENT
        else:
            pre_section = TAG_AUTHOR_CONTENT
            add_author(sec)
    elif pre_section == TAG_AUTHOR_CONTENT:
        # Need a use case for if the abstract and keywords use the same
        # font
        abstract = sec.lower().partition("keywords:")[0]
        keywords = sec.lower().partition("keywords:")[2]
        set_abstract(abstract.strip("Abstract"))
        pre_section = TAG_ABSTRACT_CONTENT
        if len(keywords) > 0:
            add_keyword(keywords)
            create_section(current_section)
            pre_section = TAG_ABSTRACT_FINISH
    elif pre_section == TAG_ABSTRACT_CONTENT:
        if sec.strip().lower().startswith("keywords"):
            pre_section = TAG_KEYWORDS
            key_line = sec.split(":")
            if len(key_line) > 1:
                add_keyword(key_line[1])
        elif not identify_subtitle(sec):
            set_abstract(sec)
        else:
            pre_section = TAG_ABSTRACT_FINISH
    elif pre_section == TAG_ABSTRACT_FINISH:
        if sec.strip().lower() == "keywords":
            pre_section = TAG_KEYWORDS
    elif pre_section == TAG_KEYWORDS:
        pre_section = TAG_KEYWORDS_CONTENT
        add_keyword(sec.partition("1.")[0])
    else:
        pre_section = TAG_BEGIN if pre_section == TAG_BEGIN else TAG_UNKNOWN


def identify_subtitle(line):
    words = re.split(" |\n", line)
    # conjunction list
    conj = ("and", "but", "or", "nor", "for", "at", "on", "in",
            "from", "with", "of", "to", "as", "like", "at", "for")
    for w in words:
        if w == "":
            continue
        if any(map(str.isupper, w)):
            continue
        else:
            if w in conj:
                continue
            elif any(map(str.isdigit, w[0])):
                continue
        return False

    return True


def set_title(t):
    global title
    t = t.replace("\n", " ")
    title = t


def add_author(a):
    global authors
    for line in a.split("\n"):
        line = line.replace("\n", "").strip()
        if len(re.split(" ", line)) == 2:
            for name in re.split(",|and", line):
                # Need to remove position
                if "University" in name or "College" in name or "School" in name:
                    break
                    # Removing email address or heading if there is no
                    # abstract
                elif "@" in name or "Introduction" in name:
                    break
                else:
                    authors.add(line.decode('utf-8'))


def add_keyword(k):
    global keywords
    keywords = ""
    for line in k.split("\n"):
        if len(line) == 0:
            continue
        if line[-1] == '-':
            keywords = keywords + line[:-1]
        else:
            keywords = keywords + line + " "
    keywords = keywords + keywords


def set_abstract(ab):
    global abstract
    abstract = ""
    for line in ab.split("\n"):
        if len(line) == 0:
            continue
        if line[-1] == '-':
            abstract = abstract + line[:-1]
        else:
            abstract = abstract + line + " "
    abstract = abstract + abstract

if __name__ == '__main__':
    decode_pdf(pdf_path)
