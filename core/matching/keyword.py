import json
from datetime import datetime

from pandas import Series

from core.helper.tables import get_database


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")


def match_by_keyword(input_list, db_name, is_json=False):
    Author, Document, KA, DA, Keyword = get_database(db_name, return_keyword=True)
    A_K = KA[KA.keyword.isin(input_list)]
    aid = A_K['authors_id'].drop_duplicates()
    temp = KA[KA.authors_id.isin(aid)].sort_values('authors_id')
    Selected = temp[temp.keyword.isin(input_list)]
    Results = Selected.groupby(['authors_id', 'keywords_id']).keyword.count().unstack()
    weight = Keyword[Keyword.keyword.isin(input_list)].weight

    Score = {}
    for i in Results.index:
        a = Results.loc[i]
        score = sum((a*weight).dropna())
        Score.update({i: score})
    Score = Series(Score)

    authors = {}
    for author_id in aid:
        profile = Author.ix[author_id].to_dict()
        profile['id'] = int(profile['id'])
        keywords = list(KA[KA.authors_id == author_id].keyword.values)
        documents_id = DA[DA.authors_id == author_id].documents_id.values
        documents = []
        for document_id in documents_id:
            document = Document.ix[document_id].to_dict()
            document['id'] = int(document['id'])
            documents.append(document)
        score = Score.ix[author_id]

        author = {
            'score': score,
            'profile': profile,
            'keywords': keywords,
            'documents': documents,
        }
        authors[profile['id']] = author
    print input_list
    print len(authors)
    if is_json:
        return json.dumps(authors, default=json_serial)
    else:
        return authors

