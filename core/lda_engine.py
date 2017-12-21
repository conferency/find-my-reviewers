import datetime
import json
import pickle

import numpy as np
import os
from flask import current_app
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from textblob import TextBlob
from collections import OrderedDict
from sqlalchemy.orm import sessionmaker

from app import app
from app.utils.environment import load_env
from .helper import models
import glob


class LdaModelWrapper:
    def __init__(self, model_folder, force_load=False, np=True, keep_state=True):

        """Initializes a Gensim LDA model.

        :param model_folder: The base folder name of the model.

        :param force_load: Force the LDA model to be loaded in the memory.

        :param np: Determine if the model is trained with noun phrases or individual tokens.
                   True for noun phrases, False for individual tokens.
                   Default: False

        :param keep_state: Keep the state in the memory.
                           Default: False.
        """

        def load_author_lib():
            try:
                return json.load(open(model_folder + "author_lib.json", "rb"))
            except IOError:
                return pickle.load(open(model_folder + "author_lib.pkl", "rb"))

        def load_paper_lib():
            return json.load(open(model_folder + 'paper_vec_lib.json', "rb"))

        self.folder = model_folder
        self.use_noun_phrases = np  # TODO: let user define if a model is trained with noun phrases
        with app.app_context():
            if not current_app.config["LAZYLOAD_LDA"] or force_load:
                self.model = LdaModel.load(model_folder + 'model.ldamodel')
                if not keep_state:
                    self.model.state = None  # Dispose internal state to save memory
                self.num_topics = self.model.num_topics
                self.num_terms = self.model.num_terms
                self.authors_lib = load_author_lib()
                self.papers_lib = load_paper_lib()
                self.dictionary = Dictionary.load(model_folder + "/model.dictionary")
                try:
                    self.html = open(model_folder + "/vis.html").read()
                    # TODO: maybe implement a visualization by pyLDAvis
                except IOError:
                    self.html = None
                print("LDA model loaded: " + model_folder + ", " + str(self.num_topics) + " topics.")
                self.database_engine = models.sdb_connect(model_folder + '/', 'db')
                self.session_maker = sessionmaker(bind=self.database_engine)
                self.keywords_cache = self.prepare_keywords_cache()
            else:
                print("Skipped LDA model preload: " + model_folder)

    def prepare_keywords_cache(self):
        cache_json = self.folder +'/' + 'models_keywords_cache.json'
        if os.path.isfile(cache_json):
            return json.load(open(cache_json, 'rb'))
        else:
            print('Generating keywords cache...')
            ret = []
            for i in range(self.num_topics):
                ret.append([term.strip().split('*') for term in self.model.print_topic(i).split("+")])
            if len(ret) < self.num_topics:
                print('Warning: num_topics and actual count of topics retrieved mismatch')
            json.dump(ret, open(cache_json, 'w'))
            return ret

    def tokenize(self, text):

        """Turns a pure text to a bag of words using the dictionary of a trained LDA model.

        :param text: Raw text string.

        :return: A bag of words.
        """

        if self.use_noun_phrases:
            tokenized = TextBlob(text.lower()).noun_phrases
        else:
            tokenized = TextBlob(text.lower()).words
        print(tokenized)
        return self.dictionary.doc2bow(tokenized)

    def predict(self, text):

        """Predicts topics from a raw text string.

        :param text: Raw text string.

        :return: a NumPy array of topics IDs and their confidence levels.
        """

        if not models:
            self.__init__(self.folder, force_load=True)
        vec = self.tokenize(text)
        print("BoW:")
        print(vec)
        topics = np.array(self.model[vec], dtype=[('topic_id', int), ('confidence', float)])
        topics[::-1].sort(order="confidence")
        # This may seem super weird, but it works and it is actually more efficient
        # see https://stackoverflow.com/questions/26984414/efficiently-sorting-a-numpy-array-in-descending-order
        print(topics)
        return topics

    def get_author_top_topics(self, author_id, top=10):

        """Generates the top N relevant topics of an author in our database.

        :param author_id: the author's ID in our database.

        :param top: Number of topics to be returned.

        :return: a NumPy array of topics IDs and their confidence levels.
        """
        try:
            author = self.authors_lib[author_id]
        except KeyError:
            author = self.authors_lib[str(author_id)]
        top_topics = []
        for topic_id, confidence in enumerate(author):
            if confidence > 1:
                top_topics.append([topic_id, confidence - 1])
        top_topics.sort(key=lambda tup: tup[1], reverse=True)
        return top_topics[:top]

    def get_topic_in_list(self, topic_id):

        """Given a topic ID in the model, generates a list of terms.

        :param topic_id: The topic's ID in the model.

        :return: A list of terms.
        """

        return self.keywords_cache[topic_id]

    def get_topic_in_string(self, topic_id, top=5):

        """Given a topic ID in the model, generates a string representation of that topic.

        :param topic_id: The topic's ID in the model.

        :param top: Top N relevant terms.

        :return: A string representation of the topic.
        """

        topic_list = self.get_topic_in_list(topic_id)
        topic_string = " / ".join([i[1] for i in topic_list][:top])
        return topic_string

    def get_topics_in_string(self, topics, confidence=False):

        """Converts a list of topics (with or without confidence levels) to a list of strings encoded in a dict.

        :param topics: The list of topics to be converted.

        :param confidence: If the input topics contains confidence levels, make sure this is set to True.

        :return: a list of dictionary that includes string representations (or with confidence levels)
        """

        if confidence:
            topics_list = []
            for topic in topics:
                topic_map = {
                    "topic_id": topic[0],
                    "string": self.get_topic_in_string(topic[0]),
                    "confidence": topic[1]
                }
                topics_list.append(topic_map)
        else:
            topics_list = []
            for topic_id in topics:
                topic_map = {
                    "topic_id": topic_id,
                    "string": self.get_topic_in_string(topic_id),
                }
                topics_list.append(topic_map)
        return topics_list

    def get_topic_authors_weights(self, topic_id, ordered=True, top=None):
        """
        Gets an OrderedDict containing authors and their weights in the given topic
        :param topic_id: The topic's ID in the model.
        :param ordered: Whether to sort the returned dict by weight, in descending order.
        :param top: Only return top N authors. If this parameter is set, the returned dict will be ordered.
        :return: An OrderedDict containing authors and their weight in the given topic: {author_id: weight_in_topic, ...}
        """

        item_tuples = ((author_id, weights[topic_id]) for author_id, weights in self.authors_lib.items())
        if ordered or top:
            item_tuples = sorted(item_tuples, key=lambda item: item[1], reverse=True)
            if top:
                item_tuples = item_tuples[:top]

        return OrderedDict(item_tuples)

    def get_articles_weights(self, topic_id, ordered=True, top=None):
        """
        Gets an OrderedDict containing papers and their weight in the given topic.\n
        Papers that are completely unrelated are not included in the returned dict.
        :param topic_id: The topic's ID in the model.
        :param ordered: Whether to sort the returned dict by weight, in descending order.
        :param top: Only return top N papers. If this parameter is set, the returned dict will be ordered.
        :return: An OrderedDict containing papers and their weights in the given topic: {paper: weight_in_topic, ...}
        """

        item_tuples = []
        for paper, confidences in self.papers_lib.items():
            target_topic_confidence = 0
            for confidence_item in confidences:
                if confidence_item[0] != topic_id:
                    continue
                target_topic_confidence = confidence_item[1]
                break

            if target_topic_confidence != 0:
                item_tuples.append((paper, target_topic_confidence))

        if ordered or top:
            item_tuples = sorted(item_tuples, key=lambda item: item[1], reverse=True)
            if top:
                item_tuples = item_tuples[:top]

        return OrderedDict(item_tuples)

    def get_topic_weights_by_year(self, topic_id, start=None, stop=None):
        """
        Gets the weights for every year from `start` tp `stop`, for the given topic.
        :param start: Starting year (included).
        :param stop: Stopping year (included).
        :return: An OrderedDict in ascending order by key `year`: { year: topic_weight_of_year , ... }
        """

        start = start if start else 0
        stop = stop if stop else datetime.date.today().year

        year_weight_dict = {}
        session = self.session_maker()
        articles_weights = self.get_articles_weights(topic_id, ordered=False)
        result_proxy = session.execute(
            '''SELECT submission_path, CAST(SUBSTR(publication_date, 1, 4) AS INTEGER) AS year
                FROM documents WHERE year BETWEEN :start AND :stop''',
            {'start': start, 'stop': stop})
        results = result_proxy.fetchall()
        results = (x for x in results if x[0] in articles_weights)

        for paper_row in results:
            year = paper_row[1]
            paper_weight = articles_weights[paper_row[0]]
            if year not in year_weight_dict:
                year_weight_dict[year] = paper_weight
            else:
                year_weight_dict[year] += paper_weight

        return OrderedDict(sorted(year_weight_dict.items(), key=lambda item: item[0]))

model_folders = glob.glob('models/*/')
models = {model_name.split('/')[-2]: LdaModelWrapper(model_name) for model_name in model_folders if model_name != 'models/resources/'}
print(models)
