import pyttsx3
import speech_recognition as sr
import datetime
import nltk
import google.generativeai as genai
from nltk.tokenize import blankline_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import creds
import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import send

SPOTIPY_CLIENT_ID = creds.client_id
SPOTIPY_CLIENT_SECRET = creds.client_secret
SPOTIPY_REDIRECT_URI = creds.redirect_url

# Spotify authorization
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="user-read-playback-state,user-modify-playback-state"))

stop_words = set(stopwords.words('english'))

engine=pyttsx3.init()
voices=engine.getProperty('voices')
rate = engine.getProperty('rate')
engine.setProperty('rate',130)
engine.setProperty('voice',voices[0].id)

genai.configure(api_key=creds.API_KEY)
model=genai.GenerativeModel("gemini-pro")

def getresponse(query):
    response=model.generate_content(query)
    l=response.text

    l=l.split("\n")
    for i in range(0,len(l)):
        text=l[i]
        s=""
        for j in text:
            if(j in ["*","(",")",":",".",'"',"'"]):
                s+=" "
            else:
                s+=j
        l[i]=s
    data=""

    for i in l:
        if(len(i)>0):
            data+=i.lower()

    return data

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def wish():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning")
    elif hour>=12 and hour<=18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    time = datetime.datetime.now().strftime('%I:%M %p')
    speak("Now the time is "+time)

def takecommand():
    recognizer=sr.Recognizer()
    print("Assistant:Listening....")
    while True:
        try:
            with sr.Microphone() as mic:
                print("Assistant:Recognizing....")
                audio=recognizer.listen(mic,timeout=3,phrase_time_limit=5)
                text=recognizer.recognize_google(audio,language="en-in")
                text=text.lower()
                print("User:",text)
                return text
        except Exception as e:
            print("Assistant:Say that again please")
            continue
        return text

def wakeup():
    recognizer=sr.Recognizer()
    while True:
        try:
            print("..")
            with sr.Microphone() as mic:
                audio=recognizer.listen(mic)
                text=recognizer.recognize_google(audio,language="en-in")
                text=text.lower()
                return text
        except Exception as e:
            continue
        return text

def search_song_on_spotify(query):
    results = sp.search(q=query, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        print(f"Playing {track['name']} by {track['artists'][0]['name']}")
        webbrowser.open(track['external_urls']['spotify'])
    else:
        print("No matching song found on Spotify.")
    return

def process_nlp_command(command):
    # Tokenize and clean the text
    tokens = word_tokenize(command.lower())
    stop_words = set(stopwords.words("english"))
    stop_words.remove("on")
    stop_words.remove("off")
    stop_words.remove("all")
    filtered_tokens = [word for word in tokens if word not in stop_words]
    print(filtered_tokens)
    # Keywords for light control
    if "light" in filtered_tokens or "lights" in filtered_tokens:
        if "on" in filtered_tokens:
            if "1" in filtered_tokens or "one" in filtered_tokens:
                send.control(1)
                return
            elif "2" in filtered_tokens or "two" in filtered_tokens:
                send.control(3)
            elif "3" in filtered_tokens or "three" in filtered_tokens:
                send.control(5)
            elif "all" in filtered_tokens:
                send.contorl(1)
                send.control(3)
                send.control(5)
        elif "off" in filtered_tokens:
            if "1" in filtered_tokens or "one" in filtered_tokens:
                send.contorl(2)
            elif "2" in filtered_tokens or "two" in filtered_tokens:
                send.control(4)
            elif "3" in filtered_tokens or "three" in filtered_tokens:
                send.control(6)
            elif "all" in filtered_tokens:
                send.control(2)
                send.control(4)
                send.control(6)
        else:
            speak("I didn't understand the command for lights.")
    
    elif "play" in filtered_tokens or ("play" in filtered_tokens and "song" in filtered_tokens):
        filtered_tokens.remove("play")
        cleaned_text = ' '.join(filtered_tokens)
        # Search and play song on Spotify
        print(cleaned_text)
        search_song_on_spotify(cleaned_text)

    elif(len(filtered_tokens)>0):
        data=""
        for i in filtered_tokens:
            data=data+i+" "
        data=getresponse(data)
        data=blankline_tokenize(data)      
        print(data[0])
        speak(data[0])
    else:
        return
    return


def initialize():
    while True:
        text=takecommand()
        if("exit" in text or "sleep" in text):
            return
        elif("terminate" in text or "end" in text):
            print("here")
            exit(0)
        else:
            process_nlp_command(text)

if __name__=="__main__":
    wish()
    initialize()
    while True:
        text=wakeup()
        print(text)
        if "wake up" in text:
            wish()
            initialize()
        else:
            print(".")
            time.sleep(5)
            continue