from flask import Flask, request, send_file
from flask_cors import CORS

# importing from uploadFiles.py
from uploadFiles import (upload_file, download_file)
from audioToText import (audio_to_text)
# importing functions
from functions import (deleteUploadedFileByName)

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = './UPLOADED_FILES'


UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']

# this is the initial route
@app.route('/')
def hello_world():
    return 'Hello visitor! - this is flask server created by Phani. Try navigating to https://react-app-collage.web.app/ instead to see how I perform.'

# API to catch the uploaded audio file
@app.route('/upload-file', methods=['POST'])
def uploadFile():
    try:
        uploadFileResponse = upload_file(request, UPLOAD_FOLDER)
        if uploadFileResponse['status'] == 'success':
            uploadedFilename = uploadFileResponse['fileInfo']['name']
            return { 'status': 'success', 'message': 'File uploaded successfully, conversion to text has begun', 'filename': uploadedFilename }
    except Exception as e:
        print('error---on---uploadfile', e)
        return { 'status': 'failed', 'message': 'Failed to uploaded the file, please try again later', 'filename': '' }

# API which receives the file name of the uploaded file and returns the text of it
@app.route('/audio-to-text', methods=['POST'])
def audioToText():
    try:
        uploadedFilename = request.json['filename']
        voiceToTextResponse = audio_to_text(uploadedFilename, UPLOAD_FOLDER)
        if voiceToTextResponse['status'] == 'success':
        # delete the audio file once text has been generated from it
            deleteUploadedFileByName(uploadedFilename, UPLOAD_FOLDER)
            return send_file(voiceToTextResponse['filePathToDownload'], as_attachment=True)
        if voiceToTextResponse['status'] == 'failed':
            return { 'status': 'failed', 'message': 'Failed to convert audio file to text. Please try again.' }
    except Exception as e:
        print('error--on--transcripting an audio file', e)
        return { 'status': 'failed', 'message': 'Failed to convert audio file to text. Please try again.' }
