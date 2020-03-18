from gtts import gTTS
import speech_recognition as sr
import playsound
import os

def speak(text):
    tts = gTTS(text=text, lang="el", lang_check=False)
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)  

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio, language="el-GR")
            print(said)
        except Exception as e:
            pass

    return said.lower()