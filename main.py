import pyttsx3
import speech_recognition as sr
import serial
import time
import google.generativeai as genai
import creds
import send

engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

genai.configure(api_key=creds.API_KEY)
model=genai.GenerativeModel("gemini-pro")

arduino=serial.Serial(port='COM4',buradate=115200,timeout=0.1)

def getresponse(query):
    response=model.generate_content(query)
    l=response.text

    l=l.split("\n")
    for i in range(0,len(l)):
        text=l[i]
        s=""
        for j in text:
            if(j in ["*","(",")",":","."]):
                s+=""
            else:
                s+=j
        l[i]=s
    data=""

    for i in l:
        if(len(i)>0):
            data+=i

    return data

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def takecommand():
    recognizer=sr.Recognizer()
    recognized=False
    n=0

    while(n<3 and not recognized):
        try:
            with sr.Microphone() as mic:
                audio=recognizer.listen(mic)
                text=recognizer.recognize_google(audio,language="en-in")
                text=text.lower()
                if(len(text)>0):
                    recognized=True
                print("Recognized",text)
        except Exception as e:
            n+=1
            print("Assistant:Say that again please")
            continue
        return text
    
    if(not recognized):
        print("Assistant:Sorry i was unable to catch what u said can u please type it")
        speak("Sorry i was unable to catch what u said can u please type it")
        time.sleep(2)
        text=input("User:")
    return text

def automate(x):
    arduino.write(bytes(x,'utf-8'))
    time.sleep(0.05)

def intialize():
    while True:
        text=takecommand()

        if("turn on" in text and "light" in text):
            send.control(1)
        elif("turn off" in text and "light" in text):
            send.control(0)
        elif("exit" in text):
            return
        else:
            text=getresponse(text)
            print("Assistant: ",text)
            speak(text)

if __name__=="__main__":
    while True:
        intialize()
        time.sleep(5)
        continue
