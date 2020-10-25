# importing libraries 
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
  
import os 
from os import path

# importing from uploadFiles.py
from uploadFiles import (upload_file, UPLOAD_FOLDER)


def voice_to_text(filename):

    AUDIO_FILE = path.join(UPLOAD_FOLDER, filename)
    # open the audio file stored in 
    # the local system as a wav file. 
    song = AudioSegment.from_wav(AUDIO_FILE) 

    # open a file where we will concatenate   
    # and store the recognized text
    fh = open("recognized.txt", "w+") 

    chunk_length_ms = 30000 # 30 seconds

    chunks = make_chunks(song, chunk_length_ms) # make chunks of 30 seconds

    # create a directory to store the audio chunks. 
    try: 
        os.mkdir('audio_chunks') 
    except(FileExistsError): 
        pass
  
    # move into the directory to 
    # store the audio files. 
    os.chdir('audio_chunks') 


    i = 0
    # process each chunk 
    for chunk in chunks: 

        # export audio chunk and save it in  
        # the current directory. 
        print("saving chunk{0}.wav".format(i)) 
        # specify the bitrate to be 192 k 
        chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav") 
  
        # the name of the newly created chunk 
        filename = 'chunk'+str(i)+'.wav'
  
        print("Processing chunk file "+filename) 
  
        # get the name of the newly created chunk 
        # in the AUDIO_FILE variable for later use. 
        file = filename 
  
        # create a speech recognition object 
        r = sr.Recognizer() 
  
        # recognize the chunk 
        with sr.AudioFile(file) as source: 
            audio = r.record(source) # read entire audio file
  
        try: 
            # try converting it to text 
            rec = r.recognize_google(audio) 
            # write the output to the file. 
            fh.write(rec+". ") 
            
        # catch any errors. 
        except sr.UnknownValueError: 
            print("Could not understand audio") 
            return {'status': 'failed', 'filePathToDownload': ''}
  
        except sr.RequestError as e: 
            print("Could not request results. check your internet connection") 
            return {'status': 'failed', 'filePathToDownload': ''}
  
        i += 1
  
    os.chdir('..')
    return {'status': 'success', 'filePathToDownload': './recognized.txt', 'text': rec}


