import requests
from os.path import exists

files = {
    "demo.ldamodel.state.sstats.npy": "0B28rFtb9-7L7emhkM3BiT0U0clU",
    "demo.ldamodel.state": "0B28rFtb9-7L7UXBkdjVhQ3pKZUU",
    "demo.ldamodel.id2word": "0B28rFtb9-7L7bEt2b01ROFBuYm8",
    "demo.ldamodel.expElogbeta.npy": "0B28rFtb9-7L7QnloRWx1V0NpMFE",
    "demo.ldamodel": "0B28rFtb9-7L7eHlvQ3RyZm9WT00",
    "demo.ldamodel.json": "0B28rFtb9-7L7eDZ5YjVOMWlNLWM",
    "demo.ldamodel.dictionary": "0B28rFtb9-7L7R2tJSE5nYTNQUjA"
}


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    print("Downloading " + destination)
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
    for file_name, file_id in files.iteritems():
        if exists(file_name):
            print("File " + file_name + " already exists. Skipping.")
        else:
            download_file_from_google_drive(file_id, file_name)
