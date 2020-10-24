# importing libraries 
import speech_recognition as sr 
  
#import os 
from os import path
  
# importing from uploadFiles.py
from uploadFiles import (upload_file, UPLOAD_FOLDER)


def voice_to_text(filename):

    # open a file where we will concatenate   
    # and store the recognized text 
    fh = open("recognized.txt", "w+") 

#    filePath = 'english.wav'
    AUDIO_FILE = path.join(UPLOAD_FOLDER, filename)

    # create a speech recognition object
    r = sr.Recognizer()

    # open the audio file
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source) # read entire audio file

#    # recognize speech using Wit.ai
#    WIT_AI_KEY = "PIH7VF3VCM4X4RTYNS2K4ZPRAWKZ6R5E"  # Wit.ai keys are 32-character uppercase alphanumeric strings
#    try:
#        rec = r.recognize_wit(audio, key=WIT_AI_KEY)
#        return("Wit.ai thinks you said " + r.recognize_wit(audio, key=WIT_AI_KEY))
#        fh.write(rec+". ") 
#    except sr.UnknownValueError:
#        return("Wit.ai could not understand audio")
#    except sr.RequestError as e:
#        return("Could not request results from Wit.ai service; {0}".format(e))


# recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        rec = r.recognize_google(audio)
        fh.write(rec+". ")
#        return("Google Speech Recognition thinks you said " + rec)
        return {'status': 'success', 'filePathToDownload': './recognized.txt'}
    except sr.UnknownValueError:
        return("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        return("Could not request results from Google Speech Recognition service; {0}".format(e))



