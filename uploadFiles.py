import os
from flask import flash, send_file
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './UPLOADED_FILES'
ALLOWED_EXTENSIONS = {
    'txt',
    'wav',
}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(request):
    # check if post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    # if file is present, then save it in UPLOAD_FOLDER
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return { 'status': 'success', 'message': 'File uploaded successfully.', 'fileInfo': { 'name': filename } }

def download_file(filepath):
    print('ddddddd', filepath)
    path = filepath
    return send_file(path, as_attachment=True)
