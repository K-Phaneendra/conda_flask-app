import os
import base64

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
        return { 'status': 'failed', 'message': 'Failed to delete a file.' }

def convertImageToBase64(imagePath):
    try:
        ENCODING = 'utf-8'
        with open(imagePath, "rb") as img_file:
            byte_content = img_file.read()
            base64_bytes = base64.b64encode(byte_content)
            base64_string = base64_bytes.decode(ENCODING)
            img_str = 'data:image/jpeg;base64,' + base64_string
        return { 'status': 'success', 'base64': img_str }
    except Exception as e:
        print('error--on--converting to base64', e)
        return { 'status': 'failed', 'message': 'Failed to convert to base64.' }
