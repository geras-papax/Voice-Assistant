from main import main
import speech_recognition as sr
from helping import get_audio

WAKE = "άνοιξε"


while True:
    text = get_audio()
    if text.count(WAKE) > 0:
        main()