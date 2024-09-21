import pyttsx3
import speech_recognition as sr
import serial
import time
import google.generativeai as genai
import creds
import send
import todo
engine=pyttsx3.init()
voices=engine.getProperty('voices')
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
            if(j in ["*","(",")",":",".","'",'"']):
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
    while True:
        try:
            with sr.Microphone() as mic:
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

def initialize():
    while True:
        text=takecommand()
        if("turn on" in text and "all" in text):
            send.control(1)
            send.control(3)
            send.control(5)
        elif("turn off" in text and "all" in text):
            send.control(2)
            send.control(4)
            send.control(6)
        elif("turn on" in text and "light" in text):
            if("one" not in text and "two" not in text and "three" not in text and "1" not in text and "2" not in text and "3" not in text):
                print("Which light you want to turn on")
                speak("Which light you want to turn on")
                num=takecommand()
            else:
                if("one" in text or "1" in text):
                    num="one"
                elif("two" in text or "2" in text):
                    num="two"
                else:
                    num="three"
            print("num",num)
            if(num=="one" or num=="1"):
                send.control(1)
            elif(num=="two" or num=="2"):
                send.control(3)
            elif(num=="three" or num=="3"):
                send.control(5)

        elif("turn off" in text and "light" in text):
            if("one" not in text and "two" not in text and "three" not in text and "1" not in text and "2" not in text and "3" not in text):
                print("Which light you want to turn off")
                speak("Which light you want to turn off")
                num=takecommand()
            else:
                if("one" in text or "1" in text):
                    num="one"
                elif("two" in text or "2" in text):
                    num="two"
                else:
                    num="three"
            
            if(num=="one"):
                send.control(2)
            elif(num=="two"):
                send.control(4)
            elif(num=="three"):
                send.control(6)
        elif("add" in text and ("to the list" in text or "work" in text)):
                work=text
                p=work.find("add")
                q=work.find("to the list")
                work=work[p+3:q]
                print(work)
                speak("Assistant:Work added")
                todo.add(work)
        elif("to do list" in text or "update to do" in text or "update work" in text or ("update" in text and "list" in text and "work" in text)):
            print("Assistant:what would you like to update in the list")
            speak("what would you like to updqate in the list")
            work=takecommand()
            if("add" in work):
                p=work.find("add")
                work=work[p+3:]
                print(work)
                speak("Assistant:Work added")
                todo.add(work)
            elif("update work status" in work):
                print("which work status you want to update")
                speak("which work status you want to update")
                work=takecommand()
                todo.updatework(work)
            elif("delete work" in work):
                print("which work you want to delete")
                speak("which work you want to delete")
                work=takecommand()
                todo.delete(work)
        elif("show work list" in text or 'show to do list' in text or ('show' in text and ("work" in text or "work list" in text))):
            res=todo.show()
            print()
            print("Workl\tstatus")
            for i in res:
                print(i[0],"\t",i[1])

        elif("exit" in text or "sleep" in text):
            return
        
        elif("terminate" in text):
            exit(0)
        else:
            text=getresponse(text)
            print("Assistant: ",text)
            speak(text)

if __name__=="__main__":
    initialize()
    while True:
        text=wakeup()
        if "wake up" in text:
            initialize()
        else:
            time.sleep(5)
            continue