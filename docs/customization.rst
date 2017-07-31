.. author: Alan Chen

Customizing Topic Extraction
============================

We use LDA model for topic extraction.

First you need a trained LDA model using ``gensim`` . You can find a
demo trained model on our the GitHub repository, or you can train one
yourself.

The extraction process consists of two parts:

1. Tokenizing (potentially includes noun phrase extraction)
2. Predicting topics with trained LDA Model

Customizing Tokenization
------------------------

The tokenizer is implemented in
:meth:`core.lda_engine.LdaModelWrapper.tokenize` . It is a method of a
LDA model since different models may need to tokenize differently (For
example, some need noun phrase extraction in addition to tokenizing).

See :meth:`core.lda_engine.LdaModelWrapper.tokenize` for more details.

Loading Your Own LDA Model
--------------------------

If you are training LDA model with ``gensim`` , you can load your
trained models in FMR by a few lines of configurations. See Installation
for details.

Make sure you also have the following components:

1. Gensim's ``.dictionary`` file, with which you trained the LDA model.
2. ``.json`` file, which stores the profiles of your pool of scholars.

Implementing LDA Model For Other Libraries
------------------------------------------

The :class:`core.lda_engine.LdaModelWrapper` class serves as an
abstraction layer between the rest of the application and the actual LDA
model.

If you have other LDA models implemented by other libraries, or even a
completely different language, you can rewrite the :class:`core.lda_engine.LdaModelWrapper`
to fit your need.

A minimal working :class:`core.lda_engine.LdaModelWrapper` should at least consists of the
following methods:

 - :meth:`core.lda_engine.LdaModelWrapper.predict` : it takes a raw text string and return a NumPy array of
   topics IDs and their confidence levels.
 - :meth:`core.lda_engine.LdaModelWrapper.get_author_top_topics`
 - :meth:`core.lda_engine.LdaModelWrapper.get_topic_in_string`
 - `core.lda_engine.LdaModelWrapper.authors_lib` : a dictionary that contains the profile of the pool
   of scholars. It must work in tandem with the matching algorithm. It will be automatically loaded if the configured correctly.
   See :ref:`LDA Models` for details.
