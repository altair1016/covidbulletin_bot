"""
Speech to text class to handle telegram voice message
@name : speech2text.py
@author: Marco Iannella (altair1016)
"""
from pydub import AudioSegment
import speech_recognition as sr

def sp2tx(file_audio):
    """
    Transform an audio file into a string
    :param file_audio: telegram audio file
    :return: string containing vocal request
    """
    file_audio_dest = convert_ogg_to_wav(file_audio)
    r = sr.Recognizer()
    audio = sr.AudioFile(file_audio_dest)
    with audio as source:
        audio = r.record(source)
    text = r.recognize_google(audio, language='it-IT')
    return text

def convert_ogg_to_wav(orig_song):
    """
    Converts a telegram OGA format to a WAV file
    :param orig_song: telegram OGA audio file
    :return: path of the wav file
    """
    dest_file = orig_song.split('.')[0] + ".wav"
    song = AudioSegment.from_ogg(orig_song)
    song.export(dest_file, format="wav")
    return dest_file



