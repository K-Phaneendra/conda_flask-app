import os
import base64
from PIL import Image
import smtplib

def deleteUploadedFileByName(fileName, UPLOAD_FOLDER):
    try:
        filePath = os.path.join(UPLOAD_FOLDER, fileName)
        # check if file exists
        if os.path.exists(UPLOAD_FOLDER):
            os.remove(filePath)
            return { 'status': 'success', 'message': 'File deleted successfully' }
        else:
            return { 'status': 'failed', 'message': 'The file does not exist' }
    except Exception as e:
        print('error--on--deleting a file', e)
        return { 'status': 'failed', 'message': 'Failed to delete a file.' }

def emptyFolder(folderPath):
    try:
        totalFiles = os.listdir(folderPath)
        deletedFilesCount = 0
        for filename in os.listdir(folderPath):
            # apart from ReadMe.txt, delete rest of the files
            if filename != 'ReadMe.txt':
                deletedFilesCount += 1
                deleteUploadedFileByName(filename, folderPath)
        if deletedFilesCount == len(totalFiles) - 1:
            # all files are successfully deleted
            return { 'status': 'success', 'message': 'Files deleted successfully' }
    except Exception as e:
        return { 'status': 'failed', 'message': 'Failed to delete a file.' }
    

def compressImage(imagePath):
    try:
        # open the image
        picture = Image.open(imagePath)
        # Save the picture with desired quality
        # To change the quality of image,
        # set the quality variable at
        # your desired level, The more 
        # the value of quality variable 
        # and lesser the compression
        picture.save(imagePath, 
                    "JPEG", 
                    optimize = True, 
                    quality = 10)
        return { 'status': 'success', 'message': 'Compressed image successfully' }
    except Exception as e:
        print('error--on--compressing image', e)
        return { 'status': 'failed', 'message': 'Failed to compress image.' }

def convertImageToBase64(imagePath):
    try:
        ENCODING = 'utf-8'
        with open(imagePath, "rb") as img_file:
            byte_content = img_file.read()
            base64_bytes = base64.b64encode(byte_content)
            base64_string = base64_bytes.decode(ENCODING)
            img_str = 'data:image/png;base64,' + base64_string
        return { 'status': 'success', 'base64': img_str }
    except Exception as e:
        print('error--on--converting to base64', e)
        return { 'status': 'failed', 'message': 'Failed to convert to base64.' }

def sendEmailWithFormDetails(formDetails):
    try:
        # TO EMAIL IS MENTIONED IN FORM formDetails
        # FROM EMAIL WILL BE gokusaiyan.z@outlook.com for now
        developerEmail = 'gokusaiyan.z@outlook.com'
        password = 'ab12c34d!'

        # COMPOSE THANK YOU EMAIL TO THE ONE WHO SUBMITTED THE FORM
        
        receiverEmail = formDetails['email']
        subject = 'Thank you '+formDetails['name']+' for contacting me'
        message = """From: Phaneendra Kosanam <"""+developerEmail+""">
To: """+formDetails['name']+""" <"""+receiverEmail+""">
MIME-Version: 1.0
Content-type: text/html
Subject: """+subject+"""

This is an e-mail message to be sent in HTML format

<b>Thank you for contacting</b>
<h1>This email is only part of the demo</h1>
<h3>Message</h3>
"""+formDetails['message']+"""
"""

        # COMPOSE INFO EMAIL TO THE DEVELOPER
        subject_info = 'Received a contact form request from '+formDetails['name']
        message_info = """To: Phaneendra Kosanam <"""+developerEmail+""">
From: Phaneendra Kosanam <"""+developerEmail+""">
MIME-Version: 1.0
Content-type: text/html
Subject: """+subject_info+"""

This is an e-mail message to be sent in HTML format

<b>Contact form request received</b>
<h1>This email is only part of the demo</h1>
<h3>Name</h3>
"""+formDetails['name']+"""
<h3>E-mail</h3>
"""+formDetails['email']+"""
<h3>Message</h3>
"""+formDetails['message']+"""
"""

        # Email config
        server = smtplib.SMTP('smtp-mail.outlook.com', 587);
        server.starttls()
        server.login(developerEmail, password)

        # SEND EMAIL TO THE ONE WHO SUBMITTED THE CONTACT FORM
        server.sendmail(developerEmail, receiverEmail, message)
        # SEND INFO EMAIL TO DEVELOPER
        server.sendmail(developerEmail, developerEmail, message_info)

        messageT = 'A thank you email has been sent to '+formDetails['email']

        return {
            'status': 'success',
            'message': messageT
        }
    except Exception as e:
        return { 'status': 'failed', 'message': str(e) }
