import requests
from os.path import exists
from os import mkdir
import os
import zipfile

files = {
    os.path.join("demo", "model.ldamodel.state.sstats.npy"): "0B28rFtb9-7L7emhkM3BiT0U0clU",
    os.path.join("demo", "model.ldamodel.state"): "0B28rFtb9-7L7UXBkdjVhQ3pKZUU",
    os.path.join("demo", "model.ldamodel.id2word"): "0B28rFtb9-7L7bEt2b01ROFBuYm8",
    os.path.join("demo", "model.ldamodel.expElogbeta.npy"): "0B28rFtb9-7L7QnloRWx1V0NpMFE",
    os.path.join("demo", "model.ldamodel"): "0B28rFtb9-7L7eHlvQ3RyZm9WT00",
    # os.path.join("demo", "model.ldamodel.json"): "0B28rFtb9-7L7eDZ5YjVOMWlNLWM",
    os.path.join("demo", "model.dictionary"): "0B28rFtb9-7L7R2tJSE5nYTNQUjA",
    os.path.join("demo", "author_lib.json.zip"): "1KxYQIDSr9ZTz3FfFJXDeqnS5qmEg9PJS",
    os.path.join("demo", "paper_vec_lib.json"): "1bElKCX0omNjITzySjvsj83QZQ75EZ5Fq"
}

def download_file_from_google_drive(file_id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    print("Downloading", destination)
    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


if __name__ == "__main__":
    if not exists('demo/'):
        mkdir('demo')
    for file_name, file_id in files.items():
        if exists(file_name):
            print("File", file_name, "already exists. Skipping.")
        else:
            download_file_from_google_drive(file_id, file_name)
    if exists(os.path.join('demo', 'author_lib.json.zip')):
        print('Extracting author_lib.json.zip...')
        z = zipfile.ZipFile(os.path.join('demo', 'author_lib.json.zip'))
        z.extractall(path='demo/')