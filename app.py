from flask import Flask, request, send_file
from flask_cors import CORS

# importing from uploadFiles.py
from uploadFiles import (upload_file, download_file, UPLOAD_FOLDER)

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# importing voice_to_text function from file functions.py
from audioToText import (voice_to_text)

@app.route('/')
def hello_world():
    return 'Hello, World! - this is flask server'

@app.route('/upload-file', methods=['POST'])
def uploadFile():
    try:
        uploadFileResponse = upload_file(request)
        if uploadFileResponse['status'] == 'success':
            uploadedFilename = uploadFileResponse['fileInfo']['name']
            return { 'status': 'success', 'message': 'File uploaded successfully, conversion to text has begun', 'filename': uploadedFilename }
    except:
        return { 'status': 'failed', 'message': 'Failed to uploaded the file, please try again later', 'filename': '' }

@app.route('/audio-to-text', methods=['POST'])
def audioToText():
#    text = voice_to_text()
#    return text
    uploadedFilename = request.json['filename']
    print('uploadedFilename', uploadedFilename)
    voiceToTextResponse = voice_to_text(uploadedFilename)
    if voiceToTextResponse['status'] == 'success':
        return send_file(voiceToTextResponse['filePathToDownload'], as_attachment=True)
    if voiceToTextResponse['status'] == 'failed':
        return { 'status': 'failed', 'message': 'Failed to convert audio file to text. Please try again.' }

if __name__ == "__main__":
    app.run(host='0.0.0.0')
