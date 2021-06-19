import os
from flask import Flask, request, send_file
from flask_cors import CORS

# importing from uploadFiles.py
from uploadFiles import (upload_file, download_file)
from audioToText import (audio_to_text)
# importing functions
from functions import (deleteUploadedFileByName, emptyFolder, compressImage, convertImageToBase64)
from machine_learning.predictGender import (predict_gender_from_image)
from machine_learning.imageToSketch import (applyFilterOnImageByConversionType)

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
            return {
                'status': 'success',
                'message': 'File uploaded successfully',
                'filename': uploadedFilename
            }
        else:
            return {
                'status': 'failed',
                'message': uploadFileResponse['message']
            }
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

# API to predict human face from the image file name
@app.route('/predict-gender-by-image-name', methods=['POST'])
def predictGender():
    try:
        uploadedFilename = request.json['filename']
        imagePath = UPLOAD_FOLDER + '/' + uploadedFilename
        res = predict_gender_from_image(imagePath, 'bgr', uploadedFilename)
        if res['status'] == 'success':
            # delete the uploaded image once prediction was done from it
            deleteUploadedFileByName(uploadedFilename, UPLOAD_FOLDER)
            compressedImage = compressImage(res['predictedImage'])
            conversionResponse = convertImageToBase64(res['predictedImage'])
            if conversionResponse['status'] == 'success':
                # delete the predicted image
                deleteUploadedFileByName(uploadedFilename, res['predictedFolderPath'])
                return {
                    'status': 'success',
                    'message': 'Predicted gender successfully',
                    'image': conversionResponse['base64']
                }
            else:
                return {
                    'status': 'failed',
                    'message': 'Failed to predict gender',
                    'image': None
                }
    except Exception as e:
        print('error--on--predicting gender API', e)
        return { 'status': 'failed', 'message': 'Failed to predict gender. Please try again.' }

# API TO DELETE THE FILE BASED ON THE FILE NAME
@app.route('/delete-file', methods=['POST'])
def deleteFile():
    try:
        uploadedFilename = request.json['filename']
        res = deleteUploadedFileByName(uploadedFilename, UPLOAD_FOLDER)
        return res;
    except Exception as e:
        return { 'status': 'failed', 'message': 'Failed to delete the file. Please try again.' }
        

# API TO CONVERT AN IMAGE TO SKETCH
@app.route('/convert-image-to-sketch', methods=['POST'])
def convertImageToSketch():
    try:
        uploadedFilename = request.json['filename']
        imagePath = os.path.join(UPLOAD_FOLDER, uploadedFilename)
        conversionType = request.json['conversionType']
        widgetParameters = request.json['widgetParameters']
        res = applyFilterOnImageByConversionType(uploadedFilename, imagePath, conversionType, widgetParameters)
        if res['status'] == 'success':
            # delete the uploaded image once prediction was done from it
            # deleteUploadedFileByName(uploadedFilename, UPLOAD_FOLDER)
            # compressedImage = compressImage(res['predictedImage'])
            conversionResponse = convertImageToBase64(res['predictedImage'])
            if conversionResponse['status'] == 'success':
                # delete the predicted image
                deleteUploadedFileByName(uploadedFilename, res['predictedFolderPath'])
                return {
                    'status': 'success',
                    'message': 'Filter applied successfully',
                    'image': conversionResponse['base64']
                }
            else:
                return {
                    'status': 'failed',
                    'message': 'Failed to apply filter',
                    'image': None
                }
    except Exception as e:
        return {
            'status': 'failed',
            'message': 'Failed to convert an image. Please try again'
        }

# API TO DELETE FILES PRESENT IN UPLOADED_FILES FOLDER
@app.route('/delete-files-in-upload-folder', methods=['POST'])
def deleteFilesInUploadFolder():
    try:
        isDeleteFiles = request.json['deleteFiles'] # a sample key to trigger delete files
        if isDeleteFiles:
            res = emptyFolder(UPLOAD_FOLDER)
            if res['status'] == 'success':
                return {
                    'status': 'success',
                    'message': 'Deleted successfully'
                }
            else:
                return {
                    'status': 'failed',
                    'message': 'Failed to empty the folder. Please try again'
                }
    except Exception as e:
        return {
            'status': 'failed',
            'message': 'Failed to empty the folder. Please try again'
        }
