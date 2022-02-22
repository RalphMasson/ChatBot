import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from scipy.io.wavfile import write
import speech_recognition as sr


fs=44100
duration = 5  # seconds
myrecording = sd.rec(duration * fs, samplerate=fs, channels=2,dtype='float64')
print ("Recording Audio")
sd.wait()
print ("Audio recording complete , Play Audio")
sd.play(myrecording, fs)
sd.wait()
print ("Play Audio Complete")
import wavio
wavio.write(r"C:\Users\MASSON\Desktop\ChatBot\input.wav",myrecording,fs,sampwidth=3)
sound = r"C:\Users\MASSON\Desktop\ChatBot\input.wav"
recognizer = sr.Recognizer()
with sr.AudioFile(sound) as source:
    # recognizer.adjust_for_ambient_noise(source)
    print("Converting the answer to text...")
    audio = recognizer.listen(source)
    text = recognizer.recognize_google(audio,language="fr-FR",show_all=True)
    print("The converted text:" + str(text['alternative'][0]['transcript']))

