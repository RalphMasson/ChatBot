## Chatbot
import sounddevice as sd
import numpy as np
import speech_recognition as sr
from gtts import gTTS
import os
import nltk
import tflearn
import random
import json
import pickle
import wavio
import time
import subprocess
import spacy

from sys import byteorder
from array import array
from struct import pack
from pydub import AudioSegment
import pyaudio
import wave
from spacy.matcher import Matcher
from mutagen.mp3 import MP3
from nltk.stem.lancaster import LancasterStemmer



# print("Import ok",flush=True)

## Read Data

class ChatBot():

    def __init__(self):
        with open(r"C:\Users\MASSON\Desktop\ChatBot\intents.json",encoding="utf-8") as file:
            self.data = json.load(file)

        with open(r"C:\Users\MASSON\Desktop\ChatBot\data.pickle","rb") as f:
            self.words, self.labels,self.training,self.output = pickle.load(f)
        self.stemmer = LancasterStemmer()
        self.net = tflearn.input_data(shape = [None,len(self.training[0])])
        self.net = tflearn.fully_connected(self.net,8)
        self.net = tflearn.fully_connected(self.net,8)
        self.net = tflearn.fully_connected(self.net,len(self.output[0]),activation = "softmax")
        self.net = tflearn.regression(self.net)
        self.model = tflearn.DNN(self.net)
        self.model.load(r"C:\Users\MASSON\Desktop\ChatBot\model.tflearn")

    def import_nlp(self):
        self.nlp = spacy.load("fr_core_news_sm")

    def bag_of_words(self,s,words):
        bag = [0 for _ in range(len(self.words))]
        s_words = nltk.word_tokenize(s,language='french')
        s_words = [self.stemmer.stem(word.lower()) for word in s_words]
        for se in s_words:
            for i,w in enumerate(words):
                if w==se:
                    bag[i] = 1
        return np.array(bag)


    def speed_change(self,sound, speed):
        sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * speed)})
        return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


    def is_silent(self,snd_data):
        "Returns 'True' if below the 'silent' threshold"
        return max(snd_data) < self.THRESHOLD

    def normalize(self,snd_data):
        "Average the volume out"
        MAXIMUM = 16384
        times = float(MAXIMUM)/max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i*times))
        return r

    def trim(self,snd_data):
        "Trim the blank spots at the start and end"
        def _trim(self,snd_data):
            snd_started = False
            r = array('h')

            for i in snd_data:
                if not snd_started and abs(i)>self.THRESHOLD:
                    snd_started = True
                    r.append(i)

                elif snd_started:
                    r.append(i)
            return r

        # Trim to the left
        snd_data = _trim(self,snd_data)

        # Trim to the right
        snd_data.reverse()
        snd_data = _trim(self,snd_data)
        snd_data.reverse()
        return snd_data

    def add_silence(self,snd_data, seconds):
        "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
        silence = [0] * int(seconds * self.RATE)
        r = array('h', silence)
        r.extend(snd_data)
        r.extend(silence)
        return r

    def record(self):
        self.THRESHOLD = 500
        self.CHUNK_SIZE = 1024
        self.FORMAT = pyaudio.paInt16
        self.RATE = 44100
        p = pyaudio.PyAudio()
        print("JARVIS : Parlez",flush=True)
        stream = p.open(format=self.FORMAT, channels=1, rate=self.RATE,input=True, output=True,frames_per_buffer=self.CHUNK_SIZE)

        num_silent = 0
        snd_started = False

        r = array('h')

        while 1:
            # little endian, signed short
            snd_data = array('h', stream.read(self.CHUNK_SIZE))
            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)

            silent = self.is_silent(snd_data)

            if silent and snd_started:
                num_silent += 1
            elif not silent and not snd_started:
                snd_started = True
            # print(num_silent)
            if snd_started and num_silent > 120:
                break

        sample_width = p.get_sample_size(self.FORMAT)
        stream.stop_stream()
        stream.close()
        p.terminate()

        r = self.normalize(r)
        r = self.trim(r)
        r = self.add_silence(r, 0.5)
        return sample_width, r

    def record_to_file(self,path):
        "Records from the microphone and outputs the resulting data to 'path'"
        sample_width, data = self.record()
        data = pack('<' + ('h'*len(data)), *data)

        wf = wave.open(path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(self.RATE)
        wf.writeframes(data)
        wf.close()

    def chat(self):
        self.context = {}
        self.pattern = [[{"TEXT": "de"}, {"POS": "PROPN"}],[{"TEXT": "de"}, {"POS": "NOUN"}],[{"TEXT": "de"}, {"POS": "NOUN"},{"POS":"ADP"},{"POS":"NOUN"}],[{"TEXT": "de"}, {"POS": "NOUN"},{"POS":"ADJ"}],[{"TEXT": "de"}, {"POS": "PROPN"},{"POS":"ADJ"}],[{"TEXT": "de"}, {"POS": "NOUN"},{"POS":"NOUN"}],[{"TEXT": "de"}, {"POS": "NOUN"},{"POS":"ADJ"}],[{"TEXT": "de"}, {"POS": "PROPN"},{"POS":"PROPN"}]]
        while True:
            self.record_to_file(r"C:\Users\MASSON\Desktop\ChatBot\input.wav")
            sound = r"C:\Users\MASSON\Desktop\ChatBot\input.wav"
            recognizer = sr.Recognizer()
            with sr.AudioFile(sound) as source:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio,language="fr-FR",show_all=True)

            inp = str(text['alternative'][0]['transcript'])
            print("MOI : "+inp,flush=True)
            time.sleep(0.1)
            print("",flush=True)
            results = self.model.predict([self.bag_of_words(inp,self.words)])[0]
            results_index = np.argmax(results)
            tag = self.labels[results_index]
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[2].id)
            engine.setProperty('rate',135)
            if results[results_index] > 0.75:
                for tg in self.data["intents"]:
                    if tg["tag"] == tag:
                        if 'context_set' in tg:
                            self.context[123] = tg['context_set']
                            # print(tg['context_set'])
                        if not 'context_filter' in tg or (123 in self.context and 'context_filter' in tg and tg['context_filter'] == self.context[123]):
                            # print(context[123])

                            responses = tg["responses"]

                        if(tag == "whatsapp"):
                            proc = "C:/Users/MASSON/AppData/Local/WhatsApp/WhatsApp.exe"
                            subprocess.call(proc)

                        if(tag == "chrome"):
                            proc = "C:\Program Files\Google\Chrome\Application\chrome.exe"
                            subprocess.call(proc)

                        if(tag == "facebook"):
                            proc = "C:\Program Files\Google\Chrome\Application\chrome.exe"
                            url = "https://www.facebook.com"
                            subprocess.Popen([proc,url])

                        if(tag == "google"):
                            about_interest_text = (inp)
                            about_interest_doc = self.nlp(about_interest_text)
                            matcher = Matcher(self.nlp.vocab)
                            matcher.add("montre", self.pattern)
                            matches = matcher(about_interest_doc)
                            matches = [about_interest_doc[start:end].text for match_id, start, end in matches]
                            matches = matches[np.argmax(matches)]

                            proc = "C:\Program Files\Google\Chrome\Application\chrome.exe"
                            url = "https://www.google.com/search?q="+matches
                            subprocess.Popen([proc,url])

                        if(tag == "mail"):
                            proc = "C:\Program Files\Google\Chrome\Application\chrome.exe"
                            url = "https://www.gmail.com"
                            subprocess.Popen([proc,url])

                        if(tag == "videos"):
                            about_interest_text = (inp)
                            about_interest_doc = self.nlp(about_interest_text)
                            matcher = Matcher(self.nlp.vocab)
                            matcher.add("montre", self.pattern)
                            matches = matcher(about_interest_doc)
                            matches = [about_interest_doc[start+1:end].text for match_id, start, end in matches]
                            matches = matches[np.argmax(matches)]

                            proc = "C:\Program Files\Google\Chrome\Application\chrome.exe"
                            url = "https://www.youtube.com/results?search_query="+matches
                            subprocess.Popen([proc,url])

                        if(tag == "images"):
                            about_interest_text = (inp)
                            about_interest_doc = self.nlp(about_interest_text)
                            matcher = Matcher(self.nlp.vocab)
                            matcher.add("montre", self.pattern)
                            matches = matcher(about_interest_doc)
                            matches = [about_interest_doc[start+1:end].text for match_id, start, end in matches]
                            matches = matches[np.argmax(matches)]

                            proc = "C:\Program Files\Google\Chrome\Application\chrome.exe"
                            url = "https://www.google.com/search?q="+matches+"&tbm=isch"
                            subprocess.Popen([proc,url])

                        if(tag == "meteo"):
                            about_interest_text = (inp)
                            about_interest_doc = self.nlp(about_interest_text)
                            if(about_interest_doc.ents[0].label_=="LOC"):
                                from meteofrance_api import MeteoFranceClient
                                client = MeteoFranceClient()
                                ville = about_interest_doc.ents[0]
                                list_places = client.search_places(str(ville))

                                my_place_weather_forecast = client.get_forecast_for_place(list_places[0])
                                meteo = my_place_weather_forecast.current_forecast.get('weather')['desc']
                                temp = my_place_weather_forecast.current_forecast.get('T')['value']
                                answer = "A "+ str(ville)+", "+meteo+" il fait "+str(temp).replace('.',',')+ "degrés"
                                print("JARVIS : "+answer,flush=True)
                                engine.say(answer)
                                engine.runAndWait()
                                engine.save_to_file(answer,r"C:\Users\MASSON\Desktop\ChatBot\a.wav")
                                time.sleep(AudioSegment.from_file(r"C:\Users\MASSON\Desktop\ChatBot\a.wav").duration_seconds)

                try:
                    rep = random.choice(responses)
                    if len(rep)>2:
                        print("JARVIS : "+rep,flush=True)

                    engine.say(rep)
                    engine.runAndWait()
                    engine.save_to_file(rep,r"C:\Users\MASSON\Desktop\ChatBot\a.wav")
                    audio = MP3(r"C:\Users\MASSON\Desktop\ChatBot\a.wav")
                    time.sleep(audio.info.length)
                    if tag == "goodbye":
                        break

                except:
                    answer = "Je n'ai pas été programmé pour répondre à cette demande"
                    print("JARVIS : "+answer,flush=True)
                    engine.say(answer)
                    engine.runAndWait()
                    engine.save_to_file(answer,r"C:\Users\MASSON\Desktop\ChatBot\a.wav")
                    time.sleep(AudioSegment.from_file(r"C:\Users\MASSON\Desktop\ChatBot\a.wav").duration_seconds)


            else:
                answer = "Je n'ai pas été programmé pour répondre à cette demande"
                print("JARVIS : "+answer,flush=True)
                engine.say(answer)
                engine.runAndWait()
                engine.save_to_file(answer,r"C:\Users\MASSON\Desktop\ChatBot\a.wav")
                time.sleep(AudioSegment.from_file(r"C:\Users\MASSON\Desktop\ChatBot\a.wav").duration_seconds)


JARVIS = ChatBot()
from threading import Thread

Thread(target = JARVIS.chat).start()
Thread(target = JARVIS.import_nlp).start()

