from flask import url_for
from . import db
from hashlib import sha256
from datetime import datetime

# TODO: Add a table for result pool and cache


class RecommendationResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)
    file_hash = db.Column(db.String())
    result_json = db.Column(db.Text)
    submission_json = db.Column(db.Text)
    matched_topics_json = db.Column(db.Text)
    email = db.Column(db.String(), index=True)
    title = db.Column(db.String())
    algorithm = db.Column(db.String())
    database = db.Column(db.String())
    created = db.Column(db.DateTime)
    best_score = db.Column(db.Float)

    def __init__(self, email, result_json, submission_json, title, algorithm, count, best_score, database,
                 matched_topics=None, tz=None):
        self.email = email
        self.result_json = result_json
        self.title = title
        self.algorithm = algorithm
        self.count = count
        self.submission_json = submission_json
        self.best_score = best_score
        self.database = database
        if matched_topics:
            self.matched_topics_json = matched_topics
        if tz:
            # TODO: implement timezone support
            self.created = datetime.now()
        else:
            self.created = datetime.now()