# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 16:56:55 2020

@author: ajava
"""

import io
import os
# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

#setting credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"C:\Users\ajava\OneDrive\Desktop\ATL\Data Collection\fullyDynamicYoutube\MyFirstProject-6946f52b5b92.json"

# Instantiating a client
client = speech.SpeechClient()


# The name of the audio file to transcribe
for videovalue in os.listdir(r'results'):
    txtfile=open(r"results\{0}\{0}.txt".format(videovalue),"a+",encoding='utf-8')
    for audio in os.listdir(r'results'+'\\'+videovalue):
        
        if (audio[-4:]=='.wav'):
            auid = audio
            with io.open(r'results'+'\\'+ videovalue +'\\'+audio, 'rb') as audio_file:
                content = audio_file.read()
                audio = types.RecognitionAudio(content=content)
        
            config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code='az-AZ',
                audio_channel_count=2)
        
            # Detects speech in the audio file
            response = client.recognize(config, audio)
            
            for result in response.results:
                text = '{0} ~ {1}\n'.format(auid,result.alternatives[0].transcript)
                txtfile.writelines(text)
                print(text)
    txtfile.close()



