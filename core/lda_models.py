from app.utils.environment import load_env
import pickle
import json


model_files = load_env('lda_models.env')


def load_file(model_name):
    try:
        return json.load(open('models' + model_files[model_name] + ".json", "rb"))
    except:
        return pickle.load(open('models' + model_files[model_name] + ".pkl", "rb"))


def load_author_libs():
    author_libs = {model_name: load_file(model_name) for model_name in model_files}
    return author_libs
