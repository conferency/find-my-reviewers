import pandas as pd
import sqlite3
import nltk
from nltk.corpus import stopwords
import glob
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import json
from textblob import TextBlob
from multiprocessing import Pool
import sys

'''
Usage:

python tokenizer.py fulltext
python tokenizer.py fulltext noun_phrases
python tokenizer.py abstract
python tokenizer.py fulltext noun_phrases
'''

con = sqlite3.connect("data.sqlite") # specify your database here
db_documents = pd.read_sql_query("SELECT * from documents", con)
db_authors = pd.read_sql_query("SELECT * from authors", con)
data = db_documents.set_index("submission_path")
args = sys.argv
tokenised = {}
split = 0
mode = "abstract" # default mode
np = False
single_file_max_documents = 10 # the maximum documents per file. Useful when you have a limited memory.

def save_json(target_object, filename):
    with open(filename, 'w') as fp:
        json.dump(target_object, fp)
    print("INFO: Saved", filename)

def save(number_suffix=""):
    global np
    if number_suffix:
        number_suffix = "_" + str(number_suffix)
    else:
        number_suffix = ""
    if np:
        save_json(tokenised, mode + "_tokenised" + number_suffix + ".json")
    else:
        save_json(tokenised, mode + "_np_tokenised" + number_suffix + ".json")

def log(result):
    global split
    global tokenised
    tokenised[result[0]] = result[1]
    if len(tokenised) == single_file_max_documents:
        print("INFO: Exceeded single_file_max_documents:", single_file_max_documents)
        save(split)
        print("INFO: Saved to split", split)
        split += 1
        tokenised = {}

def pdf2string(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO(newline=None)
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        try:
            interpreter.process_page(page)
        except:
            print("ERROR: Error while processing a page in", fname)
            pass
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text

def textblob_tokenise(path, prefix, suffix, mode, noun_phrase=False):
    filepath = prefix + path + suffix
    # filepath = "F:/FMR/aisel.aisnet.org/" + path + "/fulltext.pdf"
    print("INFO: Processing", path)
    text = data.loc[path]["title"] + " " + data.loc[path]["abstract"]
    def clean(text):
        return text.replace("<p>", " ").replace("</p>", " ").replace("- ", "").replace("-", "")
    if mode == "fulltext":
        try:
            text += " " + pdf2string(filepath)
        except:
            pass
    if noun_phrase:
        tokenised = list(TextBlob(clean(text).encode("ascii", "ignore").decode('ascii')).noun_phrases)
    else:
        tokenised = TextBlob(clean(text).encode("ascii", "ignore").decode('ascii')).words
    print("INFO:", path, "done.")
    return path, tokenised

if __name__ == "__main__":
    p = Pool()
    print(args)
    try:
        mode = args[1]
    except IndexError:
        print("WARNING: Unspecificed argument. It could be 'abstract' or 'fulltext'. Using '", mode, "'.")
    try:
        if args[2] == "noun_phrases":
            print("INFO: Using noun phrase extraction.")
            np = True
    except IndexError:
        pass
    for i in data.index:
        p.apply_async(textblob_tokenise, args = (i, "F:/FMR/aisel.aisnet.org/", "/fulltext.pdf", mode, np), callback = log)
    p.close()
    p.join()
    save(split)
