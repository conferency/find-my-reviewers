import json
import pickle

import numpy as np
from flask import current_app
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from textblob import TextBlob

from app import app
from app.utils.environment import load_env


class LdaModelWrapper:
    def __init__(self, filename, force_load=False, np=True, keep_state=True):

        """Initializes a Gensim LDA model.

        :param filename: The base file name of the model.

        :param force_load: Force the LDA model to be loaded in the memory.

        :param np: Determine if the model is trained with noun phrases or individual tokens.
                   True for noun phrases, False for individual tokens.
                   Default: False

        :param keep_state: Keep the state in the memory.
                           Default: False.
        """

        def load_author_lib():
            try:
                return json.load(open('trained/' + filename + ".json", "rb"))
            except IOError:
                return pickle.load(open('trained/' + filename + ".pkl", "rb"))

        self.filename = filename
        self.use_noun_phrases = np  # TODO: let user define if a model is trained with noun phrases
        with app.app_context():
            if not current_app.config["LAZYLOAD_LDA"] or force_load:
                self.model = LdaModel.load('trained/' + filename)
                if not keep_state:
                    self.model.state = None  # Dispose internal state to save memory
                self.num_topics = self.model.num_topics
                self.num_terms = self.model.num_terms
                self.authors_lib = load_author_lib()
                self.dictionary = Dictionary.load('trained/' + filename + ".dictionary")
                try:
                    self.html = open('trained/' + filename + ".html").read()
                    # TODO: maybe implement a visualization by pyLDAvis
                except IOError:
                    self.html = None
                print("LDA model loaded: " + filename + ", " + str(self.num_topics) + " topics.")
            else:
                print("Skipped LDA model preload: " + filename)

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
            self.__init__(self.filename, force_load=True)
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

        return [term.strip().split('*') for term in self.model.print_topic(topic_id).split("+")]

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

model_files = load_env("lda_models.env")
models = {model_name: LdaModelWrapper(model_files[model_name]) for model_name in model_files}
print(models)
