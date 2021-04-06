import os
from flask import flash, send_file
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {
    'txt',
    'wav',
    'jpg'
}

# Check if the file name is as per allowed extensions
def allowed_file(filename):
    try:
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    except Exception as e:
        print('filename is not as per allowed extinsions'. e)
        return False

def upload_file(request, UPLOAD_FOLDER):
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
    path = filepath
    return send_file(path, as_attachment=True)
