# -*- coding: utf-8 -*
"""
Created on Tue Dec  2 15:36:53 2019

@author: ajava
"""
import os
from pytube import YouTube
from pydub import AudioSegment
from pydub.silence import split_on_silence



#link = input("Enter the youtube link: ") 
link='https://www.youtube.com/watch?v=un500tl6Yec'
def getValue(link):
    return link[-11:]

videoValue=getValue(link)

folderDirectories=[r"mp4s",r"results",r"voiceOnly"]

def createFolders(folderDirs):
    
    """
    Creates folders (if they do not exist) that are used in the code. 
    If the folder are already there, handles with the exception.
    
    Parameters:
    
        folderDirs: the list of folder names
    
    """
    for directory in folderDirs:
        os.makedirs(directory, exist_ok=True) 
        os.makedirs(directory+'\\'+videoValue, exist_ok=True) 


createFolders(folderDirectories)


def getFromYoutube(adress):
    
    """
    Downloads the video in audio format (.mp4) in the specified folder.
    
    Parameters:
        
        adress: the web link of the Youtube video
    """
    
    addr=YouTube(adress)
    t=addr.streams.filter(only_audio=True).all()
    t[0].download(r'mp4s\{0}'.format(videoValue))
#   t[0].download(r'mp4s\{0}'.format(videoValue),filename=videoValue)



getFromYoutube(link)

fullNameMovie=[x[2] for x in os.walk(r'mp4s\{0}'.format(videoValue))][0][0]

movieName_noExtension=fullNameMovie[:-4] #removing .mp4 extension 


def convertToVoice(fromPath,fromFormat,toPath,toFormat):
    
    """
    Converts the audio formats by taking them from certain path and saving them in certain path.
    
    Parameters: 
        
        fromPath: The path from where the audio is taken
        
        fromFormat: The initial format of the audio
        
        toPath: The path where the converted audio to be saved
        
        toFormat: The format that audio will be converted to
    """
    
    mp4_audio = AudioSegment.from_file(fromPath, format=fromFormat)
    mp4_audio= mp4_audio.set_frame_rate(16000)
    mp4_audio.export(toPath, format=toFormat)


#convertToVoice(r'SoX\MAGoutput001.wav','wav',r'test.wav','wav')
#from pydub.utils import mediainfo
#info = mediainfo(r"results\WRZQURSfhJ4\WRZQURSfhJ4_019.wav")
#print(info['sample_rate'])
def maintain_Loudness(voice, target_dBFS):
    
    """
    Maintains the volume level (in Decibels Relative to the Full Scale) of the splitted audio piece. It adds the gain
    needed for the audio to reach the target decibel relative to the full scale.
    
    Parameters: 
        
        voice: GIven current voice piece.
        
        target_dBFS:  Desired Decibels level for the audio formats relative to the full scale.
    """
        
    changed_dBFS = target_dBFS - voice.dBFS
    return voice.apply_gain(changed_dBFS)

def splitToPieces(fromPath, minSilence, silenceThreshold, addedSilence, targetLoudness, brate):
    
    """
    Divides the specified audio file into several smaller files with respect to
    silence levels ( which are to be specified in paramters). It then saves the files in auto-generated 'results' folder. 
    
    Parameters:
        
        fromPath: The path from where the audio is taken.
        
        minSilence: Minimum silence duration, in milliseconds, expected before splitting the audio
        
        silenceThreshold: Minimum silence level, in Decibels Relative to the Full Scale (dBFS), expected before splitting the audio
        
        addedSilence: The duration, in milliseconds, of padding (artificial silence) applied to both ends of the splitted audio piece
                
        targetLoudness: Desired Decibels level for the audio formats relative to the full scale
        
        brate: The bit rate (it should be string e.g. "16k", "32k" etc. not an integer value) of the audio to be exported.
        
    """
    
    movie_voice = AudioSegment.from_mp3(fromPath)
    voiceList = split_on_silence (movie_voice, min_silence_len=minSilence, silence_thresh=silenceThreshold)
        #anything quieter than -32 dbFS will be considered as silent
    for i, singleVoice in enumerate(voiceList):
        
        # Creating 500ms long silence
        artificial_silence = AudioSegment.silent(duration=addedSilence)
        # Adding the created voice to 2 endpoints of the single voice
        new_single_voice = artificial_silence + singleVoice + artificial_silence
    
        
        loudMaintained_voice = maintain_Loudness(new_single_voice, targetLoudness)
    
        print("{0}_{1}.wav".format(videoValue,str(i).zfill(3)))
        
        loudMaintained_voice.export( 
            r"results\{0}\{1}_{2}.wav".format(videoValue,videoValue,str(i).zfill(3)),
            bitrate = brate,
            format = "wav"
        )

convertToVoice(r"mp4s\{0}\{1}.mp4".format(videoValue,movieName_noExtension),"mp4",r"voiceOnly\{0}\{1}.wav".format(videoValue, movieName_noExtension),"wav")
splitToPieces(r'voiceOnly\{0}\{1}.wav'.format(videoValue,movieName_noExtension),500,-34,500,-20.0,16000)
    


