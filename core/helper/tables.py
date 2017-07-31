# import json
# import pandas as pd
import numpy as np
import os
from core.lda_engine import model_files
from pandas import DataFrame
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.keyword_db import keyword_dbs


def db_connect(base, model_name='dss'):
    try:
        path = 'sqlite:///' + os.path.join(os.getcwd(), base, keyword_dbs[model_name] + '.sqlite')
    except KeyError:
        path = 'sqlite:///' + os.path.join(os.getcwd(), base, model_files[model_name].split(".")[0] + '.sqlite')
    print("Connecting to: ", path)
    return create_engine(path)


def toDataFrame(sql, session):
    tmpt = session.execute(sql)
    return DataFrame(tmpt.fetchall(), columns=tmpt.keys())


def get_database(model_name, return_keyword=False):
    engine = db_connect("databases", model_name=model_name)
    Session = sessionmaker(bind=engine)
    session = Session()
    doc = "select * from documents"
    auth = "select * from authors"
    Author = toDataFrame(auth, session)
    Author.index = Author.id
    Document = toDataFrame(doc, session)
    Document.index = Document.id

    Key_Auth = '''
    select authors_id, keywords_id, keyword, first_name, last_name
    from keywords k, documents_keywords dk, documents_authors da, authors a, documents d
    where a.id = da.authors_id and d.id = da.documents_id and d.id = dk.documents_id and k.id = dk.keywords_id
    '''

    Key_Auth_alt = '''
    select authors_id, keywords_id, keyword, first_name, last_name
    from keywords k, documents_keywords dk, documents_authors da, authors a, documents d
    where a.id = da.authors_id and d.id = da.documents_id and d.id = dk.documents_id and k.id = dk.keywords_id
    '''
    tmpt = session.execute(Key_Auth)
    KA = DataFrame(tmpt.fetchall(), columns=tmpt.keys())

    Docu_Auth = '''
    select authors_id, documents_id, first_name, last_name, title
    from authors a, documents b, documents_authors c
    where a.id=c.authors_id and c.documents_id=b.id;
    '''

    tmpt = session.execute(Docu_Auth)
    DA = DataFrame(tmpt.fetchall(), columns=tmpt.keys())

    Key_Freq = '''
    select keywords.id, keyword, freqency
    from (select keywords_id, count(*) freqency from documents_keywords group by keywords_id) a, keywords
    where keywords.id = a.keywords_id
    '''
    a = session.execute(Key_Freq)
    Keyword = DataFrame(a.fetchall(), columns=a.keys())
    Keyword.index = Keyword.id

    DocNum = session.execute('select count(*) from documents').first()[0]
    Keyword.loc[:, 'weight'] = np.log(DocNum / Keyword.freqency)
    if not return_keyword:
        return Author, Document, KA, DA
    else:
        return Author, Document, KA, DA, Keyword


def get_top_keywords(model_name, author_id, n):
    engine = db_connect("databases", model_name=model_name)
    Session = sessionmaker(bind=engine)
    session = Session()
    Key_Auth_ID = '''
    select keyword, count(*) as frequency
    from (select authors_id, keywords_id, keyword
          from keywords k,
               documents_keywords dk,
               documents_authors da,
               authors a,
               documents d
          where a.id = da.authors_id and
                d.id = da.documents_id and
                d.id = dk.documents_id and
                k.id = dk.keywords_id and
                authors_id = {}) as KA
    group by keywords_id
    order by frequency
    '''.format(author_id)

    tmpt = session.execute(Key_Auth_ID)
    return DataFrame(tmpt.fetchall(), columns=tmpt.keys())[:n].values.tolist()
