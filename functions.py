import os

def deleteUploadedFileByName(fileName, UPLOAD_FOLDER):
    try:
        filePath = UPLOAD_FOLDER + "/" + fileName
        # check if file exists
        if os.path.exists(UPLOAD_FOLDER):
            os.remove(filePath)
            return { 'status': 'success', 'message': 'File deleted successfully' }
        else:
            return { 'status': 'failed', 'message': 'The file does not exist' }
    except Exception as e:
        print('error--on--deleting a file', e)
        return { 'status': 'failed', 'message': 'Failed to delte a file.' }
