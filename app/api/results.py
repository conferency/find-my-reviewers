import hashlib
import json

import os
from core.helper.pdf2string import text_blob_tokenise
from flask import render_template, request, current_app, jsonify, session, redirect, url_for

from app import db
from app.models import RecommendationResult
from app.modules.main.views import requires_auth
from core.matching.keyword import match_by_keyword
from core.matching.lda import match_by_lda
from . import api


@api.route('/match/', methods=['GET', 'POST'])
@requires_auth
def dashboard_handle_match():

    """
    This function is called when a user submit a form in the dashboard.
    It will use the designated LDA model or keyword-based model (specified in the form) to generated the matching result.
    :return: redirect the user to the result page.
    """
    user = session['profile']
    form = request.form
    if form['algorithm'].startswith("keywords"):
        # Using keywords
        keywords = form['keywords'].split(',')
        db_name = form['algorithm'][9:]
        reviewers = match_by_keyword(keywords, db_name=db_name)
        best_score = max([reviewers[reviewer_id]['score'] for reviewer_id in reviewers] or [0])
        match_result = RecommendationResult(email=user['email'],
                                            title=form['title'],
                                            result_json=json.dumps(reviewers),
                                            submission_json=json.dumps(form),
                                            algorithm='Keyword-based: ' + db_name,
                                            database=db_name,
                                            count=len(reviewers),
                                            best_score=best_score)
        db.session.add(match_result)
        db.session.commit()
        return redirect(url_for("main.result", result_id=match_result.id))
    elif form['algorithm'].startswith("lda"):
        # Using lda
        # TODO: implement LDA
        model_name = form['algorithm'][4:]
        reviewers, matched_topics = match_by_lda(form["abstract"] + " " + form["full_text"], model_name)
        best_score = max([reviewers[reviewer]['score'] for reviewer in reviewers] or [0])
        match_result = RecommendationResult(email=user['email'],
                                            title=form['title'],
                                            result_json=json.dumps(reviewers),
                                            submission_json=json.dumps(form),
                                            matched_topics=json.dumps(matched_topics),
                                            algorithm='LDA: ' + model_name,
                                            database=model_name,
                                            count=len(reviewers),
                                            best_score=best_score)
        db.session.add(match_result)
        db.session.commit()
        return redirect(url_for("main.result", result_id=match_result.id))
    else:
        return redirect(url_for("main.match"))


@api.route('/result/<int:result_id>/<action>')
@requires_auth
def result_action(action, result_id):

    """
    Perform designated action on a result.
    :param action: the action, currently only "delete" is available.
    :param result_id: the ID of the result.
    :return: redirect the user back.
    """

    user = session['profile']
    result = RecommendationResult.query.get(result_id)
    if user['email'] == result.email:
        if action == "delete":
            db.session.delete(result)
            db.session.commit()
            return redirect(url_for("main.results"))
    else:
        return redirect(url_for("main.results"))
    # return redirect(url_for("main.result"))


@api.route('/get_result/<file_hash>', methods=['GET', 'POST'])
def get_result(file_hash):

    """
    Find relevant reviewers based on the default LDA model from a PDF file. For anonymous user only.
    :param file_hash: the hash of the uploaded PDF file.
    :return: a json that containing the result.
    """

    reviewers = pdf_match(file_hash)
    if reviewers:
        number_of_reviewers = len(reviewers)
        reviewers = get_rows(reviewers)
        if number_of_reviewers < 15:
            return jsonify(status="Success",
                           payload=render_template('landing/result.html', reviewers=reviewers, file_hash=file_hash))
        else:
            return jsonify(status="TooMany", message="Too many reviewers found, showing 15 out of " + str(
                number_of_reviewers) + ". Try giving us some more specific keywords.",
                           payload=render_template('landing/result.html', reviewers=reviewers[:5],
                                                   number_of_reviewers=str(number_of_reviewers), file_hash=file_hash))
    else:
        return jsonify(status="Error",
                       message="Seems that we can't find proper keywords in your paper."
                               "Try manually specifying some keywords?")


@api.route('/get_result/meta/<keywords_string>', methods=['GET', 'POST'])
def get_result_by_meta(keywords_string):

    """
    Find relevant reviewers from a list of keywords. For anonymous user only.
    :param keywords_string: a comma separated list of keywords.
    :return: a json containing the result.
    """

    keywords = keywords_string.split(",")
    args = request.args
    if args["title"] and args["abstract"]:
        title = args["title"]
        abstract = args["abstract"]
        reviewers = text_match(title + abstract)
        if reviewers:
            number_of_reviewers = len(reviewers)
            reviewers = get_rows(reviewers)
            if number_of_reviewers < 15:
                return jsonify(status="Success", payload=render_template('landing/result.html', reviewers=reviewers,
                                                                         number_of_reviewers=str(number_of_reviewers),
                                                                         file_hash='Null'))
            else:
                return jsonify(status="TooMany", message="Too many reviewers found, showing 15 out of " + str(
                    number_of_reviewers) + ". Try giving us some more specific keywords.",
                               payload=render_template('landing/result.html', reviewers=reviewers[:5],
                                                       number_of_reviewers=str(number_of_reviewers), file_hash='Null'))
        else:
            return jsonify(status="Error",
                           message="Sorry, we cannot find any reviewers suitable for your keywords.")
    else:
        # Will solely match by keywords
        reviewers = keyword_match(keywords)
        if reviewers:
            number_of_reviewers = len(reviewers)
            reviewers = get_rows(reviewers)
            if number_of_reviewers < 15:
                return jsonify(status="Success",
                               payload=render_template('landing/result.html', reviewers=reviewers,
                                                       number_of_reviewers=str(number_of_reviewers), file_hash="Null"))
            else:
                return jsonify(status="TooMany", message="Too many reviewers found, showing 15 out of " + str(
                    number_of_reviewers) + ". Try giving us some more specific keywords.",
                               payload=render_template('landing/result.html', reviewers=reviewers[:5],
                                                       number_of_reviewers=str(number_of_reviewers), file_hash="Null"))
        else:
            return jsonify(status="Error",
                           message="Sorry, we cannot find any reviewers suitable for your keywords.")


@api.route('/get_result/meta/', methods=['GET', 'POST'])
def no_keyword_exception():
    return jsonify(status="Error", message="You have to enter at least one keyword.")


class Reviewer:

    """
    This object is created solely for the convenience when rendering a list of reviewers.
    You can safely skip it.
    """

    def __init__(self, author):
        self.first_name = author["profile"]["first_name"]
        self.middle_name = author["profile"]["middle_name"]
        self.last_name = author["profile"]["last_name"]
        if author["profile"]["email"]:
            self.email = author["profile"]["email"]
        else:
            self.email = "Unknown"
        self.institution = author["profile"]["institution"]
        try:
            self.avatar_url = author["profile"]["avatar"]
        except KeyError:
            self.avatar_url = None
        self.keywords = author["keywords"]
        self.score = str(author["score"])[:3]
        self.email_hash = hashlib.sha256(self.email.lower()).hexdigest()
        self.valid = True
        self.bio = self.get_bio()
        self.json = author
        if not self.first_name or not self.last_name:
            self.valid = False

    def get_bio(self):
        if len(self.keywords) > 10:
            self.keywords = self.keywords[:5]
        if self.institution:
            institution = " is a professor in " + self.institution
        else:
            institution = ""
        try:
            if institution:
                keywords = ", who specialises in " + ", ".join(self.keywords)
            else:
                keywords = " specialises in " + ", ".join(self.keywords)
        except:
            keywords = ""
        try:
            return self.first_name + " " + self.last_name + institution + keywords + "."
        except:
            self.valid = False
            print("Invalid reviewer found:")


def pdf_match(file_hash, model=None):

    """
    This function is called when a visitor uploaded a PDF file in the landing page.
    It will return a list of Reviewer object using LDA model.

    :param file_hash: the hash of the uploaded pdf file.
    :param model: the name of the model to be used.
    :return: a list of Reviewer object.
    """
    if not model:
        model = current_app.config['DEFAULT_LDA_MODEL']
    file_path = os.path.join(current_app.config['UPLOADED_PAPERS_DEST'], file_hash + ".pdf")
    print("Tokenizing", file_path)
    text = text_blob_tokenise(file_path)
    result, matched_topics = match_by_lda(text, model)
    total_list = []
    for author in result:
        a = Reviewer(result[author])
        if a.valid:
            total_list.append(a)
    return total_list


def text_match(text, model=None):

    """
    This function is called when a visitor entered plain text using our forms in the landing page.
    It will return a list of Reviewer object using LDA model.

    :param text: the text user entered.
    :param model: the name of the model to be used.
    :return: a list of Reviewer object.
    """
    if not model:
        model = current_app.config['DEFAULT_LDA_MODEL']
    result, matched_topics = match_by_lda(text, model)
    total_list = []
    for author in result:
        a = Reviewer(result[author])
        if a.valid:
            total_list.append(a)
    return total_list


def keyword_match(keywords, db_name=None):

    """
    This function is called when a visitor entered a specific list of keywords.
    :param keywords: a list of keyword strings.
    :param db_name: name of the database to be used
    :return: a list of Reviewer object.
    """

    if not db_name:
        db_name = current_app.config['DEFAULT_DB']
    response = match_by_keyword(keywords, db_name)
    total_list = []
    for author in response:
        a = Reviewer(author)
        if a.valid:
            total_list.append(a)
    return total_list


def get_rows(total_list):

    """
    A helper that splits a list of Reviewers, and generates a list of rows of 3 Reviewers.
    :param total_list:
    :return: rows of 3 Reviewers
    """

    result_list = []
    for i in range(0, len(total_list), 3):
        three = []
        for j in range(3):
            try:
                three.append(total_list[i + j])
            except IndexError:
                pass
        result_list.append(three)
    return result_list
