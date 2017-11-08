import requests
from core.keyword_db import keyword_dbs
from core.lda_engine import models
from core.matching.lda import detailed_results
from flask import render_template, redirect, request, \
    json, session

from app.modules.main.errors import page_not_found
from app.utils.decorators import requires_auth
from .constants import auth0
from core.helper.tables import get_top_keywords
from . import main
from ...models import *

colors = ['#a50026', '#d73027', '#f46d43', '#fdae61', '#fee08b', '#ffffbf', '#d9ef8b', '#a6d96a', '#66bd63', '#1a9850',
          '#006837']


# Set cache control to private
@main.after_request
def add_header(response):
    response.cache_control.private = True
    response.cache_control.public = False
    return response


# Landing Page
@main.route('/')
def index():
    # if the user is logged in, redirect to dashboard
    if 'profile' in session:
        return redirect(url_for('main.dashboard'))
    else:
        return render_template('landing/landing.html', auth0=auth0)


@main.route('/dashboard')
@requires_auth
def dashboard():
    # TODO: Change results page to a general dashboard
    user = session['profile']
    results = RecommendationResult.query.filter_by(email=user['email'])
    return render_template('dashboard/results.html', results=results, user=user)


@main.route('/dashboard/results')
@requires_auth
def results():
    user = session['profile']
    user_results = RecommendationResult.query.filter_by(email=user['email'])
    return render_template('dashboard/results.html', results=user_results, user=user)


@main.route('/dashboard/result/<int:result_id>')
@requires_auth
def result(result_id):
    current_result = RecommendationResult.query.get(result_id)
    if not current_result:
        return page_not_found()
    reviewers = json.loads(current_result.result_json)
    submission = json.loads(current_result.submission_json)
    if current_result.matched_topics_json:
        matched_topics = json.loads(current_result.matched_topics_json)
    else:
        matched_topics = None
    return render_template('dashboard/result.html',
                           colors=colors,
                           matched_topics=matched_topics,
                           result=current_result,
                           submission=submission,
                           reviewers=reviewers,
                           user=session['profile'])


@main.route('/dashboard/result/<int:result_id>/<int:author_id>')
@requires_auth
def result_author(result_id, author_id):
    result = RecommendationResult.query.get(result_id)
    if not result:
        return page_not_found()
    reviewers = json.loads(result.result_json)
    author = reviewers[str(author_id)]  # TODO: More elegant way to store this metadata
    if result.algorithm.startswith("LDA"):
        model = models[result.algorithm[5:]]
        topics_list = model.get_author_top_topics(author_id)
        topics = model.get_topics_in_string(topics=topics_list, confidence=True)
    else:
        topics = []
    keywords = get_top_keywords(result.database, author_id, 10)
    return render_template('dashboard/result_author.html',
                           author=author,
                           topics=topics,
                           keywords=keywords,
                           user=session['profile'])


@main.route('/dashboard/<database_name>/<int:author_id>')
@requires_auth
def author(database_name, author_id):
    if database_name in models:
        model = models[database_name]
        # This is a LDA model
        topics_list = model.get_author_top_topics(author_id)
        topics = model.get_topics_in_string(topics=topics_list, confidence=True)
    else:
        topics = None
    author_ = detailed_results([[author_id, 0]], database_name)[author_id]
    keywords = get_top_keywords(database_name, author_id, 10)
    return render_template('dashboard/author.html',
                           database_name=database_name,
                           author=author_,
                           topics=topics,
                           keywords=keywords,
                           user=session['profile'])


@main.route('/dashboard/match/')
@requires_auth
def match():
    return render_template('dashboard/match.html',
                           keyword_dbs=keyword_dbs,
                           models=list(models.keys()),
                           user=session['profile'])


@main.route('/dashboard/model/<model_name>/topic/<topic_id>')
@requires_auth
def model_topic(model_name, topic_id):
    # TODO
    pass

# Auth0
@main.route('/callback')
def callback_handling():
    code = request.args.get('code')

    json_header = {'content-type': 'application/json'}

    token_url = "https://{domain}/oauth/token".format(domain='findmyreviewers.auth0.com')

    token_payload = {
        'client_id': auth0['client_id'],
        'client_secret': auth0['client_secret'],
        'redirect_uri': auth0['base_uri'] + '/callback',
        'code': code,
        'grant_type': 'authorization_code'
    }
    # print token_payload
    token_info = requests.post(token_url, data=json.dumps(token_payload), headers=json_header).json()
    # print token_info
    user_url = "https://{domain}/userinfo?access_token={access_token}" \
        .format(domain='findmyreviewers.auth0.com', access_token=token_info['access_token'])

    user_info = requests.get(user_url).json()

    # We're saving all user information into the session
    session['profile'] = user_info

    # Redirect to the User logged in page that you want here
    # In our case it's /dashboard
    return redirect('/dashboard')


@main.route('/login')
def login():
    return render_template('landing/login.html', auth0=auth0)


@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))