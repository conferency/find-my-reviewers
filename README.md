# Findmyreviewers

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/206da692fc274d868123b537d5a5c1a3)](https://www.codacy.com/app/alanzchen/find-my-reviewers?utm_source=github.com&utm_medium=referral&utm_content=conferency/find-my-reviewers&utm_campaign=Badge_Grade) [![Documentation Status](https://readthedocs.org/projects/findmyreviewers/badge/?version=latest)](http://findmyreviewers.readthedocs.io/en/latest/?badge=latest)

Findmyreviewers (FMR in short) is an open-source project that extracts *topics* from a piece of text using trained LDA models and tries to find best matching scholars from a pool of scholars.

Under the hood, it uses LDA models to extract *topics* and tries to find a set of best matches of reviewers.

The web app is built on top of `flask` and the LDA model is trained with `gensim`. With slight modification, you can also use other libraries to replace `gensim` and load your own trained LDA model.

## Installation

Make sure your Python version is 2.7.x.

### Environment

Using `virtualenv` is highly recommended.

If you do not have a virtual environment yet on the project folder, set it up with:

```
$ virtualenv venv

```

Then activate the virtual environment:

```
$ source venv/bin/activate

```

Install packages:

```
$ pip install -r requirements.txt
```

Download demo models:

```
$ cd trained
$ python download.py
$ cd ..
```

### Running the server

Initialize web app database:

```
$ python manage.py create_table
```

Run the web app server:

```
$ python manage.py runserver

```

Then after navigate to the following address:

```
127.0.0.1:5000
```

To access the dashboard, please visit:

```
127.0.0.1:5000/dashboard
```

## Customization and Development

We have a rough documents available in the `/docs` folder.

You can also checkout an online version at [http://findmyreviewers.readthedocs.io](http://findmyreviewers.readthedocs.io).

There are also some jupyter notebooks in the `/tutorial` folder. They cover:

- How we preprocess the data
- How we trained the model
- How the matching algorithm is developed

## Plan

We will keep refining the project as well as the documentation.

Currently we are looking at:

- Refining the preprocessing procedures
- Refining LDA model training
- Implementing Author-topics model

## Demo Model and Databases

A trained demo LDA model and a demo database is shipped with this repository.

The LDA model is trained with our complete full text corpus (tons of pdfs). It retains all the states and data you need to further train it with new documents.

The demo database is a portion of our complete database, as the data sources do not allow us to reveal the data.

Therefore, the matching results from our demo database may seem sub-optimal because the lack of complete data.

## Acknowledgements

To focus on more important stuff, we make use of several open-source libraries and projects. We sincerely appreciate their works.

### Python Libraries

- gensim
- nltk
- TextBlob
- flask (and several extensions)

etc.

### Web

Frontend template: https://freehtml5.co/elate-free-html5-bootstrap-template/

Dashboard template: https://github.com/puikinsh/gentelella

# Sponsors

This project is sponsored by:

<p style="text-align: center; display: block; margin: auto;"  align="center"><a href="http://www.cuhk.edu.cn"><img width="200" src="docs/_static/cuhksz.png" style="width: 200px; margin: auto; display: block;"></a></p>

<p style="text-align: center; display: block; margin: auto;"  align="center">The Chinese University of Hong Kong, Shenzhen</p>

<p style="text-align: center; display: block; margin: auto;"  align="center"><a href="http://udel.edu"><img width="200" src="docs/_static/udel.png" style="width: 200px; margin: auto; display: block"></a></p>

<p style="text-align: center; display: block; margin: auto;"  align="center">University of Delaware</p>

<p style="text-align: center; display: block; margin: auto;"  align="center"><a href="http://conferency.com"><img width="200" src="docs/_static/conferency-green.png" style="width: 200px; margin: auto; display: block"></a></p>

<p style="text-align: center; display: block; margin: auto;"  align="center">Conferency</p>