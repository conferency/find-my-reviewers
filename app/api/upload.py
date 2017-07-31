from flask import request, current_app, jsonify
from werkzeug.utils import secure_filename
from . import api
from errors import bad_request
import os
import hashlib


# upload pdf files
@api.route('/upload-file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return bad_request("Bad Request")
        uploaded_file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if uploaded_file.filename == '':
            return bad_request("No file uploaded")
        if uploaded_file and allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            full_path = os.path.join(current_app.config['UPLOADED_PAPERS_DEST'], filename)
            uploaded_file.save(full_path)
            file_size = os.path.getsize(full_path)
            file_hash = sha256(full_path)
            os.rename(os.path.join(current_app.config['UPLOADED_PAPERS_DEST'], filename),
                      os.path.join(current_app.config['UPLOADED_PAPERS_DEST'], file_hash + ".pdf"))
            return jsonify(name=filename, size=file_size, file_hash=file_hash)
    return bad_request("Unable to handle this request")


def allowed_file(filename):
    allowed_extension = ['pdf']
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in allowed_extension


def sha256(filename):
    hash_sha256 = hashlib.sha256()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()
