from __future__ import print_function
import pyowm
import speech_recognition as sr
from gtts import gTTS
import subprocess
import os
from datetime import date
import time 
import playsound
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime 
import pytz
import pickle
import wikipediaapi
import webbrowser
from helping import get_audio, speak

def weather():
    owm = pyowm.OWM('your api key from open weather',language='el')
    observation = owm.weather_at_place('Dimos Patras, GR ')
    observation_list = owm.weather_around_coords(38.2155, 21.7956)
    w = observation.get_weather()
    w.get_wind()
    w.get_humidity()
    w.get_temperature('celsius')
    print(w)
    print(w.get_wind())
    print(w.get_humidity())
    print(w.get_temperature('celsius'))
    speak('Μποφορ')
    wind = str(w.get_wind())
    speak(wind)
    speak('υγρασία')
    humidity = str(w.get_humidity())
    speak(humidity)
    temper = str(w.get_temperature('celsius'))
    speak('θερμοκρασία' )
    speak(temper)

def weather_now():
    webbrowser.open_new('https://www.meteo.gr/cf.cfm?city_id=10#')

def wiki():
    wiki_wiki = wikipediaapi.Wikipedia('el')
    for x in range(0, 2):    
        speak("Τί θέλεις να ψάξω")
        tst = get_audio()
        if tst not in "":
            page_py = wiki_wiki.page(tst)
            speak("Παρακαλώ περίμενε")
            search = page_py.summary[0:400]
            if search not in "":
                print(search)
                speak(search)
            webbrowser.open_new('www.google.com/search?q=' + tst)
    speak("Έξοδος από την αναζήτηση")


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
DAYS = ["δευτέρα","τρίτη","τετάρτη","πέμπτη","παρασκευή","σάββατο","κυριακή"]
MONTHS = ["ιανουαρίου","φεβρουαρίου","μαρτίου","απριλίου","μαΐου","ιουνίου","ιουλίου","αυγούστου","σεπτεμβρίου","οκτωβρίου","νοεμβρίου","δεκεμβρίου"]
DAY_EXTENSIONS = ["rd", "th", "st", "nd"]


def authenticate_cal():
    
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r'C:\Users\makis\OneDrive\Υπολογιστής\VoiceAssistant\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

service = authenticate_cal()

def get_events(day, service):
    
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('Δεν έχεις τίποτα προγραμματισμένο')
    else:
        speak(f"Έχεις {len(events)} συμβάντα.") 
        
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("+")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "προ μεσημβρίαν"
            else:
                start_time = str(int(start_time.split(":")[0])-12)  +" "+ start_time.split(":")[1]
                start_time = start_time + "μετά μεσημβρίαν"

            speak(event["summary"] + " στις " + start_time)

def get_date(text):
    text = text.lower()
    today = datetime.date.today()

  
    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month =MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENSIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except :
                        pass

    if month < today.month and month != -1:
        year = year+1
    if day < today.day and month == -1 and day != -1: 
        month = month +1      
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif +=7 

        return today + datetime.timedelta(dif) 

    return datetime.date(month=month, day=day, year=year)

def calend():
    speak('Για πότε;')
    txt = get_audio()
    tmp = 0
    flag = False
    while txt in "" and tmp<3:
        speak("Επανέλαβε την ημερομηνία")
        txt = get_audio()
        tmp +=1
    for word in txt.split():
        if word in MONTHS or word.isdigit() or word in DAYS:                   
            flag = True
    if not flag:
        speak("Λάθος ημερομηνία")
        print("Έξοδος από το ημερολόγιο")
    else:
        date = get_date(txt)
        get_events(get_date(txt), service)

def timeDate():
    print("Η τωρινή ημερομηνία και ώρα : ")
    now = datetime.datetime.now()
    print(now.strftime("Η ώρα είναι %H:%M"))
    speak(now.strftime("Σήμερα είναι %d/%m/%Y και η ώρα είναι %H:%M"))



def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":","-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name]) 

def notep():
    speak("Τί θες να γράψεις;")
    nte = get_audio()
    note(nte)
    speak("Σημείωση καταχωρήθηκε") 

